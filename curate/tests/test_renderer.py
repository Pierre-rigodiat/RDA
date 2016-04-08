"""
"""
from django.test import TestCase
from os.path import join
from curate.renderer import render_buttons, load_template, render_form, render_form_error, \
    render_input, render_ul, render_li, render_select
from lxml import etree
from mgi.tests import are_equals, DataHandler, VariableTypesGenerator


class RendererLoadTemplateTestSuite(TestCase):
    """
    """

    def setUp(self):
        load_template_data = join('curate', 'tests', 'data', 'renderer', 'default', 'template')
        self.load_template_data_handler = DataHandler(load_template_data)

        self.types_generator = VariableTypesGenerator()

    def test_path_exist_data_dict(self):
        tpl_path = join('test', 'sample_with_data.html')
        tpl_data = {
            'content': '<p>lorem ipsum</p>'
        }

        result_string = load_template(tpl_path, tpl_data)
        self.assertEqual(result_string, load_template(unicode(tpl_path), tpl_data))

        result_html = etree.fromstring(result_string)
        expected_html = self.load_template_data_handler.get_html2('sample_with_data')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_path_exist_data_none(self):
        tpl_path = join('test', 'sample_no_data.html')

        result_string = load_template(tpl_path)
        self.assertEqual(result_string, load_template(unicode(tpl_path)))

        result_html = etree.fromstring(result_string)
        expected_html = self.load_template_data_handler.get_html2('sample_no_data')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_path_exist_data_not_dict_not_none(self):
        tpl_path = join('test', 'sample_no_data.html')
        tpl_data = []

        try:
            for tpl_data in self.types_generator.generate_types_excluding(['dict', 'none']):
                with self.assertRaises(Exception):
                    load_template(tpl_path, tpl_data)
        except AssertionError as error:
            tpl_data_type = str(type(tpl_data))
            error.message += ' (tpl_data type: ' + tpl_data_type + ')'
            raise AssertionError(error.message)

    def test_path_not_exist(self):
        tpl_path = join('test', 'unexisting.html')

        with self.assertRaises(Exception):
            load_template(tpl_path)

    def test_path_not_str(self):
        tpl_path = 'string'

        try:
            for tpl_path in self.types_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    load_template(tpl_path)
        except AssertionError as error:
            tpl_path_type = str(type(tpl_path))
            error.message += ' (tpl_path type: ' + tpl_path_type + ')'
            raise AssertionError(error.message)

    def test_data_incorrect(self):
        tpl_path = join('test', 'sample.html')
        tpl_data = {
            'unknown': '<p>lorem ipsum</p>'
        }

        with self.assertRaises(Exception):
            load_template(tpl_path, tpl_data)


class RendererRenderFormTestSuite(TestCase):

    def setUp(self):
        form_data = join('curate', 'tests', 'data', 'renderer', 'default')
        self.form_data_handler = DataHandler(form_data)

        self.types_generator = VariableTypesGenerator()

    def test_content_str(self):
        form_content = '<p>lorem ipsum</p>'

        result_string = render_form(form_content)
        # print result_string
        self.assertEqual(result_string, render_form(unicode(form_content)))

        result_html = etree.fromstring(result_string)
        expected_html = self.form_data_handler.get_html2('form')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_content_not_str(self):
        content = 'string'

        try:
            for content in self.types_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    render_form(content)
        except AssertionError as error:
            content_type = str(type(content))
            error.message += ' (content type: ' + content_type + ')'
            raise AssertionError(error.message)


class RendererRenderFormErrorTestSuite(TestCase):

    def setUp(self):
        form_error_data = join('curate', 'tests', 'data', 'renderer', 'default')
        self.form_error_data_handler = DataHandler(form_error_data)

        self.types_generator = VariableTypesGenerator()

    def test_message_str(self):
        form_error_message = 'Sample error message'

        result_string = render_form_error(form_error_message)
        # print result_string
        self.assertEqual(result_string, render_form_error(unicode(form_error_message)))

        result_html = etree.fromstring(result_string)
        expected_html = self.form_error_data_handler.get_html2('form_error')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_message_not_str(self):
        error_message = 'string'

        try:
            for error_message in self.types_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    render_form_error(error_message)
        except AssertionError as error:
            error_message_type = str(type(error_message))
            error.message += ' (error_message type: ' + error_message_type + ')'
            raise AssertionError(error.message)


