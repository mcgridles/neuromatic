import os
import re
import time
import shutil
import logging
import pandas as pd
import multiprocessing

from sklearn.model_selection import train_test_split

from backend import layers

# Configure logging
LOG_TO_FILE = True
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
log_file = 'neuromatic_{0}.log'.format(time.strftime('%m%d%Y_%H%M%S'))

if not os.path.isdir(log_dir):
    os.makedirs(log_dir)
if LOG_TO_FILE:
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s][%(name)-12s][%(levelname)-8s] %(message)s',
                        datefmt='%H%M%S',
                        filename=os.path.join(log_dir, log_file),
                        filemode='w')
else:
    logging.basicConfig(level=logging.DEBUG)


class NetworkException(Exception):
    pass


class ControlProcess(multiprocessing.Process):

    def __init__(self, target, args):
        super(ControlProcess, self).__init__(target=target, args=args)
        self.daemon = True

    def start(self):
        """
        Override Process.start() to prevent exceptions when attempting to start a process twice
        """
        try:
            super(ControlProcess, self).start()
        except AssertionError as error:
            if str(error) != 'cannot start a process twice':
                raise error

    def terminate(self):
        """
        Override Process.terminate() to prevent exceptions if stopped process is terminated
        """
        if self.is_alive():
            super(ControlProcess, self).terminate()


