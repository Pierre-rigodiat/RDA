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

import re
from django.http import HttpResponse
from django.conf import settings
from io import BytesIO
from cStringIO import StringIO
from mgi.models import Template, Htmlform, Jsondata, XML2Download, Module, MetaSchema
import json
from mgi import common
from django.template import Context, loader

import lxml.html as html
import lxml.etree as etree

# Specific to RDF
import rdfPublisher

#XSL file loading
import os


#Class definition

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
        


################################################################################
#
# Function Name: get_hdf5_string(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   Get the values of an excel spreadsheet from the session variable
#                
#
################################################################################
def get_hdf5_string(request):
    if 'spreadsheetXML' in request.session:
        spreadsheetXML = request.session['spreadsheetXML']
        request.session['spreadsheetXML'] = ""
    else:
        spreadsheetXML = ""

    response_dict = {'spreadsheetXML': spreadsheetXML}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: update_form_list(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def update_form_list(request):
    template_id = request.session['currentTemplateID']

    select_options = ""
    saved_forms = Htmlform.objects(schema=template_id)
    if len(saved_forms) > 0:
        for htmlForm in saved_forms:
            select_options += "<option value=\"" + str(htmlForm.id) + "\">" + htmlForm.title + "</option>"
    else:
        select_options = "<option value=\"none\">None Exist"

    response_dict = {'options': select_options}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: save_html_form(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   Save the current form in MongoDB
#                
#
################################################################################
def save_html_form(request):

    save_as = request.POST['saveAs']
    content = request.POST['content']
    template_id = request.session['currentTemplateID']
    occurrences = request.session['occurrences']

    Htmlform(title=save_as, schema=template_id, content=content, occurrences=str(occurrences)).save()

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
    
    # TODO: namespaces
    xmlString = common.manageNamespace(template_id, request.POST['xmlString'])      
    try:
        common.validateXMLDocument(template_id, xmlString)
    except Exception, e:
        message= e.message.replace('"', '\'')
        response_dict = {'errors': message}
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')

    request.session['xmlString'] = xmlString
    request.session['formString'] = request.POST['xsdForm']

    return HttpResponse(json.dumps({}), content_type='application/javascript')
    

################################################################################
#
# Function Name: save_xml_data_to_db(request)
# Inputs:        request -
# Outputs:       
# Exceptions:    None
# Description:   Save the current XML document in MongoDB. The document is also
#                converted to RDF format and sent to a Jena triplestore.
#                
#
################################################################################
def save_xml_data_to_db(request):
    print 'BEGIN def saveXMLDataToDB(request)'

    response_dict = {}
    xmlString = request.session['xmlString']
    templateID = request.session['currentTemplateID']

    if xmlString != "":
        try:
            newJSONData = Jsondata(schemaID=templateID, xml=xmlString, title=request.POST['saveAs'])
            docID = newJSONData.save()
            
            xsltPath = os.path.join(settings.SITE_ROOT, 'static/resources/xsl/xml2rdf3.xsl')
            xslt = etree.parse(xsltPath)
            root = xslt.getroot()
            namespace = root.nsmap['xsl']
            URIparam = root.find("{" + namespace +"}param[@name='BaseURI']") #find BaseURI tag to insert the project URI
            URIparam.text = settings.PROJECT_URI + str(docID)
        
            # SPARQL : transform the XML into RDF/XML
            transform = etree.XSLT(xslt)
            # add a namespace to the XML string, transformation didn't work well using XML DOM    
            template = Template.objects.get(pk=templateID)
            xmlStr = xmlString.replace('>',' xmlns="' + settings.PROJECT_URI + template.hash + '">', 1) #TODO: OR schema name...
            # domXML.attrib['xmlns'] = projectURI + schemaID #didn't work well
            domXML = etree.fromstring(xmlStr)
            domRDF = transform(domXML)
        
            # SPARQL : get the rdf string
            rdfStr = etree.tostring(domRDF)
        
            # SPARQL : send the rdf to the triplestore
            rdfPublisher.sendRDF(rdfStr)
    
        except Exception, e:
            message = e.message.replace('"', '\'')
            response_dict['errors'] = message
    else:
        response_dict['errors'] = "No data to save."

    print 'END def saveXMLDataToDB(request,saveAs)'
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


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
# Function Name: load_form_for_entry(request)
# Inputs:        request -
# Outputs:       
# Exceptions:    None
# Description:   Load a saved form in the page
#                
#
################################################################################
def load_form_for_entry(request):
    try:
        form_selected = request.POST['form_selected']
        html_form_object = Htmlform.objects.get(id=form_selected)
        request.session['occurrences'] = eval(html_form_object.occurrences)

        response_dict = {'xsdForm': html_form_object.content}
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    except:
        return HttpResponse(json.dumps({}), content_type='application/javascript')


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

    template_filename = request.POST['templateFilename']
    template_id = request.POST['templateID']

    # reset global variables
    request.session['xmlString'] = ""
    request.session['formString'] = ""

    request.session['currentTemplate'] = template_filename
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
    request.session['currentTemplate'] = templateObject.title
    
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
def generateSequence(request, element, xmlTree, namespace, choiceInfo=None, fullPath=""):
    #(annotation?,(element|group|choice|sequence|any)*)
    nb_html_tags = int(request.session['nb_html_tags'])
    
    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
    minOccurs, maxOccurs = manageOccurences(element)
    
    if (minOccurs != 1) or (maxOccurs != 1):       
        text = "Sequence"
        addButton, deleteButton, nbOccurrences = manageButtons(minOccurs, maxOccurs)
        # XSD xpath
        xsd_xpath = etree.ElementTree(xmlTree).getpath(element)

        if edit:
            edit_elements = edit_data_tree.xpath(fullPath)

        # save xml element to duplicate sequence
        nbOccurs_to_save = nbOccurrences
        # Update element information to match the number of elements from the XML document
        if edit:
            # if the element is absent, nbOccurences is 0
            if len(edit_elements) == 0:
                nbOccurs_to_save = 0

        xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nbOccurs_to_save, minOccurs=minOccurs, maxOccurs=maxOccurs).save()
        if choiceInfo:
            choiceID = choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter)
            if edit:
                if len(edit_elements) == 0:
                    formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                    if min_build == True:
                        form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=None).save()
                        request.session['mapTagID'][choiceID] = str(form_element.id)
                        formString += "</ul>"
                        return formString
                else:
                    formString += "<ul id=\"" + choiceID + "\" >"
            else:
                if (choiceInfo.counter > 0):
                    formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                    if min_build == True:
                        form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=None).save()
                        request.session['mapTagID'][choiceID] = str(form_element.id)
                        formString += "</ul>"
                        return formString
                else:
                    formString += "<ul id=\"" + choiceID + "\" >"
        else:
            formString += "<ul>"
        
        for x in range (0,int(nbOccurrences)):
            tagID = "element" + str(nb_html_tags)
            nb_html_tags += 1
            request.session['nb_html_tags'] = str(nb_html_tags)
            if (minOccurs != 1) or (maxOccurs != 1):
                form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=fullPath + '[' + str(x+1) +']').save()
                request.session['mapTagID'][tagID] = str(form_element.id)
            # if tag not closed:  <element/>
            if len(list(element)) > 0 :
                formString += "<li class='sequence' id='" + str(tagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + text
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
                        formString += generateElement(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath)
                    elif (child.tag == "{0}sequence".format(namespace)):
                        formString += generateSequence(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath)
                    elif (child.tag == "{0}choice".format(namespace)):
                        formString += generateChoice(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath)
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
                    formString += generateElement(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath)
                elif (child.tag == "{0}sequence".format(namespace)):
                    formString += generateSequence(request, child, xmlTree, namespace, choiceInfo, fullPath=fullPath)
                elif (child.tag == "{0}choice".format(namespace)):
                    formString += generateChoice(request, child, xmlTree, namespace,choiceInfo, fullPath=fullPath)
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
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML choice
# 
################################################################################
def generateChoice(request, element, xmlTree, namespace, choiceInfo=None, fullPath=""):
    #(annotation?,(element|group|choice|sequence|any)*)
    nbChoicesID = int(request.session['nbChoicesID'])
    nb_html_tags = int(request.session['nb_html_tags'])
    
    formString = ""
    
    #remove the annotations
    removeAnnotations(element, namespace)
         
    # multiple roots or no min/maxOccurs
    addButton = False
    deleteButton = False
    nbOccurrences = 1
    if (not isinstance(element,list)):
        minOccurs, maxOccurs = manageOccurences(element)
        if (minOccurs != 1) or (maxOccurs != 1):
            addButton, deleteButton, nbOccurrences = manageButtons(minOccurs, maxOccurs)
        # XSD xpath
        xsd_xpath = etree.ElementTree(xmlTree).getpath(element)
 
    
    edit_elements = []
    try:
        edit_elements = edit_data_tree.xpath(fullPath)
    except:
        pass 

    xml_element = None
    if not isinstance(element,list) and ((minOccurs != 1) or (maxOccurs != 1)):
        # save xml element to duplicate sequence
        nbOccurs_to_save = nbOccurrences
        # Update element information to match the number of elements from the XML document
        if edit:
            # if the element is absent, nbOccurences is 0
            if len(edit_elements) == 0:
                nbOccurs_to_save = 0
        xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nbOccurs_to_save, minOccurs=minOccurs, maxOccurs=maxOccurs).save()

    if choiceInfo:
        choiceID = choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter)
        if edit:
            if len(edit_elements) == 0:
                formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                if min_build == True:
                    form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=None).save()
                    request.session['mapTagID'][choiceID] = str(form_element.id)
                    formString += "</ul>"
                    return formString
            else:
                formString += "<ul id=\"" + choiceID + "\" >"
        else:
            if (choiceInfo.counter > 0):
                formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                if min_build == True:
                    form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=None).save()
                    request.session['mapTagID'][choiceID] = str(form_element.id)
                    formString += "</ul>"
                    return formString
            else:
                formString += "<ul id=\"" + choiceID + "\" >"
    else:
        formString += "<ul>"
    
    if edit:
        if len(edit_elements) > 0:
            nbOccurrences = len(edit_elements)
    
    for x in range (0,int(nbOccurrences)):
        tagID = "element" + str(nb_html_tags)
        nb_html_tags += 1  
        request.session['nb_html_tags'] = str(nb_html_tags)
        if not isinstance(element,list) and ((minOccurs != 1) or (maxOccurs != 1)):
            form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=fullPath + '[' + str(x+1) +']').save()
            request.session['mapTagID'][tagID] = str(form_element.id)
        chooseID = nbChoicesID
        chooseIDStr = 'choice' + str(chooseID)
        nbChoicesID += 1
        request.session['nbChoicesID'] = str(nbChoicesID)
        
        formString += "<li class='choice' id='" + str(tagID) + "'>Choose<select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"
        
        nbSequence = 1

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
                    
                    if edit:
                        if len(edit_data_tree.xpath(elementPath)) == 0:    
                            formString += "<option value='" + opt_value + "'>" + opt_label + "</option></b><br>"
                        else:
                            formString += "<option value='" + opt_value + "' selected>" + opt_label + "</option></b><br>"
                    else:
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
                formString += generateElement(request, choiceChild, xmlTree, namespace, common.ChoiceInfo(chooseIDStr,counter), fullPath=fullPath)
            elif (choiceChild.tag == "{0}group".format(namespace)):
                pass
            elif (choiceChild.tag == "{0}choice".format(namespace)):
                pass
            elif (choiceChild.tag == "{0}sequence".format(namespace)):
                formString += generateSequence(request, choiceChild, xmlTree, namespace, common.ChoiceInfo(chooseIDStr,counter), fullPath=fullPath)
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
# Description:   Generates a section of the form that represents an XML choice
# 
################################################################################
def generateSimpleType(request, element, xmlTree, namespace, fullPath):
    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
    if hasModule(request, element):
        # XSD xpath: /element/complexType/sequence
        xsd_xpath = etree.ElementTree(xmlTree).getpath(element)
        formString += generateModule(request, element, namespace, xsd_xpath, fullPath)
        return formString
    
    if (list(element) != 0):
        child = element[0] 
        if child.tag == "{0}restriction".format(namespace):
            formString += generateRestriction(request, child, xmlTree, namespace, fullPath)
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
def generateRestriction(request, element, xmlTree, namespace, fullPath=""):
    formString = ""
    
    removeAnnotations(element, namespace)
    
    enumeration = element.findall('{0}enumeration'.format(namespace))
    if len(enumeration) > 0:
        formString += "<select>"
        if edit:
            edit_elements = edit_data_tree.xpath(fullPath) 
            selected_value = None   
            if len(edit_elements) > 0:
                if edit_elements[0].text is not None:
                    selected_value = edit_elements[0].text                 
            for enum in enumeration:
                if selected_value is not None and enum.attrib.get('value') == selected_value:
                    formString += "<option value='" + enum.attrib.get('value')  + "' selected>" + enum.attrib.get('value') + "</option>"
                else:
                    formString += "<option value='" + enum.attrib.get('value')  + "'>" + enum.attrib.get('value') + "</option>"
        else:
            for enum in enumeration:
                formString += "<option value='" + enum.attrib.get('value')  + "'>" + enum.attrib.get('value') + "</option>"
        formString += "</select>"
    else:
        simpleType = element.find('{0}simpleType'.format(namespace))
        if simpleType is not None:
            formString += generateSimpleType(request, simpleType, xmlTree, namespace, fullPath=fullPath)
        else:        
            formString += " <input type='text'/>"
            
    return formString


