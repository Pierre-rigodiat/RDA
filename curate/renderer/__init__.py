"""
"""
import types
from types import NoneType
from django.http.request import HttpRequest
from django.template.context import RequestContext
from django.template import loader
from os.path import join


def load_template(template_path, template_data=None, template_dir='default'):
    context = RequestContext(HttpRequest())

    if template_data is not None and type(template_data) != dict:
        raise TypeError('Second parameter should be a dict (' + str(type(template_data)) + ' given)')

    if template_data is not None:
        context.update(template_data)

    template_path = join('renderer', template_dir, template_path)

    template = loader.get_template(template_path)
    return template.render(context)


def render_form(content):
    """

    :param content:
    :return:
    """
    if type(content) not in [str, unicode]:
        raise TypeError('Content should be a str (' + str(type(content)) + ' given)')

    data = {
        'content': content
    }

    return load_template('form.html', data)


def render_form_error(message):
    """

    :param message:
    :return:
    """
    if type(message) not in [str, unicode]:
        raise TypeError('Content should be a str (' + str(type(message)) + ' given)')

    return load_template('form-error.html', {'message': message})


def render_input(value, placeholder, title):
    """

    :param value:
    :param placeholder:
    :param title:
    :return:
    """

    if type(value) not in [str, unicode]:
        raise TypeError('First param (value) should be a str (' + str(type(value)) + ' given)')

    if type(placeholder) not in [str, unicode]:
        raise TypeError('Second param (placeholder) should be a str (' + str(type(value)) + ' given)')

    if type(title) not in [str, unicode]:
        raise TypeError('Third param (title) should be a str (' + str(type(value)) + ' given)')

    data = {
        'value': value,
        'placeholder': placeholder,
        'title': title
    }

    return load_template('inputs/input.html', data)


def render_ul(content, element_id, chosen):
    """

    :param content:
    :param element_id:
    :param chosen:
    :return:
    """
    # FIXME Django SafeText type cause the test to fail
    # if type(content) not in [str, unicode]:
    #     raise TypeError('First param (content) should be a str (' + str(type(content)) + ' given)')

    if type(element_id) not in [str, unicode, NoneType]:
        raise TypeError('Second param (element_id) should be a str or None (' + str(type(element_id)) + ' given)')

    if type(chosen) != bool:
        raise TypeError('Third param (chosen) should be a bool (' + str(type(chosen)) + ' given)')

    data = {
        'content': content,
        'element_id': element_id,
        'chosen': chosen
    }

    return load_template('ul.html', data)


def render_li(content, li_class, li_id):
    """

    Parameters:
        content:
        li_class:
        li_id:

    :return:
    """

    # if type(content) not in [str, unicode]:
    #     raise TypeError('First param (content) should be a str (' + str(type(content)) + ' given)')
    #
    # try:
    #     tag_id = str(tag_id)
    # except:
    #     raise TypeError('Second param (tag_id) should be a parsable as a string')
    #
    # if type(element_tag) not in [str, unicode]:
    #     raise TypeError('Third param (element_tag) should be a str (' + str(type(element_tag)) + ' given)')
    #
    # if type(use) not in [str, unicode, NoneType]:
    #     raise TypeError('Fourth param (use) should be a str or None (' + str(type(use)) + ' given)')
    #
    # if type(text) not in [str, unicode, NoneType]:
    #     raise TypeError('Fifth param (text) should be a str or None (' + str(type(text)) + ' given)')
    #
    # if use is None:
    #     li_class = element_tag
    # else:
    #     li_class = element_tag + ' ' + use

    data = {
        'li_class': li_class,
        # 'tag_id': tag_id,
        'li_id': str(li_id),
        # 'text': text,
        'content': content
    }

    return load_template('li.html', data)


def render_select(select_id, option_list):
    """

    :param select_id:
    :param option_list:
    :return:
    """

    if type(select_id) not in [str, unicode, NoneType]:
        raise TypeError('First param (select_id) should be a str or None (' + str(type(select_id)) + ' given)')

    if not isinstance(option_list, types.ListType):
        raise TypeError('First param (option_list) should be a list (' + str(type(option_list)) + ' given)')

    for option in option_list:
        if not isinstance(option, types.TupleType):
            raise TypeError('Malformed param (option_list): type of item not good')

        if len(option) != 3:
            raise TypeError('Malformed param (option_list): Length of item not good')

        if type(option[0]) not in [str, unicode]:
            raise TypeError('Malformed param (option_list): item[0] should be a str')

        if type(option[1]) not in [str, unicode]:
            raise TypeError('Malformed param (option_list): item[1] should be a str')

        if type(option[2]) != bool:
            raise TypeError('Malformed param (option_list): item[2] should be a bool')

    data = {
        'select_id': select_id,
        'option_list': option_list
    }

    return load_template('inputs/select.html', data)


