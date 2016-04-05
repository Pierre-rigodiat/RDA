"""
"""
from curate.renderer import render_select, render_input, render_buttons, load_template, DefaultRenderer


def render_table(content):
    data = {
        'content': content
    }

    return load_template('table.html', data, 'table')


def render_tr(name, content):
    data = {
        'name': name,
        'content': content
    }

    return load_template('tr.html', data, 'table')


def render_top(title, content):
    data = {
        'title': title,
        'content': content
    }

    return load_template('wrap.html', data, 'table')


class TableRenderer(DefaultRenderer):
    """
    """
    # FIXME create the class AbstractTableRenderer to store additional list

    def __init__(self, xsd_data):
        super(self, TableRenderer).__init__(xsd_data, {})

    def _render_data(self, element):
        html_content = ''

        if element['tag'] == 'element':
            html_content += self._render_element(element, no_name=True)
        else:
            message = 'render_data: ' + element.tag + ' not handled'
            self.warnings.append(message)

        # return render_ul(html_content, '', True)
        return render_top(element['options']['name'], html_content)

    def _render_element(self, element, no_name=False):
        print "elem"
        children = []
        # html_content = element["options"]["name"]
        html_content = ''

        for child in element['children']:
            if child['tag'] == 'elem-iter':
                children += child['children']
            else:
                message = 'render_element (iteration): ' + child.tag + ' not handled'
                self.warnings.append(message)

        add_button = False
        del_button = False

        # if 'max' in element["options"] and element["options"]['max'] != 1:
        if 'max' in element["options"]:
            # if len(element['children']) < element["options"]["max"] or element["options"]["max"] == -1:
            if len(children) < element["options"]["max"] or element["options"]["max"] == -1:
                add_button = True

        # if 'min' in element["options"] and element["options"]['min'] != 1:
        if 'min' in element["options"]:
            # if len(element['children']) > element["options"]["min"]:
            if len(children) > element["options"]["min"]:
                del_button = True

            if len(children) < element["options"]["min"]:
                add_button = True

        buttons = render_buttons(add_button, del_button, '')

        subhtml = ''

        for child in children:
            if child['tag'] == 'complex_type':
                subhtml += self._render_complex_type(child)
            elif child['tag'] == 'input':
                subhtml += self._render_input(child)
            elif child['tag'] == 'attribute':
                subhtml += self._render_attribute(child)
            else:
                print child['tag'] + ' not handled (re_eleme)'

        if len(children) > 1 or (len(children) == 1 and children[0]['tag'] != 'input'):
            # html_content = render_collapse_button() + html_content + buttons
            # html_content = html_content + buttons
            # html_content += render_ul(subhtml, 'ulid', True)
            html_content += render_table(subhtml)
        else:
            # html_content += subhtml + buttons
            html_content += subhtml

        # return render_li(html_content, '', '', None, element["options"]["name"])
        if no_name:
            return html_content

        return render_tr(element["options"]["name"] + buttons, html_content)

    def _render_complex_type(self, element):
        print "ct"
        html_content = ''

        for child in element['children']:
            if child['tag'] == 'sequence':
                html_content += self._render_sequence(child)
            elif child['tag'] == 'simple_content':
                html_content += self._render_simple_content(child)
            elif child['tag'] == 'attribute':
                html_content += self._render_attribute(child)
            else:
                print child['tag'] + ' not handled (rend_ct)'

        return html_content

    def _render_attribute(self, element):
        print "attr"
        # html_content = element["options"]["name"]
        html_content = ''
        children = []

        for child in element['children']:
            if child['tag'] == 'elem-iter':
                children += child['children']
            else:
                print child['tag'] + 'not handled (rend_attr base)'

        for child in children:
            if child['tag'] == 'simple_type':
                html_content += self._render_simple_type(child)
            elif child['tag'] == 'input':
                html_content += self._render_input(child)
            else:
                print child['tag'] + ' not handled (rend_attr)'
            # print child['tag'] + ' not handled (rend_attr)'

        # return render_li(html_content, '', '')
        return render_tr(element['options']['name'], html_content)

    def _render_sequence(self, element):
        print "seq"
        html_content = ''

        for child in element['children']:
            if child['tag'] == 'element':
                html_content += self._render_element(child)
            else:
                print child['tag'] + '  not handled (rend_seq)'

        return html_content

    @staticmethod
    def _render_input(element):
        print "inp"
        return render_input(element['value'], '', '')

    def _render_simple_content(self, element):
        print "sc"
        html_content = ''

        for child in element['children']:
            if child['tag'] == 'element':
                html_content += self._render_element(child)
            elif child['tag'] == 'extension':
                html_content += self._render_extension(child)
            else:
                print child['tag'] + '  not handled (rend_scont)'

        return html_content

    def _render_simple_type(self, element):
        print "st"
        html_content = ''

        for child in element['children']:
            # if child['tag'] == 'element':
            #     self._render_element(child)
            if child['tag'] == 'restriction':
                html_content += self._render_restriction(child)
            else:
                print child['tag'] + '  not handled (rend_stype)'

        return html_content

    def _render_extension(self, element):
        print "ext"
        html_content = ''

        for child in element['children']:
            if child['tag'] == 'input':
                html_content += self._render_input(child)
            elif child['tag'] == 'attribute':
                html_content += self._render_attribute(child)
            else:
                print child['tag'] + ' not handled (rend_ext)'
            # print child['tag'] + '  not handled (rend_ext)'

        return html_content

    def _render_restriction(self, element):
        print "rest"
        options = []
        subhtml = ''

        for child in element['children']:
            if child['tag'] == 'enumeration':
                options.append((child['value'], child['value'], False))
            elif child['tag'] == 'input':
                subhtml += self._render_input(child)
            else:
                print child['tag'] + ' not handled (rend_ext)'

        if subhtml == '' or len(options) != 0:
            return render_select('restr', options)
        else:
            return subhtml

    def render(self):
        # print "================="
        #
        # try:
        #     s = self._render_data(self.data)
        # except Exception as exc:
        #     print "***********"
        #     print ">> " + str(exc)
        #     return exc.message
        #
        # print "================="
        # print s
        #
        # return s
        return self._render_data(self.data)










