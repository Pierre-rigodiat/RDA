"""
"""
from os.path import join
from curate.renderer import render_buttons, render_collapse_button, render_form, render_form_error, \
    render_input, render_li, render_ul, \
    render_select
from mgi.models import FormElement, XMLElement, FormData, Module
from mgi.settings import CURATE_MIN_TREE, CURATE_COLLAPSE
from bson.objectid import ObjectId
from mgi import common
from lxml import etree
from modules import get_module_view


##################################################
# Part I: Utilities
##################################################

def get_subnodes_xpath(element, xml_tree, namespace):
    """Perform a lookup in subelements to build xpath

    Parameters:
        element: XML element
        xml_tree: xml_tree
        namespace: namespace
    """
    # FIXME References returns the same object several times
    # TODO Check if min and maxOccurs are correctly reported (declared in ref but not reported elsewhere)
    xpaths = []

    if len(list(element)) > 0:
        for child in list(element):
            if child.tag == "{0}element".format(namespace):
                if 'name' in child.attrib:
                    xpaths.append({'name': child.attrib['name'], 'element': child})
                elif 'ref' in child.attrib:
                    ref = child.attrib['ref']

                    if ':' in ref:
                        ref_split = ref.split(":")
                        ref_name = ref_split[1]
                        ref_element = xml_tree.find("./{0}element[@name='{1}']".format(namespace, ref_name))
                    else:
                        ref_element = xml_tree.find("./{0}element[@name='{1}']".format(namespace, ref))

                    if ref_element is not None:
                        xpaths.append({'name': ref_element.attrib.get('name'), 'element': ref_element})
            else:
                xpaths.extend(get_subnodes_xpath(child, xml_tree, namespace))
    return xpaths


def get_nodes_xpath(elements, xml_tree, namespace):
    """Perform a lookup in subelements to build xpath.

    Get nodes' xpath, only one level deep. It's not going to every leaves. Only need to know if the
    node is here.

    Parameters:
        elements: XML element
        xml_tree: xml_tree
        namespace: namespace
    """
    # FIXME Making one function with get_subnode_xpath should be possible, both are doing the same job
 # FIXME same problems as in get_subnodes_xpath
    xpaths = []

    for element in elements:
        if element.tag == "{0}element".format(namespace):
            if 'name' in element.attrib:
                xpaths.append({'name': element.attrib['name'], 'element': element})
            elif 'ref' in element.attrib:
                ref = element.attrib['ref']

                if ':' in ref:
                    ref_split = ref.split(":")
                    ref_name = ref_split[1]
                    ref_element = xml_tree.find("./{0}element[@name='{1}']".format(namespace, ref_name))
                else:
                    ref_element = xml_tree.find("./{0}element[@name='{1}']".format(namespace, ref))

                if ref_element is not None:
                    xpaths.append({'name': ref_element.attrib.get('name'), 'element': ref_element})
        else:
            xpaths.extend(get_subnodes_xpath(element, xml_tree, namespace))
    return xpaths


def lookup_occurs(element, xml_tree, namespace, full_path, edit_data_tree):
    """Do a lookup in data to get the number of occurences of a sequence or choice without a name (not within a named
    complextype).

    get the number of times the sequence appears in the XML document that we are loading for editing
    algorithm:
    get all the possible nodes that can appear in the sequence
    for each node, count how many times it's found in the data
    the maximum count is the number of occurrences of the sequence
    only works if data are determinist enough: means we don't have an element outside the sequence, and the same in
    the sequence

    Parameters:
        element: XML element
        xml_tree: xml_tree
        namespace: namespace
        full_path: current node XPath
        edit_data_tree: XML data
    """
    # FIXME this function is not returning the correct output
    xpaths = get_nodes_xpath(element, xml_tree, namespace)
    max_occurs_found = 0

    for xpath in xpaths:
        edit_elements = edit_data_tree.xpath(full_path + '/' + xpath['name'])

        if len(edit_elements) > max_occurs_found:
            max_occurs_found = 1

            if 'maxOccurs' in xpath['element'].attrib:
                if xpath['element'].attrib != "unbounded":
                    if xpath['element'].attrib < len(edit_elements):
                        # FIXME this part of code is not reachable (hence commented)
                        # maxOccursFound = len(edit_elements)

                        exc_mess = "These data can't be loaded for now, because of the following element: "
                        exc_mess += join(full_path, xpath['name'])  # XPath of the current element

                        raise Exception(exc_mess)

    return max_occurs_found


def manage_occurences(element):
    """Store information about the occurrences of the element

    Parameters:
        element: xsd element

    Returns:
        JSON data
    """
    min_occurs = 1
    max_occurs = 1

    if 'minOccurs' in element.attrib:
        min_occurs = float(element.attrib['minOccurs'])

    if 'maxOccurs' in element.attrib:
        if element.attrib['maxOccurs'] == "unbounded":
            max_occurs = float('inf')
        else:
            max_occurs = float(element.attrib['maxOccurs'])

    return min_occurs, max_occurs


def manage_attr_occurrences(element):
    """Store information about the occurrences of an attribute

    Parameters:
        element: XSD element

    Returns:
        JSON data
    """
    # FIXME attribute use defaults to optional not required

    min_occurs = 1
    max_occurs = 1

    if 'use' in element.attrib:
        if element.attrib['use'] == "optional":
            min_occurs = 0
        elif element.attrib['use'] == "prohibited":
            min_occurs = 0
            max_occurs = 0
        elif element.attrib['use'] == "required":
            pass

    return min_occurs, max_occurs