def generateExtension(request, element, xmlTree, namespace, fullPath=""):
    formString = ""
    
    removeAnnotations(element, namespace)
    
    simpleType = element.find('{0}simpleType'.format(namespace))
    if simpleType is not None:
        formString += generateSimpleType(request, simpleType, xmlTree, namespace, fullPath=fullPath)
    else:
        defaultValue = ""
        if edit:
            edit_elements = edit_data_tree.xpath(fullPath)
            if len(edit_elements) > 0:
                if edit_elements[0].text is not None:
                    defaultValue = edit_elements[0].text
        formString += " <input type='text' value='"+ defaultValue +"'/>" 
            
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
def generateComplexType(request, element, xmlTree, namespace, fullPath):
    #(annotation?,(simpleContent|complexContent|((group|all|choice|sequence)?,((attribute|attributeGroup)*,anyAttribute?))))

    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
    if hasModule(request, element):
        # XSD xpath: /element/complexType/sequence
        xsd_xpath = etree.ElementTree(xmlTree).getpath(element)
        formString += generateModule(request, element, namespace, xsd_xpath, fullPath)
        return formString
    
    # is it a simple content?
    complexTypeChild = element.find('{0}simpleContent'.format(namespace))
    if complexTypeChild is not None:
        formString += generateSimpleContent(request, complexTypeChild, xmlTree, namespace, fullPath=fullPath)
        return formString
    
    # does it contain a attributes?
    complexTypeChildren = element.findall('{0}attribute'.format(namespace))
    if len(complexTypeChildren) > 0:
        for attribute in complexTypeChildren:
            formString += generateElement(request, attribute, xmlTree, namespace, fullPath=fullPath)
    
    # does it contain sequence or all?
    complexTypeChild = element.find('{0}sequence'.format(namespace))
    if complexTypeChild is not None:
        formString += generateSequence(request, complexTypeChild, xmlTree, namespace, fullPath=fullPath)
    else:
        complexTypeChild = element.find('{0}all'.format(namespace))
        if complexTypeChild is not None:
            formString += generateSequence(request, complexTypeChild, xmlTree, namespace, fullPath=fullPath)
        else:
            # does it contain choice ?
            complexTypeChild = element.find('{0}choice'.format(namespace))
            if complexTypeChild is not None:
                formString += generateChoice(request, complexTypeChild, xmlTree, namespace, fullPath=fullPath)
            else:
                formString += ""        
    
    return formString 