class Control(object):
    """
    Controls the backend using properties passed from the GUI.

    Attributes:
        PUBLIC
        logger: (logging.Logger) -> System logger
        canvas_properties: (dict{'string': dict}) -> All canvas and layer properties passed from the GUI
        layers: (list[Layers]) -> Stores ordered list of Layers

        PRIVATE
        __can_generate: (boolean) -> Determines if a network script can be generated
        __can_train: (boolean) -> Determines if a model has been generated and can be trained
        __training_process: (multiprocessing.Process) -> Current training process
        __add_text: (function) -> Status box "add_text" function for logging to the GUI
    """

    LAYER_TYPES = {
        'input': layers.InputLayer,
        'hidden': layers.DenseLayer,
        'dropout': layers.DropoutLayer,
        'output': layers.DenseLayer,
    }

    def __init__(self):
        """
        Control initialization
        """
        self.logger = logging.getLogger('control')

        self.canvas_properties = {}
        self.layers = []

        self.__can_generate = False
        self.__can_train = False

        self.__training_process = None
        self.__create_new_process()

        self.__add_text = None

    @property
    def can_generate(self):
        return self.__can_generate

    @can_generate.setter
    def can_generate(self, status):
        """
        Set private variable to status
        :param status: (boolean) -> Updated control status
        """
        self.__can_generate = status

    @property
    def can_train(self):
        return self.__can_train

    @can_train.setter
    def can_train(self, status):
        """
        Set private variable to status
        :param status: (boolean) -> Updated control status
        """
        self.__can_train = status

    def init_status(self, add_text):
        """
        Assign status box "add_text" function for logging to the GUI
        :param add_text: (function) -> Status box "add_text" function
        """
        self.__add_text = add_text

    def set_properties(self, properties):
        """
        Store properties passed from the GUI and perform checks checks
        :param properties: (dict{'string': dict}) -> All canvas and layer properties passed from the GUI
        """
        # Sanitize potentially dangerous inputs
        properties['canvas_name'] = self.sanitize_input(properties['canvas_name'])

        self.canvas_properties = properties
        self.layers = []
        self.__can_generate = True
        self.__can_train = True

        if 'csv' not in os.path.splitext(self.canvas_properties['data_path'])[1]:
            self.__log_status('Invalid data file type', 'error')
            self.__can_train = False

        # Set defaults
        if 'optimizer' not in self.canvas_properties:
            self.canvas_properties['optimizer'] = 'sgd'
        if 'loss' not in self.canvas_properties:
            self.canvas_properties['loss'] = 'mean_squared_error'
        if 'metrics' not in self.canvas_properties:
            self.canvas_properties['metrics'] = ['accuracy']
        if 'epochs' not in self.canvas_properties:
            self.canvas_properties['epochs'] = '1'
        elif int(self.canvas_properties['epochs']) <= 0:
            self.__log_status('Epochs must be > 0', 'warning')
            self.canvas_properties['epochs'] = '1'

        # Initialize layers
        for index, layer in enumerate(self.canvas_properties['layers']):
            layer_type = layer['type']
            layer_properties = layer

            if not layer_type in self.LAYER_TYPES and layer_type != 'empty':
                self.__log_status('Invalid layer type: {0}'.format(layer_type), 'debug')
                self.__can_generate = False
                continue
            elif layer_type == 'empty':
                self.__log_status('Ignoring empty layer', 'debug', suppress=True)
                continue

            new_layer = self.LAYER_TYPES[layer_type](layer_properties)
            self.layers.append(new_layer)

        if len(self.layers) < 3:
            self.__log_status('Not enough layers', 'debug', suppress=True)
            self.__can_generate = False
        elif type(self.layers[0]) != layers.InputLayer:
            self.__log_status('Invalid network configuration: network must start with input Layer', 'error')
            self.__can_generate = False

    def generate_network(self):
        """
        Write the Python file containing the Keras neural network
        """
        if not self.__can_generate:
            self.__log_status('Generation error', 'error')
            return
        self.__log_status('\nGenerating network...', 'info')

        file_name = os.path.join(self.canvas_properties['project_directory'],
                                 '{0}_network.py'.format(self.canvas_properties['canvas_name']))
        with open(file_name, 'w') as fd:
            # Imports
            fd.write('import h5py\n')
            fd.write('from keras.models import Sequential\n')
            fd.write('from keras.layers import InputLayer, Dense, Dropout\n')
            fd.write('from keras.utils import to_categorical\n\n')

            fd.write('def train_neural_network(X_train, y_train, X_test, y_test):\n')

            # Model creation and adding layers
            fd.write('\tmodel = Sequential([\n')
            for layer in self.layers:
                layer.write_lines(fd)
            fd.write('\t])\n\n')

            # Model compilation and training
            fd.write('\tmodel.compile(optimizer=\'{0}\', '.format(self.canvas_properties['optimizer']))
            fd.write('loss=\'{0}\', '.format(self.canvas_properties['loss']))
            fd.write('metrics=[')
            for metric in self.canvas_properties['metrics']:
                fd.write('\'{0}\','.format(metric))
            fd.write('\t])\n\n')

            if self.canvas_properties['loss'] != 'sparse_categorical_crossentropy':
                fd.write('\ty_train = to_categorical(y_train)\n')
                fd.write('\ty_test = to_categorical(y_test)\n')
            fd.write('\tmodel.fit(X_train, y_train, epochs={0})\n'.format(self.canvas_properties['epochs']))
            fd.write('\tscore = model.evaluate(X_test, y_test, batch_size=128)\n\n')

            # Saving model
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
        shutil.copy(file_name, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'network.py'))

        self.__log_status('Network generated', 'info')

    def __train_network(self, connection):
        """
        Train the created neural network
        :param connection: (multiprocess.Pipe) -> Child connection to the parent process
        """
        try:
            from backend import network
        except ImportError:
            connection.send('Cannot train without a network\n')
            return

        # Read in training data
        connection.send('Reading data...\n')
        training_data = pd.read_csv(self.canvas_properties['data_path'])
        y_data = training_data.ix[:,0]
        X_data = training_data.ix[:,1:]
        X_train, X_test, y_train, y_test = train_test_split(X_data,
                                                            y_data,
                                                            train_size=float(self.canvas_properties['training_size']),
                                                            shuffle=True)

        try:
            connection.send('Training network...\n')
            score = network.train_neural_network(X_train, y_train, X_test, y_test)

            # Test network
            connection.send('Network trained\n\n')
            connection.send('Model accuracy: {0}\n'.format(round(score, 3)))
        except (ValueError, AttributeError) as error:
            connection.send('An error occurred while training:\n')
            connection.send(str(error))

        connection.close()

    def train_in_new_thread(self):
        """
        Start a training process. This prevents the main process (GUI) from stalling while training
        happens
        """
        if not self.__can_train:
            self.__log_status('Training error', 'error')
            return

        if not self.__training_process.is_alive():
            self.__log_status('\nStarting training process', 'debug')
            try:
                # Create a new process if one has already been run
                self.__training_process.join()
                self.__create_new_process()
                self.__training_process.start()
            except AssertionError as error:
                if str(error) == 'can only join a started process':
                    self.__training_process.start()

    def terminate_training(self):
        """
        Terminate the current training process if there is one running
        """
        if self.__training_process.is_alive():
            # Terminate process and create a new one
            self.__log_status('Training canceled\n', 'debug')
            self.__training_process.terminate()
            self.__create_new_process()

    def __create_new_process(self):
        """
        Create a new training process to replace one that have already been used
        """
        self.__log_status('Creating new process', 'debug', suppress=True)
        self.parent_conn, child_conn = multiprocessing.Pipe()
        self.__training_process = ControlProcess(target=self.__train_network, args=(child_conn,))

    def check_pipe(self):
        """
        Checks the pipe between the main process and the training process for any messages.
        :return: (string) -> Status message if one has been sent
        """
        if self.parent_conn.poll():
            try:
                status = self.parent_conn.recv()
                return status
            except EOFError:
                pass

    def __log_status(self, msg, level='info', suppress=False):
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

    @staticmethod
    def sanitize_input(text):
        """
        Remove potentially dangerous characters from a string
        :param text: (string) -> String to remove characters from
        :return: (string) -> Sanitized string
        """
        bad_chars = '[;\'\"`|#\n\t]'
        return re.sub(bad_chars, '', text)
