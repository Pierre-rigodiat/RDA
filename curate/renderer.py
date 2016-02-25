"""
"""
from django.http.request import HttpRequest
from django.template.context import RequestContext
from django.template import loader
from os.path import join


def load_template(template_path, template_data=None):
    context = RequestContext(HttpRequest())

    if template_data is not None:
        context.update(template_data)

    template_path = join('renderer', 'default', template_path)

    template = loader.get_template(template_path)
    return template.render(context)


def render_form(content):
    """

    :param content:
    :return:
    """
    data = {
        'content': content
    }

    return load_template('form.html', data)


def render_form_error(message):
    """

    :param message:
    :return:
    """
    return load_template('form-error.html', {'message': message})


def render_input(value, placeholder, title):
    """

    :param value:
    :param placeholder:
    :param title:
    :return:
    """
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
    data = {
        'content': content,
        'element_id': element_id,
        'chosen': chosen
    }

    return load_template('ul.html', data)


def render_li(content, tag_id, element_tag, use=None, text=None):
    """

    :param content:
    :param tag_id:
    :param element_tag:
    :param use:
    :param text:
    :return:
    """
    if use is None:
        li_class = element_tag
    else:
        li_class = element_tag + ' ' + use

    data = {
        'li_class': li_class,
        'tag_id': str(tag_id),
        'text': text,
        'content': content
    }

    return load_template('li.html', data)


def render_select(select_id, option_list):
    """

    :param select_id:
    :param option_list:
    :return:
    """
    data = {
        'select_id': select_id,
        'option_list': option_list
    }

    return load_template('inputs/select.html', data)


def render_buttons(add_button, delete_button, tag_id):
    """Displays buttons for a duplicable/removable element

    Parameters:
        add_button: boolean
        delete_button: boolean
        tag_id: id of the tag to associate buttons to it

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
    tag_id = str(tag_id)  # Tag ID string conversion

    # the number of occurrences is fixed, don't need buttons
    if not add_button and not delete_button:
        pass
    else:
        # FIXME remove onclick from buttons (use jquery instead)
        if add_button:
            form_string += load_template('buttons/add.html', {'tag_id': tag_id, 'is_hidden': False})
        else:
            form_string += load_template('buttons/add.html', {'tag_id': tag_id, 'is_hidden': True})

        if delete_button:
            form_string += load_template('buttons/delete.html', {'tag_id': tag_id, 'is_hidden': False})
        else:
            form_string += load_template('buttons/delete.html', {'tag_id': tag_id, 'is_hidden': True})

    return form_string


def render_collapse_button():
    """

    :return:
    """
    return load_template('buttons/collapse.html')