def has_module(request, element):
    """Look for a module in XML element's attributes

    Parameters:
        request: HTTP request
        element: XML element

    Returns:
        True: the element has a module attribute
        False: the element doesn't have a module attribute
    """
    # FIXME remove request (unused)
    _has_module = False

    # check if a module is set for this element
    if '{http://mdcs.ns}_mod_mdcs_' in element.attrib:
        # get the url of the module
        url = element.attrib['{http://mdcs.ns}_mod_mdcs_']

        # check that the url is registered in the system
        if url in Module.objects.all().values_list('url'):
            _has_module = True

    return _has_module


def get_xml_element_data(xsd_element, xml_element, namespace):
    """Return the content of an xml element

    Parameters:
        xsd_element:
        xml_element:
        namespace:

    Returns:
    """
    reload_data = None

    # get data
    if xsd_element.tag == "{0}element".format(namespace):
        # leaf: get the value
        if len(list(xml_element)) == 0:
            if xml_element.text is not None:
                reload_data = xml_element.text
            else:  # if xml_element.text is None
                reload_data = ''
        else:  # branch: get the whole branch
            reload_data = etree.tostring(xml_element)
    elif xsd_element.tag == "{0}attribute".format(namespace):
        pass
    elif xsd_element.tag == "{0}complexType".format(namespace) or xsd_element.tag == "{0}simpleType".format(namespace):
        # leaf: get the value
        if len(list(xml_element)) == 0:
            if xml_element.text is not None:
                reload_data = xml_element.text
            else:  # if xml_element.text is None
                reload_data = ''
        else:  # branch: get the whole branch
            try:
                reload_data = etree.tostring(xml_element)
            except:
                # FIXME in which case would we need that?
                reload_data = str(xml_element)

    return reload_data


def get_element_type(element, xml_tree, namespace, default_prefix):
    """get XSD type to render.

    Parameters:
        element: XML element
        xml_tree: XML tree of the template
        namespace: Namespace used in the template
        default_prefix:

    Returns:       JSON data
                    Returns the type if found
                        - complexType
                        - simpleType
                    Returns None otherwise:
                        - type from default namespace (xsd:...)
                        - no type
    """
    try:
        if 'type' not in element.attrib:  # element with type declared below it
            # if tag not closed:  <element/>
            if len(list(element)) == 1:
                if element[0].tag == "{0}annotation".format(namespace):
                    return None
                else:
                    return element[0]
            # with annotations
            elif len(list(element)) == 2:
                # FIXME Not all possibilities are tested in this case
                return element[1]
            else:
                return None
        else:  # element with type attribute
            if element.attrib.get('type') in common.getXSDTypes(default_prefix):
                return None
            elif element.attrib.get('type') is not None:  # FIXME is it possible?
                # TODO: manage namespaces
                # type of the element is complex
                type_name = element.attrib.get('type')
                if ':' in type_name:
                    type_name = type_name.split(":")[1]

                xpath = "./{0}complexType[@name='{1}']".format(namespace, type_name)
                element_type = xml_tree.find(xpath)
                if element_type is None:
                    # type of the element is simple
                    xpath = "./{0}simpleType[@name='{1}']".format(namespace, type_name)
                    element_type = xml_tree.find(xpath)
                return element_type
    except:
        print "get_element_type: Something went wrong"
        return None
    return None


def remove_annotations(element, namespace):
    """Remove annotations of an element if present

    Parameters:
        element: XML element
        namespace: namespace
    """
    # FIXME annotation is not always the first child

    if len(list(element)) != 0:  # If element has children
        if element[0].tag == "{0}annotation".format(namespace):  # If first child is annotation
            element.remove(element[0])


##################################################
# Part II: Schema parsing
##################################################

def generate_form(request):
    """Renders HTMl form for display.

    Parameters:
        request: HTTP request

    Returns:
        rendered HTMl form
    """
    default_prefix = request.session['defaultPrefix']

    xml_doc_tree_str = request.session['xmlDocTree']
    xml_doc_tree = etree.fromstring(xml_doc_tree_str)

    request.session['nbChoicesID'] = '0'
    request.session['nb_html_tags'] = '0'

    if 'mapTagID' in request.session:
        del request.session['mapTagID']
    request.session['mapTagID'] = {}

    form_string = ""

    # get form data from the database (empty one or existing one)
    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(pk=ObjectId(form_data_id))

    # if editing, get the XML data to fill the form
    edit_data_tree = None
    if request.session['curate_edit']:
        # build the tree from data
        # transform unicode to str to support XML declaration
        if form_data.xml_data is not None:
            # Load a parser able to clean the XML from blanks, comments and processing instructions
            clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
            # set the parser
            etree.set_default_parser(parser=clean_parser)
            # load the XML tree from the text
            edit_data_tree = etree.XML(str(form_data.xml_data.encode('utf-8')))
        else:  # no data found, not editing
            request.session['curate_edit'] = False

    # get the namespace for the default prefix
    namespace = request.session['namespaces'][default_prefix]

    # find all root elements
    elements = xml_doc_tree.findall("./{0}element".format(namespace))

    try:
        # one root
        if len(elements) == 1:
            form_string += generate_element(request, elements[0], xml_doc_tree, namespace,
                                            edit_data_tree=edit_data_tree)
        # multiple roots
        elif len(elements) > 1:
            form_string += generate_choice(request, elements, xml_doc_tree, namespace, edit_data_tree=edit_data_tree)
        else:  # No root element detected
            raise Exception("No root element detected")

        form_string = render_form(form_string)
    except Exception as e:
        form_string = render_form_error(e.message)

    # save the list of elements for the form
    form_data.elements = request.session['mapTagID']
    # save data for the current form
    form_data.save()

    # delete temporary data structure for forms elements
    del request.session['mapTagID']

    # data are loaded, switch Edit to False, we don't need to look at the original data anymore
    request.session['curate_edit'] = False

    return form_string