class RendererRenderInputTestSuite(TestCase):

    def setUp(self):
        input_data = join('curate', 'tests', 'data', 'renderer', 'default', 'input')
        self.input_data_handler = DataHandler(input_data)

        self.types_generator = VariableTypesGenerator()

    def test_value_str_placeholder_str_title_str(self):
        value = 'val'
        placeholder = 'placeholder'
        title = 'title'

        result_string = render_input(value, placeholder, title)
        # print result_string
        self.assertEqual(result_string, render_input(unicode(value), unicode(placeholder), unicode(title)))

        result_html = etree.fromstring(result_string)
        expected_html = self.input_data_handler.get_html2('val_str_pl_str_tt_str')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_value_str_placeholder_str_title_empty_str(self):
        value = 'val'
        placeholder = 'placeholder'
        title = ''

        result_string = render_input(value, placeholder, title)
        # print result_string
        self.assertEqual(result_string, render_input(unicode(value), unicode(placeholder), unicode(title)))

        result_html = etree.fromstring(result_string)
        expected_html = self.input_data_handler.get_html2('val_str_pl_str_tt_empty')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_value_str_placeholder_empty_str_title_str(self):
        value = 'val'
        placeholder = ''
        title = 'title'

        result_string = render_input(value, placeholder, title)
        # print result_string
        self.assertEqual(result_string, render_input(unicode(value), unicode(placeholder), unicode(title)))

        result_html = etree.fromstring(result_string)
        expected_html = self.input_data_handler.get_html2('val_str_pl_empty_tt_str')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_value_str_placeholder_empty_str_title_empty_str(self):
        value = 'val'
        placeholder = ''
        title = ''

        result_string = render_input(value, placeholder, title)
        # print result_string
        self.assertEqual(result_string, render_input(unicode(value), unicode(placeholder), unicode(title)))

        result_html = etree.fromstring(result_string)
        expected_html = self.input_data_handler.get_html2('val_str_pl_empty_tt_empty')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_value_empty_str_placeholder_str_title_str(self):
        value = ''
        placeholder = 'placeholder'
        title = 'title'

        result_string = render_input(value, placeholder, title)
        # print result_string
        self.assertEqual(result_string, render_input(unicode(value), unicode(placeholder), unicode(title)))

        result_html = etree.fromstring(result_string)
        expected_html = self.input_data_handler.get_html2('val_empty_pl_str_tt_str')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_value_empty_str_placeholder_str_title_empty_str(self):
        value = ''
        placeholder = 'placeholder'
        title = ''

        result_string = render_input(value, placeholder, title)
        # print result_string
        self.assertEqual(result_string, render_input(unicode(value), unicode(placeholder), unicode(title)))

        result_html = etree.fromstring(result_string)
        expected_html = self.input_data_handler.get_html2('val_empty_pl_str_tt_empty')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_value_empty_str_placeholder_empty_str_title_str(self):
        value = ''
        placeholder = ''
        title = 'title'

        result_string = render_input(value, placeholder, title)
        # print result_string
        self.assertEqual(result_string, render_input(unicode(value), unicode(placeholder), unicode(title)))

        result_html = etree.fromstring(result_string)
        expected_html = self.input_data_handler.get_html2('val_empty_pl_empty_tt_str')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_value_empty_str_placeholder_empty_str_title_empty_str(self):
        value = ''
        placeholder = ''
        title = ''

        result_string = render_input(value, placeholder, title)
        # print result_string
        self.assertEqual(result_string, render_input(unicode(value), unicode(placeholder), unicode(title)))

        result_html = etree.fromstring(result_string)
        expected_html = self.input_data_handler.get_html2('val_empty_pl_empty_tt_empty')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_value_not_str(self):
        value = 'string'
        placeholder = 'string'
        title = 'string'

        try:
            for value in self.types_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    render_input(value, placeholder, title)
        except AssertionError as error:
            value_type = str(type(value))
            error.message += ' (value type: ' + value_type + ')'
            raise AssertionError(error.message)

    def test_placeholder_not_str(self):
        value = 'string'
        placeholder = 'string'
        title = 'string'

        try:
            for placeholder in self.types_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    render_input(value, placeholder, title)
        except AssertionError as error:
            placeholder_type = str(type(placeholder))
            error.message += ' (placeholder type: ' + placeholder_type + ')'
            raise AssertionError(error.message)

    def test_title_not_str(self):
        value = 'string'
        placeholder = 'string'
        title = 'string'

        try:
            for title in self.types_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    render_input(value, placeholder, title)
        except AssertionError as error:
            title_type = str(type(title))
            error.message += ' (title type: ' + title_type + ')'
            raise AssertionError(error.message)


