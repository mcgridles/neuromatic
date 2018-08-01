import os
import unittest
import pandas as pd
from unittest import mock
from pandas.util.testing import assert_frame_equal, assert_series_equal

from layer import Layer
from control import Controller

class TestControl(unittest.TestCase):

    def setUp(self):
        self.controller = Controller()

    @mock.patch('control.train_test_split')
    @mock.patch('control.pd')
    def test_read_csv(self, pd_mock, tts_mock):
        # Arrange
        df = pd.DataFrame(data={'Label': [0], 'Pixel1': [0], 'Pixel2': [255]})
        pd_mock.read_csv.return_value = df
        tts_mock.side_effect = lambda X, y, train_size, shuffle: (X, None, y, None)

        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/test.csv')
        self.controller.canvas_properties['training_data_path'] = file_path

        # Act
        self.controller.read_csv()

        # Assert
        assert_frame_equal(self.controller.X_train, pd.DataFrame(data={'Pixel1': [0], 'Pixel2': [255]}))
        assert_series_equal(self.controller.y_train, pd.Series(name='Label', data=[0]))

    def test_create_network(self):
        # Arrange
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generated_network.py')
        layer1_properties = {
            'name': 'dense',
            'size': 512,
            'activation': 'relu',
            'dropout': 0.2
        }
        layer2_properties = {
            'name': 'dense',
            'size': 10,
            'activation': 'softmax',
            'dropout': None
        }
        self.controller.canvas_properties['nn_path'] = file_path
        self.controller.canvas_properties['optimizer'] = 'adam'
        self.controller.canvas_properties['loss'] = 'sparse_categorical_crossentropy'
        self.controller.canvas_properties['metrics'] = ['accuracy']
        self.controller.canvas_properties['epochs'] = 5
        self.controller.canvas_properties['model_path'] = '/path/to/directory'
        self.controller.layers = [Layer(layer1_properties), Layer(layer2_properties)]

        # Act
        # Test output network
        # self.controller.create_network()