def generate_element(request, element, xml_tree, namespace, choice_info=None, full_path="", edit_data_tree=None):
    """Generate an HTML string that represents an XML element.

    Parameters:
        request: HTTP request
        element: XML element
        xml_tree: XML tree of the template
        namespace: Namespace used in the template
        choice_info:
        full_path:
        edit_data_tree:

    Returns:
        JSON data
    """
    # FIXME if elif without else need to be corrected
    # FIXME Support for unique is not present
    # FIXME Support for key / keyref
    default_prefix = request.session['defaultPrefix']
    form_string = ""

    # get appinfo elements
    app_info = common.getAppInfo(element, namespace)

    # check if the element has a module
    _has_module = has_module(request, element)

    # FIXME see if we can avoid these basic initialization
    # FIXME this is not necessarly true
    min_occurs = 1
    max_occurs = 1

    text_capitalized = ''
    element_tag = ''
    edit_elements = []
    ##############################################

    # check if XML element or attribute
    if element.tag == "{0}element".format(namespace):
        min_occurs, max_occurs = manage_occurences(element)
        element_tag = 'element'
    elif element.tag == "{0}attribute".format(namespace):
        min_occurs, max_occurs = manage_attr_occurrences(element)
        element_tag = 'attribute'

    # get the name of the element, go find the reference if there's one
    if 'ref' in element.attrib:  # type is a reference included in the document
        ref = element.attrib['ref']

        if ':' in ref:
            ref_split = ref.split(":")
            ref_name = ref_split[1]
            # TODO: manage namespaces/targetNamespaces, composed schema with different target namespaces
            # element = xml_tree.findall("./{0}element[@name='"+refName+"']".format(refNamespace))
            ref_element = xml_tree.find("./{0}element[@name='{1}']".format(namespace, ref_name))
        else:
            ref_element = xml_tree.find("./{0}element[@name='{1}']".format(namespace, ref))

        if ref_element is not None:
            text_capitalized = ref_element.attrib.get('name')
            element = ref_element
            # check if the element has a module
            _has_module = has_module(request, element)
    else:
        text_capitalized = element.attrib.get('name')

    if element_tag == 'element':
        # XML xpath:/root/element
        full_path += "/" + text_capitalized
    elif element_tag == 'attribute':
        full_path += "/@" + text_capitalized

    # XSD xpath: /element/complexType/sequence
    xsd_xpath = etree.ElementTree(xml_tree).getpath(element)

    # init variables for buttons management
    add_button = False
    delete_button = False
    nb_occurrences = 1  # nb of occurrences to render (can't be 0 or the user won't see this element at all)
    nb_occurrences_data = min_occurs  # nb of occurrences in loaded data or in form being rendered (can be 0)
    # xml_element = None
    use = ""
    removed = False

    # loading data in the form
    if request.session['curate_edit']:
        # get the number of occurrences in the data
        edit_elements = edit_data_tree.xpath(full_path)
        nb_occurrences_data = len(edit_elements)

        if nb_occurrences_data == 0:
            use = "removed"
            removed = True

        # manage buttons
        if nb_occurrences_data < max_occurs:
            add_button = True
        if nb_occurrences_data > min_occurs:
            delete_button = True

    else:  # starting an empty form
        # Don't generate the element if not necessary
        if CURATE_MIN_TREE and min_occurs == 0:
            use = "removed"
            removed = True

        if nb_occurrences_data < max_occurs:
            add_button = True
        if nb_occurrences_data > min_occurs:
            delete_button = True

    if _has_module:
        # block maxOccurs to one, the module should take care of occurrences when the element is replaced
        nb_occurrences = 1
        max_occurs = 1
    elif nb_occurrences_data > nb_occurrences:
        nb_occurrences = nb_occurrences_data

    xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nb_occurrences_data, minOccurs=min_occurs,
                             maxOccurs=max_occurs)
    xml_element.save()

    # management of elements inside a choice (don't display if not part of the currently selected choice)
    if choice_info:
        choice_id = choice_info.chooseIDStr + "-" + str(choice_info.counter)
        chosen = True

        if request.session['curate_edit']:
            if len(edit_elements) == 0:
                chosen = False

                if CURATE_MIN_TREE:
                    form_element = FormElement(html_id=choice_id, xml_element=xml_element, xml_xpath=full_path).save()

                    request.session['mapTagID'][choice_id] = str(form_element.id)

                    form_string += render_ul('', choice_id, chosen)
                    return form_string
        else:
            if choice_info.counter > 0:
                chosen = False

                if CURATE_MIN_TREE:
                    form_element = FormElement(html_id=choice_id, xml_element=xml_element, xml_xpath=full_path).save()

                    request.session['mapTagID'][choice_id] = str(form_element.id)

                    form_string += render_ul('', choice_id, chosen)
                    return form_string
    else:
        chosen = True
        choice_id = ''

    element_type = get_element_type(element, xml_tree, namespace, default_prefix)
    ul_content = ''

    for x in range(0, int(nb_occurrences)):
        nb_html_tags = int(request.session['nb_html_tags'])
        tag_id = "element" + str(nb_html_tags)
        nb_html_tags += 1
        request.session['nb_html_tags'] = str(nb_html_tags)
        form_element = FormElement(html_id=tag_id, xml_element=xml_element, xml_xpath=full_path + '[' + str(x+1) + ']',
                                   name=text_capitalized).save()
        request.session['mapTagID'][tag_id] = str(form_element.id)

        # get the use from app info element
        app_info_use = app_info['use'] if 'use' in app_info else ''
        app_info_use = app_info_use if app_info_use is not None else ''
        use += ' ' + app_info_use

        li_content = ''

        if CURATE_COLLAPSE:
            # the type is complex, can be collapsed
            if element_type is not None and element_type.tag == "{0}complexType".format(namespace):
                li_content += render_collapse_button()

        label = app_info['label'] if 'label' in app_info else text_capitalized
        label = label if label is not None else ''

        li_content += label

        # add buttons to add/remove elements
        buttons = ""
        if not (add_button is False and delete_button is False):
            buttons = render_buttons(add_button, delete_button, tag_id[7:])

        # if element not removed
        if not removed:
            # if module is present, replace default input by module
            if _has_module:
                li_content += generate_module(request, element, namespace, xsd_xpath, full_path,
                                              edit_data_tree=edit_data_tree)
            else:  # generate the type
                if element_type is None:  # no complex/simple type
                    default_value = ""

                    if request.session['curate_edit']:
                        # if elements are found at this xpath
                        if len(edit_elements) > 0:
                            # it is an XML element
                            if element_tag == 'element':
                                # get the value of the element x
                                if edit_elements[x].text is not None:
                                    # set the value of the element
                                    default_value = edit_elements[x].text
                            # it is an XMl attribute
                            elif element_tag == 'attribute':
                                # get the value of the attribute
                                if edit_elements[x] is not None:
                                    # set the value of the element
                                    default_value = edit_elements[x]
                    elif 'default' in element.attrib:
                        # if the default attribute is present
                        default_value = element.attrib['default']

                    placeholder = app_info['placeholder'] if 'placeholder' in app_info else ''
                    tooltip = app_info['tooltip'] if 'tooltip' in app_info else ''

                    li_content += ' '
                    li_content += render_input(default_value, placeholder, tooltip)
                    li_content += buttons
                else:  # complex/simple type
                    li_content += buttons

                    if element_type.tag == "{0}complexType".format(namespace):
                        li_content += generate_complex_type(request, element_type, xml_tree, namespace,
                                                            full_path=full_path+'[' + str(x+1) + ']',
                                                            edit_data_tree=edit_data_tree)
                    elif element_type.tag == "{0}simpleType".format(namespace):
                        li_content += generate_simple_type(request, element_type, xml_tree, namespace,
                                                           full_path=full_path+'[' + str(x+1) + ']',
                                                           edit_data_tree=edit_data_tree)
        else:
            li_content += buttons

        # renders the name of the element
        ul_content += render_li(li_content, tag_id, element_tag, use, text_capitalized)

    form_string += render_ul(ul_content, choice_id, chosen)
    return form_string