def generateSimpleContent(request, element, xmlTree, namespace, fullPath):
    #(annotation?,(restriction|extension))
    
    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
    # generates the sequence
    if(len(list(element)) != 0):
        child = element[0]    
        if (child.tag == "{0}restriction".format(namespace)):            
            formString += generateRestriction(request, child, xmlTree, namespace, fullPath)
        elif (child.tag == "{0}extension".format(namespace)):
            formString += generateExtension(request, child, xmlTree, namespace, fullPath)
    
    return formString


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
def generateModule(request, element, namespace, xsd_xpath=None, xml_xpath=None):    
    formString = ""
    
    reload_data = None
    if edit:
        edit_element = edit_data_tree.xpath(xml_xpath)[0]
        if element.tag == "{0}element".format(namespace):
            # leaf: get the value            
            if len(list(edit_element)) == 0:
                reload_data = edit_data_tree.xpath(xml_xpath)[0].text
            else: # branch: get the whole branch
                reload_data = etree.tostring(edit_data_tree.xpath(xml_xpath)[0])
        elif element.tag == "{0}attribute".format(namespace):
            pass
        elif element.tag == "{0}complexType".format(namespace) or element.tag == "{0}simpleType".format(namespace):
            # leaf: get the value            
            if len(list(edit_element)) == 0:
                reload_data = edit_data_tree.xpath(xml_xpath)[0].text
            else: # branch: get the whole branch
                reload_data = etree.tostring(edit_data_tree.xpath(xml_xpath)[0])
    
    # check if a module is set for this element    
    if '{http://mdcs.ns}_mod_mdcs_' in element.attrib:
        # get the url of the module
        url = element.attrib['{http://mdcs.ns}_mod_mdcs_']
        # check that the url is registered in the system
        
