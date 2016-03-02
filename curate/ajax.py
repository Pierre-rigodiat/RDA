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
from django.http import HttpResponse
from django.conf import settings
from io import BytesIO
# from cStringIO import StringIO
# from mgi.models import Template, XMLdata, XML2Download, Module, MetaSchema
from curate.parser import generate_form, generate_element, generate_sequence_absent, generate_element_absent, has_module, \
    get_element_type, generate_module, generate_complex_type, generate_simple_type, generate_sequence, generate_choice
from mgi.models import Template, XML2Download, MetaSchema
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


################################################################################
# 
# Class Name: ElementOccurrences
#
# Description: Store information about a occurrences of an element
#
################################################################################
class ElementOccurrences:
    "Class that stores information about element occurrences"
        
    def __init__(self, minOccurrences = 1, maxOccurrences = 1, nbOccurrences = 1):
        #min/max occurrence attributes
        self.minOccurrences = minOccurrences
        self.maxOccurrences = maxOccurrences
        
        #current number of occurrences of the element
        self.nbOccurrences = nbOccurrences        
    
    def __to_json__(self):
        return json.dumps(self, default=lambda o:o.__dict__)


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

    xmlString = request.session['xmlString']

    xsltPath = os.path.join(settings.SITE_ROOT, 'static', 'resources', 'xsl', 'xml2html.xsl')
    xslt = etree.parse(xsltPath)
    transform = etree.XSLT(xslt)
    xmlTree = ""
    if (xmlString != ""):
        dom = etree.fromstring(xmlString)
        newdom = transform(dom)
        xmlTree = str(newdom)

    response_dict = {"XMLHolder": xmlTree}
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
    form = generate_form(request)
    response_dict = {'xsdForm': form}
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
def download_xml(request):
    xmlString = request.session['xmlString']

    form_data_id = request.session['curateFormData']
    form_data = FormData.objects().get(pk=form_data_id)

    xml2download = XML2Download(title=form_data.name, xml=xmlString).save()
    xml2downloadID = str(xml2download.id)

    response_dict = {"xml2downloadID": xml2downloadID}
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
    xmlString = request.POST['xmlString']

    # set namespaces information in the XML document
    xmlString = common.manage_namespaces(request.POST['xmlString'],
                                         request.session['namespaces'],
                                         request.session['defaultPrefix'],
                                         request.session['target_namespace_prefix'])

    # get form data information
    form_data_id = request.session['curateFormData']
    form_data = FormData.objects().get(pk=form_data_id)

    xml2download = XML2Download(title=form_data.name, xml=xmlString).save()
    xml2downloadID = str(xml2download.id)

    response_dict = {"xml2downloadID": xml2downloadID}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


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
    if 'formString' in request.session:
        form_string = request.session['formString']
    else:
        form_string = ''

    # if the form is not generated
    if form_string == "":
        # this form was not created, generates it from the schema
        form_string += generate_form(request)

    # set the response
    response_dict = {'xsdForm': form_string}
    # save the form in the session
    request.session['formString'] = form_string

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    print 'END def generate_xsd_form(request)'


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

    namespaces = request.session['namespaces']
    defaultPrefix = request.session['defaultPrefix']
    xmlDocTreeStr = request.session['xmlDocTree']
    xmlDocTree = etree.ElementTree(etree.fromstring(xmlDocTreeStr))

    # render element
    namespace = "{" + namespaces[defaultPrefix] + "}"

    element = xmlDocTree.xpath(xml_element.xsd_xpath, namespaces=request.session['namespaces'])[0]

    # generating a choice, generate the parent element
    if tag == "choice":
        # can use generate_element to generate a choice never generated
        formString = generate_element(request, element, xmlDocTree, namespace, full_path=form_element.xml_xpath)
        # remove the opening and closing ul tags
        formString = formString[4:-4]
    else:
        if 'sequence' in element.tag:
            formString = generate_sequence_absent(request, element, xmlDocTree, namespace)
        else:
            # can't directly use generate_element because only need the body of the element not its title
            formString = generate_element_absent(request, element, xmlDocTree, form_element)


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

    tagID = "element"+ str(request.POST['tagID'])
    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(id=form_data_id)
    form_element_id = form_data.elements[tagID]
    form_element = FormElement.objects.get(id=form_element_id)
    xml_element = form_element.xml_element

    # Check that the element can be duplicated (should always be true)
    if (xml_element.nbOccurs < xml_element.maxOccurs):
        xml_element.nbOccurs += 1
        xml_element.save()
        # from 0 occurrence to 1, just enable the GUI
        if(xml_element.nbOccurs == 1):
            styleAdd=''
            if (xml_element.maxOccurs == 1):
                styleAdd = 'display:none'
            response_dict['occurs'] = 'zero'
            response_dict['tagID'] = str(tagID)
            response_dict['id'] = str(tagID[7:])
            response_dict['styleAdd'] = styleAdd
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
    if (xml_element.nbOccurs <= xml_element.maxOccurs):
        nb_html_tags = int(request.session['nb_html_tags'])
        namespaces = request.session['namespaces']
        defaultPrefix = request.session['defaultPrefix']
        xmlDocTreeStr = request.session['xmlDocTree']
        xmlDocTree = etree.ElementTree(etree.fromstring(xmlDocTreeStr))
        # render element
        namespace = "{" + namespaces[defaultPrefix] + "}"

        sequenceChild = xmlDocTree.xpath(xml_element.xsd_xpath, namespaces=request.session['namespaces'])[0]

        if sequenceChild.tag == "{0}element".format(namespace):
            element_tag='element'
        elif sequenceChild.tag == "{0}attribute".format(namespace):
            element_tag='attribute'
        elif sequenceChild.tag == "{0}sequence".format(namespace):
            element_tag = 'sequence'
        elif sequenceChild.tag == "{0}choice".format(namespace):
            element_tag = 'choice'

        # get appinfo elements
        app_info = common.getAppInfo(sequenceChild, namespace)

        _has_module = has_module(request, sequenceChild)

        if element_tag == "element" or element_tag == "attribute":
            # type is a reference included in the document
            if 'ref' in sequenceChild.attrib:
                ref = sequenceChild.attrib['ref']
                refElement = None
                if ':' in ref:
                    refSplit = ref.split(":")
                    refNamespacePrefix = refSplit[0]
                    refName = refSplit[1]
                    refNamespace = namespaces[refNamespacePrefix]
                    # TODO: manage namespaces/targetNamespaces, composed schema with different target namespaces
                    # element = xmlTree.findall("./{0}element[@name='"+refName+"']".format(refNamespace))
                    refElement = xmlDocTree.find("./{0}element[@name='{1}']".format(namespace, refName))
                else:
                    refElement = xmlDocTree.find("./{0}element[@name='{1}']".format(namespace, ref))

                if refElement is not None:
                    textCapitalized = refElement.attrib.get('name')
                    sequenceChild = refElement
            else:
                textCapitalized = sequenceChild.attrib.get('name')

            elementType = get_element_type(sequenceChild, xmlDocTree, namespace, defaultPrefix)
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
            formString += "<li class='"+ element_tag + ' ' + use +"' id='" + str(newTagID) + "' tag='"+textCapitalized+"'>"
            if CURATE_COLLAPSE:
                if elementType is not None and elementType.tag == "{0}complexType".format(namespace): # the type is complex, can be collapsed
                    formString += "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"

            label = app_info['label'] if 'label' in app_info else textCapitalized
            label = label if label is not None else ''
            formString += label

            # if module is present, replace default input by module
            if _has_module:
                formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
                formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"
                formString += generate_module(request, sequenceChild, namespace, xml_element.xsd_xpath, new_xml_xpath)
            else: # generate the type
                if elementType is None: # no complex/simple type
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
                    if elementType.tag == "{0}complexType".format(namespace):
                        formString += generate_complex_type(request, elementType, xmlDocTree, namespace, full_path=new_xml_xpath)
                    elif elementType.tag == "{0}simpleType".format(namespace):
                        formString += generate_simple_type(request, elementType, xmlDocTree, namespace, full_path=new_xml_xpath)

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
                    if (child.tag == "{0}element".format(namespace)):
                        formString += generate_element(request, child, xmlDocTree, namespace, full_path=new_xml_xpath)
                    elif (child.tag == "{0}sequence".format(namespace)):
                        formString += generate_sequence(request, child, xmlDocTree, namespace, full_path=new_xml_xpath)
                    elif (child.tag == "{0}choice".format(namespace)):
                        formString += generate_choice(request, child, xmlDocTree, namespace, full_path=new_xml_xpath)
                    elif (child.tag == "{0}any".format(namespace)):
                        pass
                    elif (child.tag == "{0}group".format(namespace)):
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
                    if (child.tag == "{0}element".format(namespace)):
                        if child.attrib.get('name') is not None:
                            opt_value = opt_label = child.attrib.get('name')
                        else:
                            opt_value = opt_label = child.attrib.get('ref')
                            if ':' in opt_label:
                                opt_label = opt_label.split(':')[1]

                        formString += "<option value='" + opt_value + "'>" + opt_label + "</option></b><br>"
                    elif (child.tag == "{0}group".format(namespace)):
                        pass
                    elif (child.tag == "{0}choice".format(namespace)):
                        pass
                    elif (child.tag == "{0}sequence".format(namespace)):
                        formString += "<option value='sequence" + str(nbSequence) + "'>Sequence " + str(nbSequence) + "</option></b><br>"
                        nbSequence += 1
                    elif (child.tag == "{0}any".format(namespace)):
                        pass

            formString += "</select>"


            formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
            formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"


            for (counter, choiceChild) in enumerate(list(sequenceChild)):
                if choiceChild.tag == "{0}element".format(namespace):
                    formString += generate_element(request, choiceChild, xmlDocTree, namespace, common.ChoiceInfo(chooseIDStr,counter), full_path=new_xml_xpath)
                elif (choiceChild.tag == "{0}group".format(namespace)):
                    pass
                elif (choiceChild.tag == "{0}choice".format(namespace)):
                    pass
                elif (choiceChild.tag == "{0}sequence".format(namespace)):
                    formString += generate_sequence(request, choiceChild, xmlDocTree, namespace, common.ChoiceInfo(chooseIDStr,counter), full_path=new_xml_xpath)
                elif (choiceChild.tag == "{0}any".format(namespace)):
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
    xmlString = request.POST['xmlString']

    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(id=form_data_id)
    form_data.xml_data = xmlString
    form_data.save()

    return HttpResponse(json.dumps({}), content_type='application/javascript')


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
        # set namespaces information in the XML document
        xmlString = common.manage_namespaces(request.POST['xmlString'],
                                             request.session['namespaces'],
                                             request.session['defaultPrefix'],
                                             request.session['target_namespace_prefix'])
        # validate XML document
        common.validateXMLDocument(template_id, xmlString)
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

    if template_id in MetaSchema.objects.all().values_list('schemaId'):
        meta = MetaSchema.objects.get(schemaId=template_id)
        xmlDocData = meta.flat_content
    else:
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

    if template_id in MetaSchema.objects.all().values_list('schemaId'):
        meta = MetaSchema.objects.get(schemaId=template_id)
        xmlDocData = meta.flat_content
    else:
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