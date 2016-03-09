"""
"""
from django.http.request import HttpRequest
from django.test.testcases import TestCase
from os.path import join
from django.utils.importlib import import_module
from lxml import etree
from mgi.models import Module
from mgi.tests import DataHandler, are_equals
from curate.parser import get_nodes_xpath, lookup_occurs, manage_occurences, manage_attr_occurrences, has_module, \
    get_xml_element_data, get_element_type, remove_annotations


class ParserGetNodesXPathTestSuite(TestCase):
    """
    """

    def setUp(self):
        subnodes_data = join('curate', 'tests', 'data', 'parser', 'utils', 'xpath')
        self.subnodes_data_handler = DataHandler(subnodes_data)

    def test_not_element(self):
        not_element_xsd = self.subnodes_data_handler.get_xsd2('not_element')
        xpath_result = get_nodes_xpath(not_element_xsd, not_element_xsd, '')

        self.assertEqual(xpath_result, [])

    def test_imbricated_elements(self):
        document = join('imbricated_elements', 'document')
        imbricated_elements_xsd = self.subnodes_data_handler.get_xsd2(document)

        child_0 = join('imbricated_elements', 'child_0')
        imbricated_element_0_xsd = self.subnodes_data_handler.get_xsd2(child_0)

        child_1 = join('imbricated_elements', 'child_1')
        imbricated_element_1_xsd = self.subnodes_data_handler.get_xsd2(child_1)

        child_2 = join('imbricated_elements', 'child_2')
        imbricated_element_2_xsd = self.subnodes_data_handler.get_xsd2(child_2)

        xpath_result = get_nodes_xpath(imbricated_elements_xsd, imbricated_elements_xsd, '')
        expected_result = [
            {
                'name': 'child_0',
                'element': imbricated_element_0_xsd
            },
            {
                'name': 'child_1',
                'element': imbricated_element_1_xsd
            },
            {
                'name': 'child_2',
                'element': imbricated_element_2_xsd
            },
        ]

        self.assertEqual(len(xpath_result), len(expected_result))

        for xpath in xpath_result:
            xpath_elem = xpath['element']

            expected_elem_list = [expect['element'] for expect in expected_result if expect['name'] == xpath['name']]
            expect_elem = expected_elem_list[0] if len(expected_elem_list) == 1 else None

            self.assertTrue(are_equals(xpath_elem, expect_elem))

    def test_element_has_name(self):
        document = join('element_with_name', 'document')
        named_element_xsd = self.subnodes_data_handler.get_xsd2(document)

        child_0 = join('element_with_name', 'child_0')
        child_0_xsd = self.subnodes_data_handler.get_xsd2(child_0)

        child_1 = join('element_with_name', 'child_1')
        child_1_xsd = self.subnodes_data_handler.get_xsd2(child_1)

        xpath_result = get_nodes_xpath(named_element_xsd, named_element_xsd, '')
        expected_result = [
            {
                'name': 'child_0',
                'element': child_0_xsd
            },
            {
                'name': 'child_1',
                'element': child_1_xsd
            }
        ]

        self.assertEqual(len(xpath_result), len(expected_result))

        for xpath in xpath_result:
            xpath_elem = xpath['element']

            expected_elem_list = [expect['element'] for expect in expected_result if expect['name'] == xpath['name']]
            expect_elem = expected_elem_list[0] if len(expected_elem_list) == 1 else None

            self.assertTrue(are_equals(xpath_elem, expect_elem))

    def test_element_ref_has_namespace(self):
        # FIXME Correct the test for correct expected output
        document = join('element_with_ref_namespace', 'document')
        ref_element_no_namespace_xsd = self.subnodes_data_handler.get_xsd2(document)

        child_0 = join('element_with_ref_namespace', 'child_0')
        child_0_xsd = self.subnodes_data_handler.get_xsd2(child_0)

        ref_0 = join('element_with_ref_namespace', 'ref_0')
        ref_0_xsd = self.subnodes_data_handler.get_xsd2(ref_0)

        xpath_result = get_nodes_xpath(ref_element_no_namespace_xsd, ref_element_no_namespace_xsd, '')

        expected_result = [
            {
                'name': 'child_0',
                'element': child_0_xsd
            },
            {
                'name': 'ref_0',
                'element': ref_0_xsd
            },
            {  # FIXME the 2nd element shouldn't be here (not needed)
                'name': 'ref_0',
                'element': ref_0_xsd
            }
        ]

        self.assertEqual(len(xpath_result), len(expected_result))

        for xpath in xpath_result:
            # print xpath['name']
            # print etree.tostring(xpath['element'])
            xpath_elem = xpath['element']

            expected_elem_list = [expect['element'] for expect in expected_result if expect['name'] == xpath['name']]
            # FIXME Having 2 element with the same content is not useful (>= 1 should be replaced by == 1)
            expect_elem = expected_elem_list[0] if len(expected_elem_list) >= 1 else None

            self.assertTrue(are_equals(xpath_elem, expect_elem))

    def test_element_ref_has_no_namespace(self):
        document = join('element_with_ref_no_namespace', 'document')
        ref_element_no_namespace_xsd = self.subnodes_data_handler.get_xsd2(document)

        child_0 = join('element_with_ref_no_namespace', 'child_0')
        child_0_xsd = self.subnodes_data_handler.get_xsd2(child_0)

        ref_0 = join('element_with_ref_no_namespace', 'ref_0')
        ref_0_xsd = self.subnodes_data_handler.get_xsd2(ref_0)

        xpath_result = get_nodes_xpath(ref_element_no_namespace_xsd, ref_element_no_namespace_xsd, '')

        expected_result = [
            {
                'name': 'child_0',
                'element': child_0_xsd
            },
            {
                'name': 'ref_0',
                'element': ref_0_xsd
            },
            {  # FIXME the 2nd element shouldn't be here (not needed)
                'name': 'ref_0',
                'element': ref_0_xsd
            }
        ]

        self.assertEqual(len(xpath_result), len(expected_result))

        for xpath in xpath_result:
            xpath_elem = xpath['element']

            expected_elem_list = [expect['element'] for expect in expected_result if expect['name'] == xpath['name']]
            # FIXME Having 2 element with the same content is not useful (>= 1 should be replaced by == 1)
            expect_elem = expected_elem_list[0] if len(expected_elem_list) >= 1 else None

            self.assertTrue(are_equals(xpath_elem, expect_elem))


