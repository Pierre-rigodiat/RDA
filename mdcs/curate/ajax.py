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

import lxml.html as html
import lxml.etree as etree

from mgi.settings import MATERIALS_MODULES

# Specific to RDF
import rdfPublisher

#XSL file loading
import os

#Class definition

################################################################################
# 
# Class Name: ElementOccurrences
#
# Description: Store information about a resource for a module
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
def manageButtons(element):
    addButton = False
    deleteButton = False
    nbOccurrences = 1
    if ('minOccurs' in element.attrib):
        if (element.attrib['minOccurs'] == '0'):
            deleteButton = True
        else:
            nbOccurrences = element.attrib['minOccurs']
    
    if ('maxOccurs' in element.attrib):
        if (element.attrib['maxOccurs'] == "unbounded"):
            addButton = True
        elif ('minOccurs' in element.attrib):
            if (int(element.attrib['maxOccurs']) > int(element.attrib['minOccurs'])
                and int(element.attrib['maxOccurs']) > 1):
                addButton = True
    return addButton, deleteButton, nbOccurrences


################################################################################
# 
# Function Name: manageAttrButtons(element)
# Inputs:        element - XML element 
# Outputs:       addButton - Boolean
#                deleteButton - Boolean
#                nbOccurrences - Integer
# Exceptions:    None
# Description:   Check element occurrences and returns buttons information
# 
################################################################################
def manageAttrButtons(element):
    addButton = False
    deleteButton = False
    nbOccurrences = 1

    if ('use' in element.attrib):
        if element.attrib['use'] == "optional":
            deleteButton = True
        elif element.attrib['use'] == "prohibited":            
            nbOccurrences = 0
        elif element.attrib['use'] == "required":
            pass
        
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
def generateSequence(request, element, xmlTree, namespace, choiceInfo=None):
    #(annotation?,(element|group|choice|sequence|any)*)
    
    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
    if (('minOccurs' in element.attrib and element.attrib['minOccurs'] != '1')
    or ('maxOccurs' in element.attrib and element.attrib['maxOccurs'] != '1')):
        xsd_elements = request.session['xsd_elements']
        mapTagElement = request.session['mapTagElement']
        
        text = "Sequence"
        addButton, deleteButton, nbOccurrences = manageButtons(element)
        elementID = len(xsd_elements)
        xsd_elements[elementID] = etree.tostring(element)
        manageOccurences(request, element, elementID)
        
        if choiceInfo:
            if (choiceInfo.counter > 0):
                formString += "<ul id=\"" + choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter) + "\" class=\"notchosen\">"
            else:
                formString += "<ul id=\"" + choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter) + "\" >"
        else:
            formString += "<ul>"
    
        for x in range (0,int(nbOccurrences)):
            tagID = "element" + str(len(mapTagElement.keys()))  
            mapTagElement[tagID] = elementID   
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
                        formString += generateElement(request, child, xmlTree, namespace, choiceInfo)
                    elif (child.tag == "{0}sequence".format(namespace)):
                        formString += generateSequence(request, child, xmlTree, namespace, choiceInfo)
                    elif (child.tag == "{0}choice".format(namespace)):
                        formString += generateChoice(request, child, xmlTree, namespace, choiceInfo)
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
                    formString += generateElement(request, child, xmlTree, namespace, choiceInfo)
                elif (child.tag == "{0}sequence".format(namespace)):
                    formString += generateSequence(request, child, xmlTree, namespace, choiceInfo)
                elif (child.tag == "{0}choice".format(namespace)):
                    formString += generateChoice(request, child, xmlTree, namespace, choiceInfo)
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
def generateChoice(request, element, xmlTree, namespace, choiceInfo=None):
    #(annotation?,(element|group|choice|sequence|any)*)
    nbChoicesID = int(request.session['nbChoicesID'])
    xsd_elements = request.session['xsd_elements']
    mapTagElement = request.session['mapTagElement']
    
    formString = ""
    
    #remove the annotations
    removeAnnotations(element, namespace)     
    
    if (not isinstance(element,list) and 
       ((('minOccurs' in element.attrib and element.attrib['minOccurs'] != '1')
         or ('maxOccurs' in element.attrib and element.attrib['maxOccurs'] != '1')))):                        
            addButton, deleteButton, nbOccurrences = manageButtons(element)
            elementID = len(xsd_elements)
            xsd_elements[elementID] = etree.tostring(element)
            manageOccurences(request, element, elementID)
    else:
        # multiple roots or no min/maxOccurs
        addButton = False
        deleteButton = False
        nbOccurrences = 1
        elementID = len(xsd_elements)
        xsd_elements[elementID] = ""
        
    if choiceInfo:
        if (choiceInfo.counter > 0):
            formString += "<ul id=\"" + choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter) + "\" class=\"notchosen\">"
        else:
            formString += "<ul id=\"" + choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter) + "\" >"
    else:
        formString += "<ul>"
            
    for x in range (0,int(nbOccurrences)):
        tagID = "element" + str(len(mapTagElement.keys()))  
        mapTagElement[tagID] = elementID        
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
                    name = child.attrib.get('name')
                    if name is None:
                        name = child.attrib.get('ref')
                    formString += "<option value='" + name + "'>" + name + "</option></b><br>"
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
                formString += generateElement(request, choiceChild, xmlTree, namespace, common.ChoiceInfo(chooseIDStr,counter))
            elif (choiceChild.tag == "{0}group".format(namespace)):
                pass
            elif (choiceChild.tag == "{0}choice".format(namespace)):
                pass
            elif (choiceChild.tag == "{0}sequence".format(namespace)):
                formString += generateSequence(request, choiceChild, xmlTree, namespace, common.ChoiceInfo(chooseIDStr,counter))
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
def generateSimpleType(request, element, xmlTree, namespace):
    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
    # TODO: modules
    formString = stubModules(request, element)
    if len(formString) > 0:
        return formString
    
    if (list(element) != 0):
        child = element[0] 
        if child.tag == "{0}restriction".format(namespace):
            formString += generateRestriction(request, child, xmlTree, namespace)            
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
def generateRestriction(request, element, xmlTree, namespace):
    formString = ""
    
    removeAnnotations(element, namespace)
    
    enumeration = element.findall('{0}enumeration'.format(namespace))
    if len(enumeration) > 0:
        formString += "<select>"
        for enum in enumeration:
            formString += "<option value='" + enum.attrib.get('value')  + "'>" + enum.attrib.get('value') + "</option>"
        formString += "</select>"
    else:
        simpleType = element.find('{0}simpleType'.format(namespace))
        if simpleType is not None:
            formString += generateSimpleType(request, simpleType, xmlTree, namespace)
        else:        
            formString += " <input type='text'/>"
            
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
def generateComplexType(request, element, xmlTree, namespace):
    #(annotation?,(simpleContent|complexContent|((group|all|choice|sequence)?,((attribute|attributeGroup)*,anyAttribute?))))

    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
    # TODO: modules
    formString = stubModules(request, element)
    if len(formString) > 0:
        return formString
    
    # does it contain an attribute?
    complexTypeChildren = element.findall('{0}attribute'.format(namespace))
    if len(complexTypeChildren) > 0:
        for attribute in complexTypeChildren:
            formString += generateElement(request, attribute, xmlTree, namespace)
    
    # does it contain sequence or all?
    complexTypeChild = element.find('{0}sequence'.format(namespace))
    if complexTypeChild is not None:
        formString += generateSequence(request, complexTypeChild, xmlTree, namespace)
    else:
        complexTypeChild = element.find('{0}all'.format(namespace))
        if complexTypeChild is not None:
            formString += generateSequence(request, complexTypeChild, xmlTree, namespace)
        else:
            # does it contain choice ?
            complexTypeChild = element.find('{0}choice'.format(namespace))
            if complexTypeChild is not None:
                formString += generateChoice(request, complexTypeChild, xmlTree, namespace)
            else:
                formString += ""        
    
    return formString 


