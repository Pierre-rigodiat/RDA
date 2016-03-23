"""
"""
from types import *
from django.template import loader

from os.path import join

from curate.renderer import render_select, render_li, render_buttons, render_collapse_button, \
    DefaultRenderer


class AbstractListRenderer(DefaultRenderer):

    def __init__(self, xsd_data):
        list_renderer_path = join('renderer', 'list')

        templates = {
            'ul': loader.get_template(join(list_renderer_path, 'ul.html'))
        }

        super(AbstractListRenderer, self).__init__(xsd_data, templates)

    def _render_ul(self, content, element_id, chosen):
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

        return self._load_template('ul', data)

    def _render_li(self):
        pass


class ListRenderer(AbstractListRenderer):
    """
    """

    def __init__(self, xsd_data):
        super(ListRenderer, self).__init__(xsd_data)

    def render(self, partial=False):
        """

        Parameters:
            partial:

        :return:
        """
        html_content = ''

        if self.data.tag == 'element':
            html_content += self.render_element(self.data)
        else:
            print self.data.tag + ' not handled (render_data)'

        if not partial:
            return self._render_ul(html_content, '', True)
        else:
            return html_content

    def render_element(self, element):
        """

        :param element:
        :return:
        """
        children = {}
        children_number = 0

        for child in element.children:
            if child.tag == 'elem-iter':
                children[child.pk] = child.children

                if len(child.children) > 0:
                    children_number += 1
            else:
                print '>> ' + child.tag + ' forwarded (re_elem pre)'
                print '>> ' + str(child) + ' forwarded (re_elem pre)'

        final_html = ''

        # Buttons generation (render once, reused many times)
        add_button = False
        del_button = False

        if 'max' in element.options:
            if children_number < element.options["max"] or element.options["max"] == -1:
                add_button = True

        if 'min' in element.options:
            if children_number > element.options["min"]:
                del_button = True

            # if children_number < element.options["min"]:
            #     add_button = True

        buttons = render_buttons(add_button, del_button)

        for child_key in children.keys():
            li_class = ''
            sub_elements = []
            sub_inputs = []

            for child in children[child_key]:
                if child.tag == 'complex_type':
                    sub_elements.append(self.render_complex_type(child))
                    sub_inputs.append(False)
                elif child.tag == 'input':
                    sub_elements.append(self._render_input(child.value, '', ''))
                    sub_inputs.append(True)
                elif child.tag == 'simple_type':
                    sub_elements.append(self.render_simple_type(child))
                    sub_inputs.append(False)
                else:
                    print child.tag + ' not handled (re_elem)'

            if children_number == 0:
                html_content = element.options["name"] + buttons
                li_class = 'removed'
            else:
                html_content = ''
                for child_index in xrange(len(sub_elements)):
                    if sub_inputs[child_index]:
                        html_content += element.options["name"] + sub_elements[child_index] + buttons
                    else:
                        html_content += render_collapse_button() + element.options["name"] + buttons
                        html_content += self._render_ul(sub_elements[child_index], 'ulid', True)

            final_html += render_li(html_content, li_class, child_key)

        return final_html

    def render_complex_type(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''

        for child in element.children:
            if child.tag == 'sequence':
                html_content += self.render_sequence(child)
            elif child.tag == 'simple_content':
                html_content += self.render_simple_content(child)
            elif child.tag == 'attribute':
                html_content += self.render_attribute(child)
            else:
                print child.tag + ' not handled (rend_ct)'

        return html_content

    def render_attribute(self, element):
        """

        :param element:
        :return:
        """
        html_content = element.options["name"]
        children = []

        for child in element.children:
            if child.tag == 'elem-iter':
                children += child.children
            else:
                print child.tag + 'not handled (rend_attr base)'

        for child in children:
            if child.tag == 'simple_type':
                html_content += self.render_simple_type(child)
            elif child.tag == 'input':
                html_content += self._render_input(child.value, '', '')
            else:
                print child.tag + ' not handled (rend_attr)'

        return render_li(html_content, '', element.pk)

    def render_sequence(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''
        children = []

        for child in element.children:
            if child.tag == 'sequence-iter':
                children += child.children
            else:
                print child.tag + '  not handled (rend_seq_pre)'

        for child in children:
            if child.tag == 'element':
                html_content += self.render_element(child)
            else:
                print child.tag + '  not handled (rend_seq)'

        return html_content

    def render_simple_content(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''

        for child in element.children:
            if child.tag == 'extension':
                html_content += self.render_extension(child)
            else:
                print child.tag + '  not handled (rend_scont)'

        return html_content

    def render_simple_type(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''

        for child in element.children:
            if child.tag == 'restriction':
                html_content += self.render_restriction(child)
            elif child.tag == 'attribute':
                html_content += self.render_attribute(child)
            else:
                print child.tag + '  not handled (rend_stype)'

        return html_content

    def render_extension(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''

        for child in element.children:
            if child.tag == 'input':
                html_content += self._render_input(child.value, '', '')
            elif child.tag == 'attribute':
                html_content += self.render_attribute(child)
            elif child.tag == 'simple_type':
                html_content += self.render_simple_type(child)
            else:
                print child.tag + ' not handled (rend_ext)'

        return html_content

    def render_restriction(self, element):
        """

        :param element:
        :return:
        """
        options = []
        subhtml = ''

        for child in element.children:
            if child.tag == 'enumeration':
                options.append((child.value, child.value, False))
            elif child.tag == 'input':
                subhtml += self._render_input(child.value, '', '')
            else:
                print child.tag + ' not handled (rend_ext)'

        if subhtml == '' or len(options) != 0:
            return render_select('restr', options)
        else:
            return subhtml

