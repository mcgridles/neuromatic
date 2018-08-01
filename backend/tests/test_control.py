import os
import unittest
import pandas as pd
from unittest import mock
from pandas.util.testing import assert_frame_equal, assert_series_equal

from layers import DenseLayer, DropoutLayer
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

    @mock.patch('control.shutil')
    @mock.patch('builtins.open')
    def test_create_network(self, mock_open, mock_shutil):
        # Arrange
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generated_network.py')
        layer1 = DenseLayer({
            'size': 512,
            'activation': 'relu'
        })
        layer2 = DropoutLayer({
            'percentage': 0.8,
        })
        layer3 = DenseLayer({
            'size': 10,
            'activation': 'softmax'
        })
        self.controller.canvas_properties['nn_path'] = file_path
        self.controller.canvas_properties['optimizer'] = 'adam'
        self.controller.canvas_properties['loss'] = 'sparse_categorical_crossentropy'
        self.controller.canvas_properties['metrics'] = ['accuracy']
        self.controller.canvas_properties['epochs'] = 5
        self.controller.canvas_properties['model_path'] = '/path/to/directory'
        self.controller.layers = [layer1, layer2, layer3]

        # Act
        self.controller.generate_network()

        # Assert
        print(mock_open.call_args)
        self.assertEqual(mock_open.call_args, mock.call(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generated_network.py'), 'w'))
        self.assertEqual(mock_open.return_value.__enter__.return_value.write.call_count, 22)
