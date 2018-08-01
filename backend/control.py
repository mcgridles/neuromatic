import os
import shutil
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

from layers import DenseLayer, DropoutLayer

class Controller(object):

    def __init__(self):
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        self.canvas_properties = {}
        self.train_size = 0.8

        self.layers = []
        self.layer_types = {
            'hidden': DenseLayer,
            'dropout': DropoutLayer,
        }

    def store_properties(self, properties):
        self.canvas_properties = properties

        self.train_size = self.canvas_properties['training_size']
        for layer in self.canvas_properties['layers']:
            new_layer = self.layer_types[layer](self.canvas_properties['layers'])

    def read_csv(self):
        training_data = pd.read_csv(self.canvas_properties['training_data_path'])
        y = training_data.ix[:,0]
        X = training_data.ix[:,1:]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, train_size=self.train_size,
                                                                                shuffle=True)

    def generate_network(self):
        with open(self.canvas_properties['nn_path'], 'w') as fd:
            # imports
            fd.write('import h5py\n')
            fd.write('from keras.models import Sequential\n')
            fd.write('from keras.layers import Flatten, Dense, Dropout\n\n')

            fd.write('def train_neural_network(X_train, y_train, X_test, y_test):\n')

            # create model object and add layers
            fd.write('\tmodel = Sequential()\n\n')
            for layer in self.layers:
                layer.write_lines(fd)
            fd.write('\n')

            fd.write('\tprint(\'Training model...\')\n')
            fd.write('\tmodel.compile(optimizer=\'{0}\', '.format(self.canvas_properties['optimizer']))
            fd.write('loss=\'{0}\', '.format(self.canvas_properties['loss']))
            fd.write('metrics=[')
            for metric in self.canvas_properties['metrics']:
                fd.write('\'{0}\','.format(metric))
            fd.write('])\n')
            fd.write('\tmodel.fit(X_train, y_train, validation_data=(X_test, y_test), epochs={0})\n\n'.format(self.canvas_properties['epochs']))

            # TODO implement filetype checks
            fd.write('\tprint(\'Saving model to disk...\')\n')
            fd.write('\tmodel.save(\'{0}/model.h5\')\n'.format(self.canvas_properties['model_path']))
            fd.write('\tmodel.save_weights(\'{0}/weights.h5\')\n'.format(self.canvas_properties['model_path']))
            fd.write('\tmodel_json = model.to_json()\n')
            fd.write('\twith open(\'{0}/model.json\', \'w\') as json_file:\n'.format(self.canvas_properties['model_path']))
            fd.write('\t\tjson_file.write(model_json)\n')

        # create local copy of network to import when training
        shutil.copy(self.canvas_properties['nn_path'],
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'network.py'))

    def train_network(self):
        from network import train_neural_network

        train_neural_network(self.X_train, self.y_train, self.X_test, self.y_test)
