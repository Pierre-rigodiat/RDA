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

# Global Variables
debugON = 0


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

    newHTMLForm = Htmlform(title=saveAs, schema=templateID, content=content).save()
    
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
# Function Name: validateXMLData(request, xmlString)
# Inputs:        request - 
#                xmlString - 
# Outputs:       
# Exceptions:    None
# Description:   Check if the current XML document is valid according to the template
#                
#
################################################################################
@dajaxice_register
def validateXMLData(request, xmlString):
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
    
        print "rdf string: " + rdfStr
    
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

    print 'formSelected: ' + formSelected
    htmlFormObject = Htmlform.objects.get(id=formSelected)

    dajax.assign('#xsdForm', 'innerHTML', htmlFormObject.content)

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
    print '>>>>' + templateFilename + ' set as current template in session'
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
        print 'template is selected'
        templateSelected = 'yes'
    else:
        print 'template is not selected'
        templateSelected = 'no'
    dajax = Dajax()

    print 'END def verifyTemplateIsSelected(request)'
    return simplejson.dumps({'templateSelected':templateSelected})


################################################################################
# 
# Function Name: generateFormSubSection(request, xpath, xmlTree, namespace)
# Inputs:        request -
#                xpath - path to the element or element itself
#                xmlTree - XML tree of the template
#                namespace - Namespace used in the template
# Outputs:       JSON data 
# Exceptions:    None
# Description:   Generate a subsection of the HTML string to be inserted in the page.
#
################################################################################
def generateFormSubSection(request, xpath, xmlTree, namespace):
    global debugON
    
    xsd_elements = request.session['xsd_elements']
    mapTagElement = request.session['mapTagElement']
    mapModules = request.session['mapModules']
    namespaces = request.session['namespaces']
    nbChoicesID = int(request.session['nbChoicesID'])
    formString = ""

    if xpath is None:
        print "xpath is none"
        return formString;

    if type(xpath) is str:
        xpathFormated = "./*[@name='"+xpath+"']"
        if debugON: formString += "xpathFormated: " + xpathFormated.format(namespace)
        elems = xmlTree.findall(xpathFormated)
        e = None
        for elem in elems:
            if elem.tag == "{0}simpleType".format(namespace) or elem.tag == "{0}complexType".format(namespace):
                e = elem
                break  
    else:
        e = xpath

    # e is None
    if e is None:
        return formString    
        
    #TODO: module
    if e.attrib.get('name') in mapModules.keys():
        formString += "<div class='module' style='display: inline'>"
        formString += mapModules[e.attrib.get('name')]
        formString += "<div class='moduleDisplay'></div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>"    
        return formString
    
    #TODO: modules
    if 'name' in e.attrib and e.attrib.get('name') == "ConstituentsType":
        formString += "<div class='module' style='display: inline'>"
        formString += "<div class=\"btn select-element\" onclick=\"selectMultipleElements(this);\"><i class=\"icon-folder-open\"></i> Select Chemical Elements</div>"
        formString += "<div class='moduleDisplay'></div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>"
        return formString
    
    #TODO: modules
    if 'name' in e.attrib and e.attrib.get('name') == "ChemicalElement":
        formString += "<div class='module' style='display: inline'>"
        formString += "<div class=\"btn select-element\" onclick=\"selectElement(this);\"><i class=\"icon-folder-open\"></i> Select Chemical Element</div>"
        formString += "<div class='moduleDisplay'>Current Selection: None</div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>" 
        return formString
    
    #TODO: modules
    if 'name' in e.attrib and e.attrib.get('name') == "Table":
        formString += "<div class='module' style='display: inline'>"
        formString += "<div class=\"btn select-element\" onclick=\"selectHDF5File('Spreadsheet File',this);\"><i class=\"icon-folder-open\"></i> Upload Spreadsheet </div>"
        formString += "<div class='moduleDisplay'></div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>"
        return formString
    
    if e.tag == "{0}complexType".format(namespace):
        if debugON: formString += "matched complexType" 
        complexTypeChild = e.find('*')        
                
        if complexTypeChild is None:
            return formString
    
        # skip the annotations
        if (complexTypeChild.tag == "{0}annotation".format(namespace)):
            e.remove(complexTypeChild)
            complexTypeChild = e.find('*')
            
        if complexTypeChild is None:
            return formString

        if complexTypeChild.tag == "{0}sequence".format(namespace):
            if debugON: formString += "complexTypeChild:" + complexTypeChild.tag + "<br>"
            sequenceChildren = complexTypeChild.findall('*')
            for sequenceChild in sequenceChildren:
                if debugON: formString += "SequenceChild:" + sequenceChild.tag + "<br>"
                if sequenceChild.tag == "{0}element".format(namespace):
                    if 'type' not in sequenceChild.attrib:
                        if 'ref' in sequenceChild.attrib: 
                            print "ref"  
                            return formString 