#         view = get_module_view(url)
# 
#         request.GET = {
#             'url': url,
#             #     'data': '<xml> or value',
#         }
#         formString += view(request).content
    return formString

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

path = "C:\\Users\\GAS2\\Documents\\Material Doc\\Carrie\\data\\data-3.xml"
# path = "C:\\Users\\GAS2\\Documents\\Material Doc\\Ken\\trc\\trc\\2012\\vol-57\\issue-1\\je200950f.xml" #800
# path = "C:\\Users\\GAS2\\Documents\\Material Doc\\Ken\\trc\\trc\\2012\\vol-57\\issue-11\\je300530z.xml" #28000
# path = "C:\\Users\\gas2\\Dev\\MGI\\mdcs\\inputs\\data\\diff\\data-3.xml"
# path = "C:\\Users\\gas2\\Dev\\MGI\\mdcs\\inputs\\data\\trc\\je300530z.xml" #28000
# path = "C:\\Users\\gas2\\Dev\\MGI\\mdcs\\inputs\\data\\trc\\je200950f.xml" #800

with open(path,'r') as xml_file:
    edit_data = xml_file.read()
edit_data_tree = etree.fromstring(edit_data)
edit = True
siblings_xpath = False # store xpath of all leaves elements and modules (siblings module)
min_build = True # build minimum tree

from mgi.models import FormElement, XMLElement, FormData
# temp_data = TempData(user="user_id", template="template_id", xml_data="")


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
def generateElement(request, element, xmlTree, namespace, choiceInfo=None, fullPath=""):
    defaultPrefix = request.session['defaultPrefix']
    
    formString = ""

    # remove the annotations
    removeAnnotations(element, namespace)
    
    has_module = hasModule(request, element)
        
    if element.tag == "{0}element".format(namespace):
        minOccurs, maxOccurs = manageOccurences(element)
        addButton, deleteButton, nbOccurrences = manageButtons(minOccurs, maxOccurs)
        element_tag='element'
    elif element.tag == "{0}attribute".format(namespace):
        minOccurs, maxOccurs = manageAttrOccurrences(element)
        addButton, deleteButton, nbOccurrences = manageButtons(minOccurs, maxOccurs)
        element_tag='attribute'
        
    # type is a reference included in the document
    if 'ref' in element.attrib: 
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
            # remove the annotations
            removeAnnotations(element, namespace)
    else:
        textCapitalized = element.attrib.get('name')
    
    # XML xpath:/root/element
    fullPath += "/" + textCapitalized
#     print fullPath
    
    # XSD xpath: /element/complexType/sequence
    xsd_xpath = etree.ElementTree(xmlTree).getpath(element)

    removed = ""
    if edit:
        # See if the element is present in the XML document
        edit_elements = edit_data_tree.xpath(fullPath)
        if len(edit_elements) > 0:
            nbOccurrences = len(edit_elements)
        else:
            # Disable element from the GUI if not present in the XML document
            if minOccurs == 0:
                removed = " removed"
                addButton = True
                deleteButton = False
    else:
        # Don't generate the element if not necessary
        if min_build and minOccurs == 0:
            removed = " removed"
            addButton = True
            deleteButton = False
  
    
    xml_element = None
    if not(minOccurs == 1 and maxOccurs == 1) or min_build == True:
        nbOccurs_to_save = nbOccurrences 
        # Update element information to match the number of elements from the XML document
        if edit:
            # if the element is absent, nbOccurences is 0
            if len(removed) > 0:
                nbOccurs_to_save = 0
        else:
            if len(removed) > 0:
                nbOccurs_to_save = 0
        # store info about element in database
        xml_element = XMLElement(xsd_xpath=xsd_xpath, nbOccurs=nbOccurs_to_save, minOccurs=minOccurs, maxOccurs=maxOccurs).save()
  
    
    # management of elements inside a choice
    if choiceInfo:
        choiceID = choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter)
        if edit:
            if len(edit_elements) == 0:
                formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                if min_build == True:
                    form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=fullPath).save()
                    request.session['mapTagID'][choiceID] = str(form_element.id)
                    formString += "</ul>"
                    return formString
            else:
                formString += "<ul id=\"" + choiceID + "\" >"
        else:
            if (choiceInfo.counter > 0):
                formString += "<ul id=\"" + choiceID + "\" class=\"notchosen\">"
                if min_build == True:
                    form_element = FormElement(html_id=choiceID, xml_element=xml_element, xml_xpath=fullPath).save()
                    request.session['mapTagID'][choiceID] = str(form_element.id)
                    formString += "</ul>"
                    return formString
            else:
                formString += "<ul id=\"" + choiceID + "\" >"
    else:
        formString += "<ul>"
    
    if 'type' not in element.attrib:
        # element with type declared below it                                                                          
        for x in range (0,int(nbOccurrences)): 
            nb_html_tags = int(request.session['nb_html_tags'])    
            # build the tagID and increase by 1
            tagID = "element" + str(nb_html_tags)
            nb_html_tags += 1
            request.session['nb_html_tags'] = str(nb_html_tags)
            form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=fullPath + '[' + str(x+1) +']', name=textCapitalized).save()
            request.session['mapTagID'][tagID] = str(form_element.id)