class RendererRenderUlTestSuite(TestCase):

    def setUp(self):
        ul_data = join('curate', 'tests', 'data', 'renderer', 'default', 'ul')
        self.ul_data_handler = DataHandler(ul_data)

        self.types_generator = VariableTypesGenerator()
        self.content = '<li>lorem ipsum</li>'

    def test_elem_id_str_chosen_true(self):
        element_id = 'string'
        chosen = True

        result_string = render_ul(self.content, element_id, chosen)
        self.assertEqual(result_string, render_ul(unicode(self.content), unicode(element_id), chosen))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.ul_data_handler.get_html2('elem_str_ch_true')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_elem_id_str_chosen_false(self):
        element_id = 'string'
        chosen = False

        result_string = render_ul(self.content, element_id, chosen)
        self.assertEqual(result_string, render_ul(unicode(self.content), unicode(element_id), chosen))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.ul_data_handler.get_html2('elem_str_ch_false')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_elem_id_empty_str_chosen_true(self):
        element_id = ''
        chosen = True

        result_string = render_ul(self.content, element_id, chosen)
        self.assertEqual(result_string, render_ul(unicode(self.content), unicode(element_id), chosen))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.ul_data_handler.get_html2('elem_empty_ch_true')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_elem_id_empty_str_chosen_false(self):
        element_id = ''
        chosen = False

        result_string = render_ul(self.content, element_id, chosen)
        self.assertEqual(result_string, render_ul(unicode(self.content), unicode(element_id), chosen))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.ul_data_handler.get_html2('elem_empty_ch_false')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_elem_id_none_chosen_true(self):
        element_id = None
        chosen = True

        result_string = render_ul(self.content, element_id, chosen)
        self.assertEqual(result_string, render_ul(unicode(self.content), element_id, chosen))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.ul_data_handler.get_html2('elem_none_ch_true')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_elem_id_none_chosen_false(self):
        element_id = 'string'
        chosen = True

        result_string = render_ul(self.content, element_id, chosen)
        self.assertEqual(result_string, render_ul(unicode(self.content), element_id, chosen))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.ul_data_handler.get_html2('elem_str_ch_true')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_content_not_str(self):
        content = 'string'
        element_id = 'string'
        chosen = True

        try:
            for content in self.types_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    render_ul(content, element_id, chosen)
        except AssertionError as error:
            content_type = str(type(content))
            error.message += ' (content type: ' + content_type + ')'
            raise AssertionError(error.message)

    def test_elem_id_not_str_not_none(self):
        content = 'string'
        element_id = 'string'
        chosen = True

        try:
            for element_id in self.types_generator.generate_types_excluding(['str', 'unicode', 'none']):
                with self.assertRaises(Exception):
                    render_ul(content, element_id, chosen)
        except AssertionError as error:
            element_id_type = str(type(element_id))
            error.message += ' (element_id type: ' + element_id_type + ')'
            raise AssertionError(error.message)

    def test_chosen_not_bool(self):
        content = 'string'
        element_id = 'string'
        chosen = True

        try:
            for chosen in self.types_generator.generate_types_excluding(['bool']):
                with self.assertRaises(Exception):
                    render_ul(content, element_id, chosen)
        except AssertionError as error:
            chosen_type = str(type(chosen))
            error.message += ' (content type: ' + chosen_type + ')'
            raise AssertionError(error.message)


