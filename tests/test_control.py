import unittest
from unittest import mock

from backend import layers
from backend import control


class TestControl(unittest.TestCase):

    def setUp(self):
        self.controller = control.Control()
        self.controller.init_status(lambda msg: msg)

    @mock.patch('backend.control.shutil')
    @mock.patch('builtins.open')
    @mock.patch('backend.control.os')
    def test_generate_network(self, mock_os, mock_open, mock_shutil):
        # Arrange
        mock_os.path.join.return_value = '/path/to/directory/neuromatic_network.py'
        layer1 = layers.InputLayer({
            'dimensions': 512
        })
        layer2 = layers.DropoutLayer({
            'percentage': 0.8
        })
        layer3 = layers.DenseLayer({
            'size': 10,
            'activation': 'softmax'
        })
        self.controller.canvas_properties['canvas_name'] = 'neuromatic'
        self.controller.canvas_properties['optimizer'] = 'adam'
        self.controller.canvas_properties['loss'] = 'sparse_categorical_crossentropy'
        self.controller.canvas_properties['metrics'] = ['accuracy']
        self.controller.canvas_properties['epochs'] = 5
        self.controller.canvas_properties['project_directory'] = '/path/to/directory'
        self.controller.layers = [layer1, layer2, layer3]
        self.controller.can_generate = True

        # Act
        with self.assertLogs('control', level='DEBUG') as log:
            self.controller.generate_network()

        # Assert
        self.assertEqual(mock_open.call_args, mock.call('/path/to/directory/neuromatic_network.py', 'w'))
        self.assertEqual(mock_open.return_value.__enter__.return_value.write.call_count, 23)
        self.assertEquals(log.output, ['INFO:control:\nGenerating network...', 'INFO:control:Network generated'])

    @mock.patch('backend.control.os')
    def test_set_properties_success(self, mock_os):
        # Arrange
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        mock_os.path.splitext.return_value = ['filename', '.csv']
        properties = {
            'canvas_name': 'neuromatic',
            'project_directory': '/path/to/directory',
            'data_path': '/path/to/file.csv',
            'training_size': 0.8,
            'optimizer': 'sgd',
            'loss': 'categorical_crossentropy',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': [
                {
                    'type': 'input',
                    'dimensions': 784
                },
                {
                    'type': 'hidden',
                    'size': 100,
                    'activation': 'sigmoid',
                },
                {
                    'type': 'output',
                    'size': 10,
                    'activation': 'softmax',
                }
            ]
        }

        # Act
        with self.assertRaises(AssertionError):
            with self.assertLogs('control', level='DEBUG') as log:
                self.controller.set_properties(properties)

        # Assert
        self.assertEqual(self.controller.canvas_properties, properties)
        self.assertEqual(len(self.controller.layers), 3)
        self.assertTrue(self.controller.can_generate)
        self.assertTrue(self.controller.can_train)

    @mock.patch('backend.control.os')
    def test_set_properties_invalid_layer(self, mock_os):
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        mock_os.path.splitext.return_value = ['filename', '.csv']
        # Arrange
        properties = {
            'canvas_name': 'neuromatic',
            'project_directory': '/path/to/directory',
            'data_path': '/path/to/file.csv',
            'training_size': 0.8,
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
        self.assertFalse(self.controller.can_generate)
        self.assertTrue(self.controller.can_train)
        self.assertEqual(log.output, [
            'DEBUG:control:Invalid layer type: bad_layer',
            'DEBUG:control:Not enough layers'
        ])

    @mock.patch('backend.control.os')
    def test_set_properties_skip_empty_slots(self, mock_os):
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        mock_os.path.splitext.return_value = ['filename', '.csv']
        # Arrange
        properties = {
            'canvas_name': 'neuromatic',
            'project_directory': '/path/to/directory',
            'data_path': '/path/to/file.csv',
            'training_size': 0.8,
            'optimizer': 'sgd',
            'loss': 'categorical_crossentropy',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': [
                {
                    'type': 'empty'
                }
            ]
        }

        # Act
        with self.assertLogs('control', level='DEBUG') as log:
            self.controller.set_properties(properties)

        # Assert
        self.assertEqual(self.controller.layers, [])
        self.assertFalse(self.controller.can_generate)
        self.assertTrue(self.controller.can_train)
        self.assertEqual(log.output, [
            'DEBUG:control:Ignoring empty layer',
            'DEBUG:control:Not enough layers'
        ])

    @mock.patch('backend.control.os')
    def test_set_missing_properties(self, mock_os):
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        mock_os.path.splitext.return_value = ['filename', '.csv']
        # Arrange
        properties = {
            'canvas_name': 'neuromatic',
            'project_directory': '/path/to/directory',
            'data_path': '/path/to/file.csv',
            'training_size': 0.8,
            'layers': [
                {
                    'type': 'input',
                    'dimensions': 784
                },
                {
                    'type': 'hidden',
                    'size': 100,
                    'activation': 'sigmoid',
                },
                {
                    'type': 'output',
                    'size': 10,
                    'activation': 'softmax',
                }
            ]
        }

        # Act
        with self.assertRaises(AssertionError):
            with self.assertLogs('control', level='DEBUG') as log:
                self.controller.set_properties(properties)

        # Assert
        self.assertEqual(self.controller.canvas_properties['optimizer'], 'sgd')
        self.assertEqual(self.controller.canvas_properties['loss'], 'mean_squared_error')
        self.assertEqual(self.controller.canvas_properties['metrics'], ['accuracy'])
        self.assertEqual(self.controller.canvas_properties['epochs'], '1')
        self.assertTrue(self.controller.can_generate)
        self.assertTrue(self.controller.can_train)

    @mock.patch('backend.control.os')
    def test_set_properties_invalid_data_file(self, mock_os):
        # Arrange
        mock_os.path.isfile.side_effect = [False, True]
        mock_os.path.isdir.return_value = True
        mock_os.path.splitext.return_value = ['file', '.xls']
        properties = {
            'canvas_name': 'neuromatic',
            'project_directory': '/path/to/directory',
            'data_path': '/path/to/file.xls',
            'training_size': 0.8,
            'optimizer': 'sgd',
            'loss': 'categorical_crossentropy',
            'metrics': ['accuracy'],
            'epochs': 5,
            'layers': [
                {
                    'type': 'input',
                    'dimensions': 784
                },
                {
                    'type': 'hidden',
                    'size': 100,
                    'activation': 'sigmoid',
                },
                {
                    'type': 'output',
                    'size': 10,
                    'activation': 'softmax',
                }
            ]
        }

        # Act
        with self.assertLogs('control', level='DEBUG') as log:
            self.controller.set_properties(properties)

        # Assert
        self.assertEqual(self.controller.canvas_properties, properties)
        self.assertEqual(len(self.controller.layers), 3)
        self.assertTrue(self.controller.can_generate)
        self.assertFalse(self.controller.can_train)
        self.assertEqual(log.output, ['ERROR:control:Invalid data file type'])

    def test_sanitize_input(self):
        # Arrange
        string1 = 'Remove these characters;`\'\"|\n\t#'
        string2 = 'Do not remove these:!@$%^&*()-_=+:/\\?<>.,[]{}'

        # Act
        sanitized1 = self.controller.sanitize_input(string1)
        sanitized2 = self.controller.sanitize_input(string2)

        # Assert
        self.assertEqual(sanitized1, 'Remove these characters')
        self.assertEqual(sanitized2, string2)