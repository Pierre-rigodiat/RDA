from os.path import join
from lxml import etree
from mgi.settings import SITE_ROOT


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


# FIXME Correct this object before commiting
class DataHandler(object):

    def __init__(self, filename):
        # FIXME only use dirname
        self.dirname = join(SITE_ROOT, filename)
        self.filename = join(SITE_ROOT, filename)

    @staticmethod
    def _get_file_content_as_xml(filename):
        file_string = ''
        is_in_tag = False

        with open(filename, 'r') as file_content:
            file_lines = [line.strip('\r\n\t ') for line in file_content.readlines()]

            for line in file_lines:
                if is_in_tag:  # Add space if we are in the tag
                    file_string += ' '

                file_string += line

                # Leave the tag if we have one more closing that opening
                if is_in_tag and line.count('>') == line.count('<') + 1:
                    is_in_tag = False
                elif line.count('<') != line.count('>'):  # In tag if opening and closing count are different
                    is_in_tag = True

                # In any other cases the tag flag doesn't change

        return etree.fromstring(file_string)

    def get_xsd(self):
        xsd_name = self.filename + '.xsd'
        return self._get_file_content_as_xml(xsd_name)

    def get_xsd2(self, filename):
        self.filename = join(self.dirname, filename)
        return self.get_xsd()

    def get_xml(self, filename):
        self.filename = join(self.dirname, filename)
        xml_name = self.filename + '.xml'
        return self._get_file_content_as_xml(xml_name)

    def get_html(self):
        html_name = self.filename + '.html'
        return self._get_file_content_as_xml(html_name)

    def get_html2(self, filename):
        self.filename = join(self.dirname, filename)
        return self.get_html()


def are_equals(xml_tree_a, xml_tree_b):
    tag_a = xml_tree_a.tag
    tag_b = xml_tree_b.tag

    attrib_a = xml_tree_a.attrib
    attrib_b = xml_tree_b.attrib

    text_a = xml_tree_a.text

    if type(text_a) == str:
        text_a = text_a.lstrip('\r\n\t ')
        text_a = text_a.rstrip('\r\n')

        if text_a == '':
            text_a = None

    text_b = xml_tree_b.text

    children_a = xml_tree_a.getchildren()
    children_b = xml_tree_b.getchildren()

    if len(children_a) != len(children_b):
        return False

    for i in xrange(len(children_a)):
        child_a = children_a[i]
        child_b = children_b[i]

        if not are_equals(child_a, child_b):
            return False

    if len(attrib_a) != len(attrib_b):
        return False

    for attr_key in attrib_a.keys():
        if attr_key not in attrib_b.keys():
            return False

        if attrib_a[attr_key] != attrib_b[attr_key]:
            return False

    return tag_a == tag_b and attrib_a == attrib_b and text_a == text_b
