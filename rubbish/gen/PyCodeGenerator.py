from rubbish.gen.PyGenClass import PyGenClass

__author__ = 'ubuntu'


class PyCodeGenerator(object):

    def __init__(self, classes=list()):
        self.classes = classes

    def create_class(self, class_name, fields, extends='object', default_fields=False):

        py_gen_class = PyGenClass(class_name, fields, extends=extends, default_fields=default_fields)

        self.classes.append(py_gen_class)

        return py_gen_class

    def write_code(self, filename):
        with open(filename, mode='wr') as pyfile:
            for class_shim in self.classes:

                lines = []
                assert isinstance(class_shim, PyGenClass)
                lines.append(class_shim.get_header_text())

                lines.append(class_shim.get_class_init())

                lines.append(class_shim.get_methods())

                pyfile.writelines(lines)
