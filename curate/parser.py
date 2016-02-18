# import re
# from django.http import HttpResponse
# from django.conf import settings
# from io import BytesIO
# from cStringIO import StringIO
# from mgi.models import Template, XMLdata, XML2Download, Module, MetaSchema
from mgi.models import Module
from mgi.models import FormElement, XMLElement, FormData
from mgi.settings import CURATE_MIN_TREE, CURATE_COLLAPSE
# import json
from bson.objectid import ObjectId
from mgi import common
# from django.template import Context, loader

# import lxml.html as html
# from lxml import html
from lxml import etree
# import lxml.etree as etree
import django.utils.html
# from django.contrib import messages

from modules import get_module_view

#XSL file loading
# import os
# from django.http.request import HttpRequest


################################################################################
#
# Function Name: reinitOccurrences(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Reinitialize the number of occurrences with original values
#
################################################################################
# FIXME this function is never used anywhere in the code
def reinitOccurrences(request):
    # reinitialize the map of occurrences with original values
    occurrences = request.session['occurrences']

    for elementID in occurrences.keys():
        elementOccurrencesStr = occurrences[str(elementID)]
        if 'inf' in elementOccurrencesStr:
            elementOccurrencesStr = elementOccurrencesStr.replace('inf','float("inf")')
        if 'Infinity' in elementOccurrencesStr:
            elementOccurrencesStr = elementOccurrencesStr.replace('Infinity','float("inf")')
        elementOccurrences = eval(elementOccurrencesStr)

        if (elementOccurrences['minOccurrences'] != 0):
            elementOccurrences['nbOccurrences'] = elementOccurrences['minOccurrences']
        else:
            elementOccurrences['nbOccurrences'] = 1
        occurrences[str(elementID)] = unicode(elementOccurrences)

    request.session['occurrences'] = occurrences


################################################################################
#
# Function Name: generateForm(request)
# Inputs:        request -
# Outputs:       rendered HTMl form
# Exceptions:    None
# Description:   Renders HTMl form for display.
#
################################################################################
def generateForm(request):
    # print 'BEGIN def generateForm(key,xmlElement)'

    defaultPrefix = request.session['defaultPrefix']
    xmlDocTreeStr = request.session['xmlDocTree']
    xmlDocTree = etree.fromstring(xmlDocTreeStr)
    request.session['nbChoicesID'] = '0'
    request.session['nb_html_tags'] = '0'
    if 'mapTagID' in request.session:
        del request.session['mapTagID']
    request.session['mapTagID'] = {}

    formString = ""

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
            clean_parser = etree.XMLParser(remove_blank_text=True,remove_comments=True,remove_pis=True)
            # set the parser
            etree.set_default_parser(parser=clean_parser)
            # load the XML tree from the text
            edit_data_tree = etree.XML(str(form_data.xml_data.encode('utf-8')))
        else: #no data found, not editing
            request.session['curate_edit'] = False


    # get the namespace for the default prefix
    namespace = request.session['namespaces'][defaultPrefix]

    # find all root elements
    elements = xmlDocTree.findall("./{0}element".format(namespace))


    try:
        # one root
        if len(elements) == 1:
            formString += "<div xmlID='root' name='xsdForm'>"
            formString += generateElement(request, elements[0], xmlDocTree,namespace, edit_data_tree=edit_data_tree)
            formString += "</div>"
        # multiple roots
        elif len(elements) > 1:
            formString += "<div xmlID='root' name='xsdForm'>"
            formString += generateChoice(request, elements, xmlDocTree, namespace, edit_data_tree=edit_data_tree)
            formString += "</div>"
    except Exception, e:
        formString = "UNSUPPORTED ELEMENT FOUND (" + e.message + ")"

    # save the list of elements for the form
    form_data.elements = request.session['mapTagID']
    # save data for the current form
    form_data.save()

    # delete temporary data structure for forms elements
    del request.session['mapTagID']

    # data are loaded, switch Edit to False, we don't need to look at the original data anymore
    request.session['curate_edit'] = False

    return formString


################################################################################
#
# Function Name: generateElement_absent(request)
# Inputs:        request -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Generate XML element for which the element is absent from the form
#
################################################################################
def generateElement_absent(request, element, xmlDocTree, form_element):
    formString = ""

    namespaces = request.session['namespaces']
    defaultPrefix = request.session['defaultPrefix']

    namespace = namespaces[defaultPrefix]

    # get appinfo elements
    app_info = common.getAppInfo(element, namespace)

    # check if the element has a module
    has_module = hasModule(request, element)

    # type is a reference included in the document
    if 'ref' in element.attrib:
        ref = element.attrib['ref']
        refElement = None
        if ':' in ref:
            refSplit = ref.split(":")
            refName = refSplit[1]
            refElement = xmlDocTree.find("./{0}element[@name='{1}']".format(namespace, refName))
        else:
            refElement = xmlDocTree.find("./{0}element[@name='{1}']".format(namespace, ref))

        if refElement is not None:
            element = refElement
            # check if the element has a module
            has_module = hasModule(request, element)

    if has_module:
        formString += generateModule(request, element, namespace, form_element.xml_element.xsd_xpath, form_element.xml_xpath)
    else:
        elementType = getElementType(element, xmlDocTree, namespace, defaultPrefix)
        # render the type
        if elementType is None: # no complex/simple type
            defaultValue = ""
            if 'default' in element.attrib:
                # if the default attribute is present
                defaultValue = element.attrib['default']

            placeholder = 'placeholder="'+app_info['placeholder']+ '"' if 'placeholder' in app_info else ''
            placeholder = placeholder if placeholder is not None else ''

            tooltip = 'title="'+app_info['tooltip']+ '"' if 'tooltip' in app_info else ''
            tooltip = tooltip if tooltip is not None else ''

            formString += " <input type='text' value='"+ django.utils.html.escape(defaultValue) +"'" + placeholder + tooltip +"/>"
        else: # complex/simple type
            if elementType.tag == "{0}complexType".format(namespace):
                formString += generateComplexType(request, elementType, xmlDocTree, namespace, fullPath=form_element.xml_xpath)
            elif elementType.tag == "{0}simpleType".format(namespace):
                formString += generateSimpleType(request, elementType, xmlDocTree, namespace, fullPath=form_element.xml_xpath)

    return formString


