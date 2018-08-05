import os
import unittest
import pandas as pd
from unittest import mock
from pandas.util.testing import assert_frame_equal, assert_series_equal

from layers import DenseLayer, DropoutLayer
from control import Control, NetworkException

class TestControl(unittest.TestCase):

    def setUp(self):
        self.controller = Control()

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
        self.controller.canvas_properties['optimizer'] = 'adam'
        self.controller.canvas_properties['loss'] = 'sparse_categorical_crossentropy'
        self.controller.canvas_properties['metrics'] = ['accuracy']
        self.controller.canvas_properties['epochs'] = 5
        self.controller.canvas_properties['output_path'] = '/path/to/directory'
        self.controller.layers = [layer1, layer2, layer3]

        # Act
        self.controller.generate_network()

        # Assert
        self.assertEqual(mock_open.call_args, mock.call('/path/to/directory/neural_network.py', 'w'))
        self.assertEqual(mock_open.return_value.__enter__.return_value.write.call_count, 22)

    @mock.patch('control.os')
    def test_set_properties_success(self, mock_os):
        # Arrange
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        properties = {
            'output_path': '/path/to/directory',
            'training_data_path': '/path/to/file.csv',
            'train_size': 0.8,
            'optimizer': 'sgd',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': {
                'input': {
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                }
            }
        }

        # Act
        status = self.controller.set_properties(properties)

        # Assert
        self.assertTrue(status)

    @mock.patch('control.os')
    def test_set_properties_output_path_is_file(self, mock_os):
        # Arrange
        mock_os.path.isfile.side_effect = [True, True]
        mock_os.path.isdir.return_value = True
        mock_os.path.dirname.return_value = '/path/to'
        properties = {
            'output_path': '/path/to/directory',
            'training_data_path': '/path/to/file.csv',
            'train_size': 0.8,
            'optimizer': 'sgd',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': {
                'input': {
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                }
            }
        }

        # Act
        status = self.controller.set_properties(properties)

        # Assert
        self.assertFalse(status)
        self.assertEqual(self.controller.canvas_properties['output_path'], '/path/to')

    @mock.patch('control.os')
    def test_set_properties_output_path_does_not_exist(self, mock_os):
        # Arrange
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = False
        properties = {
            'output_path': '/path/to/directory',
            'training_data_path': '/path/to/file.csv',
            'train_size': 0.8,
            'optimizer': 'sgd',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': {
                'input': {
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                }
            }
        }

        # Act
        status = self.controller.set_properties(properties)

        # Assert
        self.assertFalse(status)
        self.assertEquals(mock_os.makedirs.call_args, mock.call('/path/to/directory'))

    @mock.patch('control.os')
    def test_set_properties_invalid_layer(self, mock_os):
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        # Arrange
        properties = {
            'output_path': '/path/to/directory',
            'training_data_path': '/path/to/file.csv',
            'train_size': 0.8,
            'optimizer': 'sgd',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': {
                'bad_layer': {
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                }
            }
        }

        # Act/Assert
        with self.assertRaises(NetworkException):
            status = self.controller.set_properties(properties)
