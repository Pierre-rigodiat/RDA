"""
"""
from django.http.request import HttpRequest
from django.test import TestCase
from django.utils.importlib import import_module
from os.path import join
from curate.parser import generate_choice, generate_restriction, \
    generate_simple_type, generate_extension, generate_simple_content, \
    generate_sequence, generate_element, generate_complex_type, generate_element_absent, generate_sequence_absent, \
    generate_form, generate_module, generate_complex_content
from mgi.models import FormElement, FormData
from mgi.tests import DataHandler, are_equals
from lxml import etree


##################################################
# Part II: Schema parsing testing
##################################################

class ParserGenerateFormTestSuite(TestCase):
    """
    """

    def setUp(self):
        schema_data = join('curate', 'tests', 'data', 'parser', 'schema')
        self.schema_data_handler = DataHandler(schema_data)

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition

        form_data = FormData()
        form_data.name = ''
        form_data.user = ''
        form_data.template = ''

        form_data.save()

        self.request.session['curateFormData'] = form_data.pk

    def test_create_include(self):
        xsd_files = join('include', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_import(self):
        xsd_files = join('import', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_redefine(self):
        xsd_files = join('redefine', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_simple_type(self):
        xsd_files = join('simple_type', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_complex_type(self):
        xsd_files = join('complex_type', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_group(self):
        xsd_files = join('group', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_attribute_group(self):
        xsd_files = join('attribute_group', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_element_basic(self):
        xsd_files = join('element', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_element_multiple(self):
        xsd_files = join('element', 'multiple')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_attribute(self):
        xsd_files = join('attribute', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_notation(self):
        xsd_files = join('notation', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_multiple(self):
        xsd_files = join('multiple', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_target_namespace_element(self):
        xsd_files = join('target_namespace', 'element', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_target_namespace_ref(self):
        xsd_files = join('target_namespace', 'ref', 'basic')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # def test_reload_include(self):
    #     xsd_files = join('include', 'basic')
    #     xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)
    #
    #     self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)
    #     self.request.session['curate_edit'] = True
    #
    #     form_data = FormData()
    #
    #     xml_data = self.schema_data_handler.get_xml(xsd_files)
    #
    #     form_data.xml_data = etree.tostring(xml_data)
    #     form_data.name = ''
    #     form_data.user = ''
    #     form_data.template = ''
    #
    #     form_data.save()
    #
    #     self.request.session['curateFormData'] = form_data.pk
    #
    #     result_string = generate_form(self.request)
    #
    #     print result_string
    #     # result_string = '<div>' + result_string + '</div>'
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.schema_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_reload_import(self):
    #     pass
    #
    # def test_reload_redefine(self):
    #     pass
    #
    # def test_reload_simple_type(self):
    #     pass
    #
    # def test_reload_complex_type(self):
    #     pass
    #
    # def test_reload_group(self):
    #     pass
    #
    # def test_reload_attribute_group(self):
    #     pass

    def test_reload_element(self):
        xsd_files = join('element', 'basic')
        xsd_reload_files = join('element', 'basic.reload')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)
        self.request.session['curate_edit'] = True

        form_data = FormData()

        xml_data = self.schema_data_handler.get_xml(xsd_files)

        form_data.xml_data = etree.tostring(xml_data)
        form_data.name = ''
        form_data.user = ''
        form_data.template = ''

        form_data.save()

        self.request.session['curateFormData'] = form_data.pk

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_reload_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_elements(self):
        xsd_files = join('element', 'multiple')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)
        self.request.session['curate_edit'] = True

        form_data = FormData()

        xml_data = self.schema_data_handler.get_xml(xsd_files)

        form_data.xml_data = etree.tostring(xml_data)
        form_data.name = ''
        form_data.user = ''
        form_data.template = ''

        form_data.save()

        self.request.session['curateFormData'] = form_data.pk

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload__target_namespace_element(self):
        xsd_files = join('target_namespace', 'element', 'basic')
        xsd_reload_files = join('target_namespace', 'element', 'basic.reload')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)
        self.request.session['curate_edit'] = True

        form_data = FormData()

        xml_data = self.schema_data_handler.get_xml(xsd_files)

        form_data.xml_data = etree.tostring(xml_data)
        form_data.name = ''
        form_data.user = ''
        form_data.template = ''

        form_data.save()

        self.request.session['curateFormData'] = form_data.pk

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_reload_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload__target_namespace_ref(self):
        xsd_files = join('target_namespace', 'ref', 'basic')
        xsd_reload_files = join('target_namespace', 'ref', 'basic.reload')
        xsd_tree = self.schema_data_handler.get_xsd2(xsd_files)

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)
        self.request.session['curate_edit'] = True

        form_data = FormData()

        xml_data = self.schema_data_handler.get_xml(xsd_files)

        form_data.xml_data = etree.tostring(xml_data)
        form_data.name = ''
        form_data.user = ''
        form_data.template = ''

        form_data.save()

        self.request.session['curateFormData'] = form_data.pk

        result_string = generate_form(self.request)
        # print result_string
        # self.assertEqual(result_string, '')

        result_html = etree.fromstring(result_string)
        expected_html = self.schema_data_handler.get_html2(xsd_reload_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # def test_reload_attribute(self):
    #     pass
    #
    # def test_reload_multiple(self):
    #     pass


class ParserGenerateElementTestSuite(TestCase):
    """
    """

    def setUp(self):
        element_data = join('curate', 'tests', 'data', 'parser', 'element')
        self.element_data_handler = DataHandler(element_data)

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.maxDiff = None

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    def test_create_simple_type_basic(self):
        xsd_files = join('simple_type', 'basic')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_element(self.request, xsd_element, xsd_tree, full_path='')

        expected_element = {
            'value': None,
            'tag': 'element',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'simple_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'restriction',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'child0',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        },
                                        {
                                            'value': 'child1',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_simple_type_unbounded(self):
        xsd_files = join('simple_type', 'unbounded')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence/xs:element',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_element(self.request, xsd_element, xsd_tree, full_path='')

        expected_element = {
            'value': None,
            'tag': 'element',
            'occurs': (2.0, 2.0, float('infinity')),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'simple_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'restriction',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'child0',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        },
                                        {
                                            'value': 'child1',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'simple_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'restriction',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'child0',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        },
                                        {
                                            'value': 'child1',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_complex_type_basic(self):
        xsd_files = join('complex_type', 'basic')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_element(self.request, xsd_element, xsd_tree, full_path='')

        expected_element = {
            'tag': 'element',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'complex_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'sequence',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': '',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': '',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_complex_type_unbounded(self):
        xsd_files = join('complex_type', 'unbounded')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence/xs:element',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_element(self.request, xsd_element, xsd_tree, full_path='')

        expected_element = {
            'tag': 'element',
            'occurs': (2., 2., float('infinity')),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'complex_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'sequence',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': '',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': '',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'complex_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'sequence',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': '',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': '',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # def test_create_unique_basic(self):
    #     # TODO implement when support for unique is wanted
    #     xsd_files = join('unique', 'basic')
    #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/element')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.element_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_unique_unbounded(self):
    #     # TODO implement when support for unique is wanted
    #     xsd_files = join('unique', 'unbounded')
    #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence/element')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.element_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_key_basic(self):
    #     # TODO implement when support for key is wanted
    #     xsd_files = join('key', 'basic')
    #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/element')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.element_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_key_unbounded(self):
    #     # TODO implement when support for key is wanted
    #     xsd_files = join('key', 'unbounded')
    #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence/element')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.element_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_keyref_basic(self):
    #     # TODO implement when support for keyref is wanted
    #     xsd_files = join('keyref', 'basic')
    #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/element')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.element_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_keyref_unbounded(self):
    #     # TODO implement when support for keyref is wanted
    #     xsd_files = join('keyref', 'unbounded')
    #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence/element')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.element_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

    # TODO Implement unique, key and keyref for these tests
    # def test_create_simple_unique_basic(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_simple_unique_unbounded(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_simple_key_basic(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_simple_key_unbounded(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_simple_keyref_basic(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_simple_keyref_unbounded(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_complex_unique_basic(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_complex_unique_unbounded(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_complex_key_basic(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_complex_key_unbounded(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_complex_keyref_basic(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_complex_keyref_unbounded(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_multiple_basic(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_multiple_unbounded(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('element', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_simple_type_basic(self):
        xsd_files = join('simple_type', 'basic')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element', namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.element_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))

        result_string = generate_element(self.request, xsd_element, xsd_tree, full_path='',
                                         edit_data_tree=edit_data_tree)

        expected_element = {
            'value': None,
            'tag': 'element',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'simple_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'restriction',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'child0',
                                            'tag': 'enumeration/selected',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        },
                                        {
                                            'value': 'child1',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_simple_type_unbounded(self):
        xsd_files = join('simple_type', 'unbounded')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence/xs:element',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.element_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))

        result_string = generate_element(self.request, xsd_element, xsd_tree, full_path='/root',
                                         edit_data_tree=edit_data_tree)

        expected_element = {
            'value': None,
            'tag': 'element',
            'occurs': (2.0, 3, float('infinity')),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'simple_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'restriction',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'child0',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        },
                                        {
                                            'value': 'child1',
                                            'tag': 'enumeration/selected',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'simple_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'restriction',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'child0',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        },
                                        {
                                            'value': 'child1',
                                            'tag': 'enumeration/selected',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'simple_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'restriction',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'child0',
                                            'tag': 'enumeration/selected',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        },
                                        {
                                            'value': 'child1',
                                            'tag': 'enumeration',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_complex_type_basic(self):
        xsd_files = join('complex_type', 'basic')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element', namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.element_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))

        result_string = generate_element(self.request, xsd_element, xsd_tree, full_path='',
                                         edit_data_tree=edit_data_tree)

        expected_element = {
            'tag': 'element',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'complex_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'sequence',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': 'entry0',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': 'entry1',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_complex_type_unbounded(self):
        xsd_files = join('complex_type', 'unbounded')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence/xs:element',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.element_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))

        result_string = generate_element(self.request, xsd_element, xsd_tree, full_path='/root',
                                         edit_data_tree=edit_data_tree)

        expected_element = {
            'tag': 'element',
            'occurs': (2., 3, float('infinity')),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'complex_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'sequence',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': 'entry0',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': 'entry1',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'complex_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'sequence',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': 'entry2',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': 'entry3',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'tag': 'elem-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'complex_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'sequence',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': 'entry4',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': None,
                                                    'children': [
                                                        {
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'value': 'entry5',
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

        # todo implement these test when the parser implement the functionalities
        # def test_reload_unique_basic(self):
        #     xsd_files = join('unique', 'basic')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/element')[0]
        #
        #     self.request.session['curate_edit'] = True
        #
        #     xml_tree = self.element_data_handler.get_xml(xsd_files)
        #     xml_data = etree.tostring(xml_tree)
        #
        #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        #     etree.set_default_parser(parser=clean_parser)
        #     # load the XML tree from the text
        #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        #
        #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='',
        #                                     edit_data_tree=edit_data_tree)
        #     print result_string
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))

        # def test_reload_unique_unbounded(self):
        #     xsd_files = join('complex_type', 'unbounded')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence/element')[0]
        #
        #     self.request.session['curate_edit'] = True
        #
        #     xml_tree = self.element_data_handler.get_xml(xsd_files)
        #     xml_data = etree.tostring(xml_tree)
        #
        #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        #     etree.set_default_parser(parser=clean_parser)
        #     # load the XML tree from the text
        #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        #
        #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='/root',
        #                                     edit_data_tree=edit_data_tree)
        #     print result_string
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))
        #
        # def test_reload_key_basic(self):
        #     xsd_files = join('simple_type', 'basic')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/element')[0]
        #
        #     self.request.session['curate_edit'] = True
        #
        #     xml_tree = self.element_data_handler.get_xml(xsd_files)
        #     xml_data = etree.tostring(xml_tree)
        #
        #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        #     etree.set_default_parser(parser=clean_parser)
        #     # load the XML tree from the text
        #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        #
        #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='',
        #                                     edit_data_tree=edit_data_tree)
        #     print result_string
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))
        #
        # def test_reload_key_unbounded(self):
        #     xsd_files = join('complex_type', 'unbounded')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence/element')[0]
        #
        #     self.request.session['curate_edit'] = True
        #
        #     xml_tree = self.element_data_handler.get_xml(xsd_files)
        #     xml_data = etree.tostring(xml_tree)
        #
        #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        #     etree.set_default_parser(parser=clean_parser)
        #     # load the XML tree from the text
        #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        #
        #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='/root',
        #                                     edit_data_tree=edit_data_tree)
        #     print result_string
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))
        #
        # def test_reload_keyref_basic(self):
        #     xsd_files = join('simple_type', 'basic')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/element')[0]
        #
        #     self.request.session['curate_edit'] = True
        #
        #     xml_tree = self.element_data_handler.get_xml(xsd_files)
        #     xml_data = etree.tostring(xml_tree)
        #
        #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        #     etree.set_default_parser(parser=clean_parser)
        #     # load the XML tree from the text
        #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        #
        #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='',
        #                                     edit_data_tree=edit_data_tree)
        #     print result_string
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))
        #
        # def test_reload_keyref_unbounded(self):
        #     xsd_files = join('complex_type', 'unbounded')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence/element')[0]
        #
        #     self.request.session['curate_edit'] = True
        #
        #     xml_tree = self.element_data_handler.get_xml(xsd_files)
        #     xml_data = etree.tostring(xml_tree)
        #
        #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        #     etree.set_default_parser(parser=clean_parser)
        #     # load the XML tree from the text
        #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        #
        #     result_string = generate_element(self.request, xsd_element, xsd_tree, '', full_path='/root',
        #                                     edit_data_tree=edit_data_tree)
        #     print result_string
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files + '.reload')
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateElementAbsentTestSuite(TestCase):
    """
    """

    def setUp(self):
        element_data = join('curate', 'tests', 'data', 'parser', 'element_absent')
        self.element_data_handler = DataHandler(element_data)

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None

        self.maxDiff = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

        self.form_element = FormElement()
        self.form_element.xml_xpath = ''

    def test_create_simple_type_basic(self):
        xsd_files = join('simple_type', 'basic')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)

        expected_element = {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'simple_type', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'restriction', 'occurs': (1, 1, 1), 'module': None,
                 'children': [{'module': None, 'tag': 'input', 'occurs': (1, 1, 1), 'value': '', 'children': []}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_simple_type_unbounded(self):
        xsd_files = join('simple_type', 'unbounded')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)

        expected_element = {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'simple_type', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'restriction', 'occurs': (1, 1, 1), 'module': None,
                 'children': [{'module': None, 'tag': 'input', 'occurs': (1, 1, 1), 'value': '', 'children': []}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.element_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_complex_type_basic(self):
        xsd_files = join('complex_type', 'basic')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)

        expected_element = {
            'tag': 'elem-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                },
                                            ]
                                        },
                                    ]
                                },
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                },
                                            ]
                                        },
                                    ]
                                },
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.element_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_complex_type_unbounded(self):
        xsd_files = join('complex_type', 'unbounded')
        xsd_tree = etree.ElementTree(self.element_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)

        expected_element = {
            'tag': 'elem-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                },
                                            ]
                                        },
                                    ]
                                },
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                },
                                            ]
                                        },
                                    ]
                                },
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.element_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

        # def test_create_unique_basic(self):
        #     # TODO Verify this test is correct
        #     xsd_files = join('unique', 'basic')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/element')[0]
        #
        #     result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)
        #     # print result_string
        #     self.assertEqual(result_string, '')
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files)
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))
        #
        # def test_create_unique_unbounded(self):
        #     xsd_files = join('unique', 'unbounded')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/element')[0]
        #
        #     result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)
        #     # print result_string
        #     self.assertEqual(result_string, '')
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files)
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))
        #
        # def test_create_key_basic(self):
        #     # TODO Rewrite the test for key / keyref
        #     xsd_files = join('key', 'basic')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/element')[0]
        #
        #     result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)
        #     # print result_string
        #     self.assertEqual(result_string, '')
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files)
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))
        #
        # def test_create_key_unbounded(self):
        #     xsd_files = join('key', 'unbounded')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/element')[0]
        #
        #     result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)
        #     # print result_string
        #     self.assertEqual(result_string, '')
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files)
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))
        #
        # def test_create_keyref_basic(self):
        #     # TODO Rewrite the test for key / keyref
        #     xsd_files = join('keyref', 'basic')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/element')[0]
        #
        #     result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)
        #     # print result_string
        #     self.assertEqual(result_string, '')
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files)
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))
        #
        # def test_create_keyref_unbounded(self):
        #     xsd_files = join('keyref', 'unbounded')
        #     xsd_tree = self.element_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/element')[0]
        #
        #     result_string = generate_element_absent(self.request, xsd_element, xsd_tree, self.form_element)
        #     # print result_string
        #     self.assertEqual(result_string, '')
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.element_data_handler.get_html2(xsd_files)
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateSequenceTestSuite(TestCase):
    """
    """

    def setUp(self):
        sequence_data = join('curate', 'tests', 'data', 'parser', 'sequence')
        self.sequence_data_handler = DataHandler(sequence_data)

        self.maxDiff = None

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    def test_create_element_basic(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('element', 'basic')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='')

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None,
                 'children': [{'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_element_unbounded(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('element', 'unbounded')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='')

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (2.0, 2.0, float('infinity')), 'module': None,
                            'children': [{'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]}]}]},
                                         {'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('element', 'unbounded'))

        self.assertTrue(are_equals(result_html, expected_html))

    # def test_create_group_basic(self):
    #     # FIXME change test and implement group support on the parser
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('group', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_sequence(self.request, xsd_element, xsd_tree, '', full_path='')
    #     self.assertEqual(result_string, "")
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.sequence_data_handler.get_html2(join('element', 'element'))
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_group_unbounded(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('group', 'unbounded'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_sequence(self.request, xsd_element, xsd_tree, '', full_path='')
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('group', 'unbounded'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

    def test_create_choice_basic(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('choice', 'basic')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('choice', 'basic'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_choice_unbounded(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('choice', 'unbounded')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (2.0, 2.0, float('infinity')), 'module': None,
                            'children': [{'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]}]},
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]}]}]},
                                         {'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]}]},
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('choice', 'unbounded'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_sequence_basic(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('sequence', 'basic')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('sequence', 'basic'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_sequence_unbounded(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('sequence', 'unbounded')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (2.0, 2.0, float('infinity')), 'module': None,
                            'children': [{'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]}]}]}]},
                                         {'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('sequence', 'unbounded'))

        self.assertTrue(are_equals(result_html, expected_html))

    # def test_create_any_basic(self):
    #     # FIXME How do we want to handle any's?
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('any', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_sequence(self.request, xsd_element, xsd_tree, '', full_path='')
    #     self.assertEqual(result_string, '')
    #
    # def test_create_any_unbounded(self):
    #     # FIXME How do we want to handle any's?
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('any', 'unbounded'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_sequence(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.sequence_data_handler.get_html2(join('any', 'unbounded'))
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

    def test_create_multiple_basic(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('multiple', 'basic')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence(self.request, xsd_element, xsd_tree, self.namespace, full_path='')

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
            {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None,
                 'children': [{'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
            {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
                {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.sequence_data_handler.get_html2(join('multiple', 'basic'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_multiple_unbounded(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('multiple', 'unbounded')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (2.0, 2.0, float('infinity')), 'module': None,
                            'children': [{'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]}]},
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]}]},
                                              {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]}]},
                                              {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]}]},
                                                            {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                                {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                                 'module': None, 'children': [
                                                                    {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                     'module': None, 'children': []}]}]}]}]},
                                         {'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]}]},
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]}]},
                                              {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]}]},
                                              {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]}]},
                                                            {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                                {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                                 'module': None, 'children': [
                                                                    {'value': '', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                     'module': None, 'children': []}]}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('multiple', 'unbounded'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_element_basic(self):
        xsd_files = join('element', 'basic')
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.sequence_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='/root',
                                          edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': 'entry0', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_element_unbounded(self):
        # fixme correct bug
        xsd_files = join('element', 'unbounded')
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.sequence_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='/root',
                                          edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (2.0, 1, float('infinity')), 'module': None,
                            'children': [{'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'element', 'occurs': (1, 3, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': 'entry0', 'tag': 'input', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]},
                                                            {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                                {'value': 'entry1', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                 'module': None, 'children': []}]},
                                                            {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                                {'value': 'entry2', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                 'module': None, 'children': []}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    # fixme implement groups
    # def test_reload_group_basic(self):
    #     xsd_files = join('element', 'basic')
    #     xsd_tree = self.sequence_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.sequence_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_sequence(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                    edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_reload_group_unbounded(self):
    #     xsd_files = join('element', 'basic')
    #     xsd_tree = self.sequence_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.sequence_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_sequence(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                    edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_choice_basic(self):
        xsd_files = join('choice', 'basic')
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.sequence_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='/root',
                                          edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': 'entry0', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None,
                             'children': []}]}]},
                    {'value': None, 'tag': 'element', 'occurs': (1, 0, 1), 'module': None, 'children': []}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_choice_unbounded(self):
        xsd_files = join('choice', 'unbounded')
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.sequence_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='/root',
                                          edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (2.0, 1, float('infinity')), 'module': None,
                            'children': [{'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 2, 1),
                                                        'module': None, 'children': [
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': 'entry1', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]},
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': 'entry2', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]}]},
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': 'entry0', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]}]}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_sequence_basic(self):
        xsd_files = join('sequence', 'basic')
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.sequence_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='/root',
                                          edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': 'entry0', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_sequence_unbounded(self):
        xsd_files = join('sequence', 'unbounded')
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.sequence_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='/root',
                                          edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (2.0, 1, float('infinity')), 'module': None,
                            'children': [{'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'element', 'occurs': (1, 3, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': 'entry0', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]},
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': 'entry1', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]},
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': 'entry2', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    # TODO implement tests
    # def test_reload_any_basic(self):
    #     xsd_files = join('element', 'basic')
    #     xsd_tree = self.sequence_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.sequence_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_sequence(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                    edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_reload_any_unbounded(self):
    #     xsd_files = join('element', 'basic')
    #     xsd_tree = self.sequence_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.sequence_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_sequence(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                    edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_multiple_basic(self):
        xsd_files = join('multiple', 'basic')
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.sequence_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='/root',
                                          edit_data_tree=edit_data_tree)

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': 'entry0', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None,
                             'children': []}]}]},
                    {'value': None, 'tag': 'element', 'occurs': (1, 0, 1), 'module': None, 'children': []}]}]},
            {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': 'entry1', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
            {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': 'entry2', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
                {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': 'entry3', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_multiple_unbounded(self):
        xsd_files = join('multiple', 'unbounded')
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.sequence_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_sequence(self.request, xsd_element, xsd_tree, full_path='/root',
                                          edit_data_tree=edit_data_tree)

        expected_element = {'value': None, 'tag': 'sequence', 'occurs': (2.0, 1, float('infinity')), 'module': None,
                            'children': [{'value': None, 'tag': 'sequence-iter', 'occurs': (1, 1, 1), 'module': None,
                                          'children': [
                                              {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': 'entry0', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]}]},
                                                       {'value': None, 'tag': 'element', 'occurs': (1, 2, 1),
                                                        'module': None, 'children': [
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': 'entry4', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]},
                                                           {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': [
                                                               {'value': 'entry8', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                'module': None, 'children': []}]}]}]}]},
                                              {'value': None, 'tag': 'element', 'occurs': (1, 3, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                       {'value': 'entry1', 'tag': 'input', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': []}]},
                                                            {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                                {'value': 'entry5', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                 'module': None, 'children': []}]},
                                                            {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                             'module': None, 'children': [
                                                                {'value': 'entry9', 'tag': 'input', 'occurs': (1, 1, 1),
                                                                 'module': None, 'children': []}]}]},
                                              {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None,
                                               'children': [{'value': None, 'tag': 'element', 'occurs': (1, 3, 1),
                                                             'module': None, 'children': [
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': 'entry2', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]},
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': 'entry6', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]},
                                                       {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                        'module': None, 'children': [
                                                           {'value': 'entry10', 'tag': 'input', 'occurs': (1, 1, 1),
                                                            'module': None, 'children': []}]}]},
                                                            {'value': None, 'tag': 'element', 'occurs': (1, 3, 1),
                                                             'module': None, 'children': [
                                                                {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                                 'module': None, 'children': [
                                                                    {'value': 'entry3', 'tag': 'input',
                                                                     'occurs': (1, 1, 1), 'module': None,
                                                                     'children': []}]},
                                                                {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                                 'module': None, 'children': [
                                                                    {'value': 'entry7', 'tag': 'input',
                                                                     'occurs': (1, 1, 1), 'module': None,
                                                                     'children': []}]},
                                                                {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1),
                                                                 'module': None, 'children': [
                                                                    {'value': 'entry11', 'tag': 'input',
                                                                     'occurs': (1, 1, 1), 'module': None,
                                                                     'children': []}]}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateSequenceAbsentTestSuite(TestCase):
    """
    """

    def setUp(self):
        sequence_data = join('curate', 'tests', 'data', 'parser', 'sequence_absent')
        self.sequence_data_handler = DataHandler(sequence_data)

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.maxDiff = None

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    def test_create_element_basic(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('element', 'basic')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree)
        # print result_string

        expected_element = {
            'tag': 'sequence-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'element',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': '',
                                    'children': []
                                }
                            ]
                        }

                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('element', 'basic'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_element_unbounded(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('element', 'unbounded')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree)
        # print result_string

        expected_element = {
            'tag': 'sequence-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'element',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': '',
                                    'children': []
                                }
                            ]
                        }

                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('element', 'unbounded'))

        self.assertTrue(are_equals(result_html, expected_html))

    # def test_create_group_basic(self):
    #     # FIXME change test and implement group support on the parser
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('group', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree, '')
    #     self.assertEqual(result_string, "")
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.sequence_data_handler.get_html2(join('element', 'element'))
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    # def test_create_group_unbounded(self):
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('group', 'unbounded'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree, '')
    #     # print result_string
    #     self.assertEqual(result_string, "")
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.sequence_data_handler.get_html2(join('group', 'unbounded'))
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_create_choice_basic(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('choice', 'basic')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree)
        # print result_string

        expected_element = {
            'tag': 'sequence-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'choice-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                }
                                            ]
                                        }

                                    ]
                                },
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': []
                                },
                            ]
                        }

                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('choice', 'basic'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_choice_unbounded(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('choice', 'unbounded')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree)
        # print result_string

        expected_element = {
            'tag': 'sequence-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'choice-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                }
                                            ]
                                        }

                                    ]
                                },
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': []
                                },
                            ]
                        }

                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('choice', 'unbounded'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_sequence_basic(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('sequence', 'basic')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree)
        # print result_string

        expected_element = {
            'tag': 'sequence-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }

                            ]
                        }
                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('sequence', 'basic'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_sequence_unbounded(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('sequence', 'unbounded')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree)
        # print result_string

        expected_element = {
            'tag': 'sequence-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }

                            ]
                        }
                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.sequence_data_handler.get_html2(join('sequence', 'unbounded'))

        self.assertTrue(are_equals(result_html, expected_html))

    # def test_create_any_basic(self):
    #     # FIXME How do we want to handle any's?
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('any', 'basic'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree, '')
    #     self.assertEqual(result_string, '')
    #
    # def test_create_any_unbounded(self):
    #     # FIXME How do we want to handle any's?
    #     xsd_tree = self.sequence_data_handler.get_xsd2(join('any', 'unbounded'))
    #     xsd_element = xsd_tree.xpath('/schema/complexType/sequence')[0]
    #
    #     result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree, '')
    #     # print result_string
    #     self.assertEqual(result_string, '')
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.sequence_data_handler.get_html2(join('any', 'unbounded'))
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_create_multiple_basic(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('multiple', 'basic')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree)
        # print result_string

        expected_element = {
            'tag': 'sequence-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'choice-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': []
                                }

                            ]
                        }
                    ]
                },
                {
                    'tag': 'element',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': '',
                                    'children': []
                                }
                            ]
                        }

                    ]
                },
                {
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.sequence_data_handler.get_html2(join('multiple', 'basic'))

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_multiple_valid(self):
        xsd_tree = etree.ElementTree(self.sequence_data_handler.get_xsd2(join('multiple', 'unbounded')))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:sequence',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_sequence_absent(self.request, xsd_element, xsd_tree)
        # print result_string

        expected_element = {
            'tag': 'sequence-iter',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'choice-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': []
                                }

                            ]
                        }
                    ]
                },
                {
                    'tag': 'element',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': '',
                                    'children': []
                                }
                            ]
                        }

                    ]
                },
                {
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.sequence_data_handler.get_html2(join('multiple', 'unbounded'))

        self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateChoiceTestSuite(TestCase):
    """
    """

    def setUp(self):
        choice_data = join('curate', 'tests', 'data', 'parser', 'choice')
        self.choice_data_handler = DataHandler(choice_data)

        self.maxDiff = None

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    def test_create_element_basic(self):
        xsd_files = join('element', 'basic')
        xsd_tree = etree.ElementTree(self.choice_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:choice',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_choice(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'choice',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        },
                                    ]
                                },
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': []
                        }
                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.choice_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_element_unbounded(self):
        xsd_files = join('element', 'unbounded')
        xsd_tree = etree.ElementTree(self.choice_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:choice',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_choice(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'choice',
            'occurs': (2., 2., float('infinity')),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        },
                                    ]
                                },
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': []
                        }
                    ]
                },
                {
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        },
                                    ]
                                },
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': []
                        }
                    ]
                },

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.choice_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # FIXME group test are not good since it is not supported by the parser
    # def test_create_group_basic(self):
    #     xsd_files = join('group', 'basic')
    #     xsd_tree = self.choice_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/choice')[0]
    #
    #     result_string = generate_choice(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.choice_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_group_unbounded(self):
    #     xsd_files = join('group', 'unbounded')
    #     xsd_tree = self.choice_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/choice')[0]
    #
    #     result_string = generate_choice(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.choice_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

    # FIXME choice test are not good since it is not supported by the parser
    # def test_create_choice_basic(self):
    #     xsd_files = join('choice', 'basic')
    #     xsd_tree = self.choice_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/choice')[0]
    #
    #     result_string = generate_choice(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.choice_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_choice_unbounded(self):
    #     xsd_files = join('choice', 'unbounded')
    #     xsd_tree = self.choice_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/choice')[0]
    #
    #     result_string = generate_choice(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.choice_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

    def test_create_sequence_basic(self):
        xsd_files = join('sequence', 'basic')
        xsd_tree = etree.ElementTree(self.choice_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:choice',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_choice(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'choice',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                },
                                            ]
                                        },
                                    ]
                                },
                            ]
                        },
                        {
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [

                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': []
                                },
                            ]
                        }
                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.choice_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_sequence_unbounded(self):
        xsd_files = join('sequence', 'unbounded')
        xsd_tree = etree.ElementTree(self.choice_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:choice',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_choice(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'value': None,
            'tag': 'choice',
            'occurs': (2.0, 2.0, float('infinity')),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': []
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.choice_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # TODO implement later
    # def test_create_any_basic(self):
    #     pass
    #
    # def test_create_any_unbounded(self):
    #     pass

    def test_reload_element_basic(self):
        xsd_files = join('element', 'basic')
        xsd_tree = etree.ElementTree(self.choice_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:choice',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.choice_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_choice(self.request, xsd_element, xsd_tree, full_path='/root',
                                        edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {
            'tag': 'choice',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 0, 1),
                            'module': None,
                            'value': None,
                            'children': []
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': 'entry0',
                                            'children': []
                                        },
                                    ]
                                },
                            ]
                        },
                    ]
                }

            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.choice_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_element_unbounded(self):
        # FIXME correct the bug here
        xsd_files = join('element', 'unbounded')
        xsd_tree = etree.ElementTree(self.choice_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:choice',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.choice_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_choice(self.request, xsd_element, xsd_tree, full_path='/root',
                                        edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {
            'value': None,
            'tag': 'choice',
            'occurs': (2.0, 1, float('infinity')),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'entry1',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 2, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'entry0',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                },
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'entry2',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.choice_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    # TODO implement later
    # def test_reload_group_basic(self):
    #     xsd_files = join('element', 'basic')
    #     xsd_tree = self.choice_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/choice')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.choice_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_choice(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                    edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.choice_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    # def test_reload_group_unbounded(self):
    #     xsd_files = join('element', 'basic')
    #     xsd_tree = self.choice_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/choice')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.choice_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_choice(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                    edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.choice_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_reload_choice_basic(self):
    #     xsd_files = join('element', 'basic')
    #     xsd_tree = self.choice_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/choice')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.choice_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_choice(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                    edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.choice_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_reload_choice_unbounded(self):
    #     xsd_files = join('element', 'basic')
    #     xsd_tree = self.choice_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType/choice')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.choice_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_choice(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                    edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.choice_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_sequence_basic(self):
        xsd_files = join('sequence', 'basic')
        xsd_tree = etree.ElementTree(self.choice_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:choice',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.choice_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_choice(self.request, xsd_element, xsd_tree, full_path='/root',
                                        edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {
            'value': None,
            'tag': 'choice',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 0, 1),
                                    'module': None,
                                    'children': []
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry0',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.choice_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_sequence_unbounded(self):
        # fixme correct the bug
        xsd_files = join('sequence', 'unbounded')
        xsd_tree = etree.ElementTree(self.choice_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:choice',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.choice_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_choice(self.request, xsd_element, xsd_tree, full_path='/root',
                                        edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {
            'value': None,
            'tag': 'choice',
            'occurs': (2.0, 1, float('infinity')),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'choice-iter',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry2',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 2, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry0',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        },
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry1',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.choice_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

        # TODO implement later
        # def test_reload_any_basic(self):
        #     pass
        #
        # def test_reload_any_unbounded(self):
        #     pass


class ParserGenerateSimpleTypeTestSuite(TestCase):
    """
    """

    def setUp(self):
        simple_type_data = join('curate', 'tests', 'data', 'parser', 'simple_type')
        self.simple_type_data_handler = DataHandler(simple_type_data)

        self.maxDiff = None

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    def test_create_restriction(self):
        xsd_files = join('restriction', 'basic')
        xsd_tree = etree.ElementTree(self.simple_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:simpleType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_simple_type(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {
            'tag': 'simple_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'restriction',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'enumeration',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': 'child_0',
                            'children': []
                        },
                        {
                            'tag': 'enumeration',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': 'child_1',
                            'children': []
                        },
                        {
                            'tag': 'enumeration',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': 'child_2',
                            'children': []
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.simple_type_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_list(self):
        xsd_files = join('list', 'basic')
        xsd_tree = etree.ElementTree(self.simple_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:simpleType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_simple_type(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {
            'tag': 'simple_type',
            'occurs': (1, 1, 1),
            'value': None,
            'module': None,
            'children': [
                {
                    'tag': 'list',
                    'occurs': (1, 1, 1),
                    'value': '',
                    'module': None,
                    'children': []
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.simple_type_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # FIXME Union test is not good cause it has not been implemented on the server
    # def test_create_union(self):
    #     xsd_files = join('union', 'basic')
    #     xsd_tree = self.simple_type_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/simpleType')[0]
    #
    #     result_string = generate_simple_type(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #     self.assertEqual(result_string, '')
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.simple_type_data_handler.get_html2(xsd_files)
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_restriction(self):
        xsd_files = join('restriction', 'basic')
        xsd_tree = etree.ElementTree(self.simple_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:simpleType', namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.simple_type_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_simple_type(self.request, xsd_element, xsd_tree, full_path='/root',
                                             edit_data_tree=edit_data_tree)
        # print result_string

        expected_dict = {
            'tag': 'simple_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'restriction',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'enumeration',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': 'child_0',
                            'children': []
                        },
                        {
                            'tag': 'enumeration/selected',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': 'child_1',
                            'children': []
                        },
                        {
                            'tag': 'enumeration',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': 'child_2',
                            'children': []
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.simple_type_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_list(self):
        # fixme correct bugs
        xsd_files = join('list', 'basic')
        xsd_tree = etree.ElementTree(self.simple_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:simpleType', namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.simple_type_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_simple_type(self.request, xsd_element, xsd_tree, full_path='/root',
                                             edit_data_tree=edit_data_tree)
        # print result_string

        expected_dict = {
            'tag': 'simple_type',
            'occurs': (1, 1, 1),
            'value': None,
            'module': None,
            'children': [
                {
                    'tag': 'list',
                    'occurs': (1, 1, 1),
                    'value': '',
                    'module': None,
                    'children': []
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.simple_type_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

        # fixme support for union is not there yet
        # def test_reload_union(self):
        #     xsd_files = join('restriction', 'basic')
        #     xsd_tree = self.simple_type_data_handler.get_xsd2(xsd_files)
        #     xsd_element = xsd_tree.xpath('/schema/simpleType')[0]
        #
        #     self.request.session['curate_edit'] = True
        #
        #     xml_tree = self.simple_type_data_handler.get_xml(xsd_files)
        #     xml_data = etree.tostring(xml_tree)
        #
        #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        #     etree.set_default_parser(parser=clean_parser)
        #     # load the XML tree from the text
        #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        #     result_string = generate_simple_type(self.request, xsd_element, xsd_tree, '', full_path='/root',
        #                                        edit_data_tree=edit_data_tree)
        #     print result_string
        #
        #     # result_html = etree.fromstring(result_string)
        #     # expected_html = self.simple_type_data_handler.get_html2(xsd_files + '.reload')
        #     #
        #     # self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateComplexTypeTestSuite(TestCase):
    """
    """

    def setUp(self):
        complex_type_data = join('curate', 'tests', 'data', 'parser', 'complex_type')
        self.complex_type_data_handler = DataHandler(complex_type_data)

        self.maxDiff = None

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    # FIXME simpleContent not correctly supported
    def test_create_simple_content(self):
        xsd_files = join('simple_content', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'value': None,
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'simple_content',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'extension',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.complex_type_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # FIXME complexContent not properly supported
    def test_create_complex_content(self):
        xsd_files = join('complex_content', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'value': None,
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'complex_content',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'extension',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'complex_type',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'sequence',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': None,
                                                    'tag': 'element',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': [
                                                        {
                                                            'value': None,
                                                            'tag': 'elem-iter',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'children': [
                                                                {
                                                                    'value': '',
                                                                    'tag': 'input',
                                                                    'occurs': (1, 1, 1),
                                                                    'module': None,
                                                                    'children': []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                },
                                                {
                                                    'value': None,
                                                    'tag': 'element',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': [
                                                        {
                                                            'value': None,
                                                            'tag': 'elem-iter',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'children': [
                                                                {
                                                                    'value': '',
                                                                    'tag': 'input',
                                                                    'occurs': (1, 1, 1),
                                                                    'module': None,
                                                                    'children': []
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'value': None,
                                    'tag': 'sequence',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': None,
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': [
                                                        {
                                                            'value': '',
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        # self.assertEqual(result_string[0], '')
        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.complex_type_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # FIXME group not properly supported
    def test_create_group(self):
        xsd_files = join('group', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string
        self.assertEqual(result_string[0], '')

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': []
        }

        self.assertDictEqual(result_string[1], expected_element)

        # result_html = etree.fromstring(result_string)
        # expected_html = self.complex_type_data_handler.get_html2(xsd_files)
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    def test_create_all(self):
        xsd_files = join('all', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'all',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.complex_type_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_choice(self):
        xsd_files = join('choice', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'choice-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': '',
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': []
                                },
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.complex_type_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_sequence(self):
        xsd_files = join('sequence', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.complex_type_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_attribute(self):
        xsd_files = join('attribute', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'attribute',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': '',
                                    'children': []
                                },
                            ]
                        },
                    ]
                },
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.complex_type_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # FIXME attribute group is not yet supported
    # def test_create_attribute_group(self):
    #     xsd_files = join('attribute_group', 'basic')
    #     xsd_tree = self.complex_type_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType')[0]
    #
    #     result_string = generate_complex_type(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #     self.assertEqual(result_string, '')
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.complex_type_data_handler.get_html2(xsd_files)
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    # FIXME any attribute is not yet supported
    # def test_create_any_attribute(self):
    #     xsd_files = join('any_attribute', 'basic')
    #     xsd_tree = self.complex_type_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType')[0]
    #
    #     result_string = generate_complex_type(self.request, xsd_element, xsd_tree, '', full_path='')
    #     # print result_string
    #     self.assertEqual(result_string, '')
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.complex_type_data_handler.get_html2(xsd_files)
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_create_multiple(self):
        xsd_files = join('multiple', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='')

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                # FIXME Order is wrong
                {
                    'tag': 'attribute',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': '',
                                    'children': []
                                },
                            ]
                        },
                    ]
                },
                {
                    'tag': 'attribute',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': '',
                                    'children': []
                                },
                            ]
                        },
                    ]
                },
                {
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        },
                                    ]
                                },
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': '',
                                            'children': []
                                        },
                                    ]
                                },
                            ]
                        },
                    ]
                },
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.complex_type_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_simple_content(self):
        xsd_files = join('simple_content', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='/root',
                                              edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {
            'value': None,
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'simple_content',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'extension',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry0',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    # fixme complex content not implemented
    # def test_reload_complex_content(self):
    #     xsd_files = join('simple_content', 'basic')
    #     xsd_tree = self.complex_type_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_complex_type(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                         edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # fixme group not implemented
    # def test_reload_group(self):
    #     xsd_files = join('simple_content', 'basic')
    #     xsd_tree = self.complex_type_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_complex_type(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                         edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_all(self):
        xsd_files = join('all', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='/root',
                                              edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'all',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': 'entry0',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': 'entry1',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_choice(self):
        xsd_files = join('choice', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='/root',
                                              edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'choice',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'choice-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'element',
                                    'occurs': (1, 0, 1),
                                    'module': None,
                                    'value': None,
                                    'children': []
                                },
                                {
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': None,
                                            'children': [
                                                {
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'value': 'entry0',
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_sequence(self):
        xsd_files = join('sequence', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='/root',
                                              edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                {
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': 'entry0',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': 'entry1',
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    # fixme implement attribute
    # def test_reload_attribute(self):
    #     xsd_files = join('simple_content', 'basic')
    #     xsd_tree = self.complex_type_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_complex_type(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                         edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # fixme implement attributeGroup
    # def test_reload_attribute_group(self):
    #     xsd_files = join('simple_content', 'basic')
    #     xsd_tree = self.complex_type_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_complex_type(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                         edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # fixme implement anyAttribute
    # def test_reload_any_attribute(self):
    #     xsd_files = join('simple_content', 'basic')
    #     xsd_tree = self.complex_type_data_handler.get_xsd2(xsd_files)
    #     xsd_element = xsd_tree.xpath('/schema/complexType')[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_complex_type(self.request, xsd_element, xsd_tree, '', full_path='/root',
    #                                         edit_data_tree=edit_data_tree)
    #     print result_string
    #
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_multiple(self):
        # fixme test broken
        xsd_files = join('multiple', 'basic')
        xsd_tree = etree.ElementTree(self.complex_type_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.complex_type_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_complex_type(self.request, xsd_element, xsd_tree, full_path='/root',
                                              edit_data_tree=edit_data_tree)
        # print result_string

        expected_element = {
            'tag': 'complex_type',
            'occurs': (1, 1, 1),
            'module': None,
            'value': None,
            'children': [
                # FIXME Order is wrong
                {
                    'tag': 'attribute',
                    'occurs': (1, 0, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': []
                        },
                    ]
                },
                {
                    'tag': 'attribute',
                    'occurs': (1, 0, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': []
                        },
                    ]
                },
                {
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'value': None,
                    'children': [
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': 'entry0',
                                            'children': []
                                        },
                                    ]
                                },
                            ]
                        },
                        {
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'value': None,
                            'children': [
                                {
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'value': None,
                                    'children': [
                                        {
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'value': 'entry1',
                                            'children': []
                                        },
                                    ]
                                },
                            ]
                        },
                    ]
                },
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)
        result_string = '<div>' + result_string[0] + '</div>'

        result_html = etree.fromstring(result_string)
        expected_html = self.complex_type_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateModuleTestSuite(TestCase):
    """
    """

    def setUp(self):
        module_data = join('curate', 'tests', 'data', 'parser', 'module')
        self.module_data_handler = DataHandler(module_data)

        form_data = FormData()
        form_data.name = ''
        form_data.user = ''
        form_data.template = ''

        form_data.save()

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['curateFormData'] = form_data.pk
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.namespaces = {'xs': namespace}

    def test_create_module(self):
        xsd_files = 'registered_module'
        xsd_tree = etree.ElementTree(self.module_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.namespaces)[0]

        self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)

        result_string = generate_module(self.request, xsd_element)

        result_html = etree.fromstring(result_string)
        expected_html = self.module_data_handler.get_html2('new')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_module(self):
        xsd_files = 'registered_module'
        # xsd_reload_files = join('element', 'basic.reload')
        xsd_tree = etree.ElementTree(self.module_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType', namespaces=self.namespaces)[0]

        # self.request.session['xmlDocTree'] = etree.tostring(xsd_tree)
        self.request.session['curate_edit'] = True

        xml_data = self.module_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_data)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        # set the parser
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))

        result_string = generate_module(self.request, xsd_element, xsd_xpath='', xml_xpath='/module/child',
                                        xml_tree=xsd_tree, edit_data_tree=edit_data_tree)

        result_html = etree.fromstring(result_string)
        expected_html = self.module_data_handler.get_html2('reload')

        self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateSimpleContentTestSuite(TestCase):
    """
    """

    def setUp(self):
        # connect to test database
        # self.db_name = "mgi_test"
        # disconnect()
        # self.connection = connect(self.db_name, port=27018)
        #
        # test_data = join('curate', 'tests', 'data', 'parser', 'simple_content')
        #
        # create_extension_data = join(test_data, 'extension', 'create')
        # self.create_extension_data_handler = DataHandler(create_extension_data)
        #
        # create_restriction_data = join(test_data, 'restriction', 'create')
        # self.create_restriction_data_handler = DataHandler(create_restriction_data)
        simple_content_data = join('curate', 'tests', 'data', 'parser', 'simple_content')
        self.simple_content_data_handler = DataHandler(simple_content_data)

        self.maxDiff = None

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    def test_create_restriction(self):
        xsd_files = join('restriction', 'basic')
        xsd_tree = etree.ElementTree(self.simple_content_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:simpleContent',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_simple_content(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'simple_content',
            'occurs': (1, 1, 1),
            'value': None,
            'module': None,
            'children': [
                {
                    'tag': 'restriction',
                    'occurs': (1, 1, 1),
                    'value': None,
                    'module': None,
                    'children': [
                        {
                            'tag': 'enumeration',
                            'occurs': (1, 1, 1),
                            'value': 'child0',
                            'module': None,
                            'children': []
                        },
                        {
                            'tag': 'enumeration',
                            'occurs': (1, 1, 1),
                            'value': 'child1',
                            'module': None,
                            'children': []
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.simple_content_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    # FIXME extension are not fully supported by the parser
    def test_create_extension(self):
        xsd_files = join('extension', 'basic')
        xsd_tree = etree.ElementTree(self.simple_content_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:simpleContent',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_simple_content(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'value': None,
            'tag': 'simple_content',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'extension',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': '',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.simple_content_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_extension(self):
        xsd_files = join('extension', 'basic')
        xsd_tree = etree.ElementTree(self.simple_content_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:simpleContent',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.simple_content_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_simple_content(self.request, xsd_element, xsd_tree, full_path='/root',
                                                edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_element = {
            'value': None,
            'tag': 'simple_content',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'extension',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'attr0',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.simple_content_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_restriction(self):
        xsd_files = join('restriction', 'basic')
        xsd_tree = etree.ElementTree(self.simple_content_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:simpleContent',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.simple_content_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_simple_content(self.request, xsd_element, xsd_tree, full_path='/root',
                                                edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_element = {
            'tag': 'simple_content',
            'occurs': (1, 1, 1),
            'value': None,
            'module': None,
            'children': [
                {
                    'tag': 'restriction',
                    'occurs': (1, 1, 1),
                    'value': None,
                    'module': None,
                    'children': [
                        {
                            'tag': 'enumeration/selected',
                            'occurs': (1, 1, 1),
                            'value': 'child0',
                            'module': None,
                            'children': []
                        },
                        {
                            'tag': 'enumeration',
                            'occurs': (1, 1, 1),
                            'value': 'child1',
                            'module': None,
                            'children': []
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.simple_content_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateComplexContentTestSuite(TestCase):
    """
    """

    # FIXME restriction for complexContent are not working

    def setUp(self):
        extension_data = join('curate', 'tests', 'data', 'parser', 'complex_content')
        self.extension_data_handler = DataHandler(extension_data)

        self.maxDiff = None

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.namespace = "{" + namespace + "}"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    def test_create_restriction(self):
        xsd_files = join('restriction', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_content(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
        # print result_string

        expected_dict = {'value': None, 'tag': 'complex_content', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'restriction', 'occurs': (1, 1, 1), 'module': None,
             'children': [{'module': None, 'tag': 'input', 'occurs': (1, 1, 1), 'value': '', 'children': []}]}]}

        self.assertDictEqual(result_string[1], expected_dict)

        # result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string[0])
        expected_html = self.extension_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_extension(self):
        xsd_files = join('extension', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_complex_content(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
        # print result_string

        expected_dict = {
            'value': None,
            'tag': 'complex_content',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'extension',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'complex_type',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'sequence',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': None,
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': [
                                                        {
                                                            'value': '',
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            'value': None,
                                            'tag': 'element',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': None,
                                                    'tag': 'elem-iter',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': [
                                                        {
                                                            'value': '',
                                                            'tag': 'input',
                                                            'occurs': (1, 1, 1),
                                                            'module': None,
                                                            'children': []
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_restriction(self):
        xsd_files = join('restriction', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))

        result_string = generate_complex_content(self.request, xsd_element, xsd_tree, self.namespace,
                                                 full_path='/root', edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {'value': None, 'tag': 'complex_content', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'restriction', 'occurs': (1, 1, 1), 'module': None,
             'children': [{'module': None, 'tag': 'input', 'occurs': (1, 1, 1), 'value': '', 'children': []}]}]}

        self.assertDictEqual(result_string[1], expected_dict)

        # result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string[0])
        expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_extension(self):
        xsd_files = join('extension', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))

        result_string = generate_complex_content(self.request, xsd_element, xsd_tree, self.namespace,
                                                 full_path='/root', edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {'value': None, 'tag': 'complex_content', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'complex_type', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                                {'value': 'entry0', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None,
                                 'children': []}]}]},
                        {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                                {'value': 'entry1', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None,
                                 'children': []}]}]}]}]},
                {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': 'entry2', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None,
                             'children': []}]}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateRestrictionTestSuite(TestCase):
    """
    """

    def setUp(self):
        restriction_data = join('curate', 'tests', 'data', 'parser', 'restriction')
        self.restriction_data_handler = DataHandler(restriction_data)

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.maxDiff = None

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.namespaces = {'xs': namespace}

    def test_create_enumeration(self):
        xsd_files = join('enumeration', 'basic')
        xsd_tree = etree.ElementTree(self.restriction_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:simpleType/xs:restriction', namespaces=self.namespaces)[0]

        result_string = generate_restriction(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'restriction',
            'occurs': (1, 1, 1),
            'value': None,
            'module': None,
            'children': [
                {
                    'tag': 'enumeration',
                    'occurs': (1, 1, 1),
                    'value': 'child0',
                    'module': None,
                    'children': []
                },
                {
                    'tag': 'enumeration',
                    'occurs': (1, 1, 1),
                    'value': 'child1',
                    'module': None,
                    'children': []
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.restriction_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_simple_type(self):
        xsd_files = join('simple_type', 'basic')
        xsd_tree = etree.ElementTree(self.restriction_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:simpleType/xs:restriction', namespaces=self.namespaces)[0]

        result_string = generate_restriction(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_element = {
            'tag': 'restriction',
            'occurs': (1, 1, 1),
            'value': None,
            'module': None,
            'children': [
                {
                    'tag': 'simple_type',
                    'occurs': (1, 1, 1),
                    'value': None,
                    'module': None,
                    'children': [
                        {
                            'tag': 'restriction',
                            'occurs': (1, 1, 1),
                            'value': None,
                            'module': None,
                            'children': [
                                {
                                    'tag': 'enumeration',
                                    'occurs': (1, 1, 1),
                                    'value': 'child0',
                                    'module': None,
                                    'children': []
                                },
                                {
                                    'tag': 'enumeration',
                                    'occurs': (1, 1, 1),
                                    'value': 'child1',
                                    'module': None,
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.restriction_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_enumeration(self):
        xsd_files = join('enumeration', 'basic')
        xsd_tree = etree.ElementTree(self.restriction_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:simpleType/xs:restriction', namespaces=self.namespaces)[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.restriction_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_restriction(self.request, xsd_element, xsd_tree, full_path='/root',
                                             edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_element = {
            'tag': 'restriction',
            'occurs': (1, 1, 1),
            'value': None,
            'module': None,
            'children': [
                {
                    'tag': 'enumeration',
                    'occurs': (1, 1, 1),
                    'value': 'child0',
                    'module': None,
                    'children': []
                },
                {
                    'tag': 'enumeration/selected',
                    'occurs': (1, 1, 1),
                    'value': 'child1',
                    'module': None,
                    'children': []
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.restriction_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_simple_type(self):
        xsd_files = join('simple_type', 'basic')
        xsd_tree = etree.ElementTree(self.restriction_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:simpleType/xs:restriction', namespaces=self.namespaces)[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.restriction_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_restriction(self.request, xsd_element, xsd_tree, full_path='/root',
                                             edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_element = {
            'tag': 'restriction',
            'occurs': (1, 1, 1),
            'value': None,
            'module': None,
            'children': [
                {
                    'tag': 'simple_type',
                    'occurs': (1, 1, 1),
                    'value': None,
                    'module': None,
                    'children': [
                        {
                            'tag': 'restriction',
                            'occurs': (1, 1, 1),
                            'value': None,
                            'module': None,
                            'children': [
                                {
                                    'tag': 'enumeration/selected',
                                    'occurs': (1, 1, 1),
                                    'value': 'child0',
                                    'module': None,
                                    'children': []
                                },
                                {
                                    'tag': 'enumeration',
                                    'occurs': (1, 1, 1),
                                    'value': 'child1',
                                    'module': None,
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_element)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.restriction_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))


class ParserGenerateExtensionTestSuite(TestCase):
    """
    """

    def setUp(self):
        extension_data = join('curate', 'tests', 'data', 'parser', 'extension')
        self.extension_data_handler = DataHandler(extension_data)

        self.maxDiff = None

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition
        self.request.session['nb_html_tags'] = 0
        self.request.session['mapTagID'] = {}
        self.request.session['nbChoicesID'] = 0

        # set default namespace
        namespace = "http://www.w3.org/2001/XMLSchema"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    def test_create_group(self):
        xsd_files = join('group', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_all(self):
        xsd_files = join('all', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'complex_type', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'attribute', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]},
            {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
                {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}]}

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_choice(self):
        xsd_files = join('choice', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': [
            {'value': None, 'tag': 'complex_type', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'sequence', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}]},
            {'value': None, 'tag': 'choice', 'occurs': (1, 1, 1), 'module': None, 'children': [
                {'value': None, 'tag': 'choice-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': [
                        {'value': None, 'tag': 'elem-iter', 'occurs': (1, 1, 1), 'module': None, 'children': [
                            {'value': '', 'tag': 'input', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]},
                    {'value': None, 'tag': 'element', 'occurs': (1, 1, 1), 'module': None, 'children': []}]}]}]}

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_sequence(self):
        xsd_files = join('sequence', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }

                    ]
                },
                {
                    'value': None,
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': '',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': '',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_attribute(self):
        xsd_files = join('attribute', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'element',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': '',
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.extension_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_create_attribute_group(self):
        xsd_files = join('attribute_group', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': []}

        self.assertDictEqual(result_string[1], expected_dict)

        self.assertEqual(result_string[0], '')
        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files)
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    def test_create_any_attribute(self):
        xsd_files = join('any_attribute', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': []}

        self.assertDictEqual(result_string[1], expected_dict)

        self.assertEqual(result_string[0], '')
        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files)
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    def test_create_multiple(self):
        xsd_files = join('multiple', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='')
        # print result_string

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': '',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'element',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': '',
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': []
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': '',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': '',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files)

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_group(self):
        # fixme display is not correct
        xsd_files = join('group', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='/test0',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry0',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry1',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_all(self):
        # fixme bugs
        xsd_files = join('all', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='/test1',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'attribute',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'attr1',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'entry0',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'entry1',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_choice(self):
        xsd_files = join('choice', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='/test2',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry0',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry1',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'choice',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'choice-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 0, 1),
                                    'module': None,
                                    'children': []
                                },
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry2',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_sequence(self):
        xsd_files = join('sequence', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='/test3',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 0, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                },
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 0, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 0, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': []
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 0, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_attribute(self):
        xsd_files = join('attribute', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='/test4',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'element',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': 'attr0',
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': []
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_html = etree.fromstring(result_string[0])
        expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_attribute_group(self):
        xsd_files = join('attribute_group', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='/test5',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': []}

        self.assertDictEqual(result_string[1], expected_dict)
        self.assertEqual(result_string[0], '')

        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_any_attribute(self):
        xsd_files = join('any_attribute', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='/test6',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': []}

        self.assertDictEqual(result_string[1], expected_dict)

        self.assertEqual(result_string[0], '')
        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    def test_reload_multiple(self):
        xsd_files = join('multiple', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        self.request.session['curate_edit'] = True

        xml_tree = self.extension_data_handler.get_xml(xsd_files)
        xml_data = etree.tostring(xml_tree)

        clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
        etree.set_default_parser(parser=clean_parser)
        # load the XML tree from the text
        edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
        result_string = generate_extension(self.request, xsd_element, xsd_tree, full_path='/test7',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = {
            'value': None,
            'tag': 'extension',
            'occurs': (1, 1, 1),
            'module': None,
            'children': [
                {
                    'value': None,
                    'tag': 'complex_type',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'sequence',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry0',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    'value': None,
                                    'tag': 'element',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': None,
                                            'tag': 'elem-iter',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': [
                                                {
                                                    'value': 'entry1',
                                                    'tag': 'input',
                                                    'occurs': (1, 1, 1),
                                                    'module': None,
                                                    'children': []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'element',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'elem-iter',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': '0',
                                    'tag': 'input',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': []
                                }
                            ]
                        }
                    ]
                },
                {
                    'value': None,
                    'tag': 'sequence',
                    'occurs': (1, 1, 1),
                    'module': None,
                    'children': [
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'entry2',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            'value': None,
                            'tag': 'element',
                            'occurs': (1, 1, 1),
                            'module': None,
                            'children': [
                                {
                                    'value': None,
                                    'tag': 'elem-iter',
                                    'occurs': (1, 1, 1),
                                    'module': None,
                                    'children': [
                                        {
                                            'value': 'entry3',
                                            'tag': 'input',
                                            'occurs': (1, 1, 1),
                                            'module': None,
                                            'children': []
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertDictEqual(result_string[1], expected_dict)

        result_string = '<div>' + result_string[0] + '</div>'
        result_html = etree.fromstring(result_string)
        expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')

        self.assertTrue(are_equals(result_html, expected_html))
