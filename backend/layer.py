from abc import ABC, abstractmethod

class LayerException(Exception):
    pass

class Layer(ABC):

    self.valid_activations = []

    self.name = ''
    self.size = 0
    self.activation = ''

    self.script_lines = ''

    def __init__(self, activation, output_size):
        if activation not in self.valid_activations:
            # Raise exception for now, should probably just log in the future
            # to prevent crashes
            raise LayerException('Invalid activation function: {0}'.format(activation))

        self.activation = activation
        self.size = output_size
        super().__init__()

    def write_lines(self, fd):
        fd.write(self.script_lines)

    @abstractmethod
    def assemble_script(self):
        pass

class Dense(Layer):
    self.valid_activations = ['relu', 'softmax', 'sigmoid']
    self.name = 'Dense'

    def assemble_script(self):
        self.script_lines = '{0}({1}, activation={2})'.format(self.name, self.size, self.activation)

class Dropout(Layer):
    self.keras_object_name = 'Dropout'

    def assemble_script(self):
        self.script_lines = '{0}({1}, activation={2})'.format(self.name, self.size, self.activation)