################################################################################
#
# Function Name: manageButtons(element)
# Inputs:        element - XML element
# Outputs:       addButton - Boolean
#                deleteButton - Boolean
#                nbOccurrences - Integer
# Exceptions:    None
# Description:   Check element occurrences and returns buttons information
#
################################################################################
def manageButtons(minOccurs, maxOccurs):
    if type(minOccurs) is not int:
        raise TypeError('min_occurs should an integer')

    if type(maxOccurs) is not int and maxOccurs != float('inf'):
        raise TypeError('max_occurs should an integer or infinity')

    if minOccurs < 0:
        raise ValueError('min_occurs should be positive')

    if maxOccurs < 1:
        raise ValueError('max_occurs should be higher or equal to 1')

    if maxOccurs <= minOccurs:
        raise ValueError('max_occurs should be higher than min_occurs')

    addButton = False
    deleteButton = False
    nbOccurrences = 1

    if minOccurs == 0:
        deleteButton = True
    else:
        nbOccurrences = minOccurs

    if maxOccurs == float('inf'):
        addButton = True
    elif maxOccurs > minOccurs and maxOccurs > 1:
        addButton = True


    return addButton, deleteButton, nbOccurrences


################################################################################
#
# Function Name: removeAnnotations(element, namespace)
# Inputs:        element - XML element
#                namespace - namespace
# Outputs:       None
# Exceptions:    None
# Description:   Remove annotations of an element if present
#
################################################################################
def removeAnnotations(element, namespace):
    "Remove annotations of the current element"

    #check if the first child is an annotation and delete it
    if(len(list(element)) != 0):
        if (element[0].tag == "{0}annotation".format(namespace)):
            element.remove(element[0])


################################################################################
#
# Function Name: get_subnodes_xpath(element, xmlTree, namespace)
# Inputs:        element - XML element
#                xmlTree - xmlTree
#                namespace - namespace
# Outputs:       None
# Exceptions:    None
# Description:   Do a lookup in subelements to build xpath
#
################################################################################
def get_subnodes_xpath(element, xmlTree, namespace):
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
                    refElement = None
                    if ':' in ref:
                        refSplit = ref.split(":")
                        refName = refSplit[1]
                        refElement = xmlTree.find("./{0}element[@name='{1}']".format(namespace, refName))
                    else:
                        refElement = xmlTree.find("./{0}element[@name='{1}']".format(namespace, ref))
                    if refElement is not None:
                        xpaths.append({'name': refElement.attrib.get('name'), 'element': refElement})
            else:
                xpaths.extend(get_subnodes_xpath(child, xmlTree, namespace))
    return xpaths


################################################################################
#
# Function Name: get_subnodes_xpath(element, xmlTree, namespace)
# Inputs:        element - XML element
#                xmlTree - xmlTree
#                namespace - namespace
# Outputs:       None
# Exceptions:    None
# Description:   Do a lookup in subelements to build xpath.
#                Get nodes' xpath, only one level deep. It's not going to every leaves. Only need to know if the node is here.
#
################################################################################
def get_nodes_xpath(elements, xmlTree, namespace):
    # FIXME Making one function with get_subnode_xpath should be possible, both are doing the same job
    # FIXME same problems as in get_subnodes_xpath
    xpaths = []

    for element in elements:
        if element.tag == "{0}element".format(namespace):
            if 'name' in element.attrib:
                xpaths.append({'name': element.attrib['name'], 'element': element})
            elif 'ref' in element.attrib:
                ref = element.attrib['ref']
                refElement = None
                if ':' in ref:
                    refSplit = ref.split(":")
                    refName = refSplit[1]
                    refElement = xmlTree.find("./{0}element[@name='{1}']".format(namespace, refName))
                else:
                    refElement = xmlTree.find("./{0}element[@name='{1}']".format(namespace, ref))
                if refElement is not None:
                    xpaths.append({'name': refElement.attrib.get('name'), 'element': refElement})
        else:
            xpaths.extend(get_subnodes_xpath(element, xmlTree, namespace))
    return xpaths

# FIXME will this function be needed ? If not remove it!
# def isDeterminist(element, xmlTree, namespace):
#     determinist = True
#     try:
#         # look at sequence children, to see if it contains only elements
#         if(len(list(element)) != 0):
#             for child in element:
#                 if (child.tag != "{0}element".format(namespace)):
#                     determinist = False
#                     break
#             # doesn't contain only elements, need to get sub elements xpath to see if they are determinist
#             if determinist == False:
#                 # get xpath of all elements
#                 xpaths = get_nodes_xpath(list(element), xmlTree, namespace)
#                 # check that xpaths are unique
#                 if len(xpaths) == len(set(xpaths)):
#                     determinist = True
#                 else:
#                     print "NOT DETERMINISTIC"
#     except:
#         print "ERROR"
#         return False
#
#     return determinist


################################################################################
#
# Function Name: lookup_Occurs(element, xmlTree, namespace, fullPath, edit_data_tree)
# Inputs:        element - XML element
#                xmlTree - xmlTree
#                namespace - namespace
#                fullPath - current node XPath
#                edit_data_tree - XML data
# Outputs:       None
# Exceptions:    None
# Description:   Do a lookup in data to get the number of occurences of a sequence or choice without a name (not within a named complextype).
#                get the number of times the sequence appears in the XML document that we are loading for editing
#                algorithm:
#                get all the possible nodes that can appear in the sequence
#                for each node, count how many times it's found in the data
#                the maximum count is the number of occurrences of the sequence
#                only works if data are determinist enough: means we don't have an element outside the sequence, and the same in the sequence
################################################################################
def lookup_Occurs(element, xmlTree, namespace, fullPath, edit_data_tree):
    xpaths = get_nodes_xpath(element, xmlTree, namespace)
    maxOccursFound = 0
    for xpath in xpaths:
        edit_elements = edit_data_tree.xpath(fullPath + '/' + xpath['name'])
        if len(edit_elements) > maxOccursFound:
            maxOccursFound = 1
            if 'maxOccurs' in xpath['element'].attrib:
                if xpath['element'].attrib != "unbounded":
                    if xpath['element'].attrib < len(edit_elements):
                        maxOccursFound = len(edit_elements)
                        raise Exception("These data can't be loaded for now, because of the following element: " + fullPath + '/' + xpath['name'])

    return maxOccursFound


