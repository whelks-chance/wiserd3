__author__ = 'ubuntu'


class PyGenMethod(object):

    def __init__(self, method_name, attributes):
        self.method_name = method_name
        self.attributes = attributes
        self.whitespace_count = 0

    def get_method_lines(self):
        lines = []
        attribute_string = self.get_attribute_string()

        lines.append('def {}(self{}):'.format(self.method_name, attribute_string))
        lines.append('pass')
        return lines

    def get_attribute_string(self):
        if len(self.attributes):
            return ', ' + ', '.join(self.attributes)
        else:
            return ''