def generate_element_absent(request, element, xml_doc_tree, form_element):
    """
    # Inputs:        request -
    # Outputs:       JSON data
    # Exceptions:    None
    # Description:   Generate XML element for which the element is absent from the form
    Parameters:
        request:
        element:
        xml_doc_tree:
        form_element:

    Returns:
    """
    # TODO see if it is possibe to group with generate_element
    form_string = ""

    namespaces = request.session['namespaces']
    default_prefix = request.session['defaultPrefix']
    namespace = namespaces[default_prefix]

    # get appinfo elements
    app_info = common.getAppInfo(element, namespace)

    # check if the element has a module
    _has_module = has_module(request, element)

    # type is a reference included in the document
    if 'ref' in element.attrib:
        ref = element.attrib['ref']
        # refElement = None

        if ':' in ref:
            ref_split = ref.split(":")
            ref_name = ref_split[1]
            ref_element = xml_doc_tree.find("./{0}element[@name='{1}']".format(namespace, ref_name))
        else:
            ref_element = xml_doc_tree.find("./{0}element[@name='{1}']".format(namespace, ref))

        if ref_element is not None:
            element = ref_element
            # check if the element has a module
            _has_module = has_module(request, element)

    if _has_module:
        form_string += generate_module(request, element, namespace, form_element.xml_element.xsd_xpath,
                                       form_element.xml_xpath)
    else:
        element_type = get_element_type(element, xml_doc_tree, namespace, default_prefix)

        # render the type
        if element_type is None:  # no complex/simple type
            default_value = ""

            if 'default' in element.attrib:
                # if the default attribute is present
                default_value = element.attrib['default']

            placeholder = app_info['placeholder'] if 'placeholder' in app_info else ''
            tooltip = app_info['tooltip'] if 'tooltip' in app_info else ''

            form_string += render_input(default_value, placeholder, tooltip)
        else:  # complex/simple type
            if element_type.tag == "{0}complexType".format(namespace):
                form_string += generate_complex_type(request, element_type, xml_doc_tree, namespace,
                                                     full_path=form_element.xml_xpath)
            elif element_type.tag == "{0}simpleType".format(namespace):
                form_string += generate_simple_type(request, element_type, xml_doc_tree, namespace,
                                                    full_path=form_element.xml_xpath)

    return form_string