#                             refNamespace = sequenceChild.attrib.get('ref').split(":")[0]
#                             if refNamespace in namespaces.keys():
#                                 refTypeStr = sequenceChild.attrib.get('ref').split(":")[1]
#                                 try:
#                                     addButton = False
#                                     deleteButton = False
#                                     nbOccurrences = 1   
#                                     if ('minOccurs' in sequenceChild.attrib):
#                                         if (sequenceChild.attrib['minOccurs'] == '0'):
#                                             deleteButton = True
#                                         else:
#                                             nbOccurrences = sequenceChild.attrib['minOccurs']
#                                     
#                                     if ('maxOccurs' in sequenceChild.attrib):
#                                         if (sequenceChild.attrib['maxOccurs'] == "unbounded"):
#                                             addButton = True
#                                         elif ('minOccurs' in sequenceChild.attrib):
#                                             if (int(sequenceChild.attrib['maxOccurs']) > int(sequenceChild.attrib['minOccurs'])
#                                                 and int(sequenceChild.attrib['maxOccurs']) > 1):
#                                                 addButton = True   
#                                                 
#                                     elementID = len(xsd_elements)
#                                     xsd_elements[elementID] = etree.tostring(sequenceChild)
#                                     manageOccurences(request, sequenceChild, elementID)   
#                                     formString += "<ul>"                                   
#                                     for x in range (0,int(nbOccurrences)):     
#                                         tagID = "element" + str(len(mapTagElement.keys()))  
#                                         mapTagElement[tagID] = elementID             
#                                         formString += "<li id='" + str(tagID) + "'><nobr>" + refTypeStr
#                                         if (addButton == True):                                
#                                             formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"
#                                         else:
#                                             formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"                                                                             
#                                         if (deleteButton == True):
#                                             formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
#                                         else:
#                                             formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
#                                         formString += generateFormSubSection(request, sequenceChild.attrib['ref'], xmlTree, namespace)
#                                         formString += "</nobr></li>"
#                                     formString += "</ul>"
#                                 except:
#                                     formString += "<ul><li>"+refTypeStr+"</li></ul>"
#                                     print "Unable to find the following reference: " + sequenceChild.attrib.get('ref')
                        # element with type declared below it
                        else:                            
                            textCapitalized = sequenceChild.attrib.get('name')
                            addButton = False
                            deleteButton = False
                            nbOccurrences = 1
                            if ('minOccurs' in sequenceChild.attrib):
                                if (sequenceChild.attrib['minOccurs'] == '0'):
                                    deleteButton = True
                                else:
                                    nbOccurrences = sequenceChild.attrib['minOccurs']
                            
                            if ('maxOccurs' in sequenceChild.attrib):
                                if (sequenceChild.attrib['maxOccurs'] == "unbounded"):
                                    addButton = True
                                elif ('minOccurs' in sequenceChild.attrib):
                                    if (int(sequenceChild.attrib['maxOccurs']) > int(sequenceChild.attrib['minOccurs'])
                                        and int(sequenceChild.attrib['maxOccurs']) > 1):
                                        addButton = True
                                        
                            elementID = len(xsd_elements)
                            xsd_elements[elementID] = etree.tostring(sequenceChild)
                            manageOccurences(request, sequenceChild, elementID)
                            
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
                                formString += generateFormSubSection(request, sequenceChild[0], xmlTree, namespace)
                                formString += "</nobr></li>"
                            formString += "</ul>"                        
                    elif ((sequenceChild.attrib.get('type') == "xsd:string".format(namespace))
                          or (sequenceChild.attrib.get('type') == "xsd:double".format(namespace))
                          or (sequenceChild.attrib.get('type') == "xsd:float".format(namespace)) 
                          or (sequenceChild.attrib.get('type') == "xsd:integer".format(namespace)) 
                          or (sequenceChild.attrib.get('type') == "xsd:anyURI".format(namespace))):
                        textCapitalized = sequenceChild.attrib.get('name')
                        addButton = False
                        deleteButton = False
                        nbOccurrences = 1
                        if ('minOccurs' in sequenceChild.attrib):
                            if (sequenceChild.attrib['minOccurs'] == '0'):
                                deleteButton = True
                            else:
                                nbOccurrences = sequenceChild.attrib['minOccurs']
                        
                        if ('maxOccurs' in sequenceChild.attrib):
                            if (sequenceChild.attrib['maxOccurs'] == "unbounded"):
                                addButton = True
                            elif ('minOccurs' in sequenceChild.attrib):
                                if (int(sequenceChild.attrib['maxOccurs']) > int(sequenceChild.attrib['minOccurs'])
                                    and int(sequenceChild.attrib['maxOccurs']) > 1):
                                    addButton = True
                                    
                        elementID = len(xsd_elements)
                        xsd_elements[elementID] = etree.tostring(sequenceChild)
                        manageOccurences(request, sequenceChild, elementID)
                        formString += "<ul>"                                   
                        for x in range (0,int(nbOccurrences)):                         
                            tagID = "element" + str(len(mapTagElement.keys()))  
                            mapTagElement[tagID] = elementID 
                            formString += "<li id='" + str(tagID) + "'><nobr>" + textCapitalized + " <input type='text'>"
                                                
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
                        if sequenceChild.attrib.get('type') is not None:
                            textCapitalized = sequenceChild.attrib.get('name')
                            addButton = False
                            deleteButton = False
                            nbOccurrences = 1
                            if ('minOccurs' in sequenceChild.attrib):
                                if (sequenceChild.attrib['minOccurs'] == '0'):
                                    deleteButton = True
                                else:
                                    nbOccurrences = sequenceChild.attrib['minOccurs']
                            
                            if ('maxOccurs' in sequenceChild.attrib):
                                if (sequenceChild.attrib['maxOccurs'] == "unbounded"):
                                    addButton = True
                                elif ('minOccurs' in sequenceChild.attrib):
                                    if (int(sequenceChild.attrib['maxOccurs']) > int(sequenceChild.attrib['minOccurs'])
                                        and int(sequenceChild.attrib['maxOccurs']) > 1):
                                        addButton = True
                                        
                            elementID = len(xsd_elements)
                            xsd_elements[elementID] = etree.tostring(sequenceChild)
                            manageOccurences(request, sequenceChild, elementID)
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
                                formString += generateFormSubSection(request, sequenceChild.attrib.get('type'),xmlTree,namespace)
                                formString += "</nobr></li>"
                            formString += "</ul>"
                        else:
                            print "No Type:" + sequenceChild.attrib['name']
                elif sequenceChild.tag == "{0}choice".format(namespace):
                    chooseID = nbChoicesID
                    chooseIDStr = 'choice' + str(chooseID)
                    nbChoicesID += 1
                    request.session['nbChoicesID'] = str(nbChoicesID)
                    formString += "<ul><li><nobr>Choose <select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"
                    choiceChildren = sequenceChild.findall('*')
                    selectedChild = choiceChildren[0]
                    for choiceChild in choiceChildren:
                        if choiceChild.tag == "{0}element".format(namespace):
                            textCapitalized = choiceChild.attrib.get('name')
                            formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
                    formString += "</select>"
                    
                    for (counter, choiceChild) in enumerate(choiceChildren):
                        if choiceChild.tag == "{0}element".format(namespace):
                            if((choiceChild.attrib.get('type') == "xsd:string".format(namespace))
                              or (choiceChild.attrib.get('type') == "xsd:double".format(namespace))
                              or (choiceChild.attrib.get('type') == "xsd:float".format(namespace)) 
                              or (choiceChild.attrib.get('type') == "xsd:integer".format(namespace)) 
                              or (choiceChild.attrib.get('type') == "xsd:anyURI".format(namespace))):
                                textCapitalized = choiceChild.attrib.get('name')                                
                                elementID = len(xsd_elements)
                                xsd_elements[elementID] = etree.tostring(choiceChild)
                                tagID = "element" + str(len(mapTagElement.keys()))  
                                mapTagElement[tagID] = elementID 
                                manageOccurences(request, choiceChild, elementID)
                                if (counter > 0):
                                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li id='" + str(tagID) + "'><nobr>" + choiceChild.attrib.get('name') + " <input type='text'>" + "</nobr></li></ul>"
                                else:
                                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\"><li id='" + str(tagID) + "'><nobr>" + choiceChild.attrib.get('name') + " <input type='text'>" + "</nobr></li></ul>"
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
                                formString += generateFormSubSection(request, choiceChild.attrib.get('type'),xmlTree,namespace) + "</nobr></li></ul>"
                    
                    formString += "</nobr></li></ul>"
        elif complexTypeChild.tag == "{0}choice".format(namespace):
            if debugON: formString += "complexTypeChild:" + complexTypeChild.tag + "<br>"
            chooseID = nbChoicesID        
            chooseIDStr = 'choice' + str(chooseID)
            nbChoicesID += 1
            request.session['nbChoicesID'] = str(nbChoicesID)
            formString += "<ul><li><nobr>Choose <select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"
            choiceChildren = complexTypeChild.findall('*')
            selectedChild = choiceChildren[0]
            for choiceChild in choiceChildren:
                if choiceChild.tag == "{0}element".format(namespace):
                    textCapitalized = choiceChild.attrib.get('name')
                    formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
            formString += "</select>"
            for (counter, choiceChild) in enumerate(choiceChildren):
                if choiceChild.tag == "{0}element".format(namespace):
                    if((choiceChild.attrib.get('type') == "xsd:string".format(namespace))
                      or (choiceChild.attrib.get('type') == "xsd:double".format(namespace))
                      or (choiceChild.attrib.get('type') == "xsd:float".format(namespace)) 
                      or (choiceChild.attrib.get('type') == "xsd:integer".format(namespace)) 
                      or (choiceChild.attrib.get('type') == "xsd:anyURI".format(namespace))):
                        textCapitalized = choiceChild.attrib.get('name')                        
                        elementID = len(xsd_elements)
                        xsd_elements[elementID] = etree.tostring(choiceChild)
                        tagID = "element" + str(len(mapTagElement.keys()))  
                        mapTagElement[tagID] = elementID 
                        manageOccurences(request, choiceChild, elementID)
                        if (counter > 0):
                            formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li id='" + str(tagID) + "'><nobr>" + textCapitalized + " <input type='text'>" + "</nobr></li></ul>"
                        else:
                            formString += "<ul id=\""  + chooseIDStr + "-" + str(counter) + "\"><li id='" + str(tagID) + "'><nobr>" + textCapitalized + " <input type='text'>" + "</nobr></li></ul>"
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
                        formString += generateFormSubSection(request, choiceChild.attrib.get('type'),xmlTree,namespace) + "</nobr></li></ul>"

            formString += "</nobr></li></ul>"
        elif complexTypeChild.tag == "{0}attribute".format(namespace):
            textCapitalized = complexTypeChild.attrib.get('name')
            elementID = len(xsd_elements) 
            xsd_elements[elementID] = etree.tostring(complexTypeChild)
            tagID = "element" + str(len(mapTagElement.keys()))  
            mapTagElement[tagID] = elementID  
            manageOccurences(request, complexTypeChild, elementID)
            formString += "<li id='" + str(tagID) + "'>" + textCapitalized + "</li>"
    elif e.tag == "{0}simpleType".format(namespace):
        if debugON: formString += "matched simpleType"

        simpleTypeChildren = e.findall('*')
        
        if simpleTypeChildren is None:
            return formString

        
        for simpleTypeChild in simpleTypeChildren:
            if simpleTypeChild.tag == "{0}restriction".format(namespace):
                formString += "<select>"
                choiceChildren = simpleTypeChild.findall('*')
                for choiceChild in choiceChildren:
                    if choiceChild.tag == "{0}enumeration".format(namespace):
                        formString += "<option value='" + choiceChild.attrib.get('value')  + "'>" + choiceChild.attrib.get('value') + "</option>"
                formString += "</select>"        
    
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
#                     refNamespace = sequenceChild.attrib.get('ref').split(":")[0]
#                     if refNamespace in namespaces.keys():
#                         refTypeStr = sequenceChild.attrib.get('ref').split(":")[1]
#                         try:
#                             newTagID = "element" + str(len(mapTagElement.keys()))  
#                             mapTagElement[newTagID] = elementID 
#                             formString += "<li id='" + str(newTagID) + "'><nobr>" + refTypeStr + " "
#                             formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
#                             formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"           
#                             formString += duplicateFormSubSection(request, sequenceChild.attrib['ref'], xmlDocTree, namespace)  
#                             formString += "</nobr></li>"  
#                         except:
#                             formString += "<ul><li>"+refTypeStr+"</li></ul>"
#                             print "Unable to find the following reference: " + sequenceChild.attrib.get('ref')
                else:
                    # type declared below the element
                    textCapitalized = sequenceChild.attrib.get('name')
                    newTagID = "element" + str(len(mapTagElement.keys()))  
                    mapTagElement[newTagID] = elementID  
                    formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " "
                    formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                    formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"            
                    formString += duplicateFormSubSection(request, sequenceChild[0], xmlDocTree, namespace)
                    formString += "</nobr></li>"
                    
            # type is XML type
            elif ((sequenceChild.attrib.get('type') == "xsd:string".format(namespace)) or
                (sequenceChild.attrib.get('type') == "xsd:double".format(namespace)) or 
                (sequenceChild.attrib.get('type') == "xsd:integer".format(namespace)) or 
                (sequenceChild.attrib.get('type') == "xsd:anyURI".format(namespace))):
                textCapitalized = sequenceChild.attrib.get('name')                                     
                newTagID = "element" + str(len(mapTagElement.keys())) 
                mapTagElement[newTagID] = elementID
                formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " <input type='text'>"
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
                    formString += duplicateFormSubSection(request, sequenceChild.attrib['type'], xmlDocTree, namespace)
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
                
    return dajax.json()
    