################################################################################
#
# Function Name: generateSequence(request, element, xmlTree, namespace)
# Inputs:        request -
#                element - XML element
#                xmlTree - XML Tree
#                namespace - namespace
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML sequence
#
################################################################################
# FIXME Implement group, any
def generateSequence(request, element, xmlTree, namespace, choiceInfo=None, fullPath="", edit_data_tree=None):
    #(annotation?,(element|group|choice|sequence|any)*)
    formString = ""

    # remove the annotations
    removeAnnotations(element, namespace)

    minOccurs, maxOccurs = manageOccurences(element)

    if (minOccurs != 1) or (maxOccurs != 1):
        text = "Sequence"

        # XSD xpath
        xsd_xpath = etree.ElementTree(xmlTree).getpath(element)

        # init variables for buttons management
        addButton = False
        deleteButton = False
        nbOccurrences = 1 #nb of occurrences to render (can't be 0 or the user won't see this element at all)
        nbOccurrences_data = minOccurs # nb of occurrences in loaded data or in form being rendered (can be 0)
        xml_element = None

        # loading data in the form
        if request.session['curate_edit']:
            # get the number of occurrences in the data
            nbOccurrences_data = lookup_Occurs(element, xmlTree, namespace, fullPath, edit_data_tree)

            # manage buttons
            if nbOccurrences_data < maxOccurs:
                addButton = True
            if nbOccurrences_data > minOccurs:
                deleteButton = True

        else: # starting an empty form
            # Don't generate the element if not necessary
            if CURATE_MIN_TREE and minOccurs == 0:
                addButton = True
                deleteButton = False
            else:
                if nbOccurrences_data < maxOccurs:
                    addButton = True
                if nbOccurrences_data > minOccurs:
                    deleteButton = True

        if nbOccurrences_data > nbOccurrences:
            nbOccurrences = nbOccurrences_data

        xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nbOccurrences_data, minOccurs=minOccurs, maxOccurs=maxOccurs).save()

        # keeps track of elements to display depending on the selected choice
        if choiceInfo:
            choiceID = choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter)
            if request.session['curate_edit']:
                if nbOccurrences == 0:
                    formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                    if CURATE_MIN_TREE:
                        form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=None).save()
                        request.session['mapTagID'][choiceID] = str(form_element.id)
                        formString += "</ul>"
                        return formString
                else:
                    formString += "<ul id=\"" + choiceID + "\" >"
            else:
                if (choiceInfo.counter > 0):
                    formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                    if CURATE_MIN_TREE:
                        form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=None).save()
                        request.session['mapTagID'][choiceID] = str(form_element.id)
                        formString += "</ul>"
                        return formString
                else:
                    formString += "<ul id=\"" + choiceID + "\" >"
        else:
            formString += "<ul>"

        # editing data and sequence not found in data
        if nbOccurrences_data == 0:
            nb_html_tags = int(request.session['nb_html_tags'])
            tagID = "element" + str(nb_html_tags)
            nb_html_tags += 1
            request.session['nb_html_tags'] = str(nb_html_tags)
            form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=fullPath + '[1]').save()
            request.session['mapTagID'][tagID] = str(form_element.id)
            formString += "<li class='sequence removed' id='" + str(tagID) + "'>"
            formString += "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>" if CURATE_COLLAPSE else ""
            formString += text
            formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"
            formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"
        else:
            for x in range (0,int(nbOccurrences)):
                nb_html_tags = int(request.session['nb_html_tags'])
                tagID = "element" + str(nb_html_tags)
                nb_html_tags += 1
                request.session['nb_html_tags'] = str(nb_html_tags)
#                 if (minOccurs != 1) or (maxOccurs != 1):
                form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=fullPath + '[' + str(x+1) +']').save()
                request.session['mapTagID'][tagID] = str(form_element.id)

                # if tag not closed:  <element/>
                if len(list(element)) > 0 :
                    formString += "<li class='sequence' id='" + str(tagID) + "'>"
                    formString += "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>" if CURATE_COLLAPSE else ""
                    formString += text
                else:
                    formString += "<li class='sequence' id='" + str(tagID) + "'>" + text

                if (addButton == True):
                    formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"
                else:
                    formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"
                if (deleteButton == True):
                    formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"
                else:
                    formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"

                # generates the sequence
                if(len(list(element)) != 0):
                    for child in element:
                        if (child.tag == "{0}element".format(namespace)):
                            formString += generateElement(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath, edit_data_tree=edit_data_tree)
                        elif (child.tag == "{0}sequence".format(namespace)):
                            formString += generateSequence(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath, edit_data_tree=edit_data_tree)
                        elif (child.tag == "{0}choice".format(namespace)):
                            formString += generateChoice(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath, edit_data_tree=edit_data_tree)
                        elif (child.tag == "{0}any".format(namespace)):
                            pass
                        elif (child.tag == "{0}group".format(namespace)):
                            pass
                formString += "</li>"
        formString += "</ul>"

    else:
        # generates the sequence
        if(len(list(element)) != 0):
            for child in element:
                if (child.tag == "{0}element".format(namespace)):
                    formString += generateElement(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath, edit_data_tree=edit_data_tree)
                elif (child.tag == "{0}sequence".format(namespace)):
                    formString += generateSequence(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath, edit_data_tree=edit_data_tree)
                elif (child.tag == "{0}choice".format(namespace)):
                    formString += generateChoice(request, child, xmlTree, namespace,choiceInfo, fullPath=fullPath, edit_data_tree=edit_data_tree)
                elif (child.tag == "{0}any".format(namespace)):
                    pass
                elif (child.tag == "{0}group".format(namespace)):
                    pass  # TODO implement

    return formString