def generate_sequence(request, element, xml_tree, namespace, choice_info=None, full_path="", edit_data_tree=None):
    """Generates a section of the form that represents an XML sequence

    Parameters:
        request:
        element: XML element
        xml_tree: XML Tree
        namespace: namespace
        choice_info:
        full_path:
        edit_data_tree:

    Returns:       HTML string representing a sequence
    """
    # (annotation?,(element|group|choice|sequence|any)*)
    # FIXME implement group, any
    form_string = ""

    # remove the annotations
    remove_annotations(element, namespace)

    min_occurs, max_occurs = manage_occurences(element)

    if min_occurs != 1 or max_occurs != 1:
        text = "Sequence"

        # XSD xpath
        xsd_xpath = etree.ElementTree(xml_tree).getpath(element)

        # init variables for buttons management
        add_button = False
        delete_button = False
        nb_occurrences = 1  # nb of occurrences to render (can't be 0 or the user won't see this element at all)
        nb_occurrences_data = min_occurs  # nb of occurrences in loaded data or in form being rendered (can be 0)
        # xml_element = None

        # loading data in the form
        if request.session['curate_edit']:
            # get the number of occurrences in the data
            nb_occurrences_data = lookup_occurs(element, xml_tree, namespace, full_path, edit_data_tree)

            # manage buttons
            if nb_occurrences_data < max_occurs:
                add_button = True
            if nb_occurrences_data > min_occurs:
                delete_button = True
        else:  # starting an empty form
            # Don't generate the element if not necessary
            if CURATE_MIN_TREE and min_occurs == 0:
                add_button = True
                delete_button = False
            else:
                if nb_occurrences_data < max_occurs:
                    add_button = True
                if nb_occurrences_data > min_occurs:
                    delete_button = True

        if nb_occurrences_data > nb_occurrences:
            nb_occurrences = nb_occurrences_data

        xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nb_occurrences_data, minOccurs=min_occurs,
                                 maxOccurs=max_occurs).save()

        # keeps track of elements to display depending on the selected choice
        if choice_info:
            chosen = True
            choice_id = choice_info.chooseIDStr + "-" + str(choice_info.counter)

            if request.session['curate_edit']:
                if nb_occurrences == 0:
                    chosen = False

                    if CURATE_MIN_TREE:
                        form_element = FormElement(html_id=choice_id, xml_element=xml_element, xml_xpath=None).save()

                        request.session['mapTagID'][choice_id] = str(form_element.id)

                        form_string += render_ul('', choice_id, chosen)
                        return form_string
            else:
                if choice_info.counter > 0:
                    chosen = False

                    if CURATE_MIN_TREE:
                        form_element = FormElement(html_id=choice_id, xml_element=xml_element, xml_xpath=None).save()

                        request.session['mapTagID'][choice_id] = str(form_element.id)

                        form_string += render_ul('', choice_id, chosen)
                        return form_string
        else:
            chosen = True
            choice_id = ''

        ul_content = ''

        # editing data and sequence not found in data
        if nb_occurrences_data == 0:
            nb_html_tags = int(request.session['nb_html_tags'])
            tag_id = "element" + str(nb_html_tags)
            nb_html_tags += 1
            request.session['nb_html_tags'] = str(nb_html_tags)
            form_element = FormElement(html_id=tag_id, xml_element=xml_element, xml_xpath=full_path + '[1]').save()
            request.session['mapTagID'][tag_id] = str(form_element.id)

            li_content = ''

            if CURATE_COLLAPSE:
                li_content += render_collapse_button()

            li_content += text
            li_content += render_buttons(True, False, str(tag_id[7:]))

            ul_content += render_li(li_content, tag_id, 'sequence', 'removed')
        else:
            for x in range(0, int(nb_occurrences)):
                nb_html_tags = int(request.session['nb_html_tags'])
                tag_id = "element" + str(nb_html_tags)
                nb_html_tags += 1
                request.session['nb_html_tags'] = str(nb_html_tags)
#                 if (minOccurs != 1) or (maxOccurs != 1):
                form_element = FormElement(html_id=tag_id, xml_element=xml_element,
                                           xml_xpath=full_path + '[' + str(x+1) + ']')
                form_element.save()
                request.session['mapTagID'][tag_id] = str(form_element.pk)

                li_content = ''

                if len(list(element)) > 0 and CURATE_COLLAPSE:
                    li_content += render_collapse_button()

                li_content += text
                li_content += render_buttons(add_button, delete_button, str(tag_id[7:]))

                # generates the sequence
                if len(list(element)) != 0:
                    for child in element:
                        if child.tag == "{0}element".format(namespace):
                            li_content += generate_element(request, child, xml_tree, namespace, choice_info,
                                                           full_path=full_path, edit_data_tree=edit_data_tree)
                        elif child.tag == "{0}sequence".format(namespace):
                            li_content += generate_sequence(request, child, xml_tree, namespace, choice_info,
                                                            full_path=full_path, edit_data_tree=edit_data_tree)
                        elif child.tag == "{0}choice".format(namespace):
                            li_content += generate_choice(request, child, xml_tree, namespace, choice_info,
                                                          full_path=full_path, edit_data_tree=edit_data_tree)
                        elif child.tag == "{0}any".format(namespace):
                            pass
                        elif child.tag == "{0}group".format(namespace):
                            pass

                ul_content += render_li(li_content, tag_id, 'sequence')

        form_string += render_ul(ul_content, choice_id, chosen)
    else:
        # generates the sequence
        if len(list(element)) != 0:
            for child in element:
                if child.tag == "{0}element".format(namespace):
                    form_string += generate_element(request, child, xml_tree, namespace, choice_info,
                                                    full_path=full_path, edit_data_tree=edit_data_tree)
                elif child.tag == "{0}sequence".format(namespace):
                    form_string += generate_sequence(request, child, xml_tree, namespace, choice_info,
                                                     full_path=full_path, edit_data_tree=edit_data_tree)
                elif child.tag == "{0}choice".format(namespace):
                    form_string += generate_choice(request, child, xml_tree, namespace, choice_info,
                                                   full_path=full_path, edit_data_tree=edit_data_tree)
                elif child.tag == "{0}any".format(namespace):
                    pass
                elif child.tag == "{0}group".format(namespace):
                    pass

    return form_string