################################################################################
# 
# Function Name: duplicateFormSubSection(request, xpath)
# Inputs:        request -
#                xpath -
#                xmlTree - 
#                namespace - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   Duplicate subsection of an element when the type is complex.
#
################################################################################
def duplicateFormSubSection(request, xpath, xmlTree, namespace):
    print 'BEGIN def duplicateFormSubSection(xpath)'
    
    global debugON
    
    xsd_elements = request.session['xsd_elements']
    mapTagElement = request.session['mapTagElement']
    mapModules = request.session['mapModules']
    namespaces = request.session['namespaces']
    nbChoicesID = int(request.session['nbChoicesID'])
    formString = ""    
 
    if type(xpath) is str:
        xpathFormated = "./*[@name='"+xpath+"']"
        if debugON: formString += "xpathFormated: " + xpathFormated.format(namespace)
        e = xmlTree.find(xpathFormated.format(namespace))
    else:
        e = xpath
        
    if e is None:
        return formString    
    
    #TODO: modules
    if e.attrib.get('name') in mapModules.keys():
        formString += "<div class='module' style='display: inline'>"
        formString += mapModules[e.attrib.get('name')]
        formString += "<div class='moduleDisplay'></div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>"    
        return formString
    
    #TODO: modules
    if 'name' in e.attrib and e.attrib.get('name') == "ConstituentMaterial":
        formString += "<div class='module' style='display: inline'>"
        formString += "<div class=\"btn select-element\" onclick=\"selectMultipleElements(this);\"><i class=\"icon-folder-open\"></i> Select Chemical Elements</div>"
        formString += "<div class='moduleDisplay'></div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>"
        return formString
    
    #TODO: modules
    if 'name' in e.attrib and e.attrib.get('name') == "ChemicalElement":
        formString += "<div class='module' style='display: inline'>"
        formString += "<div class=\"btn select-element\" onclick=\"selectElement(this);\"><i class=\"icon-folder-open\"></i> Select Chemical Element</div>"
        formString += "<div class='moduleDisplay'>Current Selection: None</div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>" 
        return formString
    
    #TODO: modules
    if 'name' in e.attrib and e.attrib.get('name') == "Table":
        formString += "<div class='module' style='display: inline'>"
        formString += "<div class=\"btn select-element\" onclick=\"selectHDF5File('Spreadsheet File',this);\"><i class=\"icon-folder-open\"></i> Upload Spreadsheet </div>"
        formString += "<div class='moduleDisplay'></div>"
        formString += "<div class='moduleResult' style='display: none'></div>"
        formString += "</div>"
        return formString
    
    if e.tag == "{0}complexType".format(namespace):
        if debugON: formString += "matched complexType" 
        print "matched complexType"
        complexTypeChild = e.find('*')

        if complexTypeChild is None:
            return formString

        #TODO: modules
        if 'name' in e.attrib and e.attrib.get('name') == "ConstituentMaterial":
            formString += "<div class='module' style='display: inline'>"
            formString += "<div class=\"btn select-element\" onclick=\"selectMultipleElements(this);\"><i class=\"icon-folder-open\"></i> Select Chemical Elements</div>"
            formString += "<div class='moduleDisplay'></div>"
            formString += "<div class='moduleResult' style='display: none'></div>"
            formString += "</div>"
            return formString
        
        #TODO: modules
        if 'name' in e.attrib and e.attrib.get('name') == "ChemicalElement":
            formString += "<div class='module' style='display: inline'>"
            formString += "<div class=\"btn select-element\" onclick=\"selectElement(this));\"><i class=\"icon-folder-open\"></i> Select Chemical Element</div>"
            formString += "<div class='moduleDisplay'>Current Selection: None</div>"
            formString += "<div class='moduleResult' style='display: none'></div>"
            formString += "</div>" 
            return formString
        
        if complexTypeChild.tag == "{0}sequence".format(namespace):
            if debugON: formString += "complexTypeChild:" + complexTypeChild.tag + "<br>"
            sequenceChildren = complexTypeChild.findall('*')
            for sequenceChild in sequenceChildren:
                if debugON: formString += "SequenceChild:" + sequenceChild.tag + "<br>"
                print "SequenceChild: " + sequenceChild.tag 
                if sequenceChild.tag == "{0}element".format(namespace):
                    if 'type' not in sequenceChild.attrib:
                        if 'ref' in sequenceChild.attrib: 
                            print "ref"  
                            return formString
