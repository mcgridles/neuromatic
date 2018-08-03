import os
import shutil
import signal
import logging
import multiprocessing
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from layers import InputLayer, DenseLayer, DropoutLayer

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
        thread_lock: (multiprocessing.Lock) -> Thread lock to prevent conflicting functions from being called at the
            same time
    """
    LAYER_TYPES = {
        'input': InputLayer,
        'dense': DenseLayer,
        'dropout': DropoutLayer,
    }

    def __init__(self):
        self.logger = logging.getLogger('control')

        self.canvas_properties = {}
        self.layers = []

        self.__can_train = False
        self.__thread_lock = multiprocessing.Lock()

    def set_properties(self, properties):
        """
        Stores and performs checks on properties passed from the GUI
        :param properties: (dict{'string': dict}) -> All canvas and layer properties passed from the GUI
        :return: (boolean) -> True if properties set correctly, False if warnings/errors
        """
        self.canvas_properties = properties
        self.layers = []
        status = True

        # Check properties
        if os.path.isfile(self.canvas_properties['output_path']):
            file_path = self.canvas_properties['output_path']
            self.canvas_properties['output_path'] = os.path.dirname(self.canvas_properties['output_path'])
            self.logger.warning('{0} is a file, setting output path to {1}'.format(file_path, self.canvas_properties['output_path']))
            status = False
        if not os.path.isdir(self.canvas_properties['output_path']):
            self.logger.warning('{0} does not exist - creating'.format(self.canvas_properties['output_path']))
            os.makedirs(self.canvas_properties['output_path'])
            status = False
        if not os.path.isfile(self.canvas_properties['training_data_path']):
            self.logger.error('{0} is not a file or does not exist'.format(self.canvas_properties['training_data_path']))
            self.__can_train = False
            status = False

        if self.canvas_properties['train_size'] <= 0 or self.canvas_properties['train_size'] >= 1:
            self.logger.error('Training size must be between 0 and 1')
            status = False

        if not self.canvas_properties['optimizer']:
            self.canvas_properties['optimizer'] = 'sgd'
        if not self.canvas_properties['metrics']:
            self.canvas_properties['metrics'] = ['accuracy']

        # Initialize layers
        for layer in self.canvas_properties['layers']:
            if not layer in self.LAYER_TYPES:
                raise NetworkException('Invalid layer type: {0}'.format(layer))

            new_layer = self.LAYER_TYPES[layer](self.canvas_properties['layers'][layer])
            self.layers.append(new_layer)

        return status

    def generate_network(self):
        """
        Writes the Python file containing the Keras neural network
        """
        signal.signal(signal.SIGTERM, self.safe_terminate)
        self.__thread_lock.acquire()

        with open(os.path.join(self.canvas_properties['output_path'], 'neural_network.py'), 'w') as fd:
            # Imports
            fd.write('import h5py\n')
            fd.write('from keras.models import Sequential\n')
            fd.write('from keras.layers import Flatten, Dense, Dropout\n\n')

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
            fd.write('])\n')
            fd.write('\tmodel.fit(X_train, y_train, validation_data=(X_test, y_test), epochs={0})\n\n'.format(self.canvas_properties['epochs']))

            # Saving model
            fd.write('\tprint(\'Saving model to disk...\')\n')
            fd.write('\tmodel.save(\'{0}/model.h5\')\n'.format(self.canvas_properties['output_path']))
            fd.write('\tmodel.save_weights(\'{0}/weights.h5\')\n'.format(self.canvas_properties['output_path']))
            fd.write('\tmodel_json = model.to_json()\n')
            fd.write('\twith open(\'{0}/model.json\', \'w\') as json_file:\n'.format(self.canvas_properties['output_path']))
            fd.write('\t\tjson_file.write(model_json)\n')

        # Create local copy of network to import when training
        shutil.copy(os.path.join(self.canvas_properties['output_path'], 'neural_network.py'),
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'network.py'))

        self.__can_train = True
        self.__thread_lock.release()

    def train_network(self):
        """
        Trains the created neural network
        """
        if not self.__can_train:
            raise NetworkException('Cannot train without a model')
        signal.signal(signal.SIGTERM, self.safe_terminate)
        self.__thread_lock.acquire()

        from network import train_neural_network

        # Read in training data
        training_data = pd.read_csv(self.canvas_properties['training_data_path'])
        y_data = training_data.ix[:,0]
        X_data = training_data.ix[:,1:]
        X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, train_size=self.canvas_properties['train_size'], shuffle=True)

        train_neural_network(X_train, y_train, X_test, y_test)

        self.__thread_lock.release()

    def safe_terminate(self, *args):
        self.logger.warning('Process terminated')

        if self.__thread_lock.locked():
            self.__thread_lock.release()