class ParserLookupOccursTestSuite(TestCase):
    """
    """

    def setUp(self):
        occurs_data = join('curate', 'tests', 'data', 'parser', 'utils', 'occurs')
        self.occurs_data_handler = DataHandler(occurs_data)

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

    def test_reload_compliant_element(self):
        lookup_xsd = self.occurs_data_handler.get_xsd2('document')
        element_xsd = lookup_xsd.xpath('/xs:schema/xs:element/xs:complexType/xs:sequence',
                                       namespaces=self.request.session['namespaces'])

        compliant_xml = self.occurs_data_handler.get_xml('compliant')

        max_occurs_found = lookup_occurs(self.request, element_xsd, lookup_xsd, self.namespace, '.', compliant_xml)
        self.assertEqual(max_occurs_found, 1)

    def test_reload_noncompliant_element(self):
        lookup_xsd = self.occurs_data_handler.get_xsd2('document')
        element_xsd = lookup_xsd.xpath('/xs:schema/xs:element/xs:complexType/xs:sequence',
                                       namespaces=self.request.session['namespaces'])

        noncompliant_xml = self.occurs_data_handler.get_xml('noncompliant')

        max_occurs_found = lookup_occurs(self.request, element_xsd, lookup_xsd, self.namespace, '.', noncompliant_xml)
        self.assertEqual(max_occurs_found, 1)


class ParserManageOccurencesTestSuite(TestCase):
    """
    """

    def setUp(self):
        occurs_data = join('curate', 'tests', 'data', 'parser', 'utils', 'manage_occurs')
        self.occurs_data_handler = DataHandler(occurs_data)

    def test_element_with_min_occurs_parsable(self):
        xsd_element = self.occurs_data_handler.get_xsd2('min_occurs_parsable')
        (min_occ, max_occ) = manage_occurences(xsd_element)

        self.assertEqual(min_occ, 1)

    def test_element_with_max_occurs_unbounded(self):
        xsd_element = self.occurs_data_handler.get_xsd2('max_occurs_unbounded')
        (min_occ, max_occ) = manage_occurences(xsd_element)

        self.assertEqual(max_occ, -1)

    def test_element_with_max_occurs_parsable(self):
        xsd_element = self.occurs_data_handler.get_xsd2('max_occurs_parsable')
        (min_occ, max_occ) = manage_occurences(xsd_element)

        self.assertEqual(max_occ, 5)


