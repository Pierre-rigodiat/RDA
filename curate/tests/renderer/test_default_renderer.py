from django.test.testcases import TestCase


class InitTestSuite(TestCase):

    def setUp(self):
        pass

    def test_xsd_data_is_list(self):
        pass

    def test_xsd_data_not_list(self):
        pass

    def test_template_list_not_set(self):
        pass

    def test_template_list_is_dict(self):
        pass

    def test_template_list_not_dict(self):
        pass


class LoadTemplateTestSuite(TestCase):

    def setUp(self):
        pass

    def test_key_exists(self):
        pass

    def test_key_not_exists(self):
        pass

    def test_key_not_str(self):
        pass

    def test_tpl_data_not_set(self):
        pass

    def test_tpl_data_is_dict(self):
        pass

    def test_tpl_data_not_dict(self):
        pass


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


