import os
import time
import shutil
import signal
import logging
import threading
import pandas as pd

from sklearn.model_selection import train_test_split

from backend import layers

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
log_file = 'neuromatic_{0}.log'.format(time.strftime('%m%d%Y_%H%M%S'))
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s][%(name)-12s][%(levelname)-8s] %(message)s',
                    datefmt='%H%M%S',
                    filename=os.path.join(log_dir, log_file),
                    filemode='w')


class NetworkException(Exception):
    pass


class Control(object):
    """
    Controls the backend using properties passed from the GUI.

    Attributes:
        PUBLIC
        logger: (logging.Logger) -> System logger
        canvas_properties: (dict{'string': dict}) -> All canvas and layer properties passed from the GUI
        layers: (list[Layers]) -> Stores ordered list of Layers

        PRIVATE
        can_train: (boolean) -> Determines if a model has been generated and can be trained
        thread_lock: (threading.Lock) -> Thread lock to prevent conflicting functions from being called at the
            same time
        add_text: (function) -> Status box "add_text" function for logging to the GUI
    """

    LAYER_TYPES = {
        'Input': layers.InputLayer,
        'Hidden': layers.DenseLayer,
        'Dropout': layers.DropoutLayer,
        'Output': layers.DenseLayer,
    }

    def __init__(self, add_text):
        """
        Control initialization
        :param add_text: (function) -> Status box "add_text" function for logging to the GUI
        """
        self.logger = logging.getLogger('control')

        self.canvas_properties = {}
        self.layers = []

        self.__can_train = False
        self.__thread_lock = threading.Lock()

        self.__add_text = add_text

    def set_properties(self, properties):
        """
        Stores and performs checks on properties passed from the GUI
        :param properties: (dict{'string': dict}) -> All canvas and layer properties passed from the GUI
        """
        self.canvas_properties = properties
        self.layers = []
        status = True

        # Check properties
        # TODO Some of these are already covered by the GUI
        # if os.path.isfile(self.canvas_properties['project_directory']):
        #     file_path = self.canvas_properties['project_directory']
        #     self.canvas_properties['project_directory'] = os.path.dirname(self.canvas_properties['project_directory'])
        #     self.log_status('{0} is a file, setting output path to {1}'.format(file_path, self.canvas_properties['project_directory']), 'warning')
        #     status = False
        # if not os.path.isdir(self.canvas_properties['project_directory']):
        #     self.log_status('{0} does not exist - creating'.format(self.canvas_properties['project_directory']), 'warning')
        #     os.makedirs(self.canvas_properties['project_directory'])
        #     status = False
        if not os.path.isfile(self.canvas_properties['data_path']):
            self.log_status('{0} is not a file or does not exist'.format(self.canvas_properties['data_path']), 'error')
            self.__can_train = False
            status = False

        self.canvas_properties['training_size'] = float(self.canvas_properties['training_size'])
        if self.canvas_properties['training_size'] <= 0 or self.canvas_properties['training_size'] >= 1:
            self.log_status('Training size must be between 0 and 1', 'error')
            status = False

        if 'optimizer' not in self.canvas_properties:
            self.canvas_properties['optimizer'] = 'sgd'
        if 'loss' not in self.canvas_properties:
            self.canvas_properties['loss'] = 'sparse_categorical_crossentropy'
        if 'metrics' not in self.canvas_properties:
            self.canvas_properties['metrics'] = ['accuracy']
        if 'epochs' not in self.canvas_properties:
            self.canvas_properties['epochs'] = 5
        elif self.canvas_properties['epochs'] <= 0:
            self.log_status('Epochs must be > 0', 'warning')
            self.canvas_properties['epochs'] = 1

        # Initialize layers
        for index, layer in enumerate(self.canvas_properties['layers']):
            # TODO establish correct dict layout
            layer_type = list(layer.keys())[0]
            layer_properties = list(layer.values())[0]

            if not layer_type in self.LAYER_TYPES and layer_type != 'Empty':
                self.log_status('Invalid layer type: {0}'.format(layer_type), 'debug')
                status = False
                continue
            elif layer_type == 'Empty':
                continue
            if index == 0 and layer_type != 'Input':
                self.log_status('Invalid network configuration: network must start with Input Layer', 'error')
                status = False

            # if not layer['type'] in self.LAYER_TYPES:
            #     self.log_status('Invalid layer type: {0}'.format(layer['type']), 'debug')
            #     status = False
            #     continue
            # if layer['type'] == 'input':
            #     input_seen = True

            # new_layer = self.LAYER_TYPES[layer['type']](layer)

            new_layer = self.LAYER_TYPES[layer_type](layer_properties)
            self.layers.append(new_layer)

        if not status:
            self.log_status('Some parameters were invalid', 'warning')

    def generate_network(self):
        """
        Writes the Python file containing the Keras neural network
        """
        self.log_status('Generating network...', 'info')
        with open(os.path.join(self.canvas_properties['project_directory'], 'neural_network.py'), 'w') as fd:
            # Imports
            fd.write('import h5py\n')
            fd.write('from keras.models import Sequential\n')
            fd.write('from keras.layers import Input, Dense, Dropout\n')
            fd.write('from keras.utils import to_categorical\n\n')

            fd.write('def train_neural_network(X_train, y_train, X_test, y_test):\n')

            # Model creation and adding layers
            fd.write('\tmodel = Sequential()\n\n')
            for layer in self.layers:
                layer.write_lines(fd)
            fd.write('\n')

            # Model compilation and training
            fd.write('\tprint(\'Training model...\')\n')
            fd.write('\tmodel.compile(optimizer=\'{0}\', '.format(self.canvas_properties['optimizer']))
            fd.write('loss=\'{0}\', '.format(self.canvas_properties['loss']))
            fd.write('metrics=[')
            for metric in self.canvas_properties['metrics']:
                fd.write('\'{0}\','.format(metric))
            fd.write('])\n\n')

            if self.canvas_properties['loss'] != 'sparse_categorical_crossentropy':
                fd.write('\ty_train = to_categorical(y_train)\n')
            fd.write('\tmodel.fit(X_train, y_train, epochs={0})\n'.format(self.canvas_properties['epochs']))
            fd.write('\tscore = model.evaluate(X_test, y_test, batch_size=128)\n\n')

            # Saving model
            fd.write('\tprint(\'Saving model to disk...\')\n')
            fd.write('\tmodel.save(\'{0}\')\n'.format(os.path.join(self.canvas_properties['project_directory'],
                                                                   self.canvas_properties['canvas_name'] + '_model.h5')))
            fd.write('\tmodel.save_weights(\'{0}\')\n'.format(os.path.join(self.canvas_properties['project_directory'],
                                                                           self.canvas_properties['canvas_name'] + '_weights.h5')))
            fd.write('\tmodel_json = model.to_json()\n')
            fd.write('\twith open(\'{0}\', \'w\') as json_file:\n'.format(os.path.join(self.canvas_properties['project_directory'],
                                                                                       self.canvas_properties['canvas_name'] + '_model.json')))
            fd.write('\t\tjson_file.write(model_json)\n\n')

            fd.write('\treturn score[1]')

        # Create local copy of network to import when training
        shutil.copy(os.path.join(self.canvas_properties['project_directory'], 'neural_network.py'),
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'network.py'))

        self.log_status('Network generated.', 'info')
        self.__can_train = True

    def train_network(self):
        """
        Trains the created neural network
        """
        if not self.__can_train:
            self.log_status('Cannot train without a model', 'error')
            return
        signal.signal(signal.SIGTERM, self.safe_terminate)
        self.__thread_lock.acquire()

        from backend import network

        # Read in training data
        self.log_status('Reading data...', 'info')
        training_data = pd.read_csv(self.canvas_properties['data_path'])
        y_data = training_data.ix[:,0]
        X_data = training_data.ix[:,1:]
        X_train, X_test, y_train, y_test = train_test_split(X_data,
                                                            y_data,
                                                            train_size=self.canvas_properties['training_size'],
                                                            shuffle=True)

        self.log_status('Training network...', 'debug')
        score = network.train_neural_network(X_train, y_train, X_test, y_test)

        self.log_status('Network trained.', 'debug')
        self.log_status('Model accuracy: {0}'.format(round(score, 3)))

        self.__thread_lock.release()

    def safe_terminate(self, sig_num, frame):
        """
        Safely terminate thread and release lock
        :param sig_num: (int) -> Signal number
        :param frame: (frame) -> Current stack frame
        """
        self.log_status('Terminating...'.format(sig_num), 'warning')
        self.log_status('Process terminated with signal {0}'.format(sig_num), 'warning', True)

        if self.__thread_lock.locked():
            self.__thread_lock.release()

    def log_status(self, msg, level='info', suppress=False):
        """
        Log status to status box and logger
        :param msg: (string) -> Message to log
        :param level: (string) -> Logger level
        :param suppress: (boolean) -> True if not logging to status box
        """
        logger_level = {
            'info': self.logger.info,
            'debug': self.logger.debug,
            'warning': self.logger.warning,
            'error': self.logger.error,
            'critical': self.logger.critical
        }
        logger_level[level](msg)

        if msg[-1] != '\n':
            msg += '\n'
        if not suppress:
            self.__add_text(msg)
