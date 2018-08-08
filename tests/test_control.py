import unittest
from unittest import mock

from backend.layers import DenseLayer, DropoutLayer
from backend.control import Control


class TestControl(unittest.TestCase):

    def setUp(self):
        add_text = lambda msg: msg
        self.controller = Control(add_text)

    @mock.patch('backend.control.shutil')
    @mock.patch('builtins.open')
    def test_generate_network(self, mock_open, mock_shutil):
        # Arrange
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
        with self.assertLogs('control', level='DEBUG') as log:
            self.controller.generate_network()

        # Assert
        self.assertEqual(mock_open.call_args, mock.call('/path/to/directory/neural_network.py', 'w'))
        self.assertEqual(mock_open.return_value.__enter__.return_value.write.call_count, 24)
        self.assertEquals(log.output, ['INFO:control:Generating network...', 'INFO:control:Network generated.'])

    @mock.patch('backend.control.os')
    def test_set_properties_success(self, mock_os):
        # Arrange
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        properties = {
            'output_path': '/path/to/directory',
            'training_data_path': '/path/to/file.csv',
            'train_size': 0.8,
            'optimizer': 'sgd',
            'loss': 'categorical_crossentropy',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': [
                {
                    'type': 'input',
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                },
                {
                    'type': 'dense',
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                }
            ]
        }

        # Act
        with self.assertRaises(AssertionError):
            with self.assertLogs('control', level='DEBUG') as log:
                self.controller.set_properties(properties)

        # Assert
        self.assertEqual(self.controller.canvas_properties, properties)
        self.assertEqual(len(self.controller.layers), 2)

    @mock.patch('backend.control.os')
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
            'loss': 'categorical_crossentropy',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': [
                {
                    'type': 'input',
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                }
            ]
        }

        # Act
        with self.assertLogs('control', level='DEBUG') as log:
            self.controller.set_properties(properties)

        # Assert
        self.assertEqual(self.controller.canvas_properties['output_path'], '/path/to')
        self.assertEqual(log.output, [
            'WARNING:control:/path/to/directory is a file, setting output path to /path/to',
            'WARNING:control:Some parameters were invalid'
        ])

    @mock.patch('backend.control.os')
    def test_set_properties_output_path_does_not_exist(self, mock_os):
        # Arrange
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = False
        properties = {
            'output_path': '/path/to/directory',
            'training_data_path': '/path/to/file.csv',
            'train_size': 0.8,
            'optimizer': 'sgd',
            'loss': 'categorical_crossentropy',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': [
                {
                    'type': 'input',
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                }
            ]
        }

        # Act
        with self.assertLogs('control', level='DEBUG') as log:
            self.controller.set_properties(properties)

        # Assert
        self.assertEquals(mock_os.makedirs.call_args, mock.call('/path/to/directory'))
        self.assertEqual(len(self.controller.layers), 1)
        self.assertEqual(log.output, [
            'WARNING:control:/path/to/directory does not exist - creating',
            'WARNING:control:Some parameters were invalid'
        ])

    @mock.patch('backend.control.os')
    def test_set_properties_invalid_layer(self, mock_os):
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        # Arrange
        properties = {
            'output_path': '/path/to/directory',
            'training_data_path': '/path/to/file.csv',
            'train_size': 0.8,
            'optimizer': 'sgd',
            'loss': 'categorical_crossentropy',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': [
                {
                    'type': 'bad_layer',
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                }
            ]
        }

        # Act
        with self.assertLogs('control', level='DEBUG') as log:
            self.controller.set_properties(properties)

        # Assert
        self.assertEqual(self.controller.layers, [])
        self.assertEqual(log.output, [
            'DEBUG:control:Invalid layer type: bad_layer',
            'ERROR:control:Invalid network configuration',
            'WARNING:control:Some parameters were invalid'
        ])

    @mock.patch('backend.control.os')
    def test_set_missing_properties(self, mock_os):
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        # Arrange
        properties = {
            'output_path': '/path/to/directory',
            'training_data_path': '/path/to/file.csv',
            'train_size': 0.8,
            'epochs': 5,
            'layers': [
                {
                    'type': 'input',
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                },
                {
                    'type': 'dense',
                    'size': 10,
                    'activation': 'sigmoid',
                    'batch_size': 100,
                    'input_dim': 784
                }
            ]
        }

        # Act
        with self.assertRaises(AssertionError):
            with self.assertLogs('control', level='DEBUG') as log:
                self.controller.set_properties(properties)

        # Assert
        self.assertEqual(self.controller.canvas_properties['optimizer'], 'sgd')
        self.assertEqual(self.controller.canvas_properties['loss'], 'sparse_categorical_crossentropy')
        self.assertEqual(self.controller.canvas_properties['metrics'], ['accuracy'])
