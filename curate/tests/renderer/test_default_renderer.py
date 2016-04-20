from django.template.base import Template
from django.test.testcases import TestCase
from curate.models import SchemaElement
from curate.renderer import DefaultRenderer
from mgi.tests import VariableTypesGenerator


class InitTestSuite(TestCase):

    def setUp(self):
        self.maxDiff = None
        self.type_generator = VariableTypesGenerator()

    def test_xsd_data_is_schema_element(self):
        xsd_data = SchemaElement()
        xsd_data.tag = "test"

        renderer = DefaultRenderer(xsd_data)

        self.assertEqual(xsd_data, renderer.data)

    def test_xsd_data_not_schema_element(self):
        xsd_data = None

        try:
            for xsd_data in self.type_generator.generate_types_excluding([]):
                with self.assertRaises(Exception):
                    DefaultRenderer(xsd_data)
        except AssertionError as error:
            xsd_data_type = str(type(xsd_data))
            error.message += ' (xsd_data type: ' + xsd_data_type + ')'
            raise AssertionError(error.message)

    def test_template_list_not_set(self):
        xsd_data = SchemaElement()
        xsd_data.tag = "test"

        renderer = DefaultRenderer(xsd_data)

        # Loose comparison is enough for this test
        self.assertEqual(len(renderer.templates), 7)

    def test_template_list_is_correct_dict(self):
        xsd_data = SchemaElement()
        xsd_data.tag = "test"

        template_list = {
            "t1": Template('a'),
            "t2": Template('b'),
            "t3": Template('c')
        }

        base_renderer = DefaultRenderer(xsd_data)
        base_renderer.templates.update(template_list)

        renderer = DefaultRenderer(xsd_data, template_list)

        self.assertEqual(renderer.templates.keys(), base_renderer.templates.keys())

    def test_template_list_is_incorrect_dict(self):
        xsd_data = SchemaElement()
        xsd_data.tag = "test"

        template = None

        try:
            for template in self.type_generator.generate_types_excluding([]):
                template_list = {
                    "wrong": template
                }

                with self.assertRaises(Exception):
                    DefaultRenderer(xsd_data, template_list)
        except AssertionError as error:
            template_type = str(type(template))
            error.message += ' (template type: ' + template_type + ')'
            raise AssertionError(error.message)

    def test_template_list_not_dict(self):
        xsd_data = SchemaElement()
        xsd_data.tag = "test"

        template_list = None

        try:
            for template_list in self.type_generator.generate_types_excluding(['dict', 'none']):
                with self.assertRaises(Exception):
                    DefaultRenderer(xsd_data, template_list)
        except AssertionError as error:
            template_list_type = str(type(template_list))
            error.message += ' (template_list type: ' + template_list_type + ')'
            raise AssertionError(error.message)


class LoadTemplateTestSuite(TestCase):

    def setUp(self):
        xsd_data = SchemaElement()
        xsd_data.tag = "test"

        self.renderer = DefaultRenderer(xsd_data)

        self.type_generator = VariableTypesGenerator()

    def test_key_exists_data_not_set(self):
        self.renderer._load_template('btn_collapse')

    def test_key_not_exists(self):
        with self.assertRaises(Exception):
            self.renderer._load_template('unexisting_key')

    def test_key_not_str(self):
        tpl_key = None

        try:
            for tpl_key in self.type_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    self.renderer._load_template(tpl_key)
        except AssertionError as error:
            tpl_key_type = str(type(tpl_key))
            error.message += ' (tpl_key type: ' + tpl_key_type + ')'
            raise AssertionError(error.message)

    def test_tpl_data_is_dict(self):
        self.renderer._load_template('btn_add', {'is_hidden': True})

    def test_tpl_data_not_dict(self):
        tpl_data = None

        try:
            for tpl_data in self.type_generator.generate_types_excluding(['dict', 'none']):
                with self.assertRaises(Exception):
                    self.renderer._load_template('btn_add', tpl_data)
        except AssertionError as error:
            tpl_data_type = str(type(tpl_data))
            error.message += ' (tpl_data type: ' + tpl_data_type + ')'
            raise AssertionError(error.message)


class RenderFormTestSuite(TestCase):

    def setUp(self):
        pass

    def test_content_is_html(self):
        pass

    def test_content_not_html(self):
        pass

    def test_content_not_string(self):
        pass


class RenderFormErrorTestSuite(TestCase):

    def setUp(self):
        pass

    def test_error_is_string(self):
        pass

    def test_content_not_string(self):
        pass


class RenderInputTestSuite(TestCase):

    def setUp(self):
        pass

    def test_input_id_is_db_element(self):
        pass

    def test_input_id_not_str(self):
        pass

    def test_input_id_not_db_element(self):
        pass

    def test_value_is_str(self):
        pass

    def test_value_not_str(self):
        pass

    def test_placeholder_is_str(self):
        pass

    def test_placeholder_not_str(self):
        pass

    def test_title_is_str(self):
        pass

    def test_title_not_str(self):
        pass


class RenderSelectTestSuite(TestCase):

    def setUp(self):
        pass

    def test_select_id_is_db_elem(self):
        pass

    def test_select_id_not_db_element(self):
        pass

    def test_select_id_not_str(self):
        pass

    def test_options_list_is_list_with_good_tuples(self):
        pass

    def test_options_list_is_list_with_bad_tuples(self):
        pass

    def test_options_list_is_list_without_tuples(self):
        pass

    def test_options_list_is_not_list(self):
        pass


class RenderButtonsTestSuite(TestCase):

    def setUp(self):
        pass

    def test_min_occurs(self):
        pass

    def test_max_occurs(self):
        pass

    def test_occurence(self):
        pass


class RenderCollapseButtonsTestSuite(TestCase):

    def setUp(self):
        pass

    def test_rendering(self):
        pass
