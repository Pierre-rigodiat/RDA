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
from django.utils import simplejson
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.conf import settings
from mongoengine import *
from io import BytesIO
from mgi.models import XMLSchema 
from cStringIO import StringIO
from django.core.servers.basehttp import FileWrapper
from mgi.models import Template, Htmlform, Jsondata, XML2Download, Module, Type, MetaSchema
from bson.objectid import ObjectId
import json
from mgi import utils

import lxml.html as html
import lxml.etree as etree

# Specific to RDF
import rdfPublisher

#XSL file loading
import os
from django.core.files.temp import NamedTemporaryFile


#Class definition

################################################################################
# 
# Class Name: ElementOccurrences
#
# Description: Store information about a resource for a module
#
################################################################################
class ElementOccurrences:
    "Class that store information about element occurrences"
        
    def __init__(self, minOccurrences = 1, maxOccurrences = 1, nbOccurrences = 1):
        #self.__class__.count += 1
        
        #min/max occurrence attributes
        self.minOccurrences = minOccurrences
        self.maxOccurrences = maxOccurrences
        
        #current number of occurrences of the element
        self.nbOccurrences = nbOccurrences        
    
    def __to_json__(self):
        return json.dumps(self, default=lambda o:o.__dict__)

################################################################################
#
# Function Name: getHDF5String(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   Get the values of an excel spreadsheet from the session variable
#                
#
################################################################################
@dajaxice_register
def getHDF5String(request):
    dajax = Dajax() 
    if 'spreadsheetXML' in request.session:
        spreadsheetXML = request.session['spreadsheetXML']
        request.session['spreadsheetXML'] = ""
    else:
        spreadsheetXML = ""

    return simplejson.dumps({'spreadsheetXML':spreadsheetXML})

################################################################################
#
# Function Name: updateFormList(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
@dajaxice_register
def updateFormList(request):
    print '>>>>  BEGIN def updateFormList(request)'
    dajax = Dajax()

    templateID = request.session['currentTemplateID']

    selectOptions = ""
    availableHTMLForms = Htmlform.objects(schema=templateID)
    if len(availableHTMLForms) > 0:
        for htmlForm in availableHTMLForms:
            selectOptions += "<option value=\"" + str(htmlForm.id) + "\">" + htmlForm.title + "</option>"
    else:
        selectOptions = "<option value=\"none\">None Exist"

    dajax.assign('#listOfForms', 'innerHTML', selectOptions)

    print '>>>> END def updateFormList(request)'
    return dajax.json()

################################################################################
#
# Function Name: saveHTMLForm(request,saveAs,content)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   Save the current form in MongoDB
#                
#
################################################################################
@dajaxice_register
def saveHTMLForm(request,saveAs,content):    
    dajax = Dajax()

    templateID = request.session['currentTemplateID']
    occurrences = request.session['occurrences']

    newHTMLForm = Htmlform(title=saveAs, schema=templateID, content=content, occurrences=str(occurrences)).save()
    
    return dajax.json()


################################################################################
#
# Function Name: downloadHTMLForm(request,saveAs,content)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   Download the HTML form      
#
################################################################################
@dajaxice_register
def downloadHTMLForm(request,saveAs,content):    
    dajax = Dajax()

    templateID = request.session['currentTemplateID']

    newHTMLForm = Htmlform(title=saveAs, schema=templateID, content=content).save()
    
    dajax.redirect('/curate/enter-data/download-form?id='+str(newHTMLForm.id))
    
    return dajax.json()

################################################################################
#
# Function Name: validateXMLData(request, xmlString, xsdForm)
# Inputs:        request - 
#                xmlString - XML string generated from the form
#                xsdForm -  Current form
# Outputs:       
# Exceptions:    None
# Description:   Check if the current XML document is valid according to the template
#                
#
################################################################################
@dajaxice_register
def validateXMLData(request, xmlString, xsdForm):
    dajax = Dajax()
    
    templateID = request.session['currentTemplateID']
    
    request.session['xmlString'] = ""
          
    try:
        utils.validateXMLDocument(templateID, xmlString)   
    except Exception, e:
        message= e.message.replace('"','\'')
        dajax.script("""
            $("#saveErrorMessage").html(" """+ message + """ ");
            saveXMLDataToDBError();
        """)
        return dajax.json()

    request.session['xmlString'] = xmlString
    request.session['formString'] = xsdForm
    
    dajax.script("""
        viewData();
    """)
    
    return dajax.json()
    