class RendererRenderLiTestSuite(TestCase):

    def setUp(self):
        li_data = join('curate', 'tests', 'data', 'renderer', 'default', 'li')
        self.li_data_handler = DataHandler(li_data)

        self.types_generator = VariableTypesGenerator()

        self.content = 'lorem ipsum'
        self.tag_id = '0'
        self.element_tag = 'element'

    def test_default_parameters(self):
        result_string = render_li(self.content, self.tag_id, self.element_tag)
        self.assertEqual(result_string, render_li(unicode(self.content), unicode(self.tag_id),
                                                  unicode(self.element_tag)))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.li_data_handler.get_html2('default')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_use_str_text_str(self):
        use = 'use'
        text = 'text'

        result_string = render_li(self.content, self.tag_id, self.element_tag, use, text)
        self.assertEqual(result_string, render_li(unicode(self.content), unicode(self.tag_id),
                                                  unicode(self.element_tag), use, text))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.li_data_handler.get_html2('use_str_text_str')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_use_str_text_none(self):
        use = 'use'
        text = None

        result_string = render_li(self.content, self.tag_id, self.element_tag, use, text)
        self.assertEqual(result_string, render_li(unicode(self.content), unicode(self.tag_id),
                                                  unicode(self.element_tag), use, text))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.li_data_handler.get_html2('use_str_text_none')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_use_none_text_str(self):
        use = None
        text = 'text'

        result_string = render_li(self.content, self.tag_id, self.element_tag, use, text)
        self.assertEqual(result_string, render_li(unicode(self.content), unicode(self.tag_id),
                                                  unicode(self.element_tag), use, text))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.li_data_handler.get_html2('use_none_text_str')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_text_not_str_not_none(self):
        use = 'string'
        text = 'string'

        try:
            for text in self.types_generator.generate_types_excluding(['str', 'unicode', 'none']):
                with self.assertRaises(Exception):
                    render_li(self.content, self.tag_id, self.element_tag, use, text)
        except AssertionError as error:
            text_type = str(type(text))
            error.message += ' (use type: ' + text_type + ')'
            raise AssertionError(error.message)

    def test_use_not_str_not_none(self):
        use = 'string'

        try:
            for use in self.types_generator.generate_types_excluding(['str', 'unicode', 'none']):
                with self.assertRaises(Exception):
                    render_li(self.content, self.tag_id, self.element_tag, use)
        except AssertionError as error:
            use_type = str(type(use))
            error.message += ' (use type: ' + use_type + ')'
            raise AssertionError(error.message)

    def test_content_not_str(self):
        content = 'string'

        try:
            for content in self.types_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    render_li(content, self.tag_id, self.element_tag)
        except AssertionError as error:
            content_type = str(type(content))
            error.message += ' (content type: ' + content_type + ')'
            raise AssertionError(error.message)

    def test_element_tag_not_str(self):
        element_tag = 'string'

        try:
            for element_tag in self.types_generator.generate_types_excluding(['str', 'unicode']):
                with self.assertRaises(Exception):
                    render_li(self.content, self.tag_id, element_tag)
        except AssertionError as error:
            element_tag_type = str(type(element_tag))
            error.message += ' (element_tag type: ' + element_tag_type + ')'
            raise AssertionError(error.message)

    def test_tag_id_not_parsable(self):
        class TestTagID(object):
            item = None

            def __str__(self):
                return 'undefined' + self.item

        with self.assertRaises(Exception):
            render_li(self.content, TestTagID(), self.element_tag)