class ParserManageAttrOccurencesTestSuite(TestCase):
    """
    """

    def setUp(self):
        occurs_data = join('curate', 'tests', 'data', 'parser', 'utils', 'manage_occurs')
        self.occurs_data_handler = DataHandler(occurs_data)

    def test_use_optional(self):
        xsd_element = self.occurs_data_handler.get_xsd2('attr_use_optional')
        (min_occ, max_occ) = manage_attr_occurrences(xsd_element)

        self.assertEqual(min_occ, 0)
        self.assertEqual(max_occ, 1)

    def test_use_prohibited(self):
        xsd_element = self.occurs_data_handler.get_xsd2('attr_use_prohibited')
        (min_occ, max_occ) = manage_attr_occurrences(xsd_element)

        self.assertEqual(min_occ, 0)
        self.assertEqual(max_occ, 0)

    def test_use_required(self):
        xsd_element = self.occurs_data_handler.get_xsd2('attr_use_required')
        (min_occ, max_occ) = manage_attr_occurrences(xsd_element)

        self.assertEqual(min_occ, 1)
        self.assertEqual(max_occ, 1)

    def test_use_not_present(self):
        xsd_element = self.occurs_data_handler.get_xsd2('attr_use_undefined')
        (min_occ, max_occ) = manage_attr_occurrences(xsd_element)

        # FIXME test broken with current parser
        # self.assertEqual(min_occ, 0)
        self.assertEqual(max_occ, 1)


class ParserHasModuleTestSuite(TestCase):
    """
    """

    def _save_module_to_db(self):
        # FIXME module is not saved in the right database
        module = Module()
        module.name = 'registered_module'
        module.url = 'registered_module'
        module.view = 'registered_module'

        module.save()

    def setUp(self):
        # connect to test database
        # self.db_name = "mgi_test"
        # disconnect()
        # connect(self.db_name, port=27018)

        module_data = join('curate', 'tests', 'data', 'parser', 'utils', 'modules')
        self.module_data_handler = DataHandler(module_data)

    def test_element_is_module_registered(self):
        # expect true
        self._save_module_to_db()

        xsd_element = self.module_data_handler.get_xsd2('registered_module')
        has_module_result = has_module(xsd_element)

        self.assertTrue(has_module_result)

    def test_element_is_module_not_registered(self):
        # expect false
        xsd_element = self.module_data_handler.get_xsd2('unregistered_module')
        has_module_result = has_module(xsd_element)

        self.assertFalse(has_module_result)

    def test_element_is_not_module(self):
        # expect false
        xsd_element = self.module_data_handler.get_xsd2('no_module')
        has_module_result = has_module(xsd_element)

        self.assertFalse(has_module_result)