def generate_sequence_absent(request, element, xml_tree, namespace):
    """Generates a section of the form that represents an XML sequence

    Parameters:
        request:
        element: XML element
        xml_tree: XML Tree
        namespace: namespace

    Returns:
        HTML string representing a sequence
    """
    # TODO see if it can be merged in generate_sequence
    form_string = ""

    # generates the sequence
    if len(list(element)) != 0:
        for child in element:
            if child.tag == "{0}element".format(namespace):
                form_string += generate_element(request, child, xml_tree, namespace)
            elif child.tag == "{0}sequence".format(namespace):
                form_string += generate_sequence(request, child, xml_tree, namespace)
            elif child.tag == "{0}choice".format(namespace):
                form_string += generate_choice(request, child, xml_tree, namespace)
            elif child.tag == "{0}any".format(namespace):
                pass
            elif child.tag == "{0}group".format(namespace):
                pass

    return form_string


def generate_choice(request, element, xml_tree, namespace, choice_info=None, full_path="", edit_data_tree=None):
    """Generates a section of the form that represents an XML choice

    Parameters:
        request:
        element: XML element
        xml_tree: XML Tree
        namespace: namespace
        choice_info: to keep track of branches to display (chosen ones) when going recursively down the tree
        full_path: XML xpath being built
        edit_data_tree: XML tree of data being edited

    Returns:       HTML string representing a sequence
    """
    # (annotation?,(element|group|choice|sequence|any)*)
    # FIXME Group not supported
    # FIXME Choice not supported
    form_string = ""

    # remove the annotations
    remove_annotations(element, namespace)

    # init variables for buttons management
    add_button = False
    delete_button = False
    nb_occurrences = 1  # nb of occurrences to render (can't be 0 or the user won't see this element at all)
    # nb_occurrences_data = 1
    xml_element = None

    # not multiple roots
    if not isinstance(element, list):
        # XSD xpath: don't need it when multiple root (can't duplicate a root)
        xsd_xpath = etree.ElementTree(xml_tree).getpath(element)

        # get element's min/max occurs attributes
        min_occurs, max_occurs = manage_occurences(element)
        nb_occurrences_data = min_occurs  # nb of occurrences in loaded data or in form being rendered (can be 0)

        # loading data in the form
        if request.session['curate_edit']:
            # get the number of occurrences in the data
            nb_occurrences_data = lookup_occurs(element, xml_tree, namespace, full_path, edit_data_tree)

            if nb_occurrences_data < max_occurs:
                add_button = True
            if nb_occurrences_data > min_occurs:
                delete_button = True
        else:  # starting an empty form
            # Don't generate the element if not necessary
            if CURATE_MIN_TREE and min_occurs == 0:
                add_button = True
                delete_button = False
            else:
                if nb_occurrences_data < max_occurs:
                    add_button = True
                if nb_occurrences_data > min_occurs:
                    delete_button = True

        if nb_occurrences_data > nb_occurrences:
            nb_occurrences = nb_occurrences_data

        xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nb_occurrences_data, minOccurs=min_occurs,
                                 maxOccurs=max_occurs)
        xml_element.save()

    # keeps track of elements to display depending on the selected choice
    if choice_info:
        choice_id = choice_info.chooseIDStr + "-" + str(choice_info.counter)
        chosen = True

        if request.session['curate_edit']:
            if nb_occurrences == 0:
                chosen = False

                if CURATE_MIN_TREE:
                    form_element = FormElement(html_id=choice_id, xml_element=xml_element, xml_xpath=None).save()

                    request.session['mapTagID'][choice_id] = str(form_element.id)

                    form_string += render_ul('', choice_id, chosen)
                    return form_string
        else:
            if choice_info.counter > 0:
                chosen = False

                if CURATE_MIN_TREE:
                    form_element = FormElement(html_id=choice_id, xml_element=xml_element, xml_xpath=None).save()

                    request.session['mapTagID'][choice_id] = str(form_element.id)

                    form_string += render_ul('', choice_id, chosen)
                    return form_string
    else:
        choice_id = ''
        chosen = True

    ul_content = ''

    for x in range(0, int(nb_occurrences)):
        nb_html_tags = int(request.session['nb_html_tags'])
        tag_id = "element" + str(nb_html_tags)
        nb_html_tags += 1
        request.session['nb_html_tags'] = str(nb_html_tags)

        form_element = FormElement(html_id=tag_id, xml_element=xml_element,
                                   xml_xpath=full_path + '[' + str(x+1) + ']')
        form_element.save()

        request.session['mapTagID'][tag_id] = str(form_element.pk)

        nb_choices_id = int(request.session['nbChoicesID'])
        choose_id = nb_choices_id
        choose_id_str = 'choice' + str(choose_id)
        nb_choices_id += 1

        request.session['nbChoicesID'] = str(nb_choices_id)

        is_removed = (nb_occurrences == 0)
        li_content = ''
        nb_sequence = 1
        options = []

        # generates the choice
        if len(list(element)) != 0:
            for child in element:
                entry = None

                if child.tag == "{0}element".format(namespace):
                    if child.attrib.get('name') is not None:
                        opt_value = opt_label = child.attrib.get('name')
                    else:
                        opt_value = opt_label = child.attrib.get('ref')

                        if ':' in child.attrib.get('ref'):
                            opt_label = opt_label.split(':')[1]

                    # look for active choice when editing
                    element_path = full_path + '/' + opt_label
                    entry = (opt_label, opt_value)

                    # FIXME put all element as selected, not what we want
                    if request.session['curate_edit'] and len(edit_data_tree.xpath(element_path)) != 0:
                        entry += (True,)
                    else:
                        entry += (False,)

                elif child.tag == "{0}group".format(namespace):
                    pass
                elif child.tag == "{0}choice".format(namespace):
                    pass
                elif child.tag == "{0}sequence".format(namespace):
                    entry = ('sequence' + str(nb_sequence), 'Sequence ' + str(nb_sequence), False)
                    nb_sequence += 1
                elif child.tag == "{0}any".format(namespace):
                    pass

                if entry is not None:
                    options.append(entry)

        li_content += render_select(choose_id_str, options)
        # FIXME this case generate buttons even when not needed (add and delete == False)
        li_content += render_buttons(add_button, delete_button, tag_id[7:])

        for (counter, choiceChild) in enumerate(list(element)):
            if choiceChild.tag == "{0}element".format(namespace):
                li_content += generate_element(request, choiceChild, xml_tree, namespace,
                                               common.ChoiceInfo(choose_id_str, counter), full_path=full_path,
                                               edit_data_tree=edit_data_tree)
            elif choiceChild.tag == "{0}group".format(namespace):
                pass
            elif choiceChild.tag == "{0}choice".format(namespace):
                pass
            elif choiceChild.tag == "{0}sequence".format(namespace):
                li_content += generate_sequence(request, choiceChild, xml_tree, namespace,
                                                common.ChoiceInfo(choose_id_str, counter), full_path=full_path,
                                                edit_data_tree=edit_data_tree)
            elif choiceChild.tag == "{0}any".format(namespace):
                pass

        ul_content += render_li('Choose'+li_content, tag_id, 'choice', 'removed' if is_removed else None)

    form_string += render_ul(ul_content, choice_id, chosen)

    return form_string


