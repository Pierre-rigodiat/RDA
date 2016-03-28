################################################################################
#
# File Name: ajax.py
# Application: curate
# Purpose:   AJAX methods used by the Curator
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

# import re
from copy import deepcopy

from bson.objectid import ObjectId
from django.http import HttpResponse
from django.conf import settings
from io import BytesIO
from django.core.servers.basehttp import FileWrapper
from cStringIO import StringIO

# from cStringIO import StringIO
# from mgi.models import Template, XMLdata, XML2Download, Module, MetaSchema
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from curate.models import SchemaElement
from curate.parser import generate_form, generate_element, generate_sequence_absent, generate_element_absent, has_module, \
    get_element_type, generate_module, generate_complex_type, generate_simple_type, generate_sequence, generate_choice, \
    get_element_namespace, load_schema_data_in_db
from curate.renderer.xml import XmlRenderer
from mgi.common import LXML_SCHEMA_NAMESPACE
# from mgi.models import Template, XML2Download
from curate.renderer.list import ListRenderer
from mgi.models import Template, XML2Download
from mgi.models import FormElement, XMLElement, FormData
# from mgi.settings import CURATE_MIN_TREE, CURATE_COLLAPSE
from mgi.settings import CURATE_COLLAPSE
import json
# from bson.objectid import ObjectId
from mgi import common
# from django.template import Context, loader
import lxml.html as html
import lxml.etree as etree
import django.utils.html
from django.contrib import messages
# from modules import get_module_view
import os
# from django.http.request import HttpRequest
import urllib2
from utils.XSDflattener.XSDflattener import XSDFlattenerURL

######################################################################################################################
# AJAX Requests
# TODO Needs to be moved in views
#########################

################################################################################
#
# Function Name: change_owner_form(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Change the form owner
#
################################################################################
def change_owner_form(request):
    if 'formId' and 'userID' in request.POST:
        form_data_id = request.POST['formID']
        user_id = request.POST['userID']
        try:
            form_data = FormData.objects().get(pk=form_data_id)
            form_data.user = user_id
            form_data.save()
            messages.add_message(request, messages.INFO, 'Form Owner changed with success !')
        except Exception, e:
            return HttpResponse({},status=400)
    return HttpResponse({})


################################################################################
#
# Function Name: cancel_form(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Cancel a form being entered
#
################################################################################
def cancel_form(request):
    try:
        form_data_id = request.session['curateFormData']
        form_data = FormData.objects().get(pk=form_data_id)
        # cascade delete references
        for form_element_id in form_data.elements.values():
            try:
                form_element = FormElement.objects().get(pk=form_element_id)
                if form_element.xml_element is not None:
                    try:
                        xml_element = XMLElement.objects().get(pk=str(form_element.xml_element.id))
                        xml_element.delete()
                    except:
                        # raise an exception when element not found
                        pass
                form_element.delete()
            except:
                # raise an exception when element not found
                pass
        form_data.delete()
        messages.add_message(request, messages.INFO, 'Form deleted with success.')
        return HttpResponse({},status=204)
    except Exception, e:
        return HttpResponse({},status=400)


################################################################################
#
# Function Name: delete_form(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Deletes a saved form
#
################################################################################
def delete_form(request):
    if 'id' in request.GET:
        form_data_id = request.GET['id']
        try:
            form_data = FormData.objects().get(pk=form_data_id)
            # cascade delete references
            for form_element_id in form_data.elements.values():
                try:
                    form_element = FormElement.objects().get(pk=form_element_id)
                    if form_element.xml_element is not None:
                        try:
                            xml_element = XMLElement.objects().get(pk=str(form_element.xml_element.id))
                            xml_element.delete()
                        except:
                            # raise an exception when element not found
                            pass
                    form_element.delete()
                except:
                    # raise an exception when element not found
                    pass
            form_data.delete()
            messages.add_message(request, messages.INFO, 'Form deleted with success.')
        except Exception, e:
            return HttpResponse({},status=400)
    return HttpResponse({})


