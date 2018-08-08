import unittest
from unittest import mock

from backend.layers import InputLayer, DenseLayer, DropoutLayer

@mock.patch('builtins.open')
class TestLayers(unittest.TestCase):

    def setUp(self):
        self.layer_properties = {
            'size': 10,
            'activation': 'sigmoid',
            'batch_size': 1000,
            'input_dim': 784,
            'percentage': 0.2,
        }

    def test_input_layer_write(self, mock_open):
        # Arrange
        input_layer = InputLayer(self.layer_properties)

        # Act
        input_layer.write_lines(mock_open.return_value.__enter__.return_value)

        # Assert
        self.assertTrue(mock_open.return_value.__enter__.return_value.write.call_once_with(
            '\tmodel.add(Dense(10, activation=\'sigmoid\', input_shape=(1000,784)))'
        ))

    def test_dense_layer_write(self, mock_open):
        # Arrange
        dense_layer = DenseLayer(self.layer_properties)

        # Act
        dense_layer.write_lines(mock_open.return_value.__enter__.return_value)

        # Assert
        self.assertTrue(mock_open.return_value.__enter__.return_value.write.call_once_with(
            '\tmodel.add(Dense(10, activation=\'sigmoid\'))'
        ))

    def test_dropout_layer_write(self, mock_open):
        # Arrange
        dropout_layer = DropoutLayer(self.layer_properties)

        # Act
        dropout_layer.write_lines(mock_open.return_value.__enter__.return_value)

        # Assert
        self.assertTrue(mock_open.return_value.__enter__.return_value.write.call_once_with(
            '\tmodel.add(Dropout(0.2))'
        ))