#             form_data.elements.append(form_element)
             
            # if tag not closed:  <element/>
            if len(list(element)) > 0 :
                if element[0].tag == "{0}complexType".format(namespace):
                    formString += "<li class='"+ element_tag + removed +"' id='" + str(tagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + textCapitalized
                else: 
                    formString += "<li class='"+ element_tag + removed +"' id='" + str(tagID) + "'>" + textCapitalized
            else:
                formString += "<li class='"+ element_tag + removed +"' id='" + str(tagID) + "'>" + textCapitalized
            
            if not (addButton is False and deleteButton is False):
                formString += renderButtons(addButton, deleteButton, tagID[7:])
            
            if len(removed) == 0:
                # if module, replace element by module
                if has_module:
                    formString += generateModule(request, element, namespace, xsd_xpath, fullPath+'['+ str(x+1) +']')
                else:   
                    # if tag not closed:  <element/>
                    if len(list(element)) > 0 :                
                        if element[0].tag == "{0}complexType".format(namespace):
                            formString += generateComplexType(request, element[0], xmlTree, namespace, fullPath=fullPath+'['+ str(x+1) +']')
                        elif element[0].tag == "{0}simpleType".format(namespace):
                            formString += generateSimpleType(request, element[0], xmlTree, namespace, fullPath=fullPath+'['+ str(x+1) +']')
                    else:
                        # if tag closed:  <element/>
                        pass
            formString += "</li>"
    elif element.attrib.get('type') in common.getXSDTypes(defaultPrefix):
        # element is an element from default XML namespace                      
        for x in range (0,int(nbOccurrences)):
            nb_html_tags = int(request.session['nb_html_tags'])           
            tagID = "element" + str(nb_html_tags)
            nb_html_tags += 1
            request.session['nb_html_tags'] = str(nb_html_tags)           
            form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=fullPath + '[' + str(x+1) +']', name=textCapitalized).save()
            request.session['mapTagID'][tagID] = str(form_element.id)
#             form_data.elements.append(form_element)                
            
            defaultValue = ""
            if edit:
                # if elements are found at this xpath
                if len(edit_elements) > 0:
                    # get the value of the element x
                    if edit_elements[x].text is not None:
                        # set the value of the element
                        defaultValue = edit_elements[x].text
            elif 'default' in element.attrib:
                # if the default attribute is present
                defaultValue = element.attrib['default']

            formString += "<li class='"+ element_tag + removed +"' id='" + str(tagID) + "'>" + textCapitalized
                
            # if module is present, replace input by module       
            if has_module:
                    formString += generateModule(request, element, namespace, xsd_xpath, fullPath+'['+ str(x+1) +']')
            else:
                formString += " <input type='text' value='"+ defaultValue +"'/>" 
            
            if not (addButton is False and deleteButton is False):
                formString += renderButtons(addButton, deleteButton, tagID[7:])
    
            formString += "</li>"             
    else:
        if element.attrib.get('type') is not None:  
            # the element has a type
            for x in range (0,int(nbOccurrences)): 
                nb_html_tags = int(request.session['nb_html_tags'])                           
                tagID = "element" + str(nb_html_tags)
                nb_html_tags += 1
                request.session['nb_html_tags'] = str(nb_html_tags)            
                form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=fullPath + '[' + str(x+1) +']', name=textCapitalized).save()
                request.session['mapTagID'][tagID] = str(form_element.id)
