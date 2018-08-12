from abc import ABC, abstractmethod

class GenericLayer(ABC):
    """
    Neural network layer base class.

    Available Properties:
        size: (int) -> The number of neurons in the layer
        batch_size: (int) -> The number of batches in the training data
        input_dim: (int) -> The number of features in the training data
        activation: (string) -> The chosen activation function
        percentage: (float) -> The percent chance a node is ignored for a given batch

    Adding a new layer:
        1. Create a new layer class that inherits from GenericLayer
        2. Import the class into `control.py` and add it to the `LAYER_TYPES` dict
        3. Add the available properties that can be set in the GUI
    """
    def __init__(self, properties):
        self.layer_properties = properties

    @abstractmethod
    def write_lines(self, fd):
        """
        Writes the lines to the Python neural network file that define the layer.
        :param fd: (file handle) -> Handle for the open file
        """
        pass

class InputLayer(GenericLayer):
    """
    Fully-connected or Dense layer type with specified input shape

    Properties:
        size: (int) -> The number of neurons in the layer
        batch_size: (int) -> The number of batches in the training data
        input_dim: (int) -> The number of features in the training data
    """
    def __init__(self, properties):
        super(InputLayer, self).__init__(properties)

    def write_lines(self, fd):
        # TODO dimsensions should not be indexed
        line = '\tmodel(Input(shape=({0},)))\n'.format(self.layer_properties['dimensions'])
        fd.write(line)

class DenseLayer(GenericLayer):
    """
    Fully-connected or Dense layer type. This class applies to both hidden and output layers.

    Properties:
        size: (int) -> The number of neurons in the layer
        activation: (string) -> The chosen activation function
    """
    def __init__(self, properties):
        super(DenseLayer, self).__init__(properties)

    def write_lines(self, fd):
        line = '\tmodel.add(Dense({0}, activation=\'{1}\'))\n'.format(self.layer_properties['size'],
                                                                      self.layer_properties['activation'])
        fd.write(line)

class DropoutLayer(GenericLayer):
    """
    Dropout layer type

    Properties:
        percentage: (float) -> The percent chance a node is ignored for a given batch
    """
    def __init__(self, properties):
        super(DropoutLayer, self).__init__(properties)

    def write_lines(self, fd):
        line = '\tmodel.add(Dropout({0}))\n'.format(self.layer_properties['percentage'])
        fd.write(line)