################################################################################
#
# Function Name: saveXMLDataToDB(request, saveAs)
# Inputs:        request - 
#                saveAs - title of the document
# Outputs:       
# Exceptions:    None
# Description:   Save the current XML document in MongoDB. The document is also
#                converted to RDF format and sent to a Jena triplestore.
#                
#
################################################################################
@dajaxice_register
def saveXMLDataToDB(request,saveAs):
    print '>>>>  BEGIN def saveXMLDataToDB(request,saveAs)'
    dajax = Dajax()

    xmlString = request.session['xmlString']
    templateID = request.session['currentTemplateID']


    try:
        newJSONData = Jsondata(schemaID=templateID, xml=xmlString, title=saveAs)
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
        
        dajax.script("""
            savedXMLDataToDB();
        """)
    except Exception, e:
        message= e.message.replace('"','\'')
        dajax.script("""
            $("#saveErrorMessage").html(" """+ message + """ ");
            saveXMLDataToDBError();
        """)
    print '>>>>  END def saveXMLDataToDB(request,saveAs)'
    return dajax.json()

################################################################################
#
# Function Name: saveXMLData(request,formContent)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   Save the content of the current form in session
#                
#
################################################################################
@dajaxice_register
def saveXMLData(request, formContent):
    print '>>>>  BEGIN def saveXMLData(request,formContent)'
    dajax = Dajax()
    
    request.session['formString'] = formContent

    print '>>>> END def saveXMLData(request,formContent)'
    return dajax.json()

################################################################################
#
# Function Name: loadFormForEntry(request,formSelected)
# Inputs:        request - 
#                formSelected - 
# Outputs:       
# Exceptions:    None
# Description:   Load a saved form in the page
#                
#
################################################################################
@dajaxice_register
def loadFormForEntry(request,formSelected):
    print '>>>>  BEGIN def loadFormForEntry(request,formSelected)'
    dajax = Dajax()

    try:
        htmlFormObject = Htmlform.objects.get(id=formSelected)
        request.session['occurrences'] = eval(htmlFormObject.occurrences)
        
        dajax.assign('#xsdForm', 'innerHTML', htmlFormObject.content)
    except:
        pass
    
    print '>>>> END def loadFormForEntry(request,formSelected)'
    return dajax.json()

################################################################################
# 
# Function Name: setCurrentTemplate(request,templateFilename,templateID)
# Inputs:        request - 
#                templateFilename -  
#                templateID - 
# Outputs:       JSON data with success or failure
# Exceptions:    None
# Description:   Set the current template to input argument.  Template is read 
#                into an xsdDocTree for use later.
#
################################################################################
@dajaxice_register
def setCurrentTemplate(request,templateFilename,templateID):
    print 'BEGIN def setCurrentTemplate(request)'

    # reset global variables
    request.session['xmlString'] = ""
    request.session['formString'] = ""

    request.session['currentTemplate'] = templateFilename
    request.session['currentTemplateID'] = templateID
    request.session.modified = True
    dajax = Dajax()

    if templateID in MetaSchema.objects.all().values_list('schemaId'):
        meta = MetaSchema.objects.get(schemaId=templateID)
        xmlDocData = meta.flat_content
    else:
        templateObject = Template.objects.get(pk=templateID)
        xmlDocData = templateObject.content

    XMLSchema.tree = etree.parse(BytesIO(xmlDocData.encode('utf-8')))
    request.session['xmlDocTree'] = etree.tostring(XMLSchema.tree)

    print 'END def setCurrentTemplate(request)'
    return dajax.json()

################################################################################
# 
# Function Name: setCurrentUserTemplate(request, templateID)
# Inputs:        request - 
#                templateID -  
# Outputs:       JSON data with success or failure
# Exceptions:    None
# Description:   Set the current template to input argument.  Template is read 
#                into an xsdDocTree for use later. This case is for templates
#                defined using the composer.
#
################################################################################
@dajaxice_register
def setCurrentUserTemplate(request,templateID):
    print 'BEGIN def setCurrentTemplate(request)'

    # reset global variables
    request.session['xmlString'] = ""
    request.session['formString'] = ""
    
    request.session['currentTemplateID'] = templateID
    request.session.modified = True
    
    dajax = Dajax()

    templateObject = Template.objects.get(pk=templateID)
    request.session['currentTemplate'] = templateObject.title
    
    if templateID in MetaSchema.objects.all().values_list('schemaId'):
        meta = MetaSchema.objects.get(schemaId=templateID)
        xmlDocData = meta.flat_content
    else:
        xmlDocData = templateObject.content

    XMLSchema.tree = etree.parse(BytesIO(xmlDocData.encode('utf-8')))
    request.session['xmlDocTree'] = etree.tostring(XMLSchema.tree)

    print 'END def setCurrentTemplate(request)'
    return dajax.json()