################################################################################
#
# Function Name: generateSequence_absent(request, element, xmlTree, namespace)
# Inputs:        request -
#                element - XML element
#                xmlTree - XML Tree
#                namespace - namespace
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML sequence
#
################################################################################
def generateSequence_absent(request, element, xmlTree, namespace):

    formString = ""
    # generates the sequence
    if(len(list(element)) != 0):
        for child in element:
            if (child.tag == "{0}element".format(namespace)):
                formString += generateElement(request, child, xmlTree, namespace)
            elif (child.tag == "{0}sequence".format(namespace)):
                formString += generateSequence(request, child, xmlTree, namespace)
            elif (child.tag == "{0}choice".format(namespace)):
                formString += generateChoice(request, child, xmlTree, namespace)
            elif (child.tag == "{0}any".format(namespace)):
                pass
            elif (child.tag == "{0}group".format(namespace)):
                pass

    return formString


################################################################################
#
# Function Name: generateChoice(request, element, xmlTree, namespace)
# Inputs:        request -
#                element - XML element
#                xmlTree - XML Tree
#                namespace - namespace
#                choiceInfo - to keep track of branches to display (chosen ones) when going recursively down the tree
#                fullPath - XML xpath being built
#                edit_data_tree - XML tree of data being edited
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML choice
#
################################################################################
# FIXME Group not supported
# FIXME Choice not supported
def generateChoice(request, element, xmlTree, namespace, choiceInfo=None, fullPath="", edit_data_tree=None):
    #(annotation?,(element|group|choice|sequence|any)*)

    formString = ""

    #remove the annotations
    removeAnnotations(element, namespace)

    # init variables for buttons management
    addButton = False
    deleteButton = False
    nbOccurrences = 1 #nb of occurrences to render (can't be 0 or the user won't see this element at all)
    nbOccurrences_data = 1
    xml_element = None

    # not multiple roots
    if (not isinstance(element,list)):
        # XSD xpath: don't need it when multiple root (can't duplicate a root)
        xsd_xpath = etree.ElementTree(xmlTree).getpath(element)

        # get element's min/max occurs attributes
        minOccurs, maxOccurs = manageOccurences(element)
        nbOccurrences_data = minOccurs # nb of occurrences in loaded data or in form being rendered (can be 0)


        # loading data in the form
        if request.session['curate_edit']:
            # get the number of occurrences in the data
            nbOccurrences_data = lookup_Occurs(element, xmlTree, namespace, fullPath, edit_data_tree)

            if nbOccurrences_data < maxOccurs:
                addButton = True
            if nbOccurrences_data > minOccurs:
                deleteButton = True

        else: # starting an empty form
            # Don't generate the element if not necessary
            if CURATE_MIN_TREE and minOccurs == 0:
                addButton = True
                deleteButton = False
            else:
                if nbOccurrences_data < maxOccurs:
                    addButton = True
                if nbOccurrences_data > minOccurs:
                    deleteButton = True

        if nbOccurrences_data > nbOccurrences:
            nbOccurrences = nbOccurrences_data

        xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nbOccurrences_data, minOccurs=minOccurs, maxOccurs=maxOccurs).save()

#         # loading data in the form
#         if request.session['curate_edit']:
#             # get the number of occurrences in the data
#             nbOccurrences_data = lookup_Occurs(element, xmlTree, namespace, fullPath, edit_data_tree)
#             # manage buttons
#             if nbOccurrences_data < maxOccurs:
#                 addButton = True
#             if nbOccurrences_data > minOccurs:
#                 deleteButton = True
#         else: # starting an empty form
#             if (minOccurs != 1) or (maxOccurs != 1):
#                 addButton, deleteButton, nbOccurrences = manageButtons(minOccurs, maxOccurs)
#
#         if nbOccurrences_data > nbOccurrences:
#             nbOccurrences = nbOccurrences_data
#
#         xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nbOccurrences_data, minOccurs=minOccurs, maxOccurs=maxOccurs).save()

    # keeps track of elements to display depending on the selected choice
    if choiceInfo:
        choiceID = choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter)
        if request.session['curate_edit']:
            if nbOccurrences == 0:
                formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                if CURATE_MIN_TREE:
                    form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=None).save()
                    request.session['mapTagID'][choiceID] = str(form_element.id)
                    formString += "</ul>"
                    return formString
            else:
                formString += "<ul id=\"" + choiceID + "\" >"
        else:
            if (choiceInfo.counter > 0):
                formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                if CURATE_MIN_TREE:
                    form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=None).save()
                    request.session['mapTagID'][choiceID] = str(form_element.id)
                    formString += "</ul>"
                    return formString
            else:
                formString += "<ul id=\"" + choiceID + "\" >"
    else:
        formString += "<ul>"

    for x in range (0,int(nbOccurrences)):
        nb_html_tags = int(request.session['nb_html_tags'])
        tagID = "element" + str(nb_html_tags)
        nb_html_tags += 1
        request.session['nb_html_tags'] = str(nb_html_tags)
#         if not isinstance(element,list) and ((minOccurs != 1) or (maxOccurs != 1)):
        form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=fullPath + '[' + str(x+1) +']').save()
        request.session['mapTagID'][tagID] = str(form_element.id)
        nbChoicesID = int(request.session['nbChoicesID'])
        chooseID = nbChoicesID
        chooseIDStr = 'choice' + str(chooseID)
        nbChoicesID += 1
        request.session['nbChoicesID'] = str(nbChoicesID)

        if nbOccurrences_data == 0:
            formString += "<li class='choice removed' id='" + str(tagID) + "'>Choose<select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"
        else:
            formString += "<li class='choice' id='" + str(tagID) + "'>Choose<select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"

        nbSequence = 1