def generate_simple_type(request, element, xml_tree, namespace, full_path, edit_data_tree=None):
    """Generates a section of the form that represents an XML simple type

    Parameters:
        request:
        element:
        xml_tree:
        namespace:
        full_path:
        edit_data_tree:

    Returns:
        HTML string representing a sequence
    """
    # FIXME implement union, correct list
    form_string = ""

    # remove the annotations
    remove_annotations(element, namespace)

    if has_module(request, element):
        # XSD xpath: /element/complexType/sequence
        xsd_xpath = etree.ElementTree(xml_tree).getpath(element)
        form_string += generate_module(request, element, namespace, xsd_xpath, full_path, edit_data_tree=edit_data_tree)
        return form_string

    if list(element) != 0:
        child = element[0]

        if child.tag == "{0}restriction".format(namespace):
            form_string += generate_restriction(request, child, xml_tree, namespace, full_path,
                                                edit_data_tree=edit_data_tree)
        elif child.tag == "{0}list".format(namespace):
            # TODO list can contain a restriction/enumeration
            form_string += render_input('', '', '')
        elif child.tag == "{0}union".format(namespace):
            pass

    return form_string


def generate_complex_type(request, element, xml_tree, namespace, full_path, edit_data_tree=None):
    """Generates a section of the form that represents an XML complexType

    Parameters:
        request:
        element: XML element
        xml_tree: XML Tree
        namespace: namespace
        full_path:
        edit_data_tree:

    Returns:
        HTML string representing a sequence
    """
    # FIXME add support for complexContent, group, attributeGroup, anyAttribute
    # (
    #   annotation?,
    #   (
    #       simpleContent|complexContent|(
    #           (group|all|choice|sequence)?,
    #           (
    #               (attribute|attributeGroup)*,
    #               anyAttribute?
    #           )
    #       )
    #   )
    # )

    form_string = ""

    # remove the annotations
    remove_annotations(element, namespace)

    if has_module(request, element):
        # XSD xpath: /element/complexType/sequence
        xsd_xpath = etree.ElementTree(xml_tree).getpath(element)
        form_string += generate_module(request, element, namespace, xsd_xpath, full_path, edit_data_tree=edit_data_tree)
        return form_string

    # is it a simple content?
    complex_type_child = element.find('{0}simpleContent'.format(namespace))
    if complex_type_child is not None:
        form_string += generate_simple_content(request, complex_type_child, xml_tree, namespace, full_path=full_path,
                                               edit_data_tree=edit_data_tree)
        return form_string

    # does it contain any attributes?
    complex_type_children = element.findall('{0}attribute'.format(namespace))
    if len(complex_type_children) > 0:
        for attribute in complex_type_children:
            form_string += generate_element(request, attribute, xml_tree, namespace, full_path=full_path,
                                            edit_data_tree=edit_data_tree)

    # does it contain sequence or all?
    complex_type_child = element.find('{0}sequence'.format(namespace))
    if complex_type_child is not None:
        form_string += generate_sequence(request, complex_type_child, xml_tree, namespace, full_path=full_path,
                                         edit_data_tree=edit_data_tree)
    else:
        complex_type_child = element.find('{0}all'.format(namespace))
        if complex_type_child is not None:
            form_string += generate_sequence(request, complex_type_child, xml_tree, namespace, full_path=full_path,
                                             edit_data_tree=edit_data_tree)
        else:
            # does it contain choice ?
            complex_type_child = element.find('{0}choice'.format(namespace))
            if complex_type_child is not None:
                form_string += generate_choice(request, complex_type_child, xml_tree, namespace, full_path=full_path,
                                               edit_data_tree=edit_data_tree)
            else:
                form_string += ""

    return form_string


