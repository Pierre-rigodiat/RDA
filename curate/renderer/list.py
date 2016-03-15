"""
"""
from curate.renderer import render_select, render_ul, render_input, render_li, render_buttons, render_collapse_button, \
    DefaultRenderer


class ListRenderer(DefaultRenderer):
    """
    """

    def __init__(self, xsd_data):
        super(ListRenderer, self).__init__(xsd_data, None)

    def _render_data(self, element, partial=False):
        """

        :param element:
        :return:
        """
        html_content = ''

        # if element['tag'] == 'element':
        if element.tag == 'element':
            html_content += self._render_element(element)
        else:
            # print element['tag'] + ' not handled'
            print element.tag + ' not handled (render_data)'

        if not partial:
            return render_ul(html_content, '', True)
        else:
            return html_content

    def _render_element(self, element):
        """

        :param element:
        :return:
        """
        children = {}
        children_number = 0

        # for child in element['children']:
        for child in element.children:
            # if child['tag'] == 'elem-iter':
            if child.tag == 'elem-iter':
                # children += child['children']
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

            if children_number < element.options["min"]:
                add_button = True

        buttons = render_buttons(add_button, del_button, '')

        for child_key in children.keys():
            li_class = ''
            sub_elements = []
            sub_inputs = []

            for child in children[child_key]:
                # if child['tag'] == 'complex_type':
                if child.tag == 'complex_type':
                    sub_elements.append(self._render_complex_type(child))
                    sub_inputs.append(False)
                # elif child['tag'] == 'input':
                elif child.tag == 'input':
                    sub_elements.append(self.render_input(child.value, '', ''))
                    sub_inputs.append(True)
                # elif child['tag'] == 'attribute':
                elif child.tag == 'attribute':
                    sub_elements.append(self._render_attribute(child))
                    sub_inputs.append(False)
                else:
                    # print child['tag'] + ' not handled (re_eleme)'
                    print child.tag + ' not handled (re_eleme)'

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
                        html_content += render_ul(sub_elements[child_index], 'ulid', True)

            # elif children_number == 1 and children[child_key][0].tag == 'input':
            #     html_content = element.options["name"] + sub_elements[0] + buttons
            # else:
            #     header = render_collapse_button() + element.options["name"] + buttons
            #     html_content = ''
            #
            #     for sub_elem in sub_elements:
            #         html_content += header + render_ul(sub_elem, 'ulid', True)

            final_html += render_li(html_content, li_class, child_key)

        return final_html

    def _render_complex_type(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''

        # for child in element['children']:
        #     if child['tag'] == 'sequence':
        #         html_content += self._render_sequence(child)
        #     elif child['tag'] == 'simple_content':
        #         html_content += self._render_simple_content(child)
        #     elif child['tag'] == 'attribute':
        #         html_content += self._render_attribute(child)
        #     else:
        #         print child['tag'] + ' not handled (rend_ct)'

        for child in element.children:
            if child.tag == 'sequence':
                html_content += self._render_sequence(child)
            elif child.tag == 'simple_content':
                html_content += self._render_simple_content(child)
            elif child.tag == 'attribute':
                html_content += self._render_attribute(child)
            else:
                print child.tag + ' not handled (rend_ct)'

        return html_content

    def _render_attribute(self, element):
        """

        :param element:
        :return:
        """
        # html_content = element["options"]["name"]
        # children = []
        #
        # for child in element['children']:
        #     if child['tag'] == 'elem-iter':
        #         children += child['children']
        #     else:
        #         print child['tag'] + 'not handled (rend_attr base)'
        #
        # for child in children:
        #     if child['tag'] == 'simple_type':
        #         html_content += self._render_simple_type(child)
        #     elif child['tag'] == 'input':
        #         html_content += self._render_input(child)
        #     else:
        #         print child['tag'] + ' not handled (rend_attr)'
        html_content = element.options["name"]
        children = []

        for child in element.children:
            if child.tag == 'elem-iter':
                children += child.children
            else:
                print child.tag + 'not handled (rend_attr base)'

        for child in children:
            if child.tag == 'simple_type':
                html_content += self._render_simple_type(child)
            elif child.tag == 'input':
                html_content += self.render_input(child.value, '', '')
            else:
                print child.tag + ' not handled (rend_attr)'

        return render_li(html_content, '', element.pk)

    def _render_sequence(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''
        children = []

        # for child in element['children']:
        #     if child['tag'] == 'element':
        #         html_content += self._render_element(child)
        #     else:
        #         print child['tag'] + '  not handled (rend_seq)'

        for child in element.children:
            if child.tag == 'sequence-iter':
                children += child.children
            else:
                print child.tag + '  not handled (rend_seq_pre)'

        for child in children:
            if child.tag == 'element':
                html_content += self._render_element(child)
            else:
                print child.tag + '  not handled (rend_seq)'

        return html_content

    # def _render_input(self, element):
    #     """
    #
    #     :param element:
    #     :return:
    #     """
    #     # return render_input(element['value'], '', '')
    #     # return render_input(element.value, '', '')
    #     return self.render_input(element.value, '', '')

    def _render_simple_content(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''

        # for child in element['children']:
        #     if child['tag'] == 'element':
        #         html_content += self._render_element(child)
        #     elif child['tag'] == 'extension':
        #         html_content += self._render_extension(child)
        #     else:
        #         print child['tag'] + '  not handled (rend_scont)'

        for child in element.children:
            if child.tag == 'element':
                html_content += self._render_element(child)
            elif child.tag == 'extension':
                html_content += self._render_extension(child)
            else:
                print child.tag + '  not handled (rend_scont)'

        return html_content

    def _render_simple_type(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''

        # for child in element['children']:
        #     # if child['tag'] == 'element':
        #     #     self._render_element(child)
        #     if child['tag'] == 'restriction':
        #         html_content += self._render_restriction(child)
        #     else:
        #         print child['tag'] + '  not handled (rend_stype)'

        for child in element.children:
            if child.tag == 'restriction':
                html_content += self._render_restriction(child)
            else:
                print child.tag + '  not handled (rend_stype)'

        return html_content

    def _render_extension(self, element):
        """

        :param element:
        :return:
        """
        html_content = ''

        # for child in element['children']:
        #     if child['tag'] == 'input':
        #         html_content += self._render_input(child)
        #     elif child['tag'] == 'attribute':
        #         html_content += self._render_attribute(child)
        #     else:
        #         print child['tag'] + ' not handled (rend_ext)'

        for child in element.children:
            if child.tag == 'input':
                html_content += self.render_input(child.value, '', '')
            elif child.tag == 'attribute':
                html_content += self._render_attribute(child)
            else:
                print child.tag + ' not handled (rend_ext)'

        return html_content

    def _render_restriction(self, element):
        """

        :param element:
        :return:
        """
        options = []
        subhtml = ''

        # for child in element['children']:
        #     if child['tag'] == 'enumeration':
        #         options.append((child['value'], child['value'], False))
        #     elif child['tag'] == 'input':
        #         subhtml += self._render_input(child)
        #     else:
        #         print child['tag'] + ' not handled (rend_ext)'

        for child in element.children:
            if child.tag == 'enumeration':
                options.append((child.value, child.value, False))
            elif child.tag == 'input':
                subhtml += self.render_input(child.value, '', '')
            else:
                print child.tag + ' not handled (rend_ext)'

        if subhtml == '' or len(options) != 0:
            return render_select('restr', options)
        else:
            return subhtml

    def render(self, partial=False):
        """

        :return:
        """
        return self._render_data(self.data, partial)