################################################################################
# 
# Function Name: verifyTemplateIsSelected(request)
# Inputs:        request - 
# Outputs:       JSON data with templateSelected 
# Exceptions:    None
# Description:   Verifies the current template is selected.
# 
################################################################################
@dajaxice_register
def verifyTemplateIsSelected(request):
    print 'BEGIN def verifyTemplateIsSelected(request)'
    if 'currentTemplateID' in request.session:
        templateSelected = 'yes'
    else:
        templateSelected = 'no'
    dajax = Dajax()

    print 'END def verifyTemplateIsSelected(request)'
    return simplejson.dumps({'templateSelected':templateSelected})

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
def generateSequence(request, element, xmlTree, namespace):
    #(annotation?,(element|group|choice|sequence|any)*)
    
    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
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
# Outputs:       HTML string representing a sequence
# Exceptions:    None
# Description:   Generates a section of the form that represents an XML choice
# 
################################################################################
def generateChoice(request, element, xmlTree, namespace):
    #(annotation?,(element|group|choice|sequence|any)*)
    nbChoicesID = int(request.session['nbChoicesID'])
    xsd_elements = request.session['xsd_elements']
    mapTagElement = request.session['mapTagElement']
    defaultPrefix = request.session['defaultPrefix']
    
    formString = ""
    
    #remove the annotations
    removeAnnotations(element, namespace) 
    
    chooseID = nbChoicesID
    chooseIDStr = 'choice' + str(chooseID)
    nbChoicesID += 1
    request.session['nbChoicesID'] = str(nbChoicesID)
    formString += "<ul><li><nobr>Choose <select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"
    
    # generates the choice
    if(len(list(element)) != 0):
        for child in element:
            if (child.tag == "{0}element".format(namespace)):            
                name = child.attrib.get('name')
                formString += "<option value='" + name + "'>" + name + "</option></b><br>"
            elif (child.tag == "{0}group".format(namespace)):
                pass
            elif (child.tag == "{0}choice".format(namespace)):
                pass
            elif (child.tag == "{0}sequence".format(namespace)):
                pass
            elif (child.tag == "{0}any".format(namespace)):
                pass

    formString += "</select>"
    
    for (counter, choiceChild) in enumerate(list(element)):
        if choiceChild.tag == "{0}element".format(namespace):
            if 'type' not in choiceChild.attrib:
                # type is a reference included in the document
                if 'ref' in choiceChild.attrib: 
                    pass
                     
                # element with type declared below it
                else:                            
                    textCapitalized = choiceChild.attrib.get('name')
                    addButton, deleteButton, nbOccurrences = manageButtons(choiceChild)
                                                            
                    elementID = len(xsd_elements)
                    xsd_elements[elementID] = etree.tostring(choiceChild)
                    manageOccurences(request, choiceChild, elementID)
                    
                    formString += "<ul>"                                   
                    for x in range (0,int(nbOccurrences)):     
                        tagID = "element" + str(len(mapTagElement.keys()))  
                        mapTagElement[tagID] = elementID             
                        formString += "<li id='" + str(tagID) + "'><nobr>" + textCapitalized
                        if (addButton == True):                                
                            formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"
                        else:
                            formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"                                                                             
                        if (deleteButton == True):
                            formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                        else:
                            formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                        if choiceChild[0].tag == "{0}complexType".format(namespace):
                            formString += generateComplexType(request, choiceChild[0], xmlTree, namespace)
                        elif choiceChild[0].tag == "{0}simpleType".format(namespace):
                            formString += generateSimpleType(request, choiceChild[0], xmlTree, namespace)
                        formString += "</nobr></li>"
                    formString += "</ul>"
            elif choiceChild.attrib.get('type') in utils.getXSDTypes(defaultPrefix):
                textCapitalized = choiceChild.attrib.get('name')                                
                elementID = len(xsd_elements)
                xsd_elements[elementID] = etree.tostring(choiceChild)
                tagID = "element" + str(len(mapTagElement.keys()))  
                mapTagElement[tagID] = elementID 
                manageOccurences(request, choiceChild, elementID)
                defaultValue = ""
                if 'default' in choiceChild.attrib:
                    defaultValue = choiceChild.attrib['default']
                if (counter > 0):
                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li id='" + str(tagID) + "'><nobr>" + choiceChild.attrib.get('name') + " <input type='text' value='"+ defaultValue +"'/>" + "</nobr></li></ul>"
                else:
                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\"><li id='" + str(tagID) + "'><nobr>" + choiceChild.attrib.get('name') + " <input type='text' value='"+ defaultValue +"'/>" + "</nobr></li></ul>"
            else:
                textCapitalized = choiceChild.attrib.get('name')
                elementID = len(xsd_elements)
                xsd_elements[elementID] = etree.tostring(choiceChild)
                tagID = "element" + str(len(mapTagElement.keys()))  
                mapTagElement[tagID] = elementID 
                manageOccurences(request, choiceChild, elementID)
                if (counter > 0):
                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li id='" + str(tagID) + "'><nobr>" + textCapitalized
                else:
                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\"><li id='" + str(tagID) + "'><nobr>" + textCapitalized
                
                xpath = "./*[@name='"+choiceChild.attrib.get('type')+"']"
                elementType = xmlTree.find(xpath)
                if elementType.tag == "{0}complexType".format(namespace):
                    formString += generateComplexType(request, elementType, xmlTree, namespace)
                elif elementType.tag == "{0}simpleType".format(namespace):
                    formString += generateSimpleType(request, elementType, xmlTree, namespace)    
                
                formString += "</nobr></li></ul>"
        else:
            pass
    
    formString += "</nobr></li></ul>"
    
    
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
def generateSimpleType(request, element, xmlTree, namespace):
    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
    # TODO: modules
    formString = stubModules(request, element)
    if len(formString) > 0:
        return formString
    
    for child in list(element):
        if child.tag == "{0}restriction".format(namespace):
            enumeration = child.findall('{0}enumeration'.format(namespace))
            if len(enumeration) > 0:
                formString += "<select>"
                for enum in enumeration:
                    formString += "<option value='" + enum.attrib.get('value')  + "'>" + enum.attrib.get('value') + "</option>"
                formString += "</select>"
            else:
                if child.attrib['base'] in utils.getXSDTypes(request.session['defaultPrefix']):
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
    formString = ""
    
    # remove the annotations
    removeAnnotations(element, namespace)
    
    # TODO: modules
    formString = stubModules(request, element)
    if len(formString) > 0:
        return formString
    
    # TODO: does it contain attributes ?
        
    # does it contain sequence or all?
    complexTypeChild = element.find('{0}sequence'.format(namespace))
    if complexTypeChild is not None:
        return generateSequence(request, complexTypeChild, xmlTree, namespace)
    else:
        complexTypeChild = element.find('{0}all'.format(namespace))
        if complexTypeChild is not None:
            return generateSequence(request, complexTypeChild, xmlTree, namespace)
        else:
            # does it contain choice ?
            complexTypeChild = element.find('{0}choice'.format(namespace))
            if complexTypeChild is not None:
                return generateChoice(request, complexTypeChild, xmlTree, namespace)
            else:
                return formString
    
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
    
    #TODO: modules
    if 'name' in element.attrib and element.attrib.get('name') == "ConstituentsType":
        formString += "<div class='module' style='display: inline'>"
        formString += "<div class=\"btn select-element\" onclick=\"selectMultipleElements(this);\"><i class=\"icon-folder-open\"></i> Select Chemical Elements</div>"
        formString += "<div class='moduleDisplay'></div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>"
    
    #TODO: modules
    if 'name' in element.attrib and element.attrib.get('name') == "ChemicalElement":
        formString += "<div class='module' style='display: inline'>"
        formString += "<div class=\"btn select-element\" onclick=\"selectElement(this);\"><i class=\"icon-folder-open\"></i> Select Chemical Element</div>"
        formString += "<div class='moduleDisplay'>Current Selection: None</div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>" 
    
    #TODO: modules
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
def generateElement(request, element, xmlTree, namespace):
    
    xsd_elements = request.session['xsd_elements']
    mapTagElement = request.session['mapTagElement']
    defaultPrefix = request.session['defaultPrefix']
    
    formString = ""

    
    if 'type' not in element.attrib:
        # type is a reference included in the document
        if 'ref' in element.attrib: 
            pass