#         nbChoice = 1

        # generates the choice
        if(len(list(element)) != 0):
            for child in element:
                if (child.tag == "{0}element".format(namespace)):
                    if child.attrib.get('name') is not None:
                        opt_value = opt_label = child.attrib.get('name')
                    else:
                        opt_value = opt_label = child.attrib.get('ref')
                        if ':' in opt_label:
                            opt_label = opt_label.split(':')[1]
                    # look for active choice when editing
                    elementPath = fullPath + '/' + opt_label

                    if request.session['curate_edit']:
                        if len(edit_data_tree.xpath(elementPath)) == 0:
                            formString += "<option value='" + opt_value + "'>" + opt_label + "</option><br/>"
                        else:
                            formString += "<option value='" + opt_value + "' selected='selected'>" + opt_label + "</option><br/>"
                    else:
                        formString += "<option value='" + opt_value + "'>" + opt_label + "</option><br/>"
                elif (child.tag == "{0}group".format(namespace)):
                    pass
                elif (child.tag == "{0}choice".format(namespace)):
                    pass
#                     formString += "<option value='choice" + str(nbChoice) + "'>Choice " + str(nbChoice) + "</option></b><br/>"
#                     nbChoice += 1
                elif (child.tag == "{0}sequence".format(namespace)):
                    formString += "<option value='sequence" + str(nbSequence) + "'>Sequence " + str(nbSequence) + "</option><br/>"
                    nbSequence += 1
                elif (child.tag == "{0}any".format(namespace)):
                    pass

        formString += "</select>"

        if (addButton == True):
            formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"
        else:
            formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"
        if (deleteButton == True):
            formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"
        else:
            formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"

        for (counter, choiceChild) in enumerate(list(element)):
            if choiceChild.tag == "{0}element".format(namespace):
                formString += generateElement(request, choiceChild, xmlTree, namespace, common.ChoiceInfo(chooseIDStr,counter), fullPath=fullPath, edit_data_tree=edit_data_tree)
            elif (choiceChild.tag == "{0}group".format(namespace)):
                pass
            elif (choiceChild.tag == "{0}choice".format(namespace)):
                pass
#                 formString += generateChoice(request, choiceChild, xmlTree, namespace, common.ChoiceInfo(chooseIDStr,counter), fullPath=fullPath, edit_data_tree=edit_data_tree)
            elif (choiceChild.tag == "{0}sequence".format(namespace)):
                formString += generateSequence(request, choiceChild, xmlTree, namespace, common.ChoiceInfo(chooseIDStr,counter), fullPath=fullPath, edit_data_tree=edit_data_tree)
            elif (choiceChild.tag == "{0}any".format(namespace)):
                pass

        formString += "</li>"
    formString += "</ul>"

    return formString


################################################################################
#
# Function Name: generateSimpleType(request, element, xmlTree, namespace)
# Inputs:        request -
#                element - XML element
#                xmlTree - XML Tree
#                namespace - namespace
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML simple type
#
################################################################################
# fixme implement union, correct list
def generateSimpleType(request, element, xmlTree, namespace, fullPath, edit_data_tree=None):
    formString = ""

    # remove the annotations
    removeAnnotations(element, namespace)

    if hasModule(request, element):
        # XSD xpath: /element/complexType/sequence
        xsd_xpath = etree.ElementTree(xmlTree).getpath(element)
        formString += generateModule(request, element, namespace, xsd_xpath, fullPath, edit_data_tree=edit_data_tree)
        return formString

    if (list(element) != 0):
        child = element[0]
        if child.tag == "{0}restriction".format(namespace):
            formString += generateRestriction(request, child, xmlTree, namespace, fullPath, edit_data_tree=edit_data_tree)
        elif child.tag == "{0}list".format(namespace):
            #TODO: list can contain a restriction/enumeration, what can we do about that?
            formString += "<input type='text'/>"
        elif child.tag == "{0}union".format(namespace):
            pass

    return formString


################################################################################
#
# Function Name: generateRestriction(request, element, xmlTree, namespace)
# Inputs:        request -
#                element - XML element
#                xmlTree - XML Tree
#                namespace - namespace
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML restriction
#
################################################################################
# FIXME doesn't represent all the possibilities (http://www.w3schools.com/xml/el_restriction.asp)
def generateRestriction(request, element, xmlTree, namespace, fullPath="", edit_data_tree=None):
    formString = ""

    removeAnnotations(element, namespace)

    enumeration = element.findall('{0}enumeration'.format(namespace))
    if len(enumeration) > 0:
        formString += "<select>"
        if request.session['curate_edit']:
            edit_elements = edit_data_tree.xpath(fullPath)
            selected_value = None
            if len(edit_elements) > 0:
                if '@' in fullPath:
                    if edit_elements[0] is not None:
                        selected_value = edit_elements[0]
                else:
                    if edit_elements[0].text is not None:
                        selected_value = edit_elements[0].text
            for enum in enumeration:
                if selected_value is not None and enum.attrib.get('value') == selected_value:
                    formString += "<option value='" + enum.attrib.get('value')  + "' selected='selected'>" + enum.attrib.get('value') + "</option>"
                else:
                    formString += "<option value='" + enum.attrib.get('value')  + "'>" + enum.attrib.get('value') + "</option>"
        else:
            for enum in enumeration:
                formString += "<option value='" + enum.attrib.get('value')  + "'>" + enum.attrib.get('value') + "</option>"
        formString += "</select>"
    else:
        simpleType = element.find('{0}simpleType'.format(namespace))
        if simpleType is not None:
            formString += generateSimpleType(request, simpleType, xmlTree, namespace, fullPath=fullPath, edit_data_tree=edit_data_tree)
        else:
            formString += " <input type='text'/>"

    return formString


################################################################################
#
# Function Name: generateExtension(request, element, xmlTree, namespace)
# Inputs:        request -
#                element - XML element
#                xmlTree - XML Tree
#                namespace - namespace
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML extension
#
################################################################################
# FIXME doesn't represent all the possibilities (http://www.w3schools.com/xml/el_extension.asp)
def generateExtension(request, element, xmlTree, namespace, fullPath="", edit_data_tree=None):
    formString = ""

    removeAnnotations(element, namespace)