################################################################################
# 
# Function Name: stubModules(request, element)
# Inputs:        request - 
#                element - XML element
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Temporary hardcoded modules for materials scientist
# 
################################################################################
def stubModules(request, element):
    mapModules = request.session['mapModules']
    
    formString = ""
    
    #TODO: modules
    if element.attrib.get('name') in mapModules.keys():
        formString += "<div class='module' style='display: inline'>"
        formString += mapModules[element.attrib.get('name')]
        formString += "<div class='moduleDisplay'></div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>"    
        
    if MATERIALS_MODULES == True:
        if 'name' in element.attrib and element.attrib.get('name') == "ConstituentsType":
            formString += "<div class='module' style='display: inline'>"
            formString += "<div class=\"btn select-element\" onclick=\"selectMultipleElements(this);\"><i class=\"icon-folder-open\"></i> Select Chemical Elements</div>"
            formString += "<div class='moduleDisplay'></div>"
            formString += "<div class='moduleResult' style='display: none'></div>"
            formString += "</div>"
        
        if 'name' in element.attrib and element.attrib.get('name') == "ChemicalElement":
#             formString += "<div class='module' style='display: inline'>"
#             formString += "<div class=\"btn select-element\" onclick=\"selectElement(this);\"><i class=\"icon-folder-open\"></i> Select Chemical Element</div>"
#             formString += "<div class='moduleDisplay'>Current Selection: None</div>"
#             formString += "<div class='moduleResult' style='display: none'></div>"
#             formString += "</div>" 
            formString += "<div class='module' style='display: inline'>"
            formString += "<div class='moduleContent'></div>"
            formString += "<div class='moduleDisplay'></div>"
            formString += "<div class='moduleResult' style='display: none'></div>"
            formString += "<div class='moduleURL' style='display: none'>diffusion/periodic-table</div>"
            formString += "</div>" 
        
        if 'name' in element.attrib and element.attrib.get('name') == "Table":
            formString += "<div class='module' style='display: inline'>"
            formString += "<div class=\"btn select-element\" onclick=\"selectHDF5File('Spreadsheet File',this);\"><i class=\"icon-folder-open\"></i> Upload Spreadsheet </div>"
            formString += "<div class='moduleDisplay'></div>"
            formString += "<div class='moduleResult' style='display: none'></div>"
            formString += "</div>"
    
    return formString

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
def generateElement(request, element, xmlTree, namespace, choiceInfo=None):
    
    xsd_elements = request.session['xsd_elements']
    mapTagElement = request.session['mapTagElement']
    defaultPrefix = request.session['defaultPrefix']
    
    formString = ""

    # remove the annotations
    removeAnnotations(element, namespace)
    
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
    
    
    elementID = len(xsd_elements)
    if element.tag == "{0}element".format(namespace):
        # don't save element representation if never need to duplicate it
        if ('maxOccurs' not in element.attrib) or (element.attrib['maxOccurs']=="1"):
            xsd_elements[elementID] = ""
        else:
            xsd_elements[elementID] = etree.tostring(element)
        manageOccurences(request, element, elementID)
        addButton, deleteButton, nbOccurrences = manageButtons(element)
        element_tag='element'
    elif element.tag == "{0}attribute".format(namespace):
        # don't save attribute representation because never needs to duplicate it
        xsd_elements[elementID] = ""
        manageAttrOccurrences(request, element, elementID)
        addButton, deleteButton, nbOccurrences = manageAttrButtons(element)
        element_tag='attribute'
        
    if choiceInfo:
        if (choiceInfo.counter > 0):
            formString += "<ul id=\"" + choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter) + "\" class=\"notchosen\">"
        else:
            formString += "<ul id=\"" + choiceInfo.chooseIDStr + "-" + str(choiceInfo.counter) + "\" >"
    else:
        formString += "<ul>"
    
    if 'type' not in element.attrib:
        # element with type declared below it                                                                          
        for x in range (0,int(nbOccurrences)):     
            tagID = "element" + str(len(mapTagElement.keys()))  
            mapTagElement[tagID] = elementID    
            
            # if tag not closed:  <element/>
            if len(list(element)) > 0 :
                if element[0].tag == "{0}complexType".format(namespace):
                    formString += "<li class='"+ element_tag +"' id='" + str(tagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + textCapitalized
                else: 
                    formString += "<li class='"+ element_tag +"' id='" + str(tagID) + "'>" + textCapitalized
            else:
                formString += "<li class='"+ element_tag +"' id='" + str(tagID) + "'>" + textCapitalized
            if (addButton == True):                                
                formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"
            else:
                formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"                                                                             
            if (deleteButton == True):
                formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"
            else:
                formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"
            
            # if tag not closed:  <element/>
            if len(list(element)) > 0 :
                if element[0].tag == "{0}complexType".format(namespace):                    
                    formString += generateComplexType(request, element[0], xmlTree, namespace)
                elif element[0].tag == "{0}simpleType".format(namespace):
                    formString += generateSimpleType(request, element[0], xmlTree, namespace)
            formString += "</li>"
    elif element.attrib.get('type') in common.getXSDTypes(defaultPrefix):                         
        for x in range (0,int(nbOccurrences)):                         
            tagID = "element" + str(len(mapTagElement.keys()))  
            mapTagElement[tagID] = elementID 
            defaultValue = ""
            if 'default' in element.attrib:
                defaultValue = element.attrib['default']
            formString += "<li class='"+ element_tag +"' id='" + str(tagID) + "'>" + textCapitalized + " <input type='text' value='"+ defaultValue +"'/>"
                                
            if (addButton == True):                                
                formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"
            else:
                formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"                                

            if (deleteButton == True):
                formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"
            else:
                formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"
            formString += "</li>"                    
    else:
        if element.attrib.get('type') is not None:  
            for x in range (0,int(nbOccurrences)):                            
                tagID = "element" + str(len(mapTagElement.keys()))  
                mapTagElement[tagID] = elementID
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
                    formString += "<li class='"+ element_tag +"' id='" + str(tagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + textCapitalized
                else: 
                    formString += "<li class='"+ element_tag +"' id='" + str(tagID) + "'>" + textCapitalized
                    
                if (addButton == True):                                
                    formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"
                else:
                    formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',"+str(tagID[7:])+");\"></span>"
                    
                if (deleteButton == True):
                    formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"
                else:
                    formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',"+str(tagID[7:])+");\"></span>"
                
                if elementType is not None:
                    if elementType.tag == "{0}complexType".format(namespace):
                        formString += generateComplexType(request, elementType, xmlTree, namespace)
                    elif elementType.tag == "{0}simpleType".format(namespace):
                        formString += generateSimpleType(request, elementType, xmlTree, namespace)
        
                formString += "</li>"
                
    formString += "</ul>"
        
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
def manageOccurences(request, element, elementID):
    occurrences = request.session['occurrences']
    elementOccurrences = ElementOccurrences()
    
    if ('minOccurs' in element.attrib):
        elementOccurrences.minOccurrences = int(element.attrib['minOccurs'])
        if (element.attrib['minOccurs'] != '0'):
            elementOccurrences.nbOccurrences = elementOccurrences.minOccurrences
    if ('maxOccurs' in element.attrib):
        if (element.attrib['maxOccurs'] == "unbounded"):
            elementOccurrences.maxOccurrences = float('inf')
        else:
            elementOccurrences.maxOccurrences = int(element.attrib['maxOccurs'])
    
    occurrences[elementID] = elementOccurrences.__to_json__()

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
def manageAttrOccurrences(request, element, elementID):
    occurrences = request.session['occurrences']
    elementOccurrences = ElementOccurrences()
    
    elementOccurrences.nbOccurrences = 1
    elementOccurrences.minOccurrences = 1
    elementOccurrences.maxOccurrences = 1
    if ('use' in element.attrib):
        if element.attrib['use'] == "optional":
            elementOccurrences.minOccurrences = 0
        elif element.attrib['use'] == "prohibited":            
            elementOccurrences.nbOccurrences = 0
            elementOccurrences.minOccurrences = 0
            elementOccurrences.maxOccurrences = 0
        elif element.attrib['use'] == "required":
            pass
    
    occurrences[elementID] = elementOccurrences.__to_json__()
    


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
    occurrences = request.session['occurrences']
    mapTagElement = request.session['mapTagElement']
    
    tagID = "element"+ str(request.POST['tagID'])
    elementID = mapTagElement[tagID]
    elementOccurrencesStr = occurrences[str(elementID)]
    if 'inf' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('inf','float("inf")')
    if 'Infinity' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('Infinity','float("inf")') 
    elementOccurrences = eval(elementOccurrencesStr)

    # test if the element can be removed (should always be true)
    if (elementOccurrences['nbOccurrences'] > elementOccurrences['minOccurrences']):
        elementOccurrences['nbOccurrences'] -= 1
        occurrences[str(elementID)] = unicode(elementOccurrences)
        request.session['occurrences'] = occurrences
        
        if (elementOccurrences['nbOccurrences'] == 0):    
            response_dict['occurs'] = 'zero'
            response_dict['tagID'] = str(tagID)
            response_dict['id'] = str(tagID[7:])
        else:
            response_dict['occurs'] = 'notzero'
    else:
        pass

    request.session.modified = True
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
    occurrences = request.session['occurrences']
    mapTagElement = request.session['mapTagElement']
    
    tagID = "element"+ str(request.POST['tagID'])
    elementID = mapTagElement[tagID]
    elementOccurrencesStr = occurrences[str(elementID)]
    if 'inf' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('inf','float("inf")')
    if 'Infinity' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('Infinity','float("inf")') 
    elementOccurrences = eval(elementOccurrencesStr)

    if (elementOccurrences['nbOccurrences'] > elementOccurrences['minOccurrences']):                
        addButton = False
        deleteButton = False
        
        if (elementOccurrences['nbOccurrences'] < elementOccurrences['maxOccurrences']):
            addButton = True
        if (elementOccurrences['nbOccurrences'] > elementOccurrences['minOccurrences']):
            deleteButton = True
            
        htmlTree = html.fromstring(request.POST['xsdForm'])
        currentElement = htmlTree.get_element_by_id(tagID)
        parent = currentElement.getparent()
        
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
        
        parent.remove(currentElement)
        
        response_dict = {'xsdForm': html.tostring(htmlTree)}
    
    request.session.modified = True
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
    occurrences = request.session['occurrences']
    mapTagElement = request.session['mapTagElement']
    
    tagID = "element"+ str(request.POST['tagID'])
    elementID = mapTagElement[tagID]    
    elementOccurrencesStr = occurrences[str(elementID)]
    if 'inf' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('inf','float("inf")')
    if 'Infinity' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('Infinity','float("inf")') 
    elementOccurrences = eval(elementOccurrencesStr)

    # Check that the element can be duplicated (should always be true)
    if (elementOccurrences['nbOccurrences'] < elementOccurrences['maxOccurrences']):        
        elementOccurrences['nbOccurrences'] += 1
        occurrences[str(elementID)] = unicode(elementOccurrences)
        request.session['occurrences'] = occurrences
        
        # from 0 occurrence to 1, just enable the GUI
        if(elementOccurrences['nbOccurrences'] == 1):      
            styleAdd=''
            if (elementOccurrences['maxOccurrences'] == 1):
                styleAdd = 'display:none'
            response_dict['occurs'] = 'zero'
            response_dict['tagID'] = str(tagID)
            response_dict['id'] = str(tagID[7:])
            response_dict['styleAdd'] = styleAdd
        else:
            response_dict['occurs'] = 'notzero'
    else:
        pass

    request.session.modified = True
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
    xsd_elements = request.session['xsd_elements']
    occurrences = request.session['occurrences']
    mapTagElement = request.session['mapTagElement']
    
    formString = ""
    tagID = "element"+ str(request.POST['tagID'])
    elementID = mapTagElement[tagID]    
    elementOccurrencesStr = occurrences[str(elementID)]
    if 'inf' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('inf','float("inf")')
    if 'Infinity' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('Infinity','float("inf")') 
    elementOccurrences = eval(elementOccurrencesStr)

    # Check that the element can be duplicated
    if (elementOccurrences['nbOccurrences'] < elementOccurrences['maxOccurrences']):                       
        sequenceChild = etree.fromstring(xsd_elements[str(elementID)])
        namespaces = request.session['namespaces']
        defaultPrefix = request.session['defaultPrefix']
        xmlDocTreeStr = request.session['xmlDocTree']
        xmlDocTree = etree.fromstring(xmlDocTreeStr)
        # render element
        namespace = namespaces[defaultPrefix]
        # remove the annotations
        removeAnnotations(sequenceChild, namespace)

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
            newTagID = "element" + str(len(mapTagElement.keys()))  
            mapTagElement[newTagID] = elementID  
            if sequenceChild[0].tag == "{0}complexType".format(namespace):
                formString += "<li id='" + str(newTagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + textCapitalized
            else: 
                formString += "<li id='" + str(newTagID) + "'>" + textCapitalized
            
            formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
            formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"            
            if sequenceChild[0].tag == "{0}complexType".format(namespace):
                formString += generateComplexType(request, sequenceChild[0], xmlDocTree, namespace)
            elif sequenceChild[0].tag == "{0}simpleType".format(namespace):
                formString += generateSimpleType(request, sequenceChild[0], xmlDocTree, namespace)
            formString += "</li>"
                
        # type is a primitive XML type
        elif sequenceChild.attrib.get('type') in common.getXSDTypes(defaultPrefix):
            newTagID = "element" + str(len(mapTagElement.keys())) 
            mapTagElement[newTagID] = elementID
            defaultValue = ""
            if 'default' in sequenceChild.attrib:
                defaultValue = sequenceChild.attrib['default']
            formString += "<li id='" + str(newTagID) + "'>" + textCapitalized + " <input type='text' value='"+ defaultValue +"'/>"
            formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
            formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"         
            formString += "</li>"
        else:
            # type is declared in the document
            if sequenceChild.attrib.get('type') is not None:                  
                newTagID = "element" + str(len(mapTagElement.keys()))  
                mapTagElement[newTagID] = elementID 
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
                    formString += "<li id='" + str(newTagID) + "'>" + "<span class='collapse' style='cursor:pointer;' onclick='showhideCurate(event);'></span>"  + textCapitalized
                else: 
                    formString += "<li id='" + str(newTagID) + "'>" + textCapitalized
                
                formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',"+str(newTagID[7:])+");\"></span>"
                formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',"+str(newTagID[7:])+");\"></span>"           
                
                if elementType is not None:
                    if elementType.tag == "{0}complexType".format(namespace):
                        formString += generateComplexType(request, elementType, xmlDocTree, namespace)
                    elif elementType.tag == "{0}simpleType".format(namespace):
                        formString += generateSimpleType(request, elementType, xmlDocTree, namespace)                    
                formString += "</li>"                   

        htmlTree = html.fromstring(request.POST['xsdForm'])
        currentElement = htmlTree.get_element_by_id(tagID)
        parent = currentElement.getparent()
        parent.append(html.fragment_fromstring(formString))          
        addButton = False
        deleteButton = False
        
        if (elementOccurrences['nbOccurrences'] < elementOccurrences['maxOccurrences']):
            addButton = True
        if (elementOccurrences['nbOccurrences'] > elementOccurrences['minOccurrences']):
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
    
    request.session.modified = True
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
# 
# Function Name: get_namespaces(file)
# Inputs:        file -
# Outputs:       namespaces
# Exceptions:    None
# Description:   Get the namespaces used in the document
#
################################################################################
def get_namespaces(file):
    "Reads and returns the namespaces in the schema tag"
    events = "start", "start-ns"
    ns = {}
    for event, elem in etree.iterparse(file, events):
        if event == "start-ns":
            if elem[0] in ns and ns[elem[0]] != elem[1]:
                raise Exception("Duplicate prefix with different URI found.")
            ns[elem[0]] = "{%s}" % elem[1]
        elif event == "start":
            break
    return ns

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
    
    if 'xsd_elements' in request.session:
        del request.session['xsd_elements']
    if 'mapTagElement' in request.session:
        del request.session['mapTagElement']  
    if 'spreadsheetXML' in request.session:
        del request.session['spreadsheetXML']
    request.session['xsd_elements'] = dict()   
    request.session['mapTagElement'] = dict()
    request.session['spreadsheetXML'] = ""
    defaultPrefix = request.session['defaultPrefix']
    xmlDocTreeStr = request.session['xmlDocTree']
    xmlDocTree = etree.fromstring(xmlDocTreeStr)
    request.session['nbChoicesID'] = '0'
    
    formString = ""
    
    namespace = request.session['namespaces'][defaultPrefix]
    elements = xmlDocTree.findall("./{0}element".format(namespace))

    try:
        if len(elements) == 1:
            formString += "<div xmlID='root'>"
            formString += generateElement(request, elements[0], xmlDocTree,namespace)
            formString += "</div>"
        elif len(elements) > 1:     
            formString += "<div xmlID='root'>"
            formString += generateChoice(request, elements, xmlDocTree, namespace)
            formString += "</div>"
    except Exception, e:
        formString = "UNSUPPORTED ELEMENT FOUND (" + e.message + ")" 
        
    return formString

################################################################################
# 
# Function Name: loadModuleResources(templateID)
# Inputs:        templateID -
# Outputs:       
# Exceptions:    None
# Description:   Get the resources needed to display a module of the template,
#                and returns a string to be inserted in the HTML page.
#
################################################################################
def loadModuleResources(templateID):
    modules = Module.objects(templates__contains=templateID)
    html = ""
    for module in modules:
        for resource in module.resources:
            if resource.type == "js":
                html += "<script>" + resource.content + "</script>"
            elif resource.type == "html":
                html += "<div>" + resource.content + "</div>"
            elif resource.type == "css":
                html += "<style>" + resource.content + "</style>"
    return html


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
        
    # load modules from the database
    if 'mapModules' in request.session:
        del request.session['mapModules']
    resources_html = loadModuleResources(template_id)
    response_dict['modules'] = resources_html
    mapModules = dict()    
    modules = Module.objects(templates__contains=template_id)
    for module in modules:
        mapModules[module.tag] = module.htmlTag
    request.session['mapModules'] = mapModules    
    
    # find the namespaces
    request.session['namespaces'] = get_namespaces(BytesIO(str(xmlDocTree)))
    for prefix, url in request.session['namespaces'].items():
        if (url == "{http://www.w3.org/2001/XMLSchema}"):            
            request.session['defaultPrefix'] = prefix
            break
    
    if (formString == ""):     
        # this form was not created, generates it from the schema           
        formString = "<form id=\"dataEntryForm\" name=\"xsdForm\">"
        formString += generateForm(request)
        formString += "</form>"
        request.session['originalForm'] = formString

    #TODO: modules
    pathFile = "{0}/static/resources/files/{1}"
    path = pathFile.format(settings.SITE_ROOT,"periodic.html")
    periodicTableDoc = open(path,'r')
    periodicTableString = periodicTableDoc.read()

    response_dict['periodicTable'] = periodicTableString

    pathFile = "{0}/static/resources/files/{1}"
    path = pathFile.format(settings.SITE_ROOT,"periodicMultiple.html")
    periodicMultipleTableDoc = open(path,'r')
    periodicTableMultipleString = periodicMultipleTableDoc.read()

    response_dict['periodicTableMultiple'] = periodicTableMultipleString
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