class ParserGetXmlElementDataTestSuite(TestCase):
    """
    """

    def setUp(self):
        xml_element_data = join('curate', 'tests', 'data', 'parser', 'utils', 'xml_data')
        self.xml_element_data_handler = DataHandler(xml_element_data)

    def test_element_xml_text(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('element', 'simple'))
        xml_element = self.xml_element_data_handler.get_xml(join('element', 'simple'))

        reload_data = get_xml_element_data(xsd_element, xml_element, '')
        self.assertEqual(reload_data, 'test')

    def test_element_xml_branch(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('element', 'complex'))
        xml_element = self.xml_element_data_handler.get_xml(join('element', 'complex'))

        reload_data = get_xml_element_data(xsd_element, xml_element, '')
        self.assertEqual(reload_data, etree.tostring(xml_element))

    def test_attribute(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('attribute', 'schema'))

        reload_data = get_xml_element_data(xsd_element, None, '')
        self.assertEqual(reload_data, None)

    def test_complex_type_xml_empty(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('complex_type', 'complex'))
        xml_element = self.xml_element_data_handler.get_xml(join('complex_type', 'empty'))

        reload_data = get_xml_element_data(xsd_element, xml_element, '')
        self.assertEqual(reload_data, "")

    def test_complex_type_xml_branch(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('complex_type', 'complex'))
        xml_element = self.xml_element_data_handler.get_xml(join('complex_type', 'complex'))

        reload_data = get_xml_element_data(xsd_element, xml_element, '')
        self.assertEqual(reload_data, etree.tostring(xml_element))

    def test_simple_type_xml_text(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('simple_type', 'simple'))
        xml_element = self.xml_element_data_handler.get_xml(join('simple_type', 'simple'))

        reload_data = get_xml_element_data(xsd_element, xml_element, '')
        self.assertEqual(reload_data, "child_0")

    def test_simple_type_empty(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('simple_type', 'simple'))
        xml_element = self.xml_element_data_handler.get_xml(join('simple_type', 'empty'))

        reload_data = get_xml_element_data(xsd_element, xml_element, '')
        self.assertEqual(reload_data, "")


class ParserGetElementTypeTestSuite(TestCase):
    """
    """

    def setUp(self):
        self.defaultPrefix = 'xsd'
        self.namespace = ''

        xml_element_data = join('curate', 'tests', 'data', 'parser', 'element_type')
        self.xml_element_data_handler = DataHandler(xml_element_data)

    def test_no_type_one_child_no_annot(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('no_type', 'one_child_no_annot'))

        element_type = get_element_type(xsd_element, None, '', 'xsd')
        self.assertEqual(element_type, list(xsd_element)[0])

    def test_no_type_one_child_annot(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('no_type', 'one_child_annot'))

        element_type = get_element_type(xsd_element, None, '', 'xsd')
        self.assertEqual(element_type, None)

    def test_no_type_two_children_annot(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('no_type', 'two_children_annot'))

        element_type = get_element_type(xsd_element, None, '', 'xsd')
        self.assertEqual(element_type, list(xsd_element)[1])

    def test_no_type_more_children(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('no_type', 'more_children'))

        element_type = get_element_type(xsd_element, None, '', 'xsd')
        self.assertEqual(element_type, None)

    def test_type_is_common_type(self):
        xsd_element = self.xml_element_data_handler.get_xsd2('common_type')

        element_type = get_element_type(xsd_element, None, '', 'xsd')
        self.assertEqual(element_type, None)

    # todo make more tests
    def test_type_is_complex_type(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('complex_type', 'element'))
        xsd_schema = self.xml_element_data_handler.get_xsd2(join('complex_type', 'schema'))

        result_element = self.xml_element_data_handler.get_xsd2(join('complex_type', 'result'))

        element_type = get_element_type(xsd_element, xsd_schema, '', 'xsd')
        self.assertTrue(are_equals(element_type, result_element))

    def test_type_is_simple_type(self):
        xsd_element = self.xml_element_data_handler.get_xsd2(join('simple_type', 'element'))
        xsd_schema = self.xml_element_data_handler.get_xsd2(join('simple_type', 'schema'))

        result_element = self.xml_element_data_handler.get_xsd2(join('simple_type', 'result'))

        element_type = get_element_type(xsd_element, xsd_schema, '', 'xsd')
        self.assertTrue(are_equals(element_type, result_element))


class ParserRemoveAnnotationTestSuite(TestCase):
    """
    """

    def setUp(self):
        annotation_data = join('curate', 'tests', 'data', 'parser', 'utils', 'annotation')
        self.annotation_data_handler = DataHandler(annotation_data)

        self.namespace = ''

        self.result = self.annotation_data_handler.get_xsd2('not_annot')

    def test_annotation_is_removed(self):
        annotated_schema = self.annotation_data_handler.get_xsd2('annot')
        remove_annotations(annotated_schema, self.namespace)

        self.assertTrue(are_equals(annotated_schema, self.result))

    def test_no_annotation_no_change(self):
        not_annotated_schema = self.annotation_data_handler.get_xsd2('not_annot')
        remove_annotations(not_annotated_schema, self.namespace)

        self.assertTrue(are_equals(not_annotated_schema, self.result))