#     # does it contain any attributes?
#     complexTypeChildren = element.findall('{0}attribute'.format(namespace))
#     if len(complexTypeChildren) > 0:
#         for attribute in complexTypeChildren:
#             formString += generateElement(request, attribute, xmlTree, namespace, fullPath=fullPath, edit_data_tree=edit_data_tree)

    # FIXME simpleType cannot be the child of extension
    simpleType = element.find('{0}simpleType'.format(namespace))
    if simpleType is not None:
        formString += generateSimpleType(request, simpleType, xmlTree, namespace, fullPath=fullPath, edit_data_tree=edit_data_tree)
    else:
        defaultValue = ""
        if request.session['curate_edit']:
            edit_elements = edit_data_tree.xpath(fullPath)
            if len(edit_elements) > 0:
                if edit_elements[0].text is not None:
                    defaultValue = edit_elements[0].text
        formString += " <input type='text' value='"+ django.utils.html.escape(defaultValue) +"'/>"

    return formString


################################################################################
#
# Function Name: generateComplexType(request, element, xmlTree, namespace)
# Inputs:        request -
#                element - XML element
#                xmlTree - XML Tree
#                namespace - namespace
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML complexType
#
################################################################################
# FIXME add support for complexContent, group, attributeGroup, anyAttribute
def generateComplexType(request, element, xmlTree, namespace, fullPath, edit_data_tree=None):
    #(annotation?,(simpleContent|complexContent|((group|all|choice|sequence)?,((attribute|attributeGroup)*,anyAttribute?))))

    formString = ""

    # remove the annotations
    removeAnnotations(element, namespace)

    if hasModule(request, element):
        # XSD xpath: /element/complexType/sequence
        xsd_xpath = etree.ElementTree(xmlTree).getpath(element)
        formString += generateModule(request, element, namespace, xsd_xpath, fullPath, edit_data_tree=edit_data_tree)
        return formString

    # is it a simple content?
    complexTypeChild = element.find('{0}simpleContent'.format(namespace))
    if complexTypeChild is not None:
        formString += generateSimpleContent(request, complexTypeChild, xmlTree, namespace, fullPath=fullPath, edit_data_tree=edit_data_tree)
        return formString

    # does it contain any attributes?
    complexTypeChildren = element.findall('{0}attribute'.format(namespace))
    if len(complexTypeChildren) > 0:
        for attribute in complexTypeChildren:
            formString += generateElement(request, attribute, xmlTree, namespace, fullPath=fullPath, edit_data_tree=edit_data_tree)

    # does it contain sequence or all?
    complexTypeChild = element.find('{0}sequence'.format(namespace))
    if complexTypeChild is not None:
        formString += generateSequence(request, complexTypeChild, xmlTree, namespace, fullPath=fullPath, edit_data_tree=edit_data_tree)
    else:
        complexTypeChild = element.find('{0}all'.format(namespace))
        if complexTypeChild is not None:
            formString += generateSequence(request, complexTypeChild, xmlTree, namespace, fullPath=fullPath, edit_data_tree=edit_data_tree)
        else:
            # does it contain choice ?
            complexTypeChild = element.find('{0}choice'.format(namespace))
            if complexTypeChild is not None:
                formString += generateChoice(request, complexTypeChild, xmlTree, namespace, fullPath=fullPath, edit_data_tree=edit_data_tree)
            else:
                formString += ""

    return formString


################################################################################
#
# Function Name: generateSimpleContent(request, element, xmlTree, namespace)
# Inputs:        request -
#                element - XML element
#                xmlTree - XML Tree
#                namespace - namespace
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML simple content
#
################################################################################
# FIXME better support for extension
def generateSimpleContent(request, element, xmlTree, namespace, fullPath, edit_data_tree=None):
    #(annotation?,(restriction|extension))

    formString = ""

    # remove the annotations
    removeAnnotations(element, namespace)

    # generates the content
    if(len(list(element)) != 0):
        child = element[0]
        if (child.tag == "{0}restriction".format(namespace)):
            formString += generateRestriction(request, child, xmlTree, namespace, fullPath, edit_data_tree=edit_data_tree)
        elif (child.tag == "{0}extension".format(namespace)):
            formString += generateExtension(request, child, xmlTree, namespace, fullPath, edit_data_tree=edit_data_tree)

    return formString


def get_Xml_element_data(xsd_element, xml_element, namespace):
    reload_data = None

    # get data
    if xsd_element.tag == "{0}element".format(namespace):
        # leaf: get the value
        if len(list(xml_element)) == 0:
            if xml_element.text is not None: # when tag is present but value empty, takes value None (we need empty text)
                reload_data = xml_element.text
            else:
                reload_data = ''
        else: # branch: get the whole branch
            reload_data = etree.tostring(xml_element)
    elif xsd_element.tag == "{0}attribute".format(namespace):
        pass
    elif xsd_element.tag == "{0}complexType".format(namespace) or xsd_element.tag == "{0}simpleType".format(namespace):
        # leaf: get the value
        if len(list(xml_element)) == 0:
            if xml_element.text is not None: # when tag is present but value empty, takes value None (we need empty text)
                reload_data = xml_element.text
            else:
                reload_data = ''
        else: # branch: get the whole branch
            try:
                reload_data = etree.tostring(xml_element)
            except:
                # FIXME in which case would we need that?
                reload_data = str(xml_element)

    return reload_data


################################################################################
#
# Function Name: generateModule(request, element)
# Inputs:        request -
#                element - XML element
# Outputs:       Module
# Exceptions:    None
# Description:   Generate a module to replace an element
#
################################################################################
def generateModule(request, element, namespace, xsd_xpath=None, xml_xpath=None, edit_data_tree=None):
    formString = ""

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
                reload_data = get_Xml_element_data(element, edit_element, namespace)
            else:
                reload_data = []
                reload_attrib = []
                for edit_element in edit_elements:
                    reload_attrib.append(dict(edit_element.attrib))
                    reload_data.append(get_Xml_element_data(element, edit_element, namespace))



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
            formString += view(mod_req).content.decode("utf-8")

    return formString


################################################################################
#
# Function Name: hasModule(request, element)
# Inputs:        request -
#                element - XML element
# Outputs:
#                True - the element has a module attribute
#                False - the element doesn't have a module attribute
# Exceptions:    None
# Description:   Look for a module in XML element's attributes
#
################################################################################
# TODO remove request (unused)
def hasModule(request, element):
    has_module = False

    # check if a module is set for this element
    if '{http://mdcs.ns}_mod_mdcs_' in element.attrib:
        # get the url of the module
        url = element.attrib['{http://mdcs.ns}_mod_mdcs_']
        # check that the url is registered in the system
        if url in Module.objects.all().values_list('url'):
            has_module = True

    return has_module