#                             refNamespace = sequenceChild.attrib.get('ref').split(":")[0]
#                             if refNamespace in namespaces.keys():
#                                 refTypeStr = sequenceChild.attrib.get('ref').split(":")[1]
#                                 try:
#                                     addButton = False
#                                     deleteButton = False
#                                     nbOccurrences = 1
#                                     if ('minOccurs' in sequenceChild.attrib):
#                                         if (sequenceChild.attrib['minOccurs'] == '0'):
#                                             deleteButton = True
#                                         else:
#                                             nbOccurrences = sequenceChild.attrib['minOccurs']
#                                     
#                                     if ('maxOccurs' in sequenceChild.attrib):
#                                         if (sequenceChild.attrib['maxOccurs'] == "unbounded"):
#                                             addButton = True
#                                         elif ('minOccurs' in sequenceChild.attrib):
#                                             if (int(sequenceChild.attrib['maxOccurs']) > int(sequenceChild.attrib['minOccurs'])
#                                                 and int(sequenceChild.attrib['maxOccurs']) > 1):
#                                                 addButton = True   
#                                                 
#                                     elementID = len(xsd_elements)
#                                     xsd_elements[elementID] = etree.tostring(sequenceChild)
#                                     manageOccurences(request, sequenceChild, elementID)   
#                                     formString += "<ul>"                                   
#                                     for x in range (0,int(nbOccurrences)):     
#                                         tagID = "element" + str(len(mapTagElement.keys()))  
#                                         mapTagElement[tagID] = elementID             
#                                         formString += "<li id='" + str(tagID) + "'><nobr>" + refTypeStr
#                                         if (addButton == True):                                
#                                             formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"
#                                         else:
#                                             formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"                                                                             
#                                         if (deleteButton == True):
#                                             formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
#                                         else:
#                                             formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
#                                         formString += duplicateFormSubSection(request, sequenceChild.attrib['ref'], xmlTree, namespace) 
#                                         formString += "</nobr></li>"
#                                     formString += "</ul>"
#                                 except:
#                                     formString += "<ul><li>"+refTypeStr+"</li></ul>"
#                                     print "Unable to find the following reference: " + sequenceChild.attrib.get('ref')
                    elif ((sequenceChild.attrib.get('type') == "xsd:string".format(namespace))
                          or (sequenceChild.attrib.get('type') == "xsd:double".format(namespace))
                          or (sequenceChild.attrib.get('type') == "xsd:float".format(namespace)) 
                          or (sequenceChild.attrib.get('type') == "xsd:integer".format(namespace)) 
                          or (sequenceChild.attrib.get('type') == "xsd:anyURI".format(namespace))):
                        textCapitalized = sequenceChild.attrib.get('name')
                        addButton = False
                        deleteButton = False
                        nbOccurrences = 1
                        if ('minOccurs' in sequenceChild.attrib):
                            if (sequenceChild.attrib['minOccurs'] == '0'):
                                deleteButton = True
                            else:
                                nbOccurrences = sequenceChild.attrib['minOccurs']
                        
                        if ('maxOccurs' in sequenceChild.attrib):
                            if (sequenceChild.attrib['maxOccurs'] == "unbounded"):
                                addButton = True
                            elif ('minOccurs' in sequenceChild.attrib):
                                if (int(sequenceChild.attrib['maxOccurs']) > int(sequenceChild.attrib['minOccurs'])
                                    and int(sequenceChild.attrib['maxOccurs']) > 1):
                                    addButton = True
                                    
                        elementID = len(xsd_elements)
                        xsd_elements[elementID] = etree.tostring(sequenceChild)
                        manageOccurences(request, sequenceChild, elementID)
                        formString += "<ul>"                                   
                        for x in range (0,int(nbOccurrences)):                                                    
                            tagID = "element" + str(len(mapTagElement.keys()))  
                            mapTagElement[tagID] = elementID 
                            formString += "<li id='" + str(tagID) + "'><nobr>" + textCapitalized + " <input type='text'>"
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
                        if sequenceChild.attrib.get('type') is not None:
                            textCapitalized = sequenceChild.attrib.get('name')
                            addButton = False
                            deleteButton = False
                            nbOccurrences = 1
                            if ('minOccurs' in sequenceChild.attrib):
                                if (sequenceChild.attrib['minOccurs'] == '0'):
                                    deleteButton = True
                                else:
                                    nbOccurrences = sequenceChild.attrib['minOccurs']
                            
                            if ('maxOccurs' in sequenceChild.attrib):
                                if (sequenceChild.attrib['maxOccurs'] == "unbounded"):
                                    addButton = True
                                elif ('minOccurs' in sequenceChild.attrib):
                                    if (int(sequenceChild.attrib['maxOccurs']) > int(sequenceChild.attrib['minOccurs'])
                                        and int(sequenceChild.attrib['maxOccurs']) > 1):
                                        addButton = True
                                        
                            elementID = len(xsd_elements)
                            xsd_elements[elementID] = etree.tostring(sequenceChild)
                            manageOccurences(request, sequenceChild, elementID)
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
                                formString += duplicateFormSubSection(request, sequenceChild.attrib.get('type'), xmlTree, namespace)
                                formString += "</nobr></li>"
                            formString += "</ul>"
                        else:
                            print "No Type"
                elif sequenceChild.tag == "{0}choice".format(namespace):
                    chooseID = nbChoicesID
                    chooseIDStr = 'choice' + str(chooseID)
                    nbChoicesID += 1
                    request.session['nbChoicesID'] = str(nbChoicesID)
                    formString += "<ul><li><nobr>Choose <select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"
                    choiceChildren = sequenceChild.findall('*')
                    selectedChild = choiceChildren[0]
                    for choiceChild in choiceChildren:
                        if choiceChild.tag == "{0}element".format(namespace):
                            textCapitalized = choiceChild.attrib.get('name')
                            formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
                    formString += "</select>"
                    
                    for (counter, choiceChild) in enumerate(choiceChildren):
                        if choiceChild.tag == "{0}element".format(namespace):
                            if((choiceChild.attrib.get('type') == "xsd:string".format(namespace))
                              or (choiceChild.attrib.get('type') == "xsd:double".format(namespace))
                              or (choiceChild.attrib.get('type') == "xsd:float".format(namespace)) 
                              or (choiceChild.attrib.get('type') == "xsd:integer".format(namespace)) 
                              or (choiceChild.attrib.get('type') == "xsd:anyURI".format(namespace))):
                                textCapitalized = choiceChild.attrib.get('name')
                                elementID = len(xsd_elements)
                                xsd_elements[elementID] = etree.tostring(choiceChild)
                                tagID = "element" + str(len(mapTagElement.keys()))  
                                mapTagElement[tagID] = elementID 
                                manageOccurences(request, choiceChild, elementID)
                                if (counter > 0):
                                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li id='" + str(tagID) + "'><nobr>" + choiceChild.attrib.get('name') + " <input type='text'>" + "</nobr></li></ul>"
                                else:
                                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\"><li id='" + str(tagID) + "'><nobr>" + choiceChild.attrib.get('name') + " <input type='text'>" + "</nobr></li></ul>"
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
                                formString += duplicateFormSubSection(request, choiceChild.attrib.get('type'), xmlTree, namespace) + "</nobr></li></ul>"
        elif complexTypeChild.tag == "{0}choice".format(namespace):
            if debugON: formString += "complexTypeChild:" + complexTypeChild.tag + "<br>"
            chooseID = nbChoicesID        
            chooseIDStr = 'choice' + str(chooseID)
            nbChoicesID += 1
            request.session['nbChoicesID'] = str(nbChoicesID)
            formString += "<ul><li><nobr>Choose <select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"
            choiceChildren = complexTypeChild.findall('*')
            selectedChild = choiceChildren[0]
            for choiceChild in choiceChildren:
                if choiceChild.tag == "{0}element".format(namespace):
                    textCapitalized = choiceChild.attrib.get('name')
                    formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
            formString += "</select>"
            
            for (counter, choiceChild) in enumerate(choiceChildren):
                if choiceChild.tag == "{0}element".format(namespace):
                    if((choiceChild.attrib.get('type') == "xsd:string".format(namespace))
                      or (choiceChild.attrib.get('type') == "xsd:double".format(namespace))
                      or (choiceChild.attrib.get('type') == "xsd:float".format(namespace)) 
                      or (choiceChild.attrib.get('type') == "xsd:integer".format(namespace)) 
                      or (choiceChild.attrib.get('type') == "xsd:anyURI".format(namespace))):
                        textCapitalized = choiceChild.attrib.get('name')
                        elementID = len(xsd_elements)
                        xsd_elements[elementID] = etree.tostring(choiceChild)
                        tagID = "element" + str(len(mapTagElement.keys()))  
                        mapTagElement[tagID] = elementID 
                        manageOccurences(request, choiceChild, elementID)
                        if (counter > 0):
                            formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li id='" + str(tagID) + "'><nobr>" + choiceChild.attrib.get('name') + " <input type='text'>" + "</nobr></li></ul>"
                        else:
                            formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\"><li id='" + str(tagID) + "'><nobr>" + choiceChild.attrib.get('name') + " <input type='text'>" + "</nobr></li></ul>"
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
                        formString += duplicateFormSubSection(request, choiceChild.attrib.get('type'), xmlTree, namespace) + "</nobr></li></ul>"
        elif complexTypeChild.tag == "{0}attribute".format(namespace):
            textCapitalized = complexTypeChild.attrib.get('name')
            tagID = "element" + str(len(mapTagElement.keys()))  
            mapTagElement[tagID] = elementID  
            manageOccurences(request, complexTypeChild, elementID)
            formString += "<li id='" + str(tagID) + "'>" + textCapitalized + "</li>"            
    elif e.tag == "{0}simpleType".format(namespace):
        if debugON: formString += "matched simpleType"

        simpleTypeChildren = e.findall('*')
        
        if simpleTypeChildren is None:
            return formString

        for simpleTypeChild in simpleTypeChildren:
            if simpleTypeChild.tag == "{0}restriction".format(namespace):
                formString += "<select>"
                choiceChildren = simpleTypeChild.findall('*')
                for choiceChild in choiceChildren:
                    if choiceChild.tag == "{0}enumeration".format(namespace):
                        formString += "<option value='" + choiceChild.attrib.get('value')  + "'>" + choiceChild.attrib.get('value') + "</option>"
                formString += "</select>"
    
    return formString

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
    if 'occurrences' in request.session:
        del request.session['occurrences']
    if 'mapTagElement' in request.session:
        del request.session['mapTagElement']  
    if 'spreadsheetXML' in request.session:
        del request.session['spreadsheetXML']
    request.session['xsd_elements'] = dict()    
    request.session['occurrences'] = dict()
    request.session['mapTagElement'] = dict()
    request.session['spreadsheetXML'] = ""
    defaultPrefix = request.session['defaultPrefix']
    xmlDocTreeStr = request.session['xmlDocTree']
    xmlDocTree = etree.fromstring(xmlDocTreeStr)
    request.session['nbChoicesID'] = '0'
    
    formString = ""
    
    namespace = request.session['namespaces'][defaultPrefix]
    if debugON: formString += "namespace: " + namespace + "<br>"
    e = xmlDocTree.findall("./{0}element".format(namespace))

    if debugON: e = xmlDocTree.findall("{0}complexType/{0}choice/{0}element".format(namespace))
    if debugON: formString += "list size: " + str(len(e))

    if len(e) > 1:
        formString += "<b>" + e[0].attrib.get('name') + "</b><br><ul><li>Choose:"
        for i in e:
            formString += "more than one: " + i.tag + "<br>"
    else:
        textCapitalized = e[0].attrib.get('name')
        formString += "<div xmlID='root'><b>" + textCapitalized + "</b><br>"
        if debugON: formString += "<b>" + e[0].attrib.get('name') + "</b><br>"
        formString += generateFormSubSection(request, e[0].attrib.get('type'), xmlDocTree,namespace)
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

    if 'formString' in request.session:
        formString = request.session['formString']  
    else:
        formString = ''
       
    if 'xmlDocTree' in request.session:
        xmlDocTree = request.session['xmlDocTree'] 
    else:
        xmlDocTree = ""
               
    templateFilename = request.session['currentTemplate']
    templateID = request.session['currentTemplateID']
    print '>>>>' + templateFilename + ' is the current template in session'

    if xmlDocTree == "":
        setCurrentTemplate(request,templateFilename, templateID)
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
    else:
        # the form has already been created and some occurrences may have been change by the user, reinitiliazes the occurrences
        reinitOccurrences(request)

    #TODO: modules
    pathFile = "{0}/static/resources/files/{1}"
    path = pathFile.format(settings.SITE_ROOT,"periodic.html")
    print 'path is ' + path
    periodicTableDoc = open(path,'r')
    periodicTableString = periodicTableDoc.read()
    
    dajax.assign('#periodicTable', 'innerHTML', periodicTableString)

    pathFile = "{0}/static/resources/files/{1}"
    path = pathFile.format(settings.SITE_ROOT,"periodicMultiple.html")
    print 'path is ' + path
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