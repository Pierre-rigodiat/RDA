"""
"""
from django.utils.html import escape
from lxml import etree


def render_form(content):
    """

    :param content:
    :return:
    """
    form = etree.Element('div')

    form.set('xmlID', 'root')
    form.set('name', 'xsdForm')

    form_content = etree.fromstring(content)
    form.append(form_content)

    return etree.tostring(form)


def render_form_error(message):
    return "<div>UNSUPPORTED ELEMENT FOUND (" + message + ")</div>"


def render_input(value, placeholder, title):
    """

    :param value:
    :param placeholder:
    :param title:
    :return:
    """
    input_attrs = ''

    if value is not None:
        input_attrs = 'value="' + escape(value) + '" '

    if placeholder != '':
        input_attrs += 'placeholder="' + placeholder + '" '

    if title != '':
        input_attrs += 'title="' + title + '" '

    return ' <input type="text" ' + input_attrs + '/>'


def render_ul(content, element_id, chosen):
    form_string = '<ul'

    if element_id != '':
        form_string += ' id="' + element_id + '" '

    if not chosen:
        form_string += ' class="notchosen"'

    form_string += '>'
    form_string += content
    form_string += '</ul>'

    return form_string


def render_li(content, tag_id, element_tag, use=None, text=None):
    form_string = "<li "

    if use is None:
        li_class = element_tag
    else:
        li_class = element_tag + ' ' + use

    form_string += "class='" + li_class + "' "
    form_string += "id='" + str(tag_id) + "' "

    if text is not None:
        form_string += "tag='" + text + "' "

    form_string += ">"

    form_string += content
    form_string += "</li>"

    return form_string


def render_select(select_id, option_list):
    select = etree.Element('select')

    if select_id is not None:
        select.set('id', select_id)
        select.set('onchange', 'changeChoice(this);')

    for option_item in option_list:
        option = etree.Element('option')
        option.set('value', option_item[0])

        if option_item[2]:
            option.set('selected', 'selected')

        option.text = option_item[1]
        select.append(option)

    return etree.tostring(select)


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
            form_string += "<span id='add" + tag_id + "' class='icon add' "
            form_string += "onclick=\"changeHTMLForm('add'," + tag_id + ");\"></span>"
        else:
            form_string += "<span id='add" + tag_id + "' class='icon add' "
            form_string += "style='display:none;' onclick=\"changeHTMLForm('add'," + tag_id + ");\"></span>"

        if delete_button:
            form_string += "<span id='remove" + tag_id + "' class='icon remove' "
            form_string += "onclick=\"changeHTMLForm('remove'," + tag_id + ");\"></span>"
        else:
            form_string += "<span id='remove" + tag_id + "' class='icon remove' "
            form_string += "style='display:none;' onclick=\"changeHTMLForm('remove'," + tag_id + ");\"></span>"

    return form_string


# TODO merge with render_buttons
# def render_buttons_2(add_button, delete_button, tag_id):
#     """Displays buttons for a duplicable/removable element
#
#     Parameters:
#         add_button: boolean
#         delete_button: boolean
#         tag_id: id of the tag to associate buttons to it
#
#     Returns:
#         JSON data
#     """
#     add_button_type = type(add_button)
#     del_button_type = type(delete_button)
#
#     if add_button_type is not bool:
#         raise TypeError('add_button type is wrong (' + str(add_button_type) + 'received, bool needed')
#
#     if del_button_type is not bool:
#         raise TypeError('add_button type is wrong (' + str(del_button_type) + 'received, bool needed')
#
#     form_string = ""
#     tag_id = str(tag_id)  # Tag ID string conversion
#
#     # the number of occurrences is fixed, don't need buttons
#     # FIXME remove onclick from buttons (use jquery instead)
#     if add_button:
#         form_string += "<span id='add" + tag_id + "' class='icon add' "
#         form_string += "onclick=\"changeHTMLForm('add'," + tag_id + ");\"></span>"
#     else:
#         form_string += "<span id='add" + tag_id + "' class='icon add' "
#         form_string += "style='display:none;' onclick=\"changeHTMLForm('add'," + tag_id + ");\"></span>"
#
#     if delete_button:
#         form_string += "<span id='remove" + tag_id + "' class='icon remove' "
#         form_string += "onclick=\"changeHTMLForm('remove'," + tag_id + ");\"></span>"
#     else:
#         form_string += "<span id='remove" + tag_id + "' class='icon remove' "
#         form_string += "style='display:none;' onclick=\"changeHTMLForm('remove'," + tag_id + ");\"></span>"
#
#     return form_string


def render_collapse_button():
    return "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"
