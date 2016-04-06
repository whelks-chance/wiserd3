from rubbish.gen.PyCodeGenerator import PyCodeGenerator

__author__ = 'ubuntu'

pycodegen = PyCodeGenerator()

class_shim_main = pycodegen.create_class(
    'MainClass',
    ['an_int', 'a_string'],
    extends='models.Model',
    default_fields=True
)

class_shim_main.add_method('a_method', ['inner_string', 'inner_int'])

pycodegen.write_code('output.py')