#                 form_data.elements.append(form_element)
                
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
                                
                if elementType.tag == "{0}complexType".format(namespace):
                    formString += "<li class='"+ element_tag + removed +"' id='" + str(tagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + textCapitalized
                else: 
                    formString += "<li class='"+ element_tag + removed +"' id='" + str(tagID) + "'>" + textCapitalized
                
                if not (addButton is False and deleteButton is False):
                    formString += renderButtons(addButton, deleteButton, tagID[7:])
                
                if len(removed) == 0 :
                    # if a module is present, replace the type by the module
                    if has_module:
                        formString += generateModule(request, element, namespace, xsd_xpath, fullPath+'['+ str(x+1) +']')
                    else:
                        if elementType is not None:
                            if elementType.tag == "{0}complexType".format(namespace):
                                formString += generateComplexType(request, elementType, xmlTree, namespace, fullPath=fullPath+'['+ str(x+1) +']')
                            elif elementType.tag == "{0}simpleType".format(namespace):
                                formString += generateSimpleType(request, elementType, xmlTree, namespace, fullPath=fullPath+'['+ str(x+1) +']')        
                formString += "</li>"
                
    formString += "</ul>"

    return formString


def renderButtons(addButton, deleteButton, tagID):
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


def generateElement_absent(request, sequenceChild, xmlDocTree, form_element):
    formString = ""

    namespaces = request.session['namespaces']
    defaultPrefix = request.session['defaultPrefix']

    # render element
    namespace = namespaces[defaultPrefix]

    # type is a reference included in the document
    if 'ref' in sequenceChild.attrib:
        ref = sequenceChild.attrib['ref']
        refElement = None
        if ':' in ref:
            refSplit = ref.split(":")
            refName = refSplit[1]
            refElement = xmlDocTree.find("./{0}element[@name='{1}']".format(namespace, refName))
        else:
            refElement = xmlDocTree.find("./{0}element[@name='{1}']".format(namespace, ref))

        if refElement is not None:
            sequenceChild = refElement
            # remove the annotations
            removeAnnotations(sequenceChild, namespace)

    # type is not present
    if 'type' not in sequenceChild.attrib:
        # type declared below the element
        if sequenceChild[0].tag == "{0}complexType".format(namespace):
            formString += generateComplexType(request, sequenceChild[0], xmlDocTree, namespace, fullPath=form_element.xml_xpath)
        elif sequenceChild[0].tag == "{0}simpleType".format(namespace):
            formString += generateSimpleType(request, sequenceChild[0], xmlDocTree, namespace, fullPath=form_element.xml_xpath)

    # type is a primitive XML type
    elif sequenceChild.attrib.get('type') in common.getXSDTypes(defaultPrefix):
        defaultValue = ""
        if 'default' in sequenceChild.attrib:
            defaultValue = sequenceChild.attrib['default']
        formString += "<input type='text' value='"+ defaultValue + "'/>"
    else:
        # type is declared in the document
        if sequenceChild.attrib.get('type') is not None:
            # TODO: manage namespaces
            # type of the element is complex
            typeName = sequenceChild.attrib.get('type')
            if ':' in typeName:
                typeName = typeName.split(":")[1]

            xpath = "./{0}complexType[@name='{1}']".format(namespace,typeName)
            elementType = xmlDocTree.find(xpath)
            if elementType is None:
                # type of the element is simple
                xpath = "./{0}simpleType[@name='{1}']".format(namespace,typeName)
                elementType = xmlDocTree.find(xpath)

            if elementType is not None:
                if elementType.tag == "{0}complexType".format(namespace):
                    formString += generateComplexType(request, elementType, xmlDocTree, namespace, fullPath=form_element.xml_xpath)
                elif elementType.tag == "{0}simpleType".format(namespace):
                    formString += generateSimpleType(request, elementType, xmlDocTree, namespace, fullPath=form_element.xml_xpath)

    return formString


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
    xmlDocTree = etree.fromstring(xmlDocTreeStr)

    # render element
    namespace = namespaces[defaultPrefix]

    xpath_namespaces = {}
    for prefix, ns in request.session['namespaces'].iteritems():
        xpath_namespaces[prefix] = ns[1:-1]

    sequenceChild = xmlDocTree.xpath(xml_element.xsd_xpath, namespaces=xpath_namespaces)[0]

    # remove the annotations
    removeAnnotations(sequenceChild, namespace)

    # generating a choice, generate the parent element
    if tag == "choice":
        # can use generateElement to generate a choice never generated
        formString = generateElement(request, sequenceChild, xmlDocTree, namespace, fullPath=form_element.xml_xpath)
        # remove the ul opening and closing tags
        formString = formString[4:-4]
    else:
        formString = generateElement_absent(request, sequenceChild, xmlDocTree, form_element)

    
    # build HTML tree for the form
    htmlTree = html.fromstring(request.POST['xsdForm'])
    # get the element we are working on
    currentElement = htmlTree.get_element_by_id(tagID)
    
    try:
        generated_element = html.fragment_fromstring(formString)
        if generated_element.tag == "ul":
            currentElement.append(generated_element)
        else:
            currentElement.insert(1, generated_element)
    except:
        for generated_element in html.fragments_fromstring(formString):
            currentElement.append(generated_element)


    # update the number of elements in database
    xml_element.nbOccurs = 1
    xml_element.save()

    if tag == "element":
        # updates buttons
        addButton = False
        
        if (xml_element.nbOccurs < xml_element.maxOccurs):
            addButton = True
        
        # enable add button if we can add more
        if(addButton == True):
            htmlTree.get_element_by_id("add" + str(id)).attrib['style'] = ''
        else:
            htmlTree.get_element_by_id("add" + str(id)).attrib['style'] = 'display:none'
        # enable delete button to come back to 0 occurs
        htmlTree.get_element_by_id("remove" + str(id)).attrib['style'] = ''

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
        xmlDocTree = etree.fromstring(xmlDocTreeStr)
        # render element
        namespace = namespaces[defaultPrefix]
        
        xpath_namespaces = {}
        for prefix, ns in request.session['namespaces'].iteritems() :
            xpath_namespaces[prefix] = ns[1:-1]
    
        sequenceChild = xmlDocTree.xpath(xml_element.xsd_xpath, namespaces=xpath_namespaces)[0]
        
        if sequenceChild.tag == "{0}element".format(namespace):
            element_tag='element'
        elif sequenceChild.tag == "{0}attribute".format(namespace):
            element_tag='attribute'
        elif sequenceChild.tag == "{0}sequence".format(namespace):
            element_tag = 'sequence'
        elif sequenceChild.tag == "{0}choice".format(namespace):
            element_tag = 'choice'
        
        # remove the annotations
        removeAnnotations(sequenceChild, namespace)

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
                    # remove the annotations
                    removeAnnotations(sequenceChild, namespace)
            else:
                textCapitalized = sequenceChild.attrib.get('name')
    
            # type is not present
            if 'type' not in sequenceChild.attrib:
                # type declared below the element
                newTagID = "element" + str(nb_html_tags)
                nb_html_tags += 1
                request.session['nb_html_tags'] = str(nb_html_tags)
                new_xml_xpath = form_element.xml_xpath[0:form_element.xml_xpath.rfind('[') + 1] + str(xml_element.nbOccurs) + ']'
                new_form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=new_xml_xpath, name=textCapitalized).save() 
                form_data.elements[newTagID] = new_form_element.id
                form_data.save()
                if sequenceChild[0].tag == "{0}complexType".format(namespace):
                    formString += "<li class='"+ element_tag +"' id='" + str(newTagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + textCapitalized
                else: 
                    formString += "<li class='"+ element_tag +"' id='" + str(newTagID) + "'>" + textCapitalized
                
                formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
                formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"            
                if sequenceChild[0].tag == "{0}complexType".format(namespace):
                    formString += generateComplexType(request, sequenceChild[0], xmlDocTree, namespace, fullPath=new_xml_xpath)
                elif sequenceChild[0].tag == "{0}simpleType".format(namespace):
                    formString += generateSimpleType(request, sequenceChild[0], xmlDocTree, namespace, fullPath=new_xml_xpath)
                formString += "</li>"
                    
            # type is a primitive XML type
            elif sequenceChild.attrib.get('type') in common.getXSDTypes(defaultPrefix):
                newTagID = "element" + str(nb_html_tags)
                nb_html_tags += 1
                request.session['nb_html_tags'] = str(nb_html_tags)
                new_xml_xpath = form_element.xml_xpath[0:form_element.xml_xpath.rfind('[') + 1] + str(xml_element.nbOccurs) + ']'
                new_form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=new_xml_xpath, name=textCapitalized).save() 
                form_data.elements[newTagID] = new_form_element.id
                form_data.save()
                defaultValue = ""
                if 'default' in sequenceChild.attrib:
                    defaultValue = sequenceChild.attrib['default']
                formString += "<li class='"+ element_tag +"' id='" + str(newTagID) + "'>" + textCapitalized + " <input type='text' value='"+ defaultValue +"'/>"
                formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
                formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"         
                formString += "</li>"
            else:
                # type is declared in the document
                if sequenceChild.attrib.get('type') is not None:                  
                    newTagID = "element" + str(nb_html_tags)
                    nb_html_tags += 1
                    request.session['nb_html_tags'] = str(nb_html_tags)
                    new_xml_xpath = form_element.xml_xpath[0:form_element.xml_xpath.rfind('[') + 1] + str(xml_element.nbOccurs) + ']'
                    new_form_element = FormElement(html_id=tagID, xml_element=xml_element, xml_xpath=new_xml_xpath, name=textCapitalized).save() 
                    form_data.elements[newTagID] = new_form_element.id
                    form_data.save()
                    # TODO: manage namespaces
                    # type of the element is complex        
                    typeName = sequenceChild.attrib.get('type')
                    if ':' in typeName:
                        typeName = typeName.split(":")[1]
                    
                    xpath = "./{0}complexType[@name='{1}']".format(namespace,typeName)
                    elementType = xmlDocTree.find(xpath)
                    if elementType is None:
                        # type of the element is simple
                        xpath = "./{0}simpleType[@name='{1}']".format(namespace,typeName)
                        elementType = xmlDocTree.find(xpath)
                    
                                        
                    if elementType.tag == "{0}complexType".format(namespace):
                        formString += "<li class='"+ element_tag +"' id='" + str(newTagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + textCapitalized
                    else: 
                        formString += "<li class='"+ element_tag +"' id='" + str(newTagID) + "'>" + textCapitalized
                    
                    formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
                    formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"           
                    
                    if elementType is not None:
                        if elementType.tag == "{0}complexType".format(namespace):
                            formString += generateComplexType(request, elementType, xmlDocTree, namespace, fullPath=new_xml_xpath)
                        elif elementType.tag == "{0}simpleType".format(namespace):
                            formString += generateSimpleType(request, elementType, xmlDocTree, namespace, fullPath=new_xml_xpath)                    
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
                formString += "<li class='sequence' id='" + str(newTagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + text
            else:
                formString += "<li class='sequence' id='" + str(newTagID) + "'>" + text
                
            formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
            formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"
            
            # generates the sequence
            if(len(list(sequenceChild)) != 0):
                for child in sequenceChild:
                    if (child.tag == "{0}element".format(namespace)):            
                        formString += generateElement(request, child, xmlDocTree, namespace, fullPath=new_xml_xpath)
                    elif (child.tag == "{0}sequence".format(namespace)):
                        formString += generateSequence(request, child, xmlDocTree, namespace, fullPath=new_xml_xpath)
                    elif (child.tag == "{0}choice".format(namespace)):
                        formString += generateChoice(request, child, xmlDocTree, namespace, fullPath=new_xml_xpath)
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
                        # look for active choice when editing                
                        elementPath = form_element.xml_xpath + '/' + opt_label
                        
                        if edit:
                            if len(edit_data_tree.xpath(elementPath)) == 0:    
                                formString += "<option value='" + opt_value + "'>" + opt_label + "</option></b><br>"
                            else:
                                formString += "<option value='" + opt_value + "' selected>" + opt_label + "</option></b><br>"
                        else:
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
                    formString += generateElement(request, choiceChild, xmlDocTree, namespace, common.ChoiceInfo(chooseIDStr,counter), fullPath=new_xml_xpath)
                elif (choiceChild.tag == "{0}group".format(namespace)):
                    pass
                elif (choiceChild.tag == "{0}choice".format(namespace)):
                    pass
                elif (choiceChild.tag == "{0}sequence".format(namespace)):
                    formString += generateSequence(request, choiceChild, xmlDocTree, namespace, common.ChoiceInfo(chooseIDStr,counter), fullPath=new_xml_xpath)
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
# Function Name: generateForm(request)
# Inputs:        request -
# Outputs:       rendered HTMl form
# Exceptions:    None
# Description:   Renders HTMl form for display.
#
################################################################################
def generateForm(request):
    print 'BEGIN def generateForm(key,xmlElement)'
     
    defaultPrefix = request.session['defaultPrefix']
    xmlDocTreeStr = request.session['xmlDocTree']
    xmlDocTree = etree.fromstring(xmlDocTreeStr)
    request.session['nbChoicesID'] = '0'
    request.session['nb_html_tags'] = '0'
    if 'mapTagID' in request.session:
        del request.session['mapTagID']
    request.session['mapTagID'] = {}
    
    formString = ""
    
    namespace = request.session['namespaces'][defaultPrefix]
    elements = xmlDocTree.findall("./{0}element".format(namespace))

    

    try:
        if len(elements) == 1:
            formString += "<div xmlID='root' name='xsdForm'>"
            formString += generateElement(request, elements[0], xmlDocTree,namespace)
            formString += "</div>"
        elif len(elements) > 1:     
            formString += "<div xmlID='root' name='xsdForm'>"
            formString += generateChoice(request, elements, xmlDocTree, namespace)
            formString += "</div>"
    except Exception, e:
        formString = "UNSUPPORTED ELEMENT FOUND (" + e.message + ")" 

    form_data = FormData(user='user_id', template='template_id', elements=request.session['mapTagID']).save()
    del request.session['mapTagID']
#     form_data.save()
    request.session['curateFormData'] = str(form_data.id)

    return formString


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

    template_id = request.session['currentTemplateID']
    response_dict = {}

    if 'formString' in request.session:
        formString = request.session['formString']  
    else:
        formString = ''
        request.session['occurrences'] = dict()  
       
    if 'xmlDocTree' in request.session:
        xmlDocTree = request.session['xmlDocTree'] 
    else:
        if template_id in MetaSchema.objects.all().values_list('schemaId'):
            meta = MetaSchema.objects.get(schemaId=template_id)
            xmlDocData = meta.flat_content
        else:
            templateObject = Template.objects.get(pk=template_id)
            xmlDocData = templateObject.content

        xmlDocTree = etree.parse(BytesIO(xmlDocData.encode('utf-8')))
        request.session['xmlDocTree'] = etree.tostring(xmlDocTree)
        xmlDocTree = request.session['xmlDocTree']   
    
    # find the namespaces
    request.session['namespaces'] = common.get_namespaces(BytesIO(str(xmlDocTree)))
    for prefix, url in request.session['namespaces'].items():
        if (url == "{http://www.w3.org/2001/XMLSchema}"):            
            request.session['defaultPrefix'] = prefix
            break
    
    if (formString == ""):     
        # this form was not created, generates it from the schema           
        formString += generateForm(request)
        request.session['originalForm'] = formString

    response_dict['xsdForm'] = formString
    request.session['formString'] = formString

    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    print 'END def generate_xsd_form(request)'


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
    
    xml2download = XML2Download(xml=xmlString).save()
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
    xmlString = request.POST['xmlString']
    
    xml2download = XML2Download(xml=xmlString).save()
    xml2downloadID = str(xml2download.id)

    response_dict = {"xml2downloadID": xml2downloadID}
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
    
    # get the original version of the form
    original_form = request.session['originalForm']
    
    reinitOccurrences(request)    

    response_dict = {'xsdForm': original_form}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
# 
# Function Name: reinitOccurrences(request)
# Inputs:        request -
# Outputs:       
# Exceptions:    None
# Description:   Reinitialize the number of occurrences with original values
#
################################################################################
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
# Function Name: load_xml(request)
# Inputs:        request - 
# Outputs:       JSON data with templateSelected 
# Exceptions:    None
# Description:   Loads the XML data in the view data page. First transforms the data.
# 
################################################################################
def load_xml(request):
    
    xmlString = request.session['xmlString']
    
    xsltPath = os.path.join(settings.SITE_ROOT, 'static/resources/xsl/xml2html.xsl')
    xslt = etree.parse(xsltPath)
    transform = etree.XSLT(xslt)
    xmlTree = ""
    if (xmlString != ""):
        dom = etree.fromstring(xmlString)
        newdom = transform(dom)
        xmlTree = str(newdom)

    response_dict = {"XMLHolder": xmlTree}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