class RendererRenderSelectTestSuite(TestCase):

    def setUp(self):
        select_data = join('curate', 'tests', 'data', 'renderer', 'default', 'select')
        self.select_data_handler = DataHandler(select_data)

        self.types_generator = VariableTypesGenerator()
        self.select_id = 'select'

    def test_id_str_options_list(self):
        options = [
            ('opt1', 'opt1', False),
            ('opt2', 'opt2', False),
            ('opt3', 'opt3', True)
        ]

        result_string = render_select(self.select_id, options)
        self.assertEqual(result_string, render_select(unicode(self.select_id), options))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.select_data_handler.get_html2('id_str_options_list')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_id_str_options_empty_list(self):
        options = []

        result_string = render_select(self.select_id, options)
        self.assertEqual(result_string, render_select(unicode(self.select_id), options))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.select_data_handler.get_html2('id_str_options_empty')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_id_none_options_list(self):
        options = [
            ('opt1', 'opt1', False),
            ('opt2', 'opt2', False),
            ('opt3', 'opt3', True)
        ]

        result_string = render_select(None, options)
        self.assertEqual(result_string, render_select(None, options))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.select_data_handler.get_html2('id_none_options_list')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_id_none_options_empty_list(self):
        options = []

        result_string = render_select(None, options)
        self.assertEqual(result_string, render_select(None, options))
        # print result_string

        result_html = etree.fromstring(result_string)
        expected_html = self.select_data_handler.get_html2('id_none_options_empty')

        self.assertTrue(are_equals(result_html, expected_html))

    def test_id_not_str_not_none(self):
        element_id = 'string'

        try:
            for element_id in self.types_generator.generate_types_excluding(['str', 'unicode', 'none']):
                with self.assertRaises(Exception):
                    render_select(element_id, [])
        except AssertionError as error:
            element_id_type = str(type(element_id))
            error.message += ' (element_id type: ' + element_id_type + ')'
            raise AssertionError(error.message)

    def test_options_not_list(self):
        options = []

        try:
            for options in self.types_generator.generate_types_excluding(['list']):
                with self.assertRaises(Exception):
                    render_select(self.select_id, options)
        except AssertionError as error:
            options_type = str(type(options))
            error.message += ' (options type: ' + options_type + ')'
            raise AssertionError(error.message)

    def test_options_not_list_of_tuple(self):
        options = [()]

        try:
            for item in self.types_generator.generate_types_excluding(['tuple']):
                options[0] = item

                with self.assertRaises(Exception):
                    render_select(self.select_id, options)
        except AssertionError as error:
            item_type = str(type(options[0]))
            error.message += ' (item type: ' + item_type + ')'
            raise AssertionError(error.message)

    def test_options_malformed_list(self):
        options = [()]

        try:
            for param in self.types_generator.generate_types_excluding(['str', 'unicode']):
                options[0] = (param, '', False)
                with self.assertRaises(Exception):
                    render_select(self.select_id, options)

                options[0] = ('', param, False)
                with self.assertRaises(Exception):
                    render_select(self.select_id, options)

            for param in self.types_generator.generate_types_excluding(['bool']):
                options[0] = ('', '', param)
                with self.assertRaises(Exception):
                    render_select(self.select_id, options)

            with self.assertRaises(Exception):
                render_select(self.select_id, [('elem0', 'elem1')])
        except AssertionError as error:
            error.message += ' (option not considered as malformed: ' + str(options) + ')'
            raise AssertionError(error.message)


