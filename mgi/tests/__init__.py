class VariableTypesGenerator(object):

    def __init__(self):
        # List extracted from https://docs.python.org/2/library/types.html
        self.possible_types = {
            'int': 50,
            'float': 4.5,
            'str': "string",
            'unicode': u"string",
            'none': None,
            'bool': False,
            'long': 1L,
            'complex': 1.0j,
            'tuples': (1, 2),
            'list': [],
            'dict': {},
            'func': lambda x: x,
            # Generator type
            'code': compile('print "compile"', 'test', 'exec'),
            # Class
            # Instance
            # Method
            # UnboundMethod
            # BuiltinFunction
            # Module
            # File
            # Xrange
            # Slice
            # Ellipsis
            # Traceback
            # Frame
            # Buffer
            # DictProxy
            # NotImplemented
            # GetSetDescriptor
            # MemberDescriptor
        }

    def generate_types_excluding(self, excluded_types_list):
        if type(excluded_types_list) != list:
            raise TypeError('generate_types_excluding only accept lists')

        return [
            val for key, val in self.possible_types.items() if key not in excluded_types_list
        ]

    def generate_type_including(self, include_types_list):
        if type(include_types_list) != list:
            raise TypeError('generate_type_including only accept lists')

        return [
            val for key, val in self.possible_types.items() if key in include_types_list
        ]