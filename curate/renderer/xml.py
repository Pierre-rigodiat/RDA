"""
"""
from django.template import loader
from os.path import join
from curate.renderer import render_select, render_li, render_collapse_button, DefaultRenderer
from curate.models import SchemaElement
from bson.objectid import ObjectId


class AbstractXmlRenderer(DefaultRenderer):

    def __init__(self, xsd_data):
        xml_renderer_path = join('renderer', 'xml')

        templates = {
            'xml': loader.get_template(join(xml_renderer_path, 'element.html'))
        }

        super(AbstractXmlRenderer, self).__init__(xsd_data, templates)

    def _render_xml(self, name, attributes, content):
        data = {
            'name': name,
            'attributes': attributes,
            'content': content
        }

        return self._load_template('xml', data)


class XmlRenderer(AbstractXmlRenderer):
    """
    """

    def __init__(self, xsd_data):
        super(XmlRenderer, self).__init__(xsd_data)

    def render(self, partial=False):
        """

        Parameters:
            partial:

        :return:
        """
        return self.render_element(self.data)

    def render_element(self, element):
        """

        :param element:
        :return:
        """
        xml_string = ''
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

        element_name = element.options['name']

        for child_key in children.keys():
            for child in children[child_key]:
                content = ['', '']

                if child.tag == 'complex_type':
                    content = self.render_complex_type(child)
                elif child.tag == 'input':
                    content[1] = child.value if child.value is not None else ''
                elif child.tag == 'simple_type':
                    content = self.render_simple_type(child)
                else:
                    print child.tag + ' not handled (re_elem)'

                # namespaces
                if 'xmlns' in element.options and element.options['xmlns'] is not None:
                    xmlns = ' xmlns="{}"'.format(element.options['xmlns'])
                    content[0] += xmlns

                xml_string += self._render_xml(element_name, content[0], content[1])

        return xml_string

    def render_attribute(self, element):
        """

        :param element:
        :return:
        """
        attr_key = element.options["name"]
        attr_list = []
        children = []

        for child in element.children:
            if child.tag == 'elem-iter':
                children += child.children
            else:
                print child.tag + 'not handled (rend_attr base)'

        for child in children:
            attr_value = ''

            if child.tag == 'simple_type':
                content = self.render_simple_type(child)
                attr_value = content[1]
            elif child.tag == 'input':
                attr_value = child.value if child.value is not None else ''
            else:
                print child.tag + ' not handled (rend_attr)'

            # if attr_value == '':
            #     attr_list.append(attr_key)
            # else:
            #     attr_list.append(attr_key + '="' + attr_value + '"')

            # namespaces
            if 'xmlns' in element.options and element.options['xmlns'] is not None:
                # check that element isn't declaring the same namespace xmlns=""
                parent = SchemaElement.objects().get(children__contains=ObjectId(element.id))
                while parent.tag != 'element':
                    parent = SchemaElement.objects().get(children__contains=ObjectId(parent.id))
                if 'xmlns' in parent.options and parent.options['xmlns'] is not None and \
                                parent.options['xmlns'] == element.options['xmlns']:
                        xmlns = ''
                else:  # parent element is in a different namespace
                    if element.options['xmlns'] != '':
                        ns_prefix = element.options['ns_prefix'] if element.options['ns_prefix'] is not None else 'ns0'
                        if ns_prefix != '':
                            xmlns = ' xmlns{0}="{1}"'.format(':' + ns_prefix, element.options['xmlns'])
                            attr_key = "{0}:{1}".format(ns_prefix, attr_key)
                        else:
                            xmlns = ' xmlns="{0}"'.format(element.options['xmlns'])
                    else:
                        xmlns = ''

                attr_list.append("{0} {1}='{2}'".format(xmlns, attr_key, attr_value))
                # TODO: check that element isn't declaring the same namespace xmlns=""
                # TODO: check that sibling attributes are not declaring the same namespaces
            else:
                attr_list.append(attr_key + '="' + attr_value + '"')

        return ' '.join(attr_list)

    def render_complex_type(self, element):
        """

        :param element:
        :return:
        """
        content = ['', '']

        for child in element.children:
            tmp_content = ['', '']

            if child.tag == 'sequence':
                tmp_content = self.render_sequence(child)
            elif child.tag == 'simple_content':
                tmp_content = self.render_simple_content(child)
            elif child.tag == 'attribute':
                tmp_content[0] = self.render_attribute(child)
            else:
                print child.tag + ' not handled (rend_ct)'

            content[0] = ' '.join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]

        return content

    def render_sequence(self, element):
        """

        :param element:
        :return:
        """
        content = ['', '']
        children = []

        for child in element.children:
            if child.tag == 'sequence-iter':
                children += child.children
            else:
                print child.tag + '  not handled (rend_seq_pre)'

        for child in children:
            if child.tag == 'element':
                content[1] += self.render_element(child)
            else:
                print child.tag + '  not handled (rend_seq)'

        return content

    def render_simple_content(self, element):
        """

        :param element:
        :return:
        """
        content = ['', '']

        for child in element.children:
            tmp_content = ['', '']

            if child.tag == 'extension':
                tmp_content = self.render_extension(child)
            else:
                print child.tag + '  not handled (rend_scont)'

            content[0] = ' '.join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]

        return content

    def render_simple_type(self, element):
        """

        :param element:
        :return:
        """
        content = ['', '']

        for child in element.children:
            tmp_content = ['', '']

            if child.tag == 'restriction':
                tmp_content = self.render_restriction(child)
            elif child.tag == 'attribute':
                tmp_content[0] = self.render_attribute(child)
            else:
                print child.tag + '  not handled (rend_stype)'

            content[0] = ' '.join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]

        return content

    def render_restriction(self, element):
        content = ['', '']
        value = element.value

        for child in element.children:
            tmp_content = ['', '']

            if child.tag == 'enumeration':
                tmp_content[1] = value if value is not None else ''
                value = None  # Avoid to copy the value several times
            elif child.tag == 'input':
                tmp_content[1] = child.value if child.value is not None else ''
            elif child.tag == 'simple_type':
                tmp_content = self.render_simple_type()
            else:
                print child.tag + '  not handled (rend_restriction)'

            content[0] = ' '.join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]

        return content

    def render_extension(self, element):
        """

        :param element:
        :return:
        """
        content = ['', '']

        for child in element.children:
            tmp_content = ['', '']

            if child.tag == 'input':
                tmp_content[1] = child.value if child.value is not None else ''
            elif child.tag == 'attribute':
                tmp_content[0] = self.render_attribute(child)
            elif child.tag == 'simple_type':
                tmp_content = self.render_simple_type(child)
            else:
                print child.tag + ' not handled (rend_ext)'

            content[0] = ' '.join([content[0], tmp_content[0]]).strip()
            content[1] += tmp_content[1]

        return content