#             ref = element.attrib['ref']
#             if ':' in ref:
#                 refSplit = ref.split(":")
#                 refNamespacePrefix = refSplit[0]
#                 refName = refSplit[1]
#                 namespaces = request.session['namespaces']
#                 refNamespace = namespaces[refNamespacePrefix]
#                 element = xmlTree.findall("./{0}element[@name='"+refName+"']".format(refNamespace))
#                 formString += generateElement(request, element, xmlTree, refNamespace)
#             else:
#                 element = xmlTree.findall("./{0}element[@name='"+ref+"']".format(namespace))
#                 formString += generateElement(request, element, xmlTree, namespace)
             
        # element with type declared below it
        else:                            
            textCapitalized = element.attrib.get('name')
            addButton, deleteButton, nbOccurrences = manageButtons(element)
                                                    
            elementID = len(xsd_elements)
            xsd_elements[elementID] = etree.tostring(element)
            manageOccurences(request, element, elementID)
            
            formString += "<ul>"                                   
            for x in range (0,int(nbOccurrences)):     
                tagID = "element" + str(len(mapTagElement.keys()))  
                mapTagElement[tagID] = elementID             
                formString += "<li id='" + str(tagID) + "'><nobr>" + textCapitalized
                if (addButton == True):                                
                    formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"
                else:
                    formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"                                                                             
                if (deleteButton == True):
                    formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                else:
                    formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                if element[0].tag == "{0}complexType".format(namespace):
                    formString += generateComplexType(request, element[0], xmlTree, namespace)
                elif element[0].tag == "{0}simpleType".format(namespace):
                    formString += generateSimpleType(request, element[0], xmlTree, namespace)
                formString += "</nobr></li>"
            formString += "</ul>"                        
    elif element.attrib.get('type') in utils.getXSDTypes(defaultPrefix):
        textCapitalized = element.attrib.get('name')
        addButton, deleteButton, nbOccurrences = manageButtons(element)
                    
        elementID = len(xsd_elements)
        xsd_elements[elementID] = etree.tostring(element)
        manageOccurences(request, element, elementID)
        
        formString += "<ul>"                                   
        for x in range (0,int(nbOccurrences)):                         
            tagID = "element" + str(len(mapTagElement.keys()))  
            mapTagElement[tagID] = elementID 
            defaultValue = ""
            if 'default' in element.attrib:
                defaultValue = element.attrib['default']
            formString += "<li id='" + str(tagID) + "'><nobr>" + textCapitalized + " <input type='text' value='"+ defaultValue +"'/>"
                                
            if (addButton == True):                                
                formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"
            else:
                formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"                                

            if (deleteButton == True):
                formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
            else:
                formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
            formString += "</nobr></li>"
        formString += "</ul>"                            
    else:
        if element.attrib.get('type') is not None:
            textCapitalized = element.attrib.get('name')
            addButton, deleteButton, nbOccurrences = manageButtons(element)
                                                    
            elementID = len(xsd_elements)
            xsd_elements[elementID] = etree.tostring(element)
            manageOccurences(request, element, elementID)
            formString += "<ul>"                                   
            for x in range (0,int(nbOccurrences)):                            
                tagID = "element" + str(len(mapTagElement.keys()))  
                mapTagElement[tagID] = elementID 
                formString += "<li id='" + str(tagID) + "'><nobr>" + textCapitalized + " "

                if (addButton == True):                                
                    formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"
                else:
                    formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"
                    
                if (deleteButton == True):
                    formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                else:
                    formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                xpath = "./*[@name='"+element.attrib.get('type')+"']"
                elementType = xmlTree.find(xpath)
                if elementType is not None:
                    if elementType.tag == "{0}complexType".format(namespace):
                        formString += generateComplexType(request, elementType, xmlTree, namespace)
                    elif elementType.tag == "{0}simpleType".format(namespace):
                        formString += generateSimpleType(request, elementType, xmlTree, namespace)
        
                formString += "</nobr></li>"
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
# Function Name: remove(request, tagID, xsdForm)
# Inputs:        request -
#                tagID - 
#                xsdForm -
# Outputs:       JSON data 
# Exceptions:    None
# Description:   Remove an element from the form: make it grey or remove the selected occurrence
#
################################################################################
@dajaxice_register
def remove(request, tagID, xsdForm):
    dajax = Dajax()
    
    occurrences = request.session['occurrences']
    mapTagElement = request.session['mapTagElement']
    
    tagID = "element"+ str(tagID)
    elementID = mapTagElement[tagID]
    elementOccurrencesStr = occurrences[str(elementID)]
    if 'inf' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('inf','float("inf")')
    if 'Infinity' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('Infinity','float("inf")') 
    elementOccurrences = eval(elementOccurrencesStr)

    if (elementOccurrences['nbOccurrences'] > elementOccurrences['minOccurrences']):
        elementOccurrences['nbOccurrences'] -= 1
        occurrences[str(elementID)] = unicode(elementOccurrences)
        request.session['occurrences'] = occurrences
        
        if (elementOccurrences['nbOccurrences'] == 0):    
            dajax.script("""
                $('#add"""+str(tagID[7:])+"""').attr('style','');
                $('#remove"""+str(tagID[7:])+"""').attr('style','display:none');
                $("#"""+tagID+"""").prop("disabled",true);
                $("#"""+tagID+"""").addClass("removed");
                $("#"""+tagID+"""").children("ul").hide(500);
            """)
        else:
            addButton = False
            deleteButton = False
            
            if (elementOccurrences['nbOccurrences'] < elementOccurrences['maxOccurrences']):
                addButton = True
            if (elementOccurrences['nbOccurrences'] > elementOccurrences['minOccurrences']):
                deleteButton = True
                
            htmlTree = html.fromstring(xsdForm)
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
            
            dajax.assign('#xsdForm', 'innerHTML', html.tostring(htmlTree))
    
    request.session.modified = True
    return dajax.json()