class RendererRenderButtonsTestSuite(TestCase):
    """ render_buttons test suite
    """

    def setUp(self):
        buttons_data = join('curate', 'tests', 'data', 'parser', 'utils', 'buttons')
        self.buttons_data_handler = DataHandler(buttons_data)

        self.types_generator = VariableTypesGenerator()
        self.default_tag_id = 'string'

    def _expected_form(self, is_add_present, is_del_present):
        add_tpl_name = "add_shown" if is_add_present else "add_hidden"
        del_tpl_name = "remove_shown" if is_del_present else "remove_hidden"

        add_html = self.buttons_data_handler.get_html2(add_tpl_name)
        del_html = self.buttons_data_handler.get_html2(del_tpl_name)

        span = etree.Element('span')
        span.append(add_html)
        span.append(del_html)

        return span

    def test_add_del_false(self):
        is_add_present = False
        is_del_present = False

        form = render_buttons(is_add_present, is_del_present, self.default_tag_id)
        self.assertEqual(form, "")

    def test_add_true_del_false(self):
        is_add_present = True
        is_del_present = False

        form_string = render_buttons(is_add_present, is_del_present, self.default_tag_id)
        form = etree.fromstring('<span>' + form_string + '</span>')

        expected_form = self._expected_form(is_add_present, is_del_present)
        # expected_form_wrapped = '<span>' + self.addButtonPresent + self.delButtonHidden + '</span>'

        self.assertTrue(
            are_equals(form, expected_form)
            # self._xmlStringAreEquals(form_wrapped, expected_form_wrapped)
        )

    def test_add_del_true(self):
        is_add_present = True
        is_del_present = True

        form_string = render_buttons(is_add_present, is_del_present, self.default_tag_id)
        # form_wrapped = '<span>' + form + '</span>'
        form = etree.fromstring('<span>' + form_string + '</span>')

        expected_form = self._expected_form(is_add_present, is_del_present)
        # expected_form_wrapped = '<span>' + self.addButtonPresent + self.delButtonPresent + '</span>'

        self.assertTrue(
            are_equals(form, expected_form)
            # self._xmlStringAreEquals(form_wrapped, expected_form_wrapped)
        )

    def test_add_false_del_true(self):
        is_add_present = False
        is_del_present = True

        form_string = render_buttons(is_add_present, is_del_present, self.default_tag_id)
        # form_wrapped = '<span>' + form + '</span>'
        form = etree.fromstring('<span>' + form_string + '</span>')

        expected_form = self._expected_form(is_add_present, is_del_present)
        # expected_form_wrapped = '<span>' + self.addButtonHidden + self.delButtonPresent + '</span>'

        self.assertTrue(
            are_equals(form, expected_form)
            # self._xmlStringAreEquals(form_wrapped, expected_form_wrapped)
        )

    def test_add_button_not_bool(self):
        is_add_present = True
        try:
            for is_add_present in self.types_generator.generate_types_excluding(['bool']):
                with self.assertRaises(Exception):
                    render_buttons(is_add_present, True, self.default_tag_id)
        except AssertionError as error:
            is_add_present_type = str(type(is_add_present))
            error.message += ' (is_add_present type: ' + is_add_present_type + ')'
            raise AssertionError(error.message)

    def test_del_button_not_bool(self):
        is_del_present = True
        try:
            for is_del_present in self.types_generator.generate_types_excluding(['bool']):
                with self.assertRaises(Exception):
                    render_buttons(True, is_del_present, self.default_tag_id)
        except AssertionError as error:
            is_del_present_type = str(type(is_del_present))
            error.message += ' (is_del_present type: ' + is_del_present_type + ')'
            raise AssertionError(error.message)

    def test_tag_id_not_str(self):
        for tag_id in self.types_generator.generate_types_excluding(['str']):
            for is_add_present in [True, False]:
                for is_del_present in [True, False]:
                    try:
                        render_buttons(is_add_present, is_del_present, tag_id)
                    except Exception as exc:
                        tag_id_type = str(type(tag_id))
                        self.fail('Unexpected exception raised with tag_id of type ' + tag_id_type + ':' + exc.message)


class RendererRenderCollapseButtonTestSuite(TestCase):
    """

    """

    def setUp(self):
        collapse_data = join('curate', 'tests', 'data', 'renderer', 'default')
        self.collapse_data_handler = DataHandler(collapse_data)

    def test_button(self):
        # result_string = render_collapse_button()
        result_string = ''
        result_html = etree.fromstring(result_string)

        expected_html = self.collapse_data_handler.get_html2('collapse')

        self.assertTrue(are_equals(result_html, expected_html))
