from django.http.request import HttpRequest
from django.test.testcases import TestCase
from os.path import join
from django.utils.importlib import import_module
from lxml import etree
from mgi.tests import DataHandler, are_equals
from curate.parser import generate_extension


class ParserCreateExtensionTestSuite(TestCase):
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
        self.namespace = "{" + namespace + "}"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    # def test_create_group(self):
    #     xsd_files = join('group', 'basic')
    #     xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
    #     xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
    #                                  namespaces=self.request.session['namespaces'])[0]
    #
    #     result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
    #     # print result_string
    #
    #     expected_dict = {
    #     }
    #
    #     self.assertDictEqual(result_string[1], expected_dict)
    #
    #     result_string = '<div>' + result_string[0] + '</div>'
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.extension_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

    # def test_create_all(self):
    #     xsd_files = join('all', 'basic')
    #     xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
    #     xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
    #                                  namespaces=self.request.session['namespaces'])[0]
    #
    #     result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
    #     # print result_string
    #
    #     expected_dict = self.extension_data_handler.get_json(xsd_files)
    #
    #     self.assertDictEqual(result_string[1], expected_dict)
    #
    #     result_string = '<div>' + result_string[0] + '</div>'
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.extension_data_handler.get_html2(xsd_files)
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

    def test_create_choice(self):
        xsd_files = join('choice', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
        # print result_string

        expected_dict = self.extension_data_handler.get_json(xsd_files)

        self.assertDictEqual(result_string[1], expected_dict)

        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files)
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    def test_create_sequence(self):
        xsd_files = join('sequence', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
        # print result_string

        expected_dict = self.extension_data_handler.get_json(xsd_files)

        self.assertDictEqual(result_string[1], expected_dict)

        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files)
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    def test_create_attribute(self):
        xsd_files = join('attribute', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
        # print result_string

        expected_dict = self.extension_data_handler.get_json(xsd_files)

        self.assertDictEqual(result_string[1], expected_dict)

        # result_html = etree.fromstring(result_string[0])
        # expected_html = self.extension_data_handler.get_html2(xsd_files)
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    # def test_create_attribute_group(self):
    #     xsd_files = join('attribute_group', 'basic')
    #     xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
    #     xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
    #                                  namespaces=self.request.session['namespaces'])[0]
    #
    #     result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
    #     # print result_string
    #
    #     expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': []}
    #
    #     self.assertDictEqual(result_string[1], expected_dict)
    #
    #     self.assertEqual(result_string[0], '')
    #     # result_string = '<div>' + result_string[0] + '</div>'
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.extension_data_handler.get_html2(xsd_files)
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_create_any_attribute(self):
    #     xsd_files = join('any_attribute', 'basic')
    #     xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
    #     xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
    #                                  namespaces=self.request.session['namespaces'])[0]
    #
    #     result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
    #     # print result_string
    #
    #     expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': []}
    #
    #     self.assertDictEqual(result_string[1], expected_dict)
    #
    #     self.assertEqual(result_string[0], '')
    #     # result_string = '<div>' + result_string[0] + '</div>'
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.extension_data_handler.get_html2(xsd_files)
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

    def test_create_multiple(self):
        xsd_files = join('multiple', 'basic')
        xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
        # print result_string

        expected_dict = self.extension_data_handler.get_json(xsd_files)

        self.assertDictEqual(result_string[1], expected_dict)

        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files)
        #
        # self.assertTrue(are_equals(result_html, expected_html))