################################################################################
# 
# Function Name: duplicate(request, tagID, xsdForm)
# Inputs:        request -
#                tagID -
#                xsdForm -
# Outputs:       JSON data 
# Exceptions:    None
# Description:   Duplicate an occurrence of an element: make it black or add one.
#
################################################################################
@dajaxice_register
def duplicate(request, tagID, xsdForm):
    dajax = Dajax()
    
    xsd_elements = request.session['xsd_elements']
    occurrences = request.session['occurrences']
    mapTagElement = request.session['mapTagElement']
    namespaces = request.session['namespaces']
    defaultPrefix = request.session['defaultPrefix']
    xmlDocTreeStr = request.session['xmlDocTree']
    xmlDocTree = etree.fromstring(xmlDocTreeStr)
    
    formString = ""
    tagID = "element"+ str(tagID)
    elementID = mapTagElement[tagID]
    sequenceChild = etree.fromstring(xsd_elements[str(elementID)])
    elementOccurrencesStr = occurrences[str(elementID)]
    if 'inf' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('inf','float("inf")')
    if 'Infinity' in elementOccurrencesStr:
        elementOccurrencesStr = elementOccurrencesStr.replace('Infinity','float("inf")') 
    elementOccurrences = eval(elementOccurrencesStr)

    if (elementOccurrences['nbOccurrences'] < elementOccurrences['maxOccurrences']):        
        elementOccurrences['nbOccurrences'] += 1
        occurrences[str(elementID)] = unicode(elementOccurrences)
        request.session['occurrences'] = occurrences
        
        if(elementOccurrences['nbOccurrences'] == 1):      
            styleAdd=''
            if (elementOccurrences['maxOccurrences'] == 1):
                styleAdd = 'display:none'
            
            dajax.script("""
                $('#add"""+str(tagID[7:])+"""').attr('style','"""+ styleAdd +"""');
                $('#remove"""+str(tagID[7:])+"""').attr('style','');
                $("#"""+tagID+"""").prop("disabled",false);
                $("#"""+tagID+"""").removeClass("removed");
                $("#"""+tagID+"""").children("ul").show(500);
            """)
        
        else:
            
            # render element
            namespace = namespaces[defaultPrefix]
            if 'type' not in sequenceChild.attrib:
                # type is not present
                if 'ref' in sequenceChild.attrib:
                    # ref is present        
                    print "ref"  
                    return formString            
                else:
                    # type declared below the element
                    textCapitalized = sequenceChild.attrib.get('name')
                    newTagID = "element" + str(len(mapTagElement.keys()))  
                    mapTagElement[newTagID] = elementID  
                    formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " "
                    formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                    formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"            
                    if sequenceChild[0].tag == "{0}complexType".format(namespace):
                        formString += generateComplexType(request, sequenceChild[0], xmlDocTree, namespace)
                    elif sequenceChild[0].tag == "{0}simpleType".format(namespace):
                        formString += generateSimpleType(request, sequenceChild[0], xmlDocTree, namespace)
                    formString += "</nobr></li>"
                    
            # type is XML type
            elif sequenceChild.attrib.get('type') in utils.getXSDTypes(defaultPrefix):
                textCapitalized = sequenceChild.attrib.get('name')                                     
                newTagID = "element" + str(len(mapTagElement.keys())) 
                mapTagElement[newTagID] = elementID
                defaultValue = ""
                if 'default' in sequenceChild.attrib:
                    defaultValue = sequenceChild.attrib['default']
                formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " <input type='text' value='"+ defaultValue +"'/>"
                formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"         
                formString += "</nobr></li>"
            else:
                # type is declared in the document
                if sequenceChild.attrib.get('type') is not None:                  
                    textCapitalized = sequenceChild.attrib.get('name')                      
                    newTagID = "element" + str(len(mapTagElement.keys()))  
                    mapTagElement[newTagID] = elementID 
                    formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " "
                    formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                    formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"           
                    xpath = "./*[@name='"+sequenceChild.attrib.get('type')+"']"
                    elementType = xmlDocTree.find(xpath)
                    if elementType is not None:
                        if elementType.tag == "{0}complexType".format(namespace):
                            formString += generateComplexType(request, elementType, xmlDocTree, namespace)
                        elif elementType.tag == "{0}simpleType".format(namespace):
                            formString += generateSimpleType(request, elementType, xmlDocTree, namespace)                    
                    formString += "</nobr></li>"    
    
            htmlTree = html.fromstring(xsdForm)
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
            
            dajax.assign('#xsdForm', 'innerHTML', html.tostring(htmlTree))            
    
    request.session.modified = True
    return dajax.json()
    
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

    
    if len(elements) == 1:
        formString += "<div xmlID='root'>"
        formString += generateElement(request, elements[0], xmlDocTree,namespace)
        formString += "</div>"
    elif len(elements) > 1:     
        formString += "<div xmlID='root'>"
        formString += generateChoice(request, elements, xmlDocTree, namespace)
        formString += "</div>"

        
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
# Function Name: initCuration(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   Reinitialize data structures
#
################################################################################
@dajaxice_register
def initCuration(request):
    dajax = Dajax()
    
    if 'formString' in request.session:
        del request.session['formString']  
       
    if 'xmlDocTree' in request.session:
        del request.session['xmlDocTree']
    
    return dajax.json()

 