################################################################################
#
# Function Name: generateElement(request, element, xmlTree, namespace)
# Inputs:        request -
#                element - XML element
#                xmlTree - XML tree of the template
#                namespace - Namespace used in the template
# Outputs:       JSON data
# Exceptions:    None
# Description:   Generate an HTML string that represents an XML element.
#
################################################################################
# FIXME Support for unique is not present
# FIXME Support for key / keyref
def generateElement(request, element, xmlTree, namespace, choiceInfo=None, fullPath="", edit_data_tree=None):
    defaultPrefix = request.session['defaultPrefix']

    formString = ""

    # get appinfo elements
    app_info = common.getAppInfo(element, namespace)

    # check if the element has a module
    has_module = hasModule(request, element)

    # check if XML element or attribute
    if element.tag == "{0}element".format(namespace):
        minOccurs, maxOccurs = manageOccurences(element)
        element_tag='element'
    elif element.tag == "{0}attribute".format(namespace):
        minOccurs, maxOccurs = manageAttrOccurrences(element)
        element_tag='attribute'

    # get the name of the element, go find the reference if there's one
    if 'ref' in element.attrib: # type is a reference included in the document
        ref = element.attrib['ref']
        refElement = None
        if ':' in ref:
            refSplit = ref.split(":")
            refNamespacePrefix = refSplit[0]
            refName = refSplit[1]
            namespaces = request.session['namespaces']
            refNamespace = namespaces[refNamespacePrefix]
            # TODO: manage namespaces/targetNamespaces, composed schema with different target namespaces
            # element = xmlTree.findall("./{0}element[@name='"+refName+"']".format(refNamespace))
            refElement = xmlTree.find("./{0}element[@name='{1}']".format(namespace, refName))
        else:
            refElement = xmlTree.find("./{0}element[@name='{1}']".format(namespace, ref))

        if refElement is not None:
            textCapitalized = refElement.attrib.get('name')
            element = refElement
            # check if the element has a module
            has_module = hasModule(request, element)
    else:
        textCapitalized = element.attrib.get('name')

    if element_tag =='element':
        # XML xpath:/root/element
        fullPath += "/" + textCapitalized
    elif element_tag =='attribute':
        fullPath += "/@" + textCapitalized
#     print fullPath

    # XSD xpath: /element/complexType/sequence
    xsd_xpath = etree.ElementTree(xmlTree).getpath(element)

    # init variables for buttons management
    addButton = False
    deleteButton = False
    nbOccurrences = 1 #nb of occurrences to render (can't be 0 or the user won't see this element at all)
    nbOccurrences_data = minOccurs # nb of occurrences in loaded data or in form being rendered (can be 0)
    xml_element = None
    use = ""
    removed = False

    # loading data in the form
    if request.session['curate_edit']:
        # get the number of occurrences in the data
        edit_elements = edit_data_tree.xpath(fullPath)
        nbOccurrences_data = len(edit_elements)

        if nbOccurrences_data == 0:
            use = "removed"
            removed = True

        # manage buttons
        if nbOccurrences_data < maxOccurs:
            addButton = True
        if nbOccurrences_data > minOccurs:
            deleteButton = True

    else: # starting an empty form
        # Don't generate the element if not necessary
        if CURATE_MIN_TREE and minOccurs == 0:
            use = "removed"
            removed = True

        if nbOccurrences_data < maxOccurs:
            addButton = True
        if nbOccurrences_data > minOccurs:
            deleteButton = True

    if has_module:
        # block maxOccurs to one, the module should take care of occurrences when the element is replaced
        nbOccurrences = 1
        maxOccurs = 1
    elif nbOccurrences_data > nbOccurrences:
        nbOccurrences = nbOccurrences_data

    xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nbOccurrences_data, minOccurs=minOccurs, maxOccurs=maxOccurs).save()

    # management of elements inside a choice (don't display if not part of the currently selected choice)
    if choiceInfo:
        choiceID = choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter)
        if request.session['curate_edit']:
            if len(edit_elements) == 0:
                formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                if CURATE_MIN_TREE:
                    form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=fullPath).save()
                    request.session['mapTagID'][choiceID] = str(form_element.id)
                    formString += "</ul>"
                    return formString
            else:
                formString += "<ul id=\"" + choiceID + "\" >"
        else:
            if (choiceInfo.counter > 0):
                formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                if CURATE_MIN_TREE:
                    form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=fullPath).save()
                    request.session['mapTagID'][choiceID] = str(form_element.id)
                    formString += "</ul>"
                    return formString
            else:
                formString += "<ul id=\"" + choiceID + "\" >"
    else:
        formString += "<ul>"


    elementType = getElementType(element, xmlTree, namespace, defaultPrefix)

    for x in range (0,int(nbOccurrences)):
        nb_html_tags = int(request.session['nb_html_tags'])
        tagID = "element" + str(nb_html_tags)
        nb_html_tags += 1
        request.session['nb_html_tags'] = str(nb_html_tags)
        form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=fullPath + '[' + str(x+1) +']', name=textCapitalized).save()
        request.session['mapTagID'][tagID] = str(form_element.id)

        # get the use from app info element
        app_info_use = app_info['use'] if 'use' in app_info else ''
        app_info_use = app_info_use if app_info_use is not None else ''
        use += ' ' + app_info_use

        # renders the name of the element
        formString += "<li class='"+ element_tag + ' ' + use +"' id='" + str(tagID) + "' tag='"+textCapitalized+"'>"
        if CURATE_COLLAPSE:
            if elementType is not None and elementType.tag == "{0}complexType".format(namespace): # the type is complex, can be collapsed
                formString += "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"

        label = app_info['label'] if 'label' in app_info else textCapitalized
        label = label if label is not None else ''
        formString += label
        # add buttons to add/remove elements
        buttons = ""
        if not (addButton is False and deleteButton is False):
            buttons = renderButtons(addButton, deleteButton, tagID[7:])

        # if element not removed
        if removed == False:
            # if module is present, replace default input by module
            if has_module:
                formString += generateModule(request, element, namespace, xsd_xpath, fullPath, edit_data_tree=edit_data_tree)
            else: # generate the type
                if elementType is None: # no complex/simple type
                    defaultValue = ""
                    if request.session['curate_edit']:
                        # if elements are found at this xpath
                        if len(edit_elements) > 0:
                            # it is an XML element
                            if element_tag == 'element':
                                # get the value of the element x
                                if edit_elements[x].text is not None:
                                    # set the value of the element
                                    defaultValue = edit_elements[x].text
                            # it is an XMl attribute
                            elif element_tag == 'attribute':
                                # get the value of the attribute
                                if edit_elements[x] is not None:
                                    # set the value of the element
                                    defaultValue = edit_elements[x]
                    elif 'default' in element.attrib:
                        # if the default attribute is present
                        defaultValue = element.attrib['default']

                    placeholder = 'placeholder="'+app_info['placeholder']+ '"' if 'placeholder' in app_info else ''
                    placeholder = placeholder if placeholder is not None else ''

                    tooltip = 'title="'+app_info['tooltip']+ '"' if 'tooltip' in app_info else ''
                    tooltip = tooltip if tooltip is not None else ''

                    formString += " <input type='text' value='"+ django.utils.html.escape(defaultValue) +"'" + placeholder + tooltip +"/>"
                    formString += buttons
                else: # complex/simple type
                    formString += buttons
                    if elementType.tag == "{0}complexType".format(namespace):
                        formString += generateComplexType(request, elementType, xmlTree, namespace, fullPath=fullPath+'['+ str(x+1) +']', edit_data_tree=edit_data_tree)
                    elif elementType.tag == "{0}simpleType".format(namespace):
                        formString += generateSimpleType(request, elementType, xmlTree, namespace, fullPath=fullPath+'['+ str(x+1) +']', edit_data_tree=edit_data_tree)
        else:
            formString += buttons

        formString += "</li>"
    formString += "</ul>"

    return formString


