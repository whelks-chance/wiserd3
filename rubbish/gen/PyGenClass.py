from rubbish.gen.PyGenMethod import PyGenMethod

__author__ = 'ubuntu'


class PyGenClass(object):

    def __init__(self, class_name, fields, extends='object', default_fields=False):
        self.extends = extends
        self.default_fields = default_fields
        self.fields = fields
        self.class_name = class_name
        
        self.methods = []
        
        self.whitespace_count = 0
        self.whitespace_block = '    '

    def get_indentation(self):
        indent = ''
        for i in range(0, self.whitespace_count):
            indent += self.whitespace_block
        return indent

    def get_header_text(self):
        return '\n\nclass {}({}):\n'.format(self.class_name, self.extends)

    def add_method(self, method_name, attributes):
        pygen_method = PyGenMethod(method_name, attributes)

        self.methods.append(pygen_method)

        return pygen_method

    def get_class_init(self):
        self.whitespace_count += 1

        lines = ['{}def __init__(self{}):'.format(self.get_indentation(), self.get_class_signiture_list())]

        self.whitespace_count += 1

        lines.append(self.get_default_fields())

        lines.append('{}pass'.format(self.get_indentation()))
        lines.append('\n')

        self.whitespace_count -= 1
        return '\n'.join(lines)

    def get_class_signiture_list(self):
        if len(self.fields):
            return ', ' + ', '.join(self.fields)
        else:
            return ''

    def get_default_fields(self):
        lines = []
        if self.default_fields:
            for field in self.fields:
                lines.append('{}self.{} = {}'.format(self.get_indentation(), field, field))

        return '\n'.join(lines)

    def get_methods(self):
        lines = []

        for method_shim in self.methods:
            assert isinstance(method_shim, PyGenMethod)
            for method_line in method_shim.get_method_lines():
                lines.append('{}{}'.format(self.get_indentation(), method_line))

        return '\n'.join(lines)