class ParserReloadExtensionTestSuite(TestCase):
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
        self.namespace = "{" + namespace + "}"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    # def test_reload_group(self):
    #     xsd_files = join('group', 'basic')
    #     xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
    #     xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
    #                                  namespaces=self.request.session['namespaces'])[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.extension_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='/test0',
    #                                        edit_data_tree=edit_data_tree)
    #     # print result_string
    #     # result_string = '<div>' + result_string + '</div>'
    #
    #     expected_dict = {
    #     }
    #
    #     self.assertDictEqual(result_string[1], expected_dict)
    #
    #     result_string = '<div>' + result_string[0] + '</div>'
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

    # def test_reload_all(self):
    #     # fixme bugs
    #     xsd_files = join('all', 'basic')
    #     xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
    #     xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:complexContent/xs:extension',
    #                                  namespaces=self.request.session['namespaces'])[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.extension_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='/test1',
    #                                        edit_data_tree=edit_data_tree)
    #     # print result_string
    #     # result_string = '<div>' + result_string + '</div>'
    #
    #     expected_dict = {
    #         'value': None,
    #         'tag': 'extension',
    #         'occurs': (1, 1, 1),
    #         'module': None,
    #         'children': [
    #             {
    #                 'value': None,
    #                 'tag': 'complex_type',
    #                 'occurs': (1, 1, 1),
    #                 'module': None,
    #                 'children': [
    #                     {
    #                         'value': None,
    #                         'tag': 'attribute',
    #                         'occurs': (1, 1, 1),
    #                         'module': None,
    #                         'children': [
    #                             {
    #                                 'value': None,
    #                                 'tag': 'elem-iter',
    #                                 'occurs': (1, 1, 1),
    #                                 'module': None,
    #                                 'children': [
    #                                     {
    #                                         'value': 'attr1',
    #                                         'tag': 'input',
    #                                         'occurs': (1, 1, 1),
    #                                         'module': None,
    #                                         'children': []
    #                                     }
    #                                 ]
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             },
    #             {
    #                 'value': None,
    #                 'tag': 'sequence',
    #                 'occurs': (1, 1, 1),
    #                 'module': None,
    #                 'children': [
    #                     {
    #                         'value': None,
    #                         'tag': 'element',
    #                         'occurs': (1, 1, 1),
    #                         'module': None,
    #                         'children': [
    #                             {
    #                                 'value': None,
    #                                 'tag': 'elem-iter',
    #                                 'occurs': (1, 1, 1),
    #                                 'module': None,
    #                                 'children': [
    #                                     {
    #                                         'value': 'entry0',
    #                                         'tag': 'input',
    #                                         'occurs': (1, 1, 1),
    #                                         'module': None,
    #                                         'children': []
    #                                     }
    #                                 ]
    #                             }
    #                         ]
    #                     },
    #                     {
    #                         'value': None,
    #                         'tag': 'element',
    #                         'occurs': (1, 1, 1),
    #                         'module': None,
    #                         'children': [
    #                             {
    #                                 'value': None,
    #                                 'tag': 'elem-iter',
    #                                 'occurs': (1, 1, 1),
    #                                 'module': None,
    #                                 'children': [
    #                                     {
    #                                         'value': 'entry1',
    #                                         'tag': 'input',
    #                                         'occurs': (1, 1, 1),
    #                                         'module': None,
    #                                         'children': []
    #                                     }
    #                                 ]
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    #
    #     self.assertDictEqual(result_string[1], expected_dict)
    #
    #     result_string = '<div>' + result_string[0] + '</div>'
    #     result_html = etree.fromstring(result_string)
    #     expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
    #
    #     self.assertTrue(are_equals(result_html, expected_html))

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
        result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='/test2',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = self.extension_data_handler.get_json(xsd_files+'.reload')

        self.assertDictEqual(result_string[1], expected_dict)

        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
        #
        # self.assertTrue(are_equals(result_html, expected_html))

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
        result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='/root[1]',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = self.extension_data_handler.get_json(xsd_files+'.reload')

        self.assertDictEqual(result_string[1], expected_dict)

        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
        #
        # self.assertTrue(are_equals(result_html, expected_html))

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
        result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='/root[1]',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = self.extension_data_handler.get_json(xsd_files+'.reload')

        self.assertDictEqual(result_string[1], expected_dict)

        # result_html = etree.fromstring(result_string[0])
        # expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    # def test_reload_attribute_group(self):
    #     xsd_files = join('attribute_group', 'basic')
    #     xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
    #     xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
    #                                  namespaces=self.request.session['namespaces'])[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.extension_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='/test5',
    #                                        edit_data_tree=edit_data_tree)
    #     # print result_string
    #     # result_string = '<div>' + result_string + '</div>'
    #
    #     expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': []}
    #
    #     self.assertDictEqual(result_string[1], expected_dict)
    #     self.assertEqual(result_string[0], '')
    #
    #     # result_string = '<div>' + result_string[0] + '</div>'
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))
    #
    # def test_reload_any_attribute(self):
    #     xsd_files = join('any_attribute', 'basic')
    #     xsd_tree = etree.ElementTree(self.extension_data_handler.get_xsd2(xsd_files))
    #     xsd_element = xsd_tree.xpath('/xs:schema/xs:element/xs:complexType/xs:simpleContent/xs:extension',
    #                                  namespaces=self.request.session['namespaces'])[0]
    #
    #     self.request.session['curate_edit'] = True
    #
    #     xml_tree = self.extension_data_handler.get_xml(xsd_files)
    #     xml_data = etree.tostring(xml_tree)
    #
    #     clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
    #     etree.set_default_parser(parser=clean_parser)
    #     # load the XML tree from the text
    #     edit_data_tree = etree.XML(str(xml_data.encode('utf-8')))
    #     result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='/test6',
    #                                        edit_data_tree=edit_data_tree)
    #     # print result_string
    #     # result_string = '<div>' + result_string + '</div>'
    #
    #     expected_dict = {'value': None, 'tag': 'extension', 'occurs': (1, 1, 1), 'module': None, 'children': []}
    #
    #     self.assertDictEqual(result_string[1], expected_dict)
    #
    #     self.assertEqual(result_string[0], '')
    #     # result_string = '<div>' + result_string[0] + '</div>'
    #     # result_html = etree.fromstring(result_string)
    #     # expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
    #     #
    #     # self.assertTrue(are_equals(result_html, expected_html))

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
        result_string = generate_extension(self.request, xsd_element, xsd_tree, self.namespace, full_path='/root[1]',
                                           edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_dict = self.extension_data_handler.get_json(xsd_files+'.reload')

        self.assertDictEqual(result_string[1], expected_dict)

        # result_string = '<div>' + result_string[0] + '</div>'
        # result_html = etree.fromstring(result_string)
        # expected_html = self.extension_data_handler.get_html2(xsd_files + '.reload')
        #
        # self.assertTrue(are_equals(result_html, expected_html))