################################################################################
#
# Function Name: getElementType(element, xmlTree, namespace, defaultPrefix)
# Inputs:        element - XML element
#                xmlTree - XML tree of the template
#                namespace - Namespace used in the template
#                defaultPrefix -
# Outputs:       JSON data
# Exceptions:    None
# Description:   get XSD type to render.
#                Returns the type if found
#                    - complexType
#                    - simpleType
#                Returns None otherwise:
#                    - type from default namespace (xsd:...)
#                    - no type
#
################################################################################
def getElementType(element, xmlTree, namespace, defaultPrefix):
    try:
        if 'type' not in element.attrib: # element with type declared below it
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
        else: # element with type attribute
            if element.attrib.get('type') in common.getXSDTypes(defaultPrefix):
                return None
            elif element.attrib.get('type') is not None:  # FIXME is it possible?
                # TODO: manage namespaces
                # type of the element is complex
                typeName = element.attrib.get('type')
                if ':' in typeName:
                    typeName = typeName.split(":")[1]

                xpath = "./{0}complexType[@name='{1}']".format(namespace,typeName)
                elementType = xmlTree.find(xpath)
                if elementType is None:
                    # type of the element is simple
                    xpath = "./{0}simpleType[@name='{1}']".format(namespace,typeName)
                    elementType = xmlTree.find(xpath)
                return elementType
    except:
        print "getElementType: Something went wrong"
        return None
    return None


################################################################################
#
# Function Name: renderButtons(addButton, deleteButton, tagID)
# Inputs:        addButton - boolean
#                deleteButton - boolean
#                tagID - id of the tag to associate buttons to it
# Outputs:       JSON data
# Exceptions:    None
# Description:   Displays buttons for a duplicable/removable element
#
################################################################################
def renderButtons(addButton, deleteButton, tagID):
    add_button_type = type(addButton)
    del_button_type = type(deleteButton)

    if add_button_type is not bool:
        raise TypeError('add_button type is wrong (' + str(add_button_type) + 'received, bool needed')

    if del_button_type is not bool:
        raise TypeError('add_button type is wrong (' + str(del_button_type) + 'received, bool needed')

    formString = ""

    # the number of occurrences is fixed, don't need buttons
    if addButton == False and deleteButton == False:
        pass
    else:
        if (addButton == True):
            formString += "<span id='add"+ str(tagID) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(tagID)+");\"></span>"
        else:
            formString += "<span id='add"+ str(tagID) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',"+str(tagID)+");\"></span>"

        if (deleteButton == True):
            formString += "<span id='remove"+ str(tagID) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(tagID)+");\"></span>"
        else:
            formString += "<span id='remove"+ str(tagID) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',"+str(tagID)+");\"></span>"

    return formString


################################################################################
#
# Function Name: manageOccurences(request, element, elementID)
# Inputs:        request -
#                element -
#                elementID -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Store information about the occurrences of the element
#
################################################################################
def manageOccurences(element):

    minOccurs = 1
    maxOccurs = 1
    if ('minOccurs' in element.attrib):
        minOccurs = float(element.attrib['minOccurs'])
    if ('maxOccurs' in element.attrib):
        if (element.attrib['maxOccurs'] == "unbounded"):
            maxOccurs = float('inf')
        else:
            maxOccurs = float(element.attrib['maxOccurs'])

    return minOccurs, maxOccurs


################################################################################
#
# Function Name: manageAttrOccurrences(request, element, elementID)
# Inputs:        request -
#                element -
#                elementID -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Store information about the occurrences of the element
#
################################################################################
def manageAttrOccurrences(element):
    # FIXME use defaults to optional not required

    minOccurrs = 1
    maxOccurrs = 1
    if ('use' in element.attrib):
        if element.attrib['use'] == "optional":
            minOccurrs = 0
        elif element.attrib['use'] == "prohibited":
            minOccurrs = 0
            maxOccurrs = 0
        elif element.attrib['use'] == "required":
            pass

    return minOccurrs, maxOccurrs