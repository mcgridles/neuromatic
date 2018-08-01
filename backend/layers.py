from abc import ABC, abstractmethod

class GenericLayer(ABC):

    def __init__(self, properties):
        self.properties = properties

    @abstractmethod
    def write_lines(self, fd):
        pass

class DenseLayer(GenericLayer):

    def __init__(self, properties):
        super(DenseLayer, self).__init__(properties)

    def write_lines(self, fd):
        line = '\tmodel.add(Dense({0}, activation=\'{1}\'))\n'.format(self.properties['size'], self.properties['activation'])
        fd.write(line)

class DropoutLayer(GenericLayer):
    def __init__(self, properties):
        super(DropoutLayer, self).__init__(properties)

    def write_lines(self, fd):
        line = '\tmodel.add(Dropout({0}))\n'.format(self.properties['percentage'])
        fd.write(line)