################################################################################
# 
# Function Name: generateXSDTreeForEnteringData(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   Renders HTMl form for display.
#
################################################################################
@dajaxice_register
def generateXSDTreeForEnteringData(request):
    print 'BEGIN def generateXSDTreeForEnteringData(request)'    
    dajax = Dajax()
    
    templateID = request.session['currentTemplateID']

    if 'formString' in request.session:
        formString = request.session['formString']  
    else:
        formString = ''
        request.session['occurrences'] = dict()  
       
    if 'xmlDocTree' in request.session:
        xmlDocTree = request.session['xmlDocTree'] 
    else:
        if templateID in MetaSchema.objects.all().values_list('schemaId'):
            meta = MetaSchema.objects.get(schemaId=templateID)
            xmlDocData = meta.flat_content
        else:
            templateObject = Template.objects.get(pk=templateID)
            xmlDocData = templateObject.content

        xmlDocTree = etree.parse(BytesIO(xmlDocData.encode('utf-8')))
        request.session['xmlDocTree'] = etree.tostring(xmlDocTree)
        xmlDocTree = request.session['xmlDocTree']
        
    # load modules from the database
    if 'mapModules' in request.session:
        del request.session['mapModules']
    html = loadModuleResources(templateID)
    dajax.assign('#modules', 'innerHTML', html)
    mapModules = dict()    
    modules = Module.objects(templates__contains=templateID)  
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
    
    dajax.assign('#periodicTable', 'innerHTML', periodicTableString)

    pathFile = "{0}/static/resources/files/{1}"
    path = pathFile.format(settings.SITE_ROOT,"periodicMultiple.html")
    periodicMultipleTableDoc = open(path,'r')
    periodicTableMultipleString = periodicMultipleTableDoc.read()
    
    dajax.assign('#periodicTableMultiple', 'innerHTML', periodicTableMultipleString)

    dajax.assign('#xsdForm', 'innerHTML', formString)
 
    request.session['formString'] = formString
    
    print 'END def generateXSDTreeForEnteringData(request)'
    return dajax.json()


