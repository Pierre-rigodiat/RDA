from django.http.request import HttpRequest
from django.test.testcases import TestCase
from os.path import join
from django.utils.importlib import import_module
from lxml import etree
from mgi.tests import DataHandler, are_equals

from curate.parser import generate_simple_content


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
        self.namespace = "{" + namespace + "}"
        self.request.session['defaultPrefix'] = 'xs'
        self.request.session['namespaces'] = {'xs': namespace}

    def test_create_restriction(self):
        xsd_files = join('restriction', 'basic')
        xsd_tree = etree.ElementTree(self.simple_content_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:simpleContent',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_simple_content(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
        # print result_string

        expected_element = self.simple_content_data_handler.get_json(xsd_files)

        self.assertDictEqual(result_string[1], expected_element)

        # result_html = etree.fromstring(result_string[0])
        # expected_html = self.simple_content_data_handler.get_html2(xsd_files)
        #
        # self.assertTrue(are_equals(result_html, expected_html))

    # FIXME extension are not fully supported by the parser
    def test_create_extension(self):
        xsd_files = join('extension', 'basic')
        xsd_tree = etree.ElementTree(self.simple_content_data_handler.get_xsd2(xsd_files))
        xsd_element = xsd_tree.xpath('/xs:schema/xs:complexType/xs:simpleContent',
                                     namespaces=self.request.session['namespaces'])[0]

        result_string = generate_simple_content(self.request, xsd_element, xsd_tree, self.namespace, full_path='')
        # print result_string

        expected_element = self.simple_content_data_handler.get_json(xsd_files)

        self.assertDictEqual(result_string[1], expected_element)

        # result_html = etree.fromstring(result_string[0])
        # expected_html = self.simple_content_data_handler.get_html2(xsd_files)
        #
        # self.assertTrue(are_equals(result_html, expected_html))

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
        result_string = generate_simple_content(self.request, xsd_element, xsd_tree, self.namespace, full_path='/root',
                                                edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_element = self.simple_content_data_handler.get_json(xsd_files + '.reload')

        self.assertDictEqual(result_string[1], expected_element)

        # result_html = etree.fromstring(result_string[0])
        # expected_html = self.simple_content_data_handler.get_html2(xsd_files + '.reload')
        #
        # self.assertTrue(are_equals(result_html, expected_html))

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
        result_string = generate_simple_content(self.request, xsd_element, xsd_tree, self.namespace, full_path='/root',
                                                edit_data_tree=edit_data_tree)
        # print result_string
        # result_string = '<div>' + result_string + '</div>'

        expected_element = self.simple_content_data_handler.get_json(xsd_files + '.reload')
        self.assertDictEqual(result_string[1], expected_element)

        # result_html = etree.fromstring(result_string[0])
        # expected_html = self.simple_content_data_handler.get_html2(xsd_files + '.reload')
        #
        # self.assertTrue(are_equals(result_html, expected_html))
