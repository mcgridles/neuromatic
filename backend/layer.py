class Layer(object):

    def __init__(self, properties):
        # properties should be JSON object which will require parsing
        self.properties = properties

    def write_lines(self, fd):
        line = '\tmodel.add({0}({1}, activation=\'{2}\'))\n'.format(self.properties['name'].capitalize(),
                                                                    self.properties['size'],
                                                                    self.properties['activation'])
        fd.write(line)

        if self.properties['dropout']:
            dropout_line = '\tmodel.add(Dropout({0}))\n'.format(self.properties['dropout'])
            fd.write(dropout_line)