def render_buttons(add_button, delete_button):
    """Displays buttons for a duplicable/removable element

    Parameters:
        add_button: boolean
        delete_button: boolean

    Returns:
        JSON data
    """
    add_button_type = type(add_button)
    del_button_type = type(delete_button)

    if add_button_type is not bool:
        raise TypeError('add_button type is wrong (' + str(add_button_type) + 'received, bool needed')

    if del_button_type is not bool:
        raise TypeError('add_button type is wrong (' + str(del_button_type) + 'received, bool needed')

    form_string = ""

    # Fixed number of occurences, don't need buttons
    if not add_button and not delete_button:
        pass
    else:
        if add_button:
            form_string += load_template('buttons/add.html', {'is_hidden': False})
        else:
            form_string += load_template('buttons/add.html', {'is_hidden': True})

        if delete_button:
            form_string += load_template('buttons/delete.html', {'is_hidden': False})
        else:
            form_string += load_template('buttons/delete.html', {'is_hidden': True})

    return form_string


def render_collapse_button():
    """

    :return:
    """
    return load_template('buttons/collapse.html')


class DefaultRenderer(object):

    def __init__(self, xsd_data, template_list):
        self.data = xsd_data

        default_renderer_path = join('renderer', 'default')
        self.templates = {
            'form_error': loader.get_template(join(default_renderer_path, 'form-error.html')),

            'input': loader.get_template(join(default_renderer_path, 'inputs', 'input.html')),
            'select': loader.get_template(join(default_renderer_path, 'inputs', 'select.html')),
            'btn_add': loader.get_template(join(default_renderer_path, 'buttons', 'add.html')),
            'btn_del': loader.get_template(join(default_renderer_path, 'buttons', 'delete.html'))
        }

        self.templates.update(template_list)

    def _load_template(self, tpl_key, tpl_data=None):
        context = RequestContext(HttpRequest())

        if tpl_key not in self.templates.keys():
            raise IndexError('Template "' + tpl_key + '" not found in registered templates ' +
                             str(self.templates.keys()))

        if tpl_data is not None and type(tpl_data) != dict:
            raise TypeError('Second parameter should be a dict (' + str(type(tpl_data)) + ' given)')

        if tpl_data is not None:
            context.update(tpl_data)

        return self.templates[tpl_key].render(context)

    def _render_form(self, content):
        pass

    def _render_form_error(self, err_message):
        context = RequestContext(HttpRequest())
        data = {
            'message': err_message
        }

        context.update(data)
        return self.templates['form_error'].render(context)

    def _render_input(self, input_id, value, placeholder, title):
        """

        :param value:
        :param placeholder:
        :param title:
        :return:
        """

        if type(value) not in [str, unicode]:
            raise TypeError('First param (value) should be a str (' + str(type(value)) + ' given)')

        if type(placeholder) not in [str, unicode]:
            raise TypeError('Second param (placeholder) should be a str (' + str(type(value)) + ' given)')

        if type(title) not in [str, unicode]:
            raise TypeError('Third param (title) should be a str (' + str(type(value)) + ' given)')

        data = {
            'id': input_id,
            'value': value,
            'placeholder': placeholder,
            'title': title
        }

        return self._load_template('input', data)

    def _render_select(self, select_id, select_class, option_list):
        if type(select_id) not in [str, unicode, NoneType]:
            raise TypeError('First param (select_id) should be a str or None (' + str(type(select_id)) + ' given)')

        if not isinstance(option_list, types.ListType):
            raise TypeError('First param (option_list) should be a list (' + str(type(option_list)) + ' given)')

        for option in option_list:
            if not isinstance(option, types.TupleType):
                raise TypeError('Malformed param (option_list): type of item not good')

            if len(option) != 3:
                raise TypeError('Malformed param (option_list): Length of item not good')

            if type(option[0]) not in [str, unicode]:
                raise TypeError('Malformed param (option_list): item[0] should be a str')

            if type(option[1]) not in [str, unicode]:
                raise TypeError('Malformed param (option_list): item[1] should be a str')

            if type(option[2]) != bool:
                raise TypeError('Malformed param (option_list): item[2] should be a bool')

        data = {
            'select_id': select_id,
            'select_class': select_class,
            'option_list': option_list
        }

        return self._load_template('select', data)

    def _render_buttons(self, min_occurs, max_occurs, occurence_count):
        """

        :param min_occurs:
        :param max_occurs:
        :param occurence_count:
        :return:
        """
        add_button = False
        del_button = False

        if occurence_count < max_occurs or max_occurs == -1:
            add_button = True

        if occurence_count > min_occurs:
            del_button = True

        if occurence_count < min_occurs:
            pass

        add_button_type = type(add_button)
        del_button_type = type(del_button)

        if add_button_type is not bool:
            raise TypeError('add_button type is wrong (' + str(add_button_type) + 'received, bool needed')

        if del_button_type is not bool:
            raise TypeError('add_button type is wrong (' + str(del_button_type) + 'received, bool needed')

        form_string = ""

        # Fixed number of occurences, don't need buttons
        if add_button or del_button:
            if add_button:
                form_string += self._load_template('btn_add', {'is_hidden': False})
            else:
                form_string += self._load_template('btn_add', {'is_hidden': True})

            if del_button:
                form_string += self._load_template('btn_del', {'is_hidden': False})
            else:
                form_string += self._load_template('btn_del', {'is_hidden': True})

        return form_string

    def _render_collapse_button(self):
        pass