################################################################################
# 
# Function Name: downloadXML(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   Make the current XML document available for download.
#
################################################################################
@dajaxice_register
def downloadXML(request):
    dajax = Dajax()

    xmlString = request.session['xmlString']
    
    xml2download = XML2Download(xml=xmlString).save()
    xml2downloadID = str(xml2download.id)
    
    dajax.redirect("/curate/view-data/download-XML?id="+xml2downloadID)
    
    return dajax.json()



################################################################################
# 
# Function Name: clearFields(request)
# Inputs:        request -
# Outputs:       
# Exceptions:    None
# Description:   Clears fields of the HTML form. Also restore the occurences.
#
################################################################################
@dajaxice_register
def clearFields(request):
    dajax = Dajax()
    
    # get the original version of the form
    originalForm = request.session['originalForm']
    
    reinitOccurrences(request)    
    
    # assign the form to the page
    dajax.assign('#xsdForm', 'innerHTML', originalForm)
    
    return dajax.json()


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
# Function Name: loadXML(request)
# Inputs:        request - 
# Outputs:       JSON data with templateSelected 
# Exceptions:    None
# Description:   Loads the XML data in the view data page. First transforms the data.
# 
################################################################################
@dajaxice_register
def loadXML(request):
    dajax = Dajax()
    
    xmlString = request.session['xmlString']
    
    xsltPath = os.path.join(settings.SITE_ROOT, 'static/resources/xsl/xml2html.xsl')
    xslt = etree.parse(xsltPath)
    transform = etree.XSLT(xslt)
    xmlTree = ""
    if (xmlString != ""):
        dom = etree.fromstring(xmlString)
        newdom = transform(dom)
        xmlTree = str(newdom)
    
    dajax.assign("#XMLHolder", "innerHTML", xmlTree)
    
    return dajax.json()