def generate_module(request, element, namespace, xsd_xpath=None, xml_xpath=None, edit_data_tree=None):
    """Generate a module to replace an element

    Parameters:
        request:
        element:
        namespace:
        xsd_xpath:
        xml_xpath:
        edit_data_tree:

    Returns:
        Module
    """
    form_string = ""
    reload_data = None
    reload_attrib = None

    if request.session['curate_edit']:
        edit_elements = edit_data_tree.xpath(xml_xpath)

        if len(edit_elements) > 0:
            if len(edit_elements) == 1:
                edit_element = edit_elements[0]

                # get attributes
                if 'attribute' not in xsd_xpath and len(edit_element.attrib) > 0:
                    reload_attrib = dict(edit_element.attrib)

                reload_data = get_xml_element_data(element, edit_element, namespace)
            else:
                reload_data = []
                reload_attrib = []

                for edit_element in edit_elements:
                    reload_attrib.append(dict(edit_element.attrib))
                    reload_data.append(get_xml_element_data(element, edit_element, namespace))

    # check if a module is set for this element
    if '{http://mdcs.ns}_mod_mdcs_' in element.attrib:
        # get the url of the module
        url = element.attrib['{http://mdcs.ns}_mod_mdcs_']

        # check that the url is registered in the system
        if url in Module.objects.all().values_list('url'):
            view = get_module_view(url)

            # build a request to send to the module to initialize it
            mod_req = request
            mod_req.method = 'GET'

            mod_req.GET = {
                'url': url,
                'xsd_xpath': xsd_xpath,
                'xml_xpath': xml_xpath,
            }

            # if the loaded doc has data, send them to the module for initialization
            if reload_data is not None:
                mod_req.GET['data'] = reload_data

            if reload_attrib is not None:
                mod_req.GET['attributes'] = reload_attrib

            # renders the module
            form_string += view(mod_req).content.decode("utf-8")

    return form_string


def generate_simple_content(request, element, xml_tree, namespace, full_path, edit_data_tree=None):
    """Generates a section of the form that represents an XML simple content

    Parameters:
        request:
        element:
        xml_tree:
        namespace:
        full_path:
        edit_data_tree:

    Returns:
        HTML string representing a simple content
    """
    # (annotation?,(restriction|extension))
    # FIXME better support for extension

    form_string = ""

    # remove the annotations
    remove_annotations(element, namespace)

    # generates the content
    if len(list(element)) != 0:
        child = element[0]

        if child.tag == "{0}restriction".format(namespace):
            form_string += generate_restriction(request, child, xml_tree, namespace, full_path,
                                                edit_data_tree=edit_data_tree)
        elif child.tag == "{0}extension".format(namespace):
            form_string += generate_extension(request, child, xml_tree, namespace, full_path,
                                              edit_data_tree=edit_data_tree)

    return form_string


def generate_restriction(request, element, xml_tree, namespace, full_path="", edit_data_tree=None):
    """Generates a section of the form that represents an XML restriction

    Parameters:
        request:
        element: XML element
        xml_tree: XML Tree
        namespace: namespace
        full_path:
        edit_data_tree:

    Returns:
        HTML string representing a sequence
    """
    # FIXME doesn't represent all the possibilities (http://www.w3schools.com/xml/el_restriction.asp)
    form_string = ""

    remove_annotations(element, namespace)

    enumeration = element.findall('{0}enumeration'.format(namespace))

    if len(enumeration) > 0:
        option_list = []

        if request.session['curate_edit']:
            edit_elements = edit_data_tree.xpath(full_path)
            selected_value = None

            if len(edit_elements) > 0:
                if '@' in full_path:
                    if edit_elements[0] is not None:
                        selected_value = edit_elements[0]
                else:
                    if edit_elements[0].text is not None:
                        selected_value = edit_elements[0].text

            for enum in enumeration:
                if selected_value is not None and enum.attrib.get('value') == selected_value:
                    entry = (enum.attrib.get('value'), enum.attrib.get('value'), True)
                else:
                    entry = (enum.attrib.get('value'), enum.attrib.get('value'), False)

                option_list.append(entry)
        else:
            for enum in enumeration:
                entry = (enum.attrib.get('value'), enum.attrib.get('value'), False)
                option_list.append(entry)

        form_string += render_select(None, option_list)
    else:
        simple_type = element.find('{0}simpleType'.format(namespace))
        if simple_type is not None:
            form_string += generate_simple_type(request, simple_type, xml_tree, namespace, full_path=full_path,
                                                edit_data_tree=edit_data_tree)
        else:
            form_string += render_input('', '', '')

    return form_string


def generate_extension(request, element, xml_tree, namespace, full_path="", edit_data_tree=None):
    """Generates a section of the form that represents an XML extension

    Parameters:
        request:
        element:
        xml_tree:
        namespace:
        full_path:
        edit_data_tree:

    Returns:
        HTML string representing an extension
    """
    # FIXME doesn't represent all the possibilities (http://www.w3schools.com/xml/el_extension.asp)
    form_string = ""

    remove_annotations(element, namespace)

    # FIXME simpleType cannot be the child of extension
    simple_type = element.find('{0}simpleType'.format(namespace))

    if simple_type is not None:
        form_string += generate_simple_type(request, simple_type, xml_tree, namespace, full_path=full_path,
                                            edit_data_tree=edit_data_tree)
    else:
        default_value = ""

        if request.session['curate_edit']:
            edit_elements = edit_data_tree.xpath(full_path)

            if len(edit_elements) > 0:
                if edit_elements[0].text is not None:
                    default_value = edit_elements[0].text

        form_string += render_input(default_value, '', '')

    return form_string