################################################################################
#
# Function Name: load_xml(request)
# Inputs:        request -
# Outputs:       JSON data with templateSelected
# Exceptions:    None
# Description:   Loads the XML data in the view data page. First transforms the data.
#
################################################################################
def load_xml(request):
    if 'form_id' not in request.session:
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    xml_form_id = SchemaElement.objects.get(pk=request.session['form_id'])

    xml_renderer = XmlRenderer(xml_form_id)
    xml_string = xml_renderer.render()

    xslt_path = os.path.join(settings.SITE_ROOT, 'static', 'resources', 'xsl', 'xml2html.xsl')
    xslt = etree.parse(xslt_path)
    transform = etree.XSLT(xslt)

    xml_tree = ""
    if xml_string != "":
        dom = etree.fromstring(xml_string)
        newdom = transform(dom)
        xml_tree = str(newdom)

    response_dict = {"XMLHolder": xml_tree}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: clear_fields(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Clears fields of the HTML form. Also restore the occurrences.
#
################################################################################
def clear_fields(request):
    # form = generate_form(request)
    # response_dict = {'xsdForm': form}
    # return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    del request.session['form_id']

    return generate_xsd_form(request)


################################################################################
#
# Function Name: download_xml(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Make the current XML document available for download.
#
################################################################################
def download_xml(request):
    # xmlString = request.session['xmlString']
    #
    # form_data_id = request.session['curateFormData']
    # form_data = FormData.objects().get(pk=form_data_id)
    #
    # xml2download = XML2Download(title=form_data.name, xml=xmlString).save()
    # xml2downloadID = str(xml2download.id)
    xml_renderer = XmlRenderer(request.session['form_id'])
    response_dict = {"xml2downloadID": xml_renderer.render()}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: download_xml(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Make the current XML document available for download.
#
################################################################################
def download_current_xml(request):
    # get the XML String built from form
    # xml_string = request.POST['xmlString']
    #
    # xml_tree_str = str(request.session['xmlDocTree'])
    #
    # # set namespaces information in the XML document
    # xml_string = common.manage_namespaces(xml_string, xml_tree_str)
    #
    # # get form data information
    # form_data_id = request.session['curateFormData']
    # form_data = FormData.objects().get(pk=form_data_id)
    #
    # xml2download = XML2Download(title=form_data.name, xml=xml_string).save()
    # xml2downloadID = str(xml2download.id)
    #
    # response_dict = {"xml2downloadID": xml2downloadID}
    # return HttpResponse(json.dumps(response_dict), content_type='application/javascript')

    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(pk=ObjectId(form_data_id))

    form_id = request.session['form_id']
    xml_root_element = SchemaElement.objects.get(pk=form_id)
    xml_renderer = XmlRenderer(xml_root_element)
    xml_data = StringIO(xml_renderer.render())

    response = HttpResponse(FileWrapper(xml_data), content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=' + form_data.name + '.xml'
    return response


################################################################################
#
# Function Name: init_curate(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Reinitialize data structures
#
################################################################################
def init_curate(request):
    if 'formString' in request.session:
        del request.session['formString']

    if 'form_id' in request.session:
        del request.session['form_id']

    if 'form_name' in request.session:
        del request.session['form_name']

    if 'xmlDocTree' in request.session:
        del request.session['xmlDocTree']

    return HttpResponse(json.dumps({}), content_type='application/javascript')


################################################################################
#
# Function Name: generateXSDTreeForEnteringData(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Renders HTMl form for display.
#
################################################################################
def generate_xsd_form(request):
    print 'BEGIN def generate_xsd_form(request)'

    # get the form when going back and forth with review step
    # if 'formString' in request.session:
    #     form_string = request.session['formString']
    # else:
    #     form_string = ''
    #
    # # if the form is not generated
    # if form_string == "":
    #     # this form was not created, generates it from the schema
    #     form_string += generate_form(request)
    #
    # # set the response
    # response_dict = {'xsdForm': form_string}
    # # save the form in the session
    # request.session['formString'] = form_string

    if 'form_id' in request.session:
        root_element_id = request.session['form_id']
    else:  # If this is a new form, generate it and store the root ID
        root_element_id = generate_form(request)
        request.session['form_id'] = str(root_element_id)

    root_element = SchemaElement.objects.get(pk=root_element_id)

    renderer = ListRenderer(root_element)
    form_string = renderer.render()

    # set the response
    response_dict = {'xsdForm': form_string}
    # save the form in the session
    # request.session['formString'] = form_string

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: generate_absent(request)
# Inputs:        request -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Generate element absent from the form
#
################################################################################
def generate_absent(request):
    response_dict = {}

    request.session['mapTagID'] = {}

    formString = ""

    tag = str(request.POST['tag'])
    id = str(request.POST['tagID'])
    tagID = tag + id
    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(id=form_data_id)
    form_element_id = form_data.elements[tagID]
    form_element = FormElement.objects.get(id=form_element_id)
    xml_element = form_element.xml_element

    # if the xml element is from an imported schema
    if xml_element.schema_location is not None:
        # open the imported file
        ref_xml_schema_file = urllib2.urlopen(xml_element.schema_location)
        # get the content of the file
        ref_xml_schema_content = ref_xml_schema_file.read()
        # build the XML tree
        xmlDocTree = etree.parse(BytesIO(ref_xml_schema_content.encode('utf-8')))
        # get the namespaces from the imported schema
        namespaces = common.get_namespaces(BytesIO(str(ref_xml_schema_content)))
    else:
        # get the content of the XML tree
        xmlDocTreeStr = request.session['xmlDocTree']
        # build the XML tree
        xmlDocTree = etree.ElementTree(etree.fromstring(xmlDocTreeStr))
        # get the namespaces
        namespaces = common.get_namespaces(BytesIO(str(xmlDocTreeStr)))

    # flatten the includes
    flattener = XSDFlattenerURL(etree.tostring(xmlDocTree))
    xml_doc_tree_str = flattener.get_flat()
    xmlDocTree = etree.parse(BytesIO(xml_doc_tree_str.encode('utf-8')))

    # render element
    element = xmlDocTree.xpath(xml_element.xsd_xpath, namespaces=namespaces)[0]

    if "element" in element.tag and tag == "choice":
        # can use generate_element to generate a choice never generated
        formString = generate_element(request, element, xmlDocTree, full_path=form_element.xml_xpath,
                                      schema_location=xml_element.schema_location)
        # remove the opening and closing ul tags
        formString = formString[4:-4]
    elif "element" in element.tag:
        # generate only the body of the element (not the title)
        formString = generate_element_absent(request, element, xmlDocTree, form_element,
                                             schema_location=xml_element.schema_location)
    elif "sequence" in element.tag:
        formString = generate_sequence_absent(request, element, xmlDocTree,
                                              schema_location=xml_element.schema_location)

    # build HTML tree for the form
    htmlTree = html.fromstring(request.POST['xsdForm'])
    # get the element we are working on
    currentElement = htmlTree.get_element_by_id(tagID)

    try:
        generated_element = html.fragment_fromstring(formString)
        if generated_element.tag == "ul":
            currentElement.append(generated_element)
        elif generated_element.tag == "div":
            currentElement.insert(3, generated_element)
        else:
            currentElement.insert(0, generated_element)
    except:
        for generated_element in html.fragments_fromstring(formString):
            currentElement.append(generated_element)


    # update the number of elements in database
    xml_element.nbOccurs = 1
    xml_element.save()

    if tag == "element":
        # updates buttons
        addButton = False
        deleteButton = False

        if (xml_element.nbOccurs < xml_element.maxOccurs):
            addButton = True
        if (xml_element.nbOccurs > xml_element.minOccurs):
            deleteButton = True

        # enable add button if we can add more
        if(addButton == True):
            htmlTree.get_element_by_id("add" + str(id)).attrib['style'] = ''
        else:
            htmlTree.get_element_by_id("add" + str(id)).attrib['style'] = 'display:none'
        # enable delete button to come back to 0 occurs
        if(deleteButton == True):
            htmlTree.get_element_by_id("remove" + str(id)).attrib['style'] = ''
        else:
            htmlTree.get_element_by_id("remove" + str(id)).attrib['style'] = 'display:none'

    response_dict['xsdForm'] = html.tostring(htmlTree)

    # add new tagID to map
    form_data.elements.update(request.session['mapTagID'])
    form_data.save()
    del request.session['mapTagID']

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: can_duplicate(request)
# Inputs:        request -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Test if element can be duplicated
#
################################################################################
def can_duplicate(request):
    response_dict = {}

    tag_id = "element" + str(request.POST['tagID'])
    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(id=form_data_id)
    form_element_id = form_data.elements[tag_id]
    form_element = FormElement.objects.get(id=form_element_id)
    xml_element = form_element.xml_element

    # Check that the element can be duplicated (should always be true)
    if xml_element.nbOccurs < xml_element.maxOccurs:
        xml_element.nbOccurs += 1
        xml_element.save()
        # from 0 occurrence to 1, just enable the GUI
        if xml_element.nbOccurs == 1:
            style_add = ''
            if xml_element.maxOccurs == 1:
                style_add = 'display:none'
            response_dict['occurs'] = 'zero'
            response_dict['tagID'] = str(tag_id)
            response_dict['id'] = str(tag_id[7:])
            response_dict['styleAdd'] = style_add
        else:
            response_dict['occurs'] = 'notzero'
    else:
        pass

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: duplicate(request)
# Inputs:        request -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Duplicate an occurrence of an element
#
################################################################################
def duplicate(request):
    # FIXME send code to the parser
    response_dict = {}

    request.session['mapTagID'] = {}

    formString = ""

    tagID = "element"+ str(request.POST['tagID'])
    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(id=form_data_id)
    form_element_id = form_data.elements[tagID]
    form_element = FormElement.objects.get(id=form_element_id)
    xml_element = form_element.xml_element

    # Check that the element can be duplicated
    if xml_element.nbOccurs <= xml_element.maxOccurs:
        # if the xml element is from an imported schema
        if xml_element.schema_location is not None:
            # open the imported file
            ref_xml_schema_file = urllib2.urlopen(xml_element.schema_location)
            # get the content of the file
            ref_xml_schema_content = ref_xml_schema_file.read()
            # build the XML tree
            xmlDocTree = etree.parse(BytesIO(ref_xml_schema_content.encode('utf-8')))
            # get the namespaces from the imported schema
            namespaces = common.get_namespaces(BytesIO(str(ref_xml_schema_content)))
        else:
            # get the content of the XML tree
            xmlDocTreeStr = request.session['xmlDocTree']
            # build the XML tree
            xmlDocTree = etree.ElementTree(etree.fromstring(xmlDocTreeStr))
            # get the namespaces
            namespaces = common.get_namespaces(BytesIO(str(xmlDocTreeStr)))
        nb_html_tags = int(request.session['nb_html_tags'])

        # flatten the includes
        flattener = XSDFlattenerURL(etree.tostring(xmlDocTree))
        xml_doc_tree_str = flattener.get_flat()
        xmlDocTree = etree.parse(BytesIO(xml_doc_tree_str.encode('utf-8')))

        # render element
        sequenceChild = xmlDocTree.xpath(xml_element.xsd_xpath, namespaces=namespaces)[0]

        if sequenceChild.tag == "{0}element".format(LXML_SCHEMA_NAMESPACE):
            element_tag='element'
        elif sequenceChild.tag == "{0}attribute".format(LXML_SCHEMA_NAMESPACE):
            element_tag='attribute'
        elif sequenceChild.tag == "{0}sequence".format(LXML_SCHEMA_NAMESPACE):
            element_tag = 'sequence'
        elif sequenceChild.tag == "{0}choice".format(LXML_SCHEMA_NAMESPACE):
            element_tag = 'choice'

        # get appinfo elements
        app_info = common.getAppInfo(sequenceChild)

        _has_module = has_module(sequenceChild)

        if element_tag == "element" or element_tag == "attribute":
            # get the name of the element, go find the reference if there's one
            if 'ref' in sequenceChild.attrib:  # type is a reference included in the document
                ref = sequenceChild.attrib['ref']
                # refElement = None
                if ':' in ref:
                    # split the ref element
                    ref_split = ref.split(":")
                    # get the namespace prefix
                    ref_namespace_prefix = ref_split[0]
                    # get the element name
                    ref_name = ref_split[1]
                    # test if referencing element within the same schema (same target namespace)
                    target_namespace_prefix = common.get_target_namespace_prefix(namespaces, xmlDocTree)
                    if target_namespace_prefix == ref_namespace_prefix:
                        ref_element = xmlDocTree.find("./{0}{1}[@name='{2}']".format(LXML_SCHEMA_NAMESPACE,
                                                                                   element_tag, ref_name))
                    else:
                        # TODO: manage ref to imported elements (different target namespace)
                        # get all import elements
                        imports = xmlDocTree.findall('//{}import'.format(LXML_SCHEMA_NAMESPACE))
                        # find the referred document using the prefix
                        for el_import in imports:
                            import_ns = el_import.attrib['namespace']
                            if namespaces[ref_namespace_prefix] == import_ns:
                                # get the location of the schema
                                ref_xml_schema_url = el_import.attrib['schemaLocation']
                                # set the schema location to save in database
                                schema_location = ref_xml_schema_url
                                # download the file
                                ref_xml_schema_file = urllib2.urlopen(ref_xml_schema_url)
                                # read the content of the file
                                ref_xml_schema_content = ref_xml_schema_file.read()
                                # build the tree
                                xml_tree = etree.parse(BytesIO(ref_xml_schema_content.encode('utf-8')))
                                # look for includes
                                includes = xml_tree.findall('//{}include'.format(LXML_SCHEMA_NAMESPACE))
                                # if includes are present
                                if len(includes) > 0:
                                    # create a flattener with the file content
                                    flattener = XSDFlattenerURL(ref_xml_schema_content)
                                    # flatten the includes
                                    ref_xml_schema_content = flattener.get_flat()
                                    # build the tree
                                    xml_tree = etree.parse(BytesIO(ref_xml_schema_content.encode('utf-8')))

                                ref_element = xml_tree.find("./{0}{1}[@name='{2}']".format(LXML_SCHEMA_NAMESPACE,
                                                                                           element_tag, ref_name))
                                break
                else:
                    ref_element = xmlDocTree.find("./{0}{1}[@name='{2}']".format(LXML_SCHEMA_NAMESPACE,
                                                                                 element_tag, ref))

                if ref_element is not None:
                    text_capitalized = ref_element.attrib.get('name')
                    sequenceChild = ref_element
                    # check if the element has a module
                    _has_module = has_module(request, sequenceChild)
                else:
                    # the element was not found where it was supposed to be
                    # could be a use case too complex for the current parser
                    print "Ref element not found" + str(sequenceChild.attrib)
                    return formString
            else:
                textCapitalized = sequenceChild.attrib.get('name')

            default_prefix = common.get_default_prefix(namespaces)
            target_namespace_prefix = common.get_target_namespace_prefix(namespaces, xmlDocTree)

            # get the element namespace
            element_ns = get_element_namespace(sequenceChild, xmlDocTree)
            tag_ns = " xmlns={0} ".format(element_ns) if element_ns is not None else ''

            element_type, xmlDocTree, schema_location = get_element_type(sequenceChild, xmlDocTree, namespaces,
                                                                         default_prefix, target_namespace_prefix)

            nb_html_tags = int(request.session['nb_html_tags'])
            newTagID = "element" + str(nb_html_tags)
            nb_html_tags += 1
            request.session['nb_html_tags'] = str(nb_html_tags)
            new_xml_xpath = form_element.xml_xpath[0:form_element.xml_xpath.rfind('[') + 1] + str(xml_element.nbOccurs) + ']'
            new_form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=new_xml_xpath, name=textCapitalized).save()
            form_data.elements[newTagID] = new_form_element.id
            form_data.save()

            # get the use from app info element
            app_info_use = app_info['use'] if 'use' in app_info else ''
            app_info_use = app_info_use if app_info_use is not None else ''
            use = app_info_use

            # renders the name of the element
            formString += "<li class='"+ element_tag + ' ' + use +"' id='" + str(newTagID) + "' "
            formString += "tag='{0}' {1}>".format(django.utils.html.escape(textCapitalized),
                                            django.utils.html.escape(tag_ns))
            if CURATE_COLLAPSE:
                if element_type is not None and element_type.tag == "{0}complexType".format(LXML_SCHEMA_NAMESPACE): # the type is complex, can be collapsed
                    formString += "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"

            label = app_info['label'] if 'label' in app_info else textCapitalized
            label = label if label is not None else ''
            formString += label

            # if module is present, replace default input by module
            if _has_module:
                formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
                formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"
                formString += generate_module(request, sequenceChild, xml_element.xsd_xpath, new_xml_xpath,
                                              xml_tree=xmlDocTree)
            else: # generate the type
                if element_type is None: # no complex/simple type
                    defaultValue = ""
                    if 'default' in sequenceChild.attrib:
                        # if the default attribute is present
                        defaultValue = sequenceChild.attrib['default']

                    placeholder = 'placeholder="'+app_info['placeholder']+ '"' if 'placeholder' in app_info else ''
                    placeholder = placeholder if placeholder is not None else ''

                    tooltip = 'title="'+app_info['tooltip']+ '"' if 'tooltip' in app_info else ''
                    tooltip = tooltip if tooltip is not None else ''

                    formString += " <input type='text' value='"+ django.utils.html.escape(defaultValue) +"'" + placeholder + tooltip +"/>"

                    formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
                    formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"
                else: # complex/simple type
                    formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
                    formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"
                    if element_type.tag == "{0}complexType".format(LXML_SCHEMA_NAMESPACE):
                        formString += generate_complex_type(request, element_type, xmlDocTree, full_path=new_xml_xpath,
                                                            schema_location=xml_element.schema_location)
                    elif element_type.tag == "{0}simpleType".format(LXML_SCHEMA_NAMESPACE):
                        formString += generate_simple_type(request, element_type, xmlDocTree, full_path=new_xml_xpath,
                                                           schema_location=xml_element.schema_location)

            formString += "</li>"


        elif element_tag == "sequence":
            newTagID = "element" + str(nb_html_tags)
            nb_html_tags += 1
            request.session['nb_html_tags'] = str(nb_html_tags)
            new_xml_xpath = form_element.xml_xpath[0:form_element.xml_xpath.rfind('[') + 1] + str(xml_element.nbOccurs) + ']'
            new_form_element = FormElement(html_id=newTagID, xml_element=xml_element, xml_xpath=form_element.xml_xpath).save()
            form_data.elements[newTagID] = new_form_element.id
            form_data.save()
            text = "Sequence"

            if len(list(sequenceChild)) > 0 :
                formString += "<li class='sequence' id='" + str(newTagID) + "'>"
                formString += "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>" if CURATE_COLLAPSE else ""
                formString += text
            else:
                formString += "<li class='sequence' id='" + str(newTagID) + "'>" + text

            formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
            formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"

            # generates the sequence
            if(len(list(sequenceChild)) != 0):
                for child in sequenceChild:
                    if (child.tag == "{0}element".format(LXML_SCHEMA_NAMESPACE)):
                        formString += generate_element(request, child, xmlDocTree, full_path=new_xml_xpath,
                                                       schema_location=xml_element.schema_location)
                    elif (child.tag == "{0}sequence".format(LXML_SCHEMA_NAMESPACE)):
                        formString += generate_sequence(request, child, xmlDocTree, full_path=new_xml_xpath,
                                                        schema_location=xml_element.schema_location)
                    elif (child.tag == "{0}choice".format(LXML_SCHEMA_NAMESPACE)):
                        formString += generate_choice(request, child, xmlDocTree, full_path=new_xml_xpath,
                                                      schema_location=xml_element.schema_location)
                    elif (child.tag == "{0}any".format(LXML_SCHEMA_NAMESPACE)):
                        pass
                    elif (child.tag == "{0}group".format(LXML_SCHEMA_NAMESPACE)):
                        pass
            formString += "</li>"
        elif element_tag == "choice":
            newTagID = "element" + str(nb_html_tags)
            nb_html_tags += 1
            request.session['nb_html_tags'] = str(nb_html_tags)
            new_xml_xpath = form_element.xml_xpath[0:form_element.xml_xpath.rfind('[') + 1] + str(xml_element.nbOccurs) + ']'
            new_form_element = FormElement(html_id=newTagID, xml_element=xml_element, xml_xpath=form_element.xml_xpath).save()
            form_data.elements[newTagID] = new_form_element.id
            form_data.save()

            nbChoicesID = int(request.session['nbChoicesID'])
            chooseID = nbChoicesID
            chooseIDStr = 'choice' + str(chooseID)
            nbChoicesID += 1
            request.session['nbChoicesID'] = str(nbChoicesID)

            formString += "<li class='choice' id='" + str(newTagID) + "'>Choose<select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"

            nbSequence = 1

            # generates the choice
            if(len(list(sequenceChild)) != 0):
                for child in sequenceChild:
                    if (child.tag == "{0}element".format(LXML_SCHEMA_NAMESPACE)):
                        if child.attrib.get('name') is not None:
                            opt_value = opt_label = child.attrib.get('name')
                        else:
                            opt_value = opt_label = child.attrib.get('ref')
                            if ':' in opt_label:
                                opt_label = opt_label.split(':')[1]

                        formString += "<option value='" + opt_value + "'>" + opt_label + "</option></b><br>"
                    elif (child.tag == "{0}group".format(LXML_SCHEMA_NAMESPACE)):
                        pass
                    elif (child.tag == "{0}choice".format(LXML_SCHEMA_NAMESPACE)):
                        pass
                    elif (child.tag == "{0}sequence".format(LXML_SCHEMA_NAMESPACE)):
                        formString += "<option value='sequence" + str(nbSequence) + "'>Sequence " + str(nbSequence) + "</option></b><br>"
                        nbSequence += 1
                    elif (child.tag == "{0}any".format(LXML_SCHEMA_NAMESPACE)):
                        pass

            formString += "</select>"


            formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
            formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"


            for (counter, choiceChild) in enumerate(list(sequenceChild)):
                if choiceChild.tag == "{0}element".format(LXML_SCHEMA_NAMESPACE):
                    formString += generate_element(request, choiceChild, xmlDocTree,
                                                   common.ChoiceInfo(chooseIDStr,counter), full_path=new_xml_xpath,
                                                   schema_location=xml_element.schema_location)
                elif (choiceChild.tag == "{0}group".format(LXML_SCHEMA_NAMESPACE)):
                    pass
                elif (choiceChild.tag == "{0}choice".format(LXML_SCHEMA_NAMESPACE)):
                    pass
                elif (choiceChild.tag == "{0}sequence".format(LXML_SCHEMA_NAMESPACE)):
                    formString += generate_sequence(request, choiceChild, xmlDocTree,
                                                    common.ChoiceInfo(chooseIDStr,counter), full_path=new_xml_xpath,
                                                    schema_location=xml_element.schema_location)
                elif (choiceChild.tag == "{0}any".format(LXML_SCHEMA_NAMESPACE)):
                    pass

            formString += "</li>"


        htmlTree = html.fromstring(request.POST['xsdForm'])
        currentElement = htmlTree.get_element_by_id(tagID)
        parent = currentElement.getparent()
        parent.append(html.fragment_fromstring(formString))
        addButton = False
        deleteButton = False

        if (xml_element.nbOccurs < xml_element.maxOccurs):
            addButton = True
        if (xml_element.nbOccurs > xml_element.minOccurs):
            deleteButton = True


        elementsOfCurrentType = parent.findall("li")
        for element in elementsOfCurrentType:
            idOfElement = element.attrib['id'][7:]
            if(addButton == True):
                htmlTree.get_element_by_id("add" + str(idOfElement)).attrib['style'] = ''
            else:
                htmlTree.get_element_by_id("add" + str(idOfElement)).attrib['style'] = 'display:none'
            if (deleteButton == True):
                htmlTree.get_element_by_id("remove" + str(idOfElement)).attrib['style'] = ''
            else:
                htmlTree.get_element_by_id("remove" + str(idOfElement)).attrib['style'] = 'display:none'

        response_dict['xsdForm'] = html.tostring(htmlTree)

    # add new tagID to map
    form_data.elements.update(request.session['mapTagID'])
    form_data.save()

    del request.session['mapTagID']
    request.session.modified = True
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: can_remove(request)
# Inputs:        request -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Test if element can be removed from the form
#
################################################################################
def can_remove(request):
    response_dict = {}

    tagID = "element"+ str(request.POST['tagID'])
    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(id=form_data_id)
    form_element_id = form_data.elements[tagID]
    form_element = FormElement.objects.get(id=form_element_id)
    xml_element = form_element.xml_element


    # test if the element can be removed (should always be true)
    if (xml_element.nbOccurs > xml_element.minOccurs):
        xml_element.nbOccurs -= 1
        xml_element.save()
        if (xml_element.nbOccurs == 0):
            response_dict['occurs'] = 'zero'
            response_dict['tagID'] = str(tagID)
        else:
            response_dict['occurs'] = 'notzero'
    else:
        pass

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: remove(request)
# Inputs:        request -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Remove an element from the form
#
################################################################################
def remove(request):
    response_dict = {}

    tagID = "element"+ str(request.POST['tagID'])
    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(id=form_data_id)
    form_element_id = form_data.elements[tagID]
    form_element = FormElement.objects.get(id=form_element_id)
    xml_element = form_element.xml_element

    if (xml_element.nbOccurs >= xml_element.minOccurs):
        addButton = False
        deleteButton = False

        if (xml_element.nbOccurs < xml_element.maxOccurs):
            addButton = True
        if (xml_element.nbOccurs > xml_element.minOccurs):
            deleteButton = True

        htmlTree = html.fromstring(request.POST['xsdForm'])
        currentElement = htmlTree.get_element_by_id(tagID)
        parent = currentElement.getparent()

        # remove element
        parent.remove(currentElement)

        # update siblings buttons add/remove to be consistent with new number of occurrencesS
        elementsOfCurrentType = parent.findall("li")
        sibling_xpath_idx = 1
        for element in elementsOfCurrentType:
            # update element xpath in database
            tagIDOfElement = element.attrib['id']
            sibling_form_element_id = form_data.elements[tagIDOfElement]
            sibling_form_element = FormElement.objects.get(id=sibling_form_element_id)
            # get the new xpath of the sibling element
            new_sibling_xpath = form_element.xml_xpath[0:form_element.xml_xpath.rfind('[') + 1] + str(sibling_xpath_idx) + ']'
            if sibling_form_element.xml_xpath != new_sibling_xpath:
                # change the xpath in the database if different only (delete last element won't change all the other xpaths)
                sibling_form_element.xml_xpath = new_sibling_xpath
                sibling_form_element.save()
            sibling_xpath_idx += 1

            # FIXME some of this can be done within the parser
            # update element on the form
            idOfElement = tagIDOfElement[7:]
            if(addButton == True):
                htmlTree.get_element_by_id("add" + str(idOfElement)).attrib['style'] = ''
            else:
                htmlTree.get_element_by_id("add" + str(idOfElement)).attrib['style'] = 'display:none'
            if (deleteButton == True):
                htmlTree.get_element_by_id("remove" + str(idOfElement)).attrib['style'] = ''
            else:
                htmlTree.get_element_by_id("remove" + str(idOfElement)).attrib['style'] = 'display:none'

        # remove element from database
        form_element.delete()
        del form_data.elements[tagID]
        response_dict = {'xsdForm': html.tostring(htmlTree)}

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: save_form(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Save the current form in MongoDB
#
#
################################################################################
def save_form(request):
    # xmlString = request.POST['xmlString']
    #
    # form_data_id = request.session['curateFormData']
    # form_data = FormData.objects.get(id=form_data_id)
    # form_data.xml_data = xmlString
    # form_data.save()
    #
    # return HttpResponse(json.dumps({}), content_type='application/javascript')

    if 'id' not in request.POST or 'value' not in request.POST:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)

    # print request.POST['inputs']

    input_element = SchemaElement.objects.get(pk=request.POST['id'])
    input_element.value = request.POST['value']
    input_element.save()

    return HttpResponse(json.dumps({}), content_type='application/json')


################################################################################
#
# Function Name: validate_xml_data(request)
# Inputs:        request -
#                xmlString - XML string generated from the form
#                xsdForm -  Current form
# Outputs:
# Exceptions:    None
# Description:   Check if the current XML document is valid according to the template
#
#
################################################################################
def validate_xml_data(request):

    template_id = request.session['currentTemplateID']
    request.session['xmlString'] = ""
    try:
        xsd_tree_str = str(request.session['xmlDocTree'])

        # set namespaces information in the XML document
        xmlString = common.manage_namespaces(request.POST['xmlString'], xsd_tree_str)
        # xmlString = request.POST['xmlString']
        # validate XML document
        common.validateXMLDocument(xmlString, xsd_tree_str)
    except etree.XMLSyntaxError, xse:
        #xmlParseEntityRef exception: use of & < > forbidden
        message= "Validation Failed. </br> May be caused by : </br> - Syntax problem </br> - Use of forbidden symbols : '&' or '<' or '>'"
        response_dict = {'errors': message}
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    except Exception, e:
        message= e.message.replace('"', '\'')
        response_dict = {'errors': message}
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')

    request.session['xmlString'] = xmlString
    request.session['formString'] = request.POST['xsdForm']

    return HttpResponse(json.dumps({}), content_type='application/javascript')


################################################################################
#
# Function Name: view_data(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Save the content of the current form in session before redirection to view data
#
################################################################################
def view_data(request):
    print 'BEGIN def saveXMLData(request)'

    request.session['formString'] = request.POST['form_content']
    return HttpResponse(json.dumps({}), content_type='application/javascript')

    print 'END def saveXMLData(request)'


################################################################################
#
# Function Name: set_current_template(request)
# Inputs:        request -
# Outputs:       JSON data with success or failure
# Exceptions:    None
# Description:   Set the current template to input argument.  Template is read
#                into an xsdDocTree for use later.
#
################################################################################
def set_current_template(request):
    print 'BEGIN def set_current_template(request)'

    template_id = request.POST['templateID']

    # reset global variables
    request.session['xmlString'] = ""
    request.session['formString'] = ""

    request.session['currentTemplateID'] = template_id
    request.session.modified = True

    templateObject = Template.objects.get(pk=template_id)
    xmlDocData = templateObject.content

    XMLtree = etree.parse(BytesIO(xmlDocData.encode('utf-8')))
    request.session['xmlDocTree'] = etree.tostring(XMLtree)

    print 'END def set_current_template(request)'
    return HttpResponse(json.dumps({}), content_type='application/javascript')


################################################################################
#
# Function Name: set_current_user_template(request)
# Inputs:        request -
# Outputs:       JSON data with success or failure
# Exceptions:    None
# Description:   Set the current template to input argument.  Template is read
#                into an xsdDocTree for use later. This case is for templates
#                defined using the composer.
#
################################################################################
def set_current_user_template(request):
    print 'BEGIN def setCurrentTemplate(request)'

    template_id = request.POST['templateID']

    # reset global variables
    request.session['xmlString'] = ""
    request.session['formString'] = ""

    request.session['currentTemplateID'] = template_id
    request.session.modified = True

    templateObject = Template.objects.get(pk=template_id)

    xmlDocData = templateObject.content

    XMLtree = etree.parse(BytesIO(xmlDocData.encode('utf-8')))
    request.session['xmlDocTree'] = etree.tostring(XMLtree)

    print 'END def setCurrentTemplate(request)'
    return HttpResponse(json.dumps({}), content_type='application/javascript')


################################################################################
#
# Function Name: verify_template_is_selected(request)
# Inputs:        request -
# Outputs:       JSON data with templateSelected
# Exceptions:    None
# Description:   Verifies the current template is selected.
#
################################################################################
def verify_template_is_selected(request):
    print 'BEGIN def verify_template_is_selected(request)'
    if 'currentTemplateID' in request.session:
        templateSelected = 'yes'
    else:
        templateSelected = 'no'

    print 'END def verify_template_is_selected(request)'

    response_dict = {'templateSelected': templateSelected}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


def gen_abs(request):
    """

    :param request:
    :return:
    """
    # TODO Most of the function can be moved to the parser core
    element_id = request.POST['id']
    sub_element = SchemaElement.objects.get(pk=element_id)
    element_list = SchemaElement.objects(children=element_id)

    if len(element_list) == 0:
        raise ValueError("No SchemaElement found")
    elif len(element_list) > 1:
        raise ValueError("More than one SchemaElement found")

    schema_element = element_list[0]

    rendering_element = SchemaElement()
    rendering_element.tag = schema_element.tag
    rendering_element.options = schema_element.options
    rendering_element.value = schema_element.value

    # namespaces = request.session['namespaces']
    # default_prefix = request.session['defaultPrefix']
    xml_doc_tree_str = request.session['xmlDocTree']
    xml_doc_tree = etree.ElementTree(etree.fromstring(xml_doc_tree_str))

    schema_location = None
    if 'schema_location' in schema_element.options:
        schema_location = schema_element.options['schema_location']

    # if the xml element is from an imported schema
    if schema_location is not None:
        # open the imported file
        ref_xml_schema_file = urllib2.urlopen(schema_element.options['schema_location'])
        # get the content of the file
        ref_xml_schema_content = ref_xml_schema_file.read()
        # build the XML tree
        # xmlDocTree = etree.parse(BytesIO(ref_xml_schema_content.encode('utf-8')))
        # get the namespaces from the imported schema
        namespaces = common.get_namespaces(BytesIO(str(ref_xml_schema_content)))
    else:
        # get the content of the XML tree
        # xmlDocTreeStr = request.session['xmlDocTree']
        # # build the XML tree
        # xmlDocTree = etree.ElementTree(etree.fromstring(xmlDocTreeStr))
        # get the namespaces
        namespaces = common.get_namespaces(BytesIO(str(xml_doc_tree_str)))

    # render element
    # namespace = "{" + namespaces[default_prefix] + "}"

    xpath_element = schema_element.options['xpath']
    xsd_xpath = xpath_element['xsd']

    xml_xpath = None
    if 'xml' in xpath_element:
        xml_xpath = xpath_element['xml']

    xml_element = xml_doc_tree.xpath(xsd_xpath, namespaces=namespaces)[0]

    # generating a choice, generate the parent element
    if schema_element.tag == "choice":
        # can use generate_element to generate a choice never generated
        form_string = generate_element(request, xml_element, xml_doc_tree, full_path=xml_xpath)
    elif schema_element.tag == 'sequence':
        form_string = generate_sequence_absent(request, xml_element, xml_doc_tree)
    else:
        # can't directly use generate_element because only need the body of the element not its title
        form_string = generate_element_absent(request, xml_element, xml_doc_tree, schema_element)
        # form_string = generate_element(request, xml_element, xml_doc_tree, schema_element)

    db_tree = form_string[1]

    # Saving the tree in MongoDB
    tree_root = load_schema_data_in_db(db_tree)

    # Updating the elements
    rendering_element.children = [tree_root]
    schema_element.update(add_to_set__children=[tree_root])

    if len(sub_element.children) == 0:
        schema_element.update(pull__children=element_id)

    schema_element.reload()
    rendering_element.save(force_insert=True)

    # Rendering the generated element
    # FIXME add the ability to render just a subelement (only one elem-iter)
    renderer = ListRenderer(rendering_element)
    html_form = renderer.render(True)

    rendering_element.delete()

    return HttpResponse(html_form)
    # return HttpResponse()


def rem_bis(request):
    element_id = request.POST['id']
    # sub_element = SchemaElement.objects.get(pk=element_id)
    element_list = SchemaElement.objects(children=element_id)

    if len(element_list) == 0:
        raise ValueError("No SchemaElement found")
    elif len(element_list) > 1:
        raise ValueError("More than one SchemaElement found")

    # Removing the element from the data structure
    schema_element = element_list[0]
    schema_element.update(pull__children=element_id)

    schema_element.reload()

    children_number = len(schema_element.children)

    # TODO Move it to parser function
    # FIXME Sequence elem it might not work
    if len(schema_element.children) == 0:
        elem_iter = SchemaElement()

        if schema_element.tag == 'element':
            elem_iter.tag = 'elem-iter'
        elif schema_element.tag == 'choice':
            elem_iter.tag = 'choice-iter'
        elif schema_element.tag == 'sequence':
            elem_iter.tag = 'sequence-iter'

        elem_iter.save()
        schema_element.update(add_to_set__children=[elem_iter])
        schema_element.reload()

    if children_number > schema_element.options['min']:
        return HttpResponse()
    else:  # len(schema_element.children) == schema_element.options['min']
        renderer = ListRenderer(schema_element)
        html_form = renderer.render(True)

        return HttpResponse(html_form)