# from xlrd import open_workbook
# 
# @dajaxice_register
# def readExcel(request, resourceContent, resourceFilename):
#     dajax = Dajax()
#     
#     request.session['excelContent'] = resourceContent
#     request.session['excelFilename'] = resourceFilename
#     
#     return dajax.json()
# 
# 
# @dajaxice_register
# def uploadExcel(request):
#     dajax = Dajax()
#     
#     resourceContent = request.session['excelContent']
#     resourceFilename = request.session['excelFilename']
#     
#     book = open_workbook(file_contents=resourceContent)
#     
#     root = etree.Element("excel")
#     root.set("name", str(resourceFilename))
#     header = etree.SubElement(root, "header")
#     values = etree.SubElement(root, "values")
#     
#     for sheet in book.sheets():
#         for rowIndex in range(sheet.nrows):
#     
#             if rowIndex != 0:
#                 row = etree.SubElement(values, "row")
#                 row.set("id", str(rowIndex))
#     
#             for colIndex in range(sheet.ncols):
#                 if rowIndex == 0:
#                     col = etree.SubElement(header, "col")
#                 else:
#                     col = etree.SubElement(row, "col")
#     
#                 col.set("id", str(colIndex))
#                 col.text = str(sheet.cell(rowIndex, colIndex).value)
#     
# 
#     hdf5String = etree.tostring(root)
# 
# 
#     templateID = request.session['currentTemplateID']
#     existingHDF5files = Hdf5file.objects(schema=templateID)
#     if existingHDF5files is not None:
#         for hdf5file in existingHDF5files:
#             hdf5file.delete()
#         newHDF5File = Hdf5file(title="hdf5file", schema=templateID, content=hdf5String).save()
#     else:
#         newHDF5File = Hdf5file(title="hdf5file", schema=templateID, content=hdf5String).save()
#     
#     return dajax.json()