################################################################################
#
# File Name: ajax.py
# Application: curate
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
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
from curate.models import XMLSchema 
import sys
from xlrd import open_workbook
from argparse import ArgumentError
from cgi import FieldStorage
from cStringIO import StringIO
from django.core.servers.basehttp import FileWrapper

#import xml.etree.ElementTree as etree
import lxml.etree as etree
import xml.dom.minidom as minidom

# Specific to MongoDB ordered inserts
from collections import OrderedDict
from pymongo import Connection
import xmltodict

# Specific to RDF
import rdfPublisher

#XSL file loading
import os
#from django.conf.settings import PROJECT_ROOT

# Global Variables
xmlString = ""
formString = ""
xmlDocTree = ""
xmlDataTree = ""
debugON = 0

# SPARQL : URI for the project (http://www.example.com/)
projectURI = "http://www.example.com/"

# ORDERED DICT : Used by the Wrapper to insert numeric values as numbers (and not string)
def postprocessor(path, key, value):
    try:
        return key, int(value)
    except (ValueError, TypeError):
        try:
            return key, float(value)
        except (ValueError, TypeError):
            return key, value
        
# Class definitions
class Template(Document):
    title = StringField(required=True)
    filename = StringField(required=True)
    content = StringField(required=True)

class Ontology(Document):
    title = StringField(required=True)
    filename = StringField(required=True)
    content = StringField(required=True)

class Htmlform(Document):
    title = StringField(required=True)
    schema = StringField(required=True)
    content = StringField(required=True)

class Xmldata(Document):
    title = StringField(required=True)
    schema = StringField(required=True)
    content = StringField(required=True)

class Hdf5file(Document):
    title = StringField(required=True)
    schema = StringField(required=True)
    content = StringField(required=True)

# ORDERED DICT : Wrapper to insert ordered dict into mongoDB, using mongoengine syntax                                                                                                                                        
class Jsondata():
    """                                                                                                                                                                                                                       
        Wrapper to manage JSON Documents, like mongoengine would have manage them (but with ordered data)                                                                                                                     
    """

    def __init__(self, schemaID=None, xml=None, title=""):
        """                                                                                                                                                                                                                   
            initialize the object                                                                                                                                                                                             
            schema = ref schema (Document)                                                                                                                                                                                    
            xml = xml string 
            title = title of the document                                                                                                                                                                                                 
        """
        # create a connection                                                                                                                                                                                                 
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        self.xmldata = db['xmldata']
        # create a new dict to keep the mongoengine order                                                                                                                                                                     
        self.content = OrderedDict()
        # insert the ref to schema                                                                                                                                                                                            
        self.content['schema'] = schemaID
        # insert the title                                                                                                                                                                                                    
        self.content['title'] = title
        # insert the json content after                                                                                                                                                                                       
        self.content['content'] = xmltodict.parse(xml, postprocessor=postprocessor)

    def save(self):
        """save into mongo db"""
        # insert the content into mongo db                                                                                                                                                                                    
        docID = self.xmldata.insert(self.content)
        return docID

################################################################################
#
# Function Name: getXsdString(request)
# Inputs:        request - 
# Outputs:       XML Schema of the current template
# Exceptions:    None
# Description:   Returns an XML Schema of the current template.
#                The template is is the unmodified version.
#
################################################################################
@dajaxice_register
def getXsdString(request):
    print '>>>> BEGIN def getXsdString(request)'
    dajax = Dajax()

    templateFilename = request.session['currentTemplate']

    templateObject = Template.objects.get(filename=templateFilename)
    xmlDocData = templateObject.content

    xmlString = xmlDocData.encode('utf-8')

    print '>>>> END def getXsdString(request)'
    return simplejson.dumps({'xmlString':xmlString})

################################################################################
#
# Function Name: getCurrentXsdString(request)
# Inputs:        request - 
# Outputs:       XML Schema of the current template
# Exceptions:    None
# Description:   Returns an XML Schema of the current *version* of the template.
#                The template is possibly modified.
#
################################################################################
@dajaxice_register
def getCurrentXsdString(request):
    print '>>>> BEGIN def getXsdString(request)'
    dajax = Dajax()

    global xmlDocTree

    xmlString = xmlDocTree.tostring()

    print '>>>> END def getXsdString(request)'
    return simplejson.dumps({'xmlString':xmlString})

################################################################################
#
# Function Name: getXmlString(request)
# Inputs:        request - 
# Outputs:       XML representation of the current data instance
# Exceptions:    None
# Description:   Returns an XML representation of the current data instance.
#                Used when user wants to download the XML file.
#
################################################################################
@dajaxice_register
def getXmlString(request):
    print '>>>>  BEGIN def getXmlString(request)'
    dajax = Dajax()

#    htmlFormObject = Htmlform.objects.get(title="Form 9")
#    xmlString = htmlFormObject.content

    print '>>>> END def getXmlString(request)'
    return simplejson.dumps({'xmlString':xmlString})

################################################################################
#
# Function Name: getHDF5String(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
@dajaxice_register
def getHDF5String(request):
    print '>>>> BEGIN def getHDF5String(request)'
    dajax = Dajax()

    templateFilename = request.session['currentTemplate']

    hdf5FileObject = Hdf5file.objects.get(title="hdf5file")
    hdf5FileContent = hdf5FileObject.content

    hdf5String = hdf5FileContent.encode('utf-8')

    print hdf5String

    print '>>>> END def getHDF5String(request)'
    return simplejson.dumps({'hdf5String':hdf5String})

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

    connect('mgi')

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
# Function Name: updateFormList(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
@dajaxice_register
def saveHTMLForm(request,saveAs,content):
    print '>>>>  BEGIN def updateFormList(request)'
    dajax = Dajax()

    global formString

    templateID = request.session['currentTemplateID']

    connect('mgi')

#    newHTMLForm = Htmlform(title=saveAs, schema=templateID, content=formString).save()
    newHTMLForm = Htmlform(title=saveAs, schema=templateID, content=content).save()

    print '>>>> END def updateFormList(request)'
    return dajax.json()

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
def saveXMLDataToDB(request,saveAs):
    print '>>>>  BEGIN def saveXMLDataToDB(request,saveAs)'
    dajax = Dajax()

    global xmlString

    templateID = request.session['currentTemplateID']

    connect('mgi')

    #newXMLData = Xmldata(title=saveAs, schema=templateID, content=xmlString).save()

    newJSONData = Jsondata(schemaID=templateID, xml=xmlString, title=saveAs)
    docID = newJSONData.save()

    #xsltPath = './xml2rdf3.xsl' #path to xslt on my machine
    #xsltFile = open(os.path.join(PROJECT_ROOT,'xml2rdf3.xsl'))
    xsltPath = os.path.join(settings.SITE_ROOT, 'static/resources/xsl/xml2rdf3.xsl')
    xslt = etree.parse(xsltPath)
    root = xslt.getroot()
    namespace = root.nsmap['xsl']
    URIparam = root.find("{" + namespace +"}param[@name='BaseURI']") #find BaseURI tag to insert the project URI
    URIparam.text = projectURI + str(docID)

    # SPARQL : transform the XML into RDF/XML
    transform = etree.XSLT(xslt)
    # add a namespace to the XML string, transformation didn't work well using XML DOM
    xmlStr = xmlString.replace('>',' xmlns="' + projectURI + templateID + '">', 1) #TODO: OR schema name...
    # domXML.attrib['xmlns'] = projectURI + schemaID #didn't work well
    domXML = etree.fromstring(xmlStr)
    domRDF = transform(domXML)

    # SPARQL : get the rdf string
    rdfStr = etree.tostring(domRDF)

    print "rdf string: " + rdfStr

    # SPARQL : send the rdf to the triplestore
    rdfPublisher.sendRDF(rdfStr)

    print '>>>>  END def saveXMLDataToDB(request,saveAs)'
    return dajax.json()

################################################################################
#
# Function Name: saveXMLData(request,xmlContent,formContent)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
@dajaxice_register
def saveXMLData(request,xmlContent,formContent):
    print '>>>>  BEGIN def saveXMLData(request,xmlContent,formContent)'
    dajax = Dajax()

    global xmlString
    global formString

    xmlString = xmlContent
    formString = formContent

    print '>>>> END def saveXMLData(request,xmlContent,formContent)'
    return dajax.json()

################################################################################
#
# Function Name: loadFormForEntry(request,formSelected)
# Inputs:        request - 
#                formSelected - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
@dajaxice_register
def loadFormForEntry(request,formSelected):
    print '>>>>  BEGIN def loadFormForEntry(request,formSelected)'
    dajax = Dajax()

    global xmlString

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
# Outputs:       JSON data with success or failure
# Exceptions:    None
# Description:   Set the current template to input argument.  Template is read 
#                into an xsdDocTree for use later.
#
################################################################################
@dajaxice_register
def setCurrentTemplate(request,templateFilename,templateID):
    print 'BEGIN def setCurrentTemplate(request)'
    
    global xmlDocTree
    global xmlString
    global formString

    # reset global variables
    xmlString = ""
    formString = ""

    request.session['currentTemplate'] = templateFilename
    request.session['currentTemplateID'] = templateID
    request.session.modified = True
    print '>>>>' + templateFilename + ' set as current template in session'
    dajax = Dajax()

    templateObject = Template.objects.get(filename=templateFilename)
    xmlDocData = templateObject.content

#    xmlDocTree = etree.parse(BytesIO(xmlDocData.encode('utf-8')))
    print XMLSchema.tree
    XMLSchema.tree = etree.parse(BytesIO(xmlDocData.encode('utf-8')))
    print XMLSchema.tree
    xmlDocTree = XMLSchema.tree

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
    if 'currentTemplate' in request.session:
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
# Function Name: uploadXMLSchema
# Inputs:        request - 
#                XMLSchema - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
# 
################################################################################
@dajaxice_register
def uploadXMLSchema(request,xmlSchemaName,xmlSchemaFilename,xmlSchemaContent):
    print 'BEGIN def uploadXMLSchema(request,xmlSchemaFilename,xmlSchemaContent)'
    dajax = Dajax()

    print 'xmlSchemaName: ' + xmlSchemaName
    print 'xmlSchemaFilename: ' + xmlSchemaFilename
    print 'xmlSchemaContent: ' + xmlSchemaContent

    connect('mgi')
    newTemplate = Template(title=xmlSchemaName, filename=xmlSchemaFilename, content=xmlSchemaContent).save()

    print 'END def uploadXMLSchema(request,xmlSchemaFilename,xmlSchemaContent)'
    return dajax.json()

################################################################################
# 
# Function Name: deleteXMLSchema
# Inputs:        request - 
#                xmlSchemaID - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
# 
################################################################################
@dajaxice_register
def deleteXMLSchema(request,xmlSchemaID):
    print 'BEGIN def deleteXMLSchema(request,xmlSchemaID)'
    dajax = Dajax()

    print 'xmlSchemaID: ' + xmlSchemaID

    connect('mgi')
    selectedSchema = Template.objects(id=xmlSchemaID)[0]
    selectedSchema.delete()

    print 'END def deleteXMLSchema(request,xmlSchemaID)'
    return dajax.json()

################################################################################
# 
# Function Name: uploadXMLOntology
# Inputs:        request - 
#                xmlOntologyFilename - 
#                xmlOntologyContent - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
# 
################################################################################
@dajaxice_register
def uploadXMLOntology(request,xmlOntologyName,xmlOntologyFilename,xmlOntologyContent):
    print 'BEGIN def uploadXMOntology(request,xmlOntologyFilename,xmlOntologyContent)'
    dajax = Dajax()

    print 'xmlOntologyName: ' + xmlOntologyName
    print 'xmlOntologyFilename: ' + xmlOntologyFilename
    print 'xmlOntologyContent: ' + xmlOntologyContent

    connect('mgi')
    newOntology = Ontology(title=xmlOntologyName, filename=xmlOntologyFilename, content=xmlOntologyContent).save()

    print 'END def uploadXMLOntology(request,xmlOntologyFilename,xmlOntologyContent)'
    return dajax.json()

################################################################################
# 
# Function Name: deleteXMLOntology
# Inputs:        request - 
#                xmlOntologyID - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
# 
################################################################################
@dajaxice_register
def deleteXMLOntology(request,xmlOntologyID):
    print 'BEGIN def deleteXMLOntology(request,xmlOntologyID)'
    dajax = Dajax()

    print 'xmlOntologyID: ' + xmlOntologyID

    connect('mgi')
    selectedOntology = Ontology.objects(id=xmlOntologyID)[0]
    selectedOntology.delete()

    print 'END def deleteXMLOntology(request,xmlOntologyID)'
    return dajax.json()

################################################################################
# 
# Function Name: setCurrentModel(request,modelFilename)
# Inputs:        request - 
#                modelFilename - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   Sets current model 
# 
################################################################################
@dajaxice_register
def setCurrentModel(request,modelFilename):
    print 'BEGIN def setCurrentModel(request)'
    request.session['currentTemplate'] = modelFilename
    request.session.modified = True
    print '>>>>' + modelFilename
    dajax = Dajax()

    print 'END def setCurrentModel(request)'
    return dajax.json()

################################################################################
# 
# Function Name: generateFormSubSection(xpath,selected,xmlElement)
# Inputs:        xpath -
#                selected -
#                xmlElement - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
#
################################################################################
def generateFormSubSection(xpath,selected,xmlElement):
    print 'BEGIN def generateFormSubSection(xpath,selected,xmlElement)'
    formString = ""
    global xmlString
    global xmlDocTree
    global xmlDataTree
    global debugON
    p = re.compile('(\{.*\})?schema', re.IGNORECASE)

    namespace = get_namespace(xmlDocTree.getroot())
#    xpathFormated = "./{0}element"
#    xpathFormated = "./{0}complexType[@name='"+xpath+"']"
    if xpath is None:
        print "xpath is none"
        return formString;

    xpathFormated = "./*[@name='"+xpath+"']"
    if debugON: formString += "xpathFormated: " + xpathFormated.format(namespace)
    e = xmlDocTree.find(xpathFormated.format(namespace))

    if e is None:
        return formString

    if e.tag == "{0}complexType".format(namespace):
        if debugON: formString += "matched complexType" 
        print "matched complexType" + "<br>"
        complexTypeChild = e.find('*')

        if complexTypeChild is None:
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
                            if sequenceChild.attrib.get('ref') == "hdf5:HDF5-File":
                                formString += "<ul><li><i><div id='hdf5File'>" + sequenceChild.attrib.get('ref') + "</div></i> "
                                formString += "<div class=\"btn select-element\" onclick=\"selectHDF5File('hdf5:HDF5-File',this);\"><i class=\"icon-folder-open\"></i> Select HDF5 File</div>"
                                formString += "</li></ul>"
                            elif sequenceChild.attrib.get('ref') == "hdf5:Field":
                                formString += "<ul><li><i><div id='hdf5Field'>" + sequenceChild.attrib.get('ref') + "</div></i> "
                                formString += "</li></ul>"
                    elif sequenceChild.attrib.get('type') == "xsd:string".format(namespace):
                        textCapitalized = sequenceChild.attrib.get('name')[0].capitalize()  + sequenceChild.attrib.get('name')[1:]
                        if sequenceChild.attrib.get('occurances') is None:
                            if sequenceChild.attrib.get('minOccurs') is not None:
                                occurances = int(sequenceChild.attrib.get('minOccurs'))
                                sequenceChild.attrib['occurances'] = str(occurances)
                            else:
                                occurances = 1
                                sequenceChild.attrib['occurances'] = str(occurances)
                        else:
                            occurances = int(sequenceChild.attrib['occurances'])
                        print "occurances: " + str(occurances)
                        if occurances == 0:
                            newElement = etree.Element("ul")
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("li")
                            newElement.attrib['text'] = textCapitalized
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("nobr")
                            newElement.text = textCapitalized
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("input")
                            newElement.attrib['type'] = "text"
                            xmlElement.append(newElement)
                            formString += "<ul occurs='0'><li><nobr>" + textCapitalized + " <input type='text' disabled>" 
                            xmlString += "<" + sequenceChild.attrib.get('name') + ">" + "</" + sequenceChild.attrib.get('name') + ">"
                            if sequenceChild.attrib.get('maxOccurs') is not None:
                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                xmlElement = newElement
                                newElement = etree.Element("span")
                                newElement.attrib['class'] = "icon add"
                                xmlElement.append(newElement)
                                formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                formString += "<span class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                            elif sequenceChild.attrib.get('minOccurs') is not None:
                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                xmlElement = newElement
                                newElement = etree.Element("span")
                                newElement.attrib['class'] = "icon remove"
                                xmlElement.append(newElement)
                                formString += "<span class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                            formString += "</nobr></li></ul>"
                        else:
                            for x in range (0,occurances):
                                newElement = etree.Element("ul")
                                xmlElement.append(newElement)
                                xmlElement = newElement
                                newElement = etree.Element("li")
                                newElement.attrib['text'] = textCapitalized
                                xmlElement.append(newElement)
                                xmlElement = newElement
                                newElement = etree.Element("nobr")
                                newElement.text = textCapitalized + " "
                                xmlElement.append(newElement)
                                xmlElement = newElement
                                newElement = etree.Element("input")
                                newElement.attrib['type'] = "text"
                                xmlElement.append(newElement)
                                formString += "<ul occurs=\""+ str(occurances) +"\"><li><nobr>" + textCapitalized + " <input type='text'>"
                                xmlString += "<" + sequenceChild.attrib.get('name') + ">" + "</" + sequenceChild.attrib.get('name') + ">"
                                if sequenceChild.attrib.get('maxOccurs') is not None:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    xmlElement = newElement
                                    newElement = etree.Element("span")
                                    newElement.attrib['class'] = "icon add"
                                    xmlElement.append(newElement)
                                    formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                    if (sequenceChild.attrib.get('maxOccurs') == "unbounded") or (int(sequenceChild.attrib.get('maxOccurs')) != occurances):
                                        currentXPath = xmlDocTree.getpath(sequenceChild)
                                        xmlElement = newElement
                                        newElement = etree.Element("span")
                                        newElement.attrib['class'] = "icon remove"
                                        xmlElement.append(newElement)
                                        formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                    else:
                                        formString += "<span class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                elif sequenceChild.attrib.get('minOccurs') is not None:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    xmlElement = newElement
                                    newElement = etree.Element("span")
                                    newElement.attrib['class'] = "icon remove"
                                    xmlElement.append(newElement)
                                    formString += "<span class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                    formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                formString += "</nobr></li></ul>"
                    elif (sequenceChild.attrib.get('type') == "xsd:double".format(namespace)) or (sequenceChild.attrib.get('type') == "xsd:integer".format(namespace)) or (sequenceChild.attrib.get('type') == "xsd:anyURI".format(namespace)):
                        textCapitalized = sequenceChild.attrib.get('name')[0].capitalize()  + sequenceChild.attrib.get('name')[1:]
                        if sequenceChild.attrib.get('occurances') is None:
                            if sequenceChild.attrib.get('minOccurs') is not None:
                                occurances = int(sequenceChild.attrib.get('minOccurs'))
                                if occurances == 0:
                                    occurances = 1
                                sequenceChild.attrib['occurances'] = str(occurances)
                            else:
                                occurances = 1
                                sequenceChild.attrib['occurances'] = str(occurances)
                        else:
                            occurances = int(sequenceChild.attrib['occurances'])
                        print "occurances: " + str(occurances)
                        if occurances == 0:
                            newElement = etree.Element("ul")
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("li")
                            newElement.attrib['text'] = textCapitalized
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("nobr")
                            newElement.text = textCapitalized + " "
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("input")
                            newElement.attrib['type'] = "text"
                            xmlElement.append(newElement)
                            formString += "<ul occurs=\"0\"><li><nobr>" + textCapitalized + " <input type='text' disabled>"
                            xmlString += "<" + sequenceChild.attrib.get('name') + ">" + "</" + sequenceChild.attrib.get('name') + ">"
                            if sequenceChild.attrib.get('maxOccurs') is not None:
                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                xmlElement = newElement
                                newElement = etree.Element("span")
                                newElement.attrib['class'] = "icon add"
                                xmlElement.append(newElement)
                                formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                formString += "<span class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                            elif sequenceChild.attrib.get('minOccurs') is not None:
                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                xmlElement = newElement
                                newElement = etree.Element("span")
                                newElement.attrib['class'] = "icon add"
                                xmlElement.append(newElement)
                                formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                formString += "<span class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                            formString += "</nobr></li></ul>"
                        else:
                            newElement = etree.Element("ul")
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("li")
                            newElement.attrib['text'] = textCapitalized
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("nobr")
                            newElement.text = textCapitalized + " "
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("input")
                            newElement.attrib['type'] = "text"
                            xmlElement.append(newElement)
                            formString += "<ul occurs=\"" + str(occurances) + "\"><li><nobr>" + textCapitalized + " <input type='text'>"
                            xmlString += "<" + sequenceChild.attrib.get('name') + ">" + "</" + sequenceChild.attrib.get('name') + ">"
                            for x in range (0,occurances):
                                if sequenceChild.attrib.get('maxOccurs') is not None:
                                    if sequenceChild.attrib.get('maxOccurs') != "unbounded":
                                        maxOccurs = int(sequenceChild.attrib.get('maxOccurs'))
                                        if maxOccurs == 0:
                                            currentXPath = xmlDocTree.getpath(sequenceChild)
                                            xmlElement = newElement
                                            newElement = etree.Element("span")
                                            newElement.attrib['class'] = "icon add"
                                            xmlElement.append(newElement)
                                            formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                            formString += "<span class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                    else:
                                        currentXPath = xmlDocTree.getpath(sequenceChild)
                                        xmlElement = newElement
                                        newElement = etree.Element("span")
                                        newElement.attrib['class'] = "icon add"
                                        xmlElement.append(newElement)
                                        formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                        formString += "<span class=\"icon remove\" style=\"display:none\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                if sequenceChild.attrib.get('minOccurs') is not None:
                                    minOccurs = int(sequenceChild.attrib.get('minOccurs'))
                                    if minOccurs == 0:
                                        currentXPath = xmlDocTree.getpath(sequenceChild)
                                        xmlElement = newElement
                                        newElement = etree.Element("span")
                                        newElement.attrib['class'] = "icon remove"
                                        xmlElement.append(newElement)
                                        formString += "<span class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                        formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                            formString += "</nobr></li></ul>"
                    else:
                        if sequenceChild.attrib.get('type') is not None:
                            textCapitalized = sequenceChild.attrib.get('name')[0].capitalize()  + sequenceChild.attrib.get('name')[1:]
                            if sequenceChild.attrib.get('occurances') is None:
                                if sequenceChild.attrib.get('minOccurs') is not None:
                                    occurances = int(sequenceChild.attrib.get('minOccurs'))
                                    if occurances == 0:
                                        occurances = 1
                                    sequenceChild.attrib['occurances'] = str(occurances)
                                else:
                                    occurances = 1
                                    sequenceChild.attrib['occurances'] = str(occurances)
                            else:
                                occurances = int(sequenceChild.attrib['occurances'])
                            print "occurances: " + str(occurances)
                            for x in range (0,occurances):
                                newElement = etree.Element("ul")
                                xmlElement.append(newElement)
                                xmlElement = newElement
                                newElement = etree.Element("li")
                                newElement.attrib['text'] = textCapitalized
                                xmlElement.append(newElement)
                                xmlElement = newElement
                                newElement = etree.Element("nobr")
                                newElement.text = textCapitalized
                                xmlElement.append(newElement)
                                formString += "<ul minOccurs='" + str(sequenceChild.attrib.get('minOccurs'))  + "' occurs=\""+ str(occurances) +"\"><li><nobr>" + textCapitalized + " "
                                xmlString += "<" + sequenceChild.attrib.get('name') + ">" 
                                if sequenceChild.attrib.get('maxOccurs') is not None:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    if (sequenceChild.attrib.get('maxOccurs') == "unbounded"):
                                        xmlElement = newElement
                                        newElement = etree.Element("span")
                                        newElement.attrib['class'] = "icon add"
                                        xmlElement.append(newElement)
                                        formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                        if sequenceChild.attrib.get('minOccurs') is not None:
                                            if (occurances > sequenceChild.attrib.get('minOccurs')):
                                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                                xmlElement = newElement
                                                newElement = etree.Element("span")
                                                newElement.attrib['class'] = "icon remove"
                                                xmlElement.append(newElement)
                                                formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                            else:
                                                formString += "<span class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                        else:
                                            if (occurances > 1):
                                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                                xmlElement = newElement
                                                newElement = etree.Element("span")
                                                newElement.attrib['class'] = "icon remove"
                                                xmlElement.append(newElement)
                                                formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                            else:
                                                formString += "<span class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                    else:
                                        if (int(sequenceChild.attrib.get('maxOccurs')) > occurances):
                                            xmlElement = newElement
                                            newElement = etree.Element("span")
                                            newElement.attrib['class'] = "icon add"
                                            xmlElement.append(newElement)
                                            formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                        if sequenceChild.attrib.get('minOccurs') is not None:
                                            print "occurances: " + str(occurances)
                                            print "minOccurs: " + str(sequenceChild.attrib.get('minOccurs'))
                                            if (occurances > int(sequenceChild.attrib.get('minOccurs'))):
                                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                                xmlElement = newElement
                                                newElement = etree.Element("span")
                                                newElement.attrib['class'] = "icon remove"
                                                xmlElement.append(newElement)
                                                formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                            else:
                                                formString += "<span class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                        else:
                                            if (occurances > 1):
                                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                                xmlElement = newElement
                                                newElement = etree.Element("span")
                                                newElement.attrib['class'] = "icon remove"
                                                xmlElement.append(newElement)
                                                formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                            else:
                                                formString += "<span class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                                elif sequenceChild.attrib.get('minOccurs') is not None:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    xmlElement = newElement
                                    newElement = etree.Element("span")
                                    newElement.attrib['class'] = "icon remove"
                                    xmlElement.append(newElement)
                                    formString += "<span class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                    formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
#                                if sequenceChild.attrib.get('maxOccurs') is not None:
#                                    if sequenceChild.attrib.get('maxOccurs') != "unbounded":
#                                        maxOccurs = int(sequenceChild.attrib.get('maxOccurs'))
#                                        if maxOccurs == 0:
#                                            currentXPath = xmlDocTree.getpath(sequenceChild)
#                                            formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
#                                    else:
#                                        currentXPath = xmlDocTree.getpath(sequenceChild)
#                                        formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
#                                if sequenceChild.attrib.get('minOccurs') is not None:
#                                    minOccurs = int(sequenceChild.attrib.get('minOccurs'))
#                                    if minOccurs == 0:
#                                        currentXPath = xmlDocTree.getpath(sequenceChild)
#                                        formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                formString += generateFormSubSection(sequenceChild.attrib.get('type'),selected,newElement)
                                xmlString += "</" + sequenceChild.attrib.get('name') + ">"
                                formString += "</nobr></li></ul>"
                            
                        else:
                            textCapitalized = sequenceChild.attrib.get('name')[0].capitalize()  + sequenceChild.attrib.get('name')[1:]
                            newElement = etree.Element("ul")
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("li")
                            newElement.attrib['text'] = textCapitalized
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("nobr")
                            newElement.text = textCapitalized
                            xmlElement.append(newElement)
                            formString += "<ul occurs=\"1\"><li><nobr>" + textCapitalized + " "
#                            formString += "<ul><li><nobr>" + textCapitalized + " "
                            xmlString += "<" + sequenceChild.attrib.get('name') + ">" 
                            if sequenceChild.attrib.get('occurances') is None:
                                sequenceChild.attrib['occurances'] = '1'
                            if sequenceChild.attrib.get('maxOccurs') is not None:
                                if sequenceChild.attrib.get('maxOccurs') != "unbounded":
                                    maxOccurs = int(sequenceChild.attrib.get('maxOccurs'))
                                    if maxOccurs == 0:
                                        currentXPath = xmlDocTree.getpath(sequenceChild)
                                        xmlElement = newElement
                                        newElement = etree.Element("span")
                                        newElement.attrib['class'] = "icon add"
                                        xmlElement.append(newElement)
                                        formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                                else:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    xmlElement = newElement
                                    newElement = etree.Element("span")
                                    newElement.attrib['class'] = "icon add"
                                    xmlElement.append(newElement)
                                    formString += "<span class=\"icon add\" onclick=\"changeHTMLForm('add',this);\"></span>"
                            if sequenceChild.attrib.get('minOccurs') is not None:
                                minOccurs = int(sequenceChild.attrib.get('minOccurs'))
                                if minOccurs == 0:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    xmlElement = newElement
                                    newElement = etree.Element("span")
                                    newElement.attrib['class'] = "icon remove"
                                    xmlElement.append(newElement)
                                    formString += "<span class=\"icon remove\" onclick=\"changeHTMLForm('remove',this);\"></span>"
                            formString += generateFormSubSection(sequenceChild.attrib.get('type'),selected,newElement)
                            xmlString += "</" + sequenceChild.attrib.get('name') + ">"
                            formString += "</nobr></li></ul>"
                elif sequenceChild.tag == "{0}choice".format(namespace):
                    newElement = etree.Element("ul")
                    xmlElement.append(newElement)
                    xmlElement = newElement
                    newElement = etree.Element("li")
                    xmlElement.append(newElement)
                    xmlElement = newElement
                    newElement = etree.Element("nobr")
                    newElement.text = "Choose "
                    xmlElement.append(newElement)
                    xmlElement = newElement
                    newElement = etree.Element("select")
                    newElement.attrib['onchange'] = "alert('change to ' + this.value);"
                    xmlElement.append(newElement)
                    xmlElement = newElement
                    formString += "<ul><li><nobr>Choose <select onchange=\"changeChoice(this);\">"
                    choiceChildren = sequenceChild.findall('*')
                    selectedChild = choiceChildren[0]
                    xmlString += "<" + selectedChild.attrib.get('name') + "/>"
                    for choiceChild in choiceChildren:
                        if choiceChild.tag == "{0}element".format(namespace):
                            textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                            newElement = etree.Element("option")
                            newElement.attrib['value'] = textCapitalized 
                            newElement.text = textCapitalized 
                            xmlElement.append(newElement)
                            formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
                    formString += "</select>"
                    print "+++++++++++++++++++++++++++++++++++++++++++"
                    if selected == "":
                        for (counter, choiceChild) in enumerate(choiceChildren):
                            if choiceChild.tag == "{0}element".format(namespace):
                                if choiceChild.attrib.get('type') != "xsd:string".format(namespace):
                                    textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                                    print textCapitalized + " is not string type"
                                    newElement = etree.Element("ul")
                                    newElement.attrib['id'] = textCapitalized
                                    xmlElement.append(newElement)
                                    xmlElement = newElement
                                    newElement = etree.Element("li")
                                    xmlElement.append(newElement)
                                    xmlElement = newElement
                                    newElement = etree.Element("nobr")
                                    newElement.text = textCapitalized
                                    xmlElement.append(newElement)
                                    if (counter > 0):
                                        formString += "<ul id=\"" + textCapitalized + "\" style=\"display:none;\"><li><nobr>" + textCapitalized
                                    else:
                                        formString += "<ul id=\"" + textCapitalized + "\"><li><nobr>" + textCapitalized
                                    xmlString += "<" + textCapitalized + ">" 
                                    formString += generateFormSubSection(choiceChild.attrib.get('type'),selected,newElement) + "</nobr></li></ul>"
                                    xmlString += "</" + textCapitalized + ">"
                                else:
                                    textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                                    print textCapitalized + " is string type"
                                    newElement = etree.Element("ul")
                                    xmlElement.append(newElement)
                                    xmlElement = newElement
                                    newElement = etree.Element("li")
                                    newElement.attrib['id'] = choiceChild.attrib.get('name').capitalize() 
                                    xmlElement.append(newElement)
                                    xmlElement = newElement
                                    newElement = etree.Element("nobr")
                                    newElement.text = choiceChild.attrib.get('name').capitalize() 
                                    xmlElement.append(newElement)
                                    xmlElement = newElement
                                    newElement = etree.Element("option")
                                    newElement.attrib['type'] = "text"
                                    xmlElement.append(newElement)
                                    formString += "<ul><li><nobr>" + choiceChild.attrib.get('name').capitalize() + " <input type='text'>" + "</nobr></li></ul>"
                    else:
                        formString += "selected not empty"
                    formString += "</nobr></li></ul>"
        elif complexTypeChild.tag == "{0}choice".format(namespace):
            if debugON: formString += "complexTypeChild:" + complexTypeChild.tag + "<br>"
            newElement = etree.Element("ul")
            xmlElement.append(newElement)
            xmlElement = newElement
            newElement = etree.Element("li")
            xmlElement.append(newElement)
            xmlElement = newElement
            newElement = etree.Element("nobr")
            newElement.text = "Choose "
            xmlElement.append(newElement)
            xmlElement = newElement
            newElement = etree.Element("select")
            newElement.attrib['onchange'] = "alert('change to ' + this.value);"
            xmlElement.append(newElement)
            xmlElement = newElement
            formString += "<ul><li><nobr>Choose <select onchange=\"changeChoice(this);\">"
            choiceChildren = complexTypeChild.findall('*')
            selectedChild = choiceChildren[0]
            xmlString += "<" + selectedChild.attrib.get('name') + "/>"
            for choiceChild in choiceChildren:
                if choiceChild.tag == "{0}element".format(namespace):
                    textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                    newElement = etree.Element("option")
                    newElement.attrib['value'] = textCapitalized 
                    newElement.text = textCapitalized 
                    xmlElement.append(newElement)
                    formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
            formString += "</select>"
            if selected == "":
                for (counter, choiceChild) in enumerate(choiceChildren):
                    if choiceChild.tag == "{0}element".format(namespace):
                        if choiceChild.attrib.get('type') != "xsd:string".format(namespace):
                            textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                            newElement = etree.Element("ul")
                            newElement.attrib['id'] = textCapitalized
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("li")
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("nobr")
                            newElement.text = textCapitalized
                            xmlElement.append(newElement)
                            if (counter > 0):
                                formString += "<ul id=\"" + textCapitalized + "\" style=\"display:none;\"><li><nobr>" + textCapitalized
                            else:
                                formString += "<ul id=\"" + textCapitalized + "\"><li><nobr>" + textCapitalized
                            xmlString += "<" + textCapitalized + ">" 
                            formString += generateFormSubSection(choiceChild.attrib.get('type'),selected,newElement) + "</nobr></li></ul>"
                            xmlString += "</" + textCapitalized + ">"
                        else:
                            textCapitalized = choiceChild.attrib.get('name').capitalize()
                            newElement = etree.Element("ul")
                            newElement.attrib['id'] = choiceChild.attrib.get('name').capitalize()
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("li")
                            xmlElement.append(newElement)
                            xmlElement = newElement
                            newElement = etree.Element("nobr")
                            newElement.text = choiceChild.attrib.get('name').capitalize()
                            xmlElement.append(newElement)
                            formString += "<ul id=\"" + textCapitalized + "\"><li><nobr>" + textCapitalized + " <input type='text'>" + "</nobr></li></ul>"
            else:
                formString += "selected not empty"
            formString += "</nobr></li></ul>"
        elif complexTypeChild.tag == "{0}attribute".format(namespace):
            textCapitalized = complexTypeChild.attrib.get('name')[0].capitalize()  + complexTypeChild.attrib.get('name')[1:]
            newElement = etree.Element("li")
            newElement.attrib['text'] = textCapitalized
            newElement.text = textCapitalized
            xmlElement.append(newElement)
            xmlElement = newElement
            formString += "<li>" + textCapitalized + "</li>"
            xmlString += "<" + textCapitalized + ">" 
            xmlString += "</" + textCapitalized + ">"
    elif e.tag == "{0}simpleType".format(namespace):
        if debugON: formString += "matched simpleType" + "<br>"

        simpleTypeChildren = e.findall('*')
        
        if simpleTypeChildren is None:
            return formString

        if e.attrib.get('name') == "ChemicalElement":
#            formString += "<div id=\"periodicTable\"></div>"
            currentXPath = xmlDocTree.getpath(e)
            formString += "<div class=\"btn select-element\" onclick=\"selectElement('None',this);\"><i class=\"icon-folder-open\"></i> Select Element</div>"
            formString += "<div id=\"elementSelected\">Current Selection: None</div>"

            return formString

        for simpleTypeChild in simpleTypeChildren:
            if simpleTypeChild.tag == "{0}restriction".format(namespace):
                newElement = etree.Element("select")
#                newElement.attrib['onchange'] = "alert('change to ' + this.value);"
                xmlElement.append(newElement)
                xmlElement = newElement
                formString += "<select>"
                choiceChildren = simpleTypeChild.findall('*')
                selectedChild = choiceChildren[0]
                xmlString += selectedChild.attrib.get('value')
                for choiceChild in choiceChildren:
                    if choiceChild.tag == "{0}enumeration".format(namespace):
                        newElement = etree.Element("option")
                        newElement.attrib['value'] = choiceChild.attrib.get('value')
                        newElement.text = choiceChild.attrib.get('value')
                        xmlElement.append(newElement)
                        formString += "<option value='" + choiceChild.attrib.get('value')  + "'>" + choiceChild.attrib.get('value') + "</option>"
                formString += "</select>"
        

#    for element in xmlDocTree.iter('*'):
#        formString += "Current element:" + element.tag + "<br>"
#        if element.find('*'):
#            elementChild = element.find('*')
#            formString += "match:" + elementChild.tag + "<br>"
#        if p.match(element.tag):
#            if element.get("name"):
#                formString += element.get("name") + "<input type='text' value='" + element.tag + "' style='width:450px'><br>" 
#            else:
#                if p.match(element.tag):
#                    formString += "<input type='text' value='" + element.tag + "' style='width:450px'><br>" 
#                else:
#                    formString += "no match<br>"

    return formString

################################################################################
# 
# Function Name: get_namespace(element)
# Inputs:        element -
# Outputs:       namespace
# Exceptions:    None
# Description:   Helper function that gets namespace
#
################################################################################
def get_namespace(element):
  m = re.match('\{.*\}', element.tag)
  return m.group(0) if m else ''

################################################################################
# 
# Function Name: generateForm(key,xmlElement)
# Inputs:        key -
#                xmlElement -
# Outputs:       rendered HTMl form
# Exceptions:    None
# Description:   Renders HTMl form for display.
#
################################################################################
def generateForm(key,xmlElement):
    print 'BEGIN def generateForm(key,xmlElement)'
    formString = ""
    global xmlString
    global xmlDocTree
    global xmlDataTree

#    schemaRoot = xmlDocTree.getroot()
#    formString += "schemaRoot: " + schemaRoot.tag + "<br>"

#    namespace = "{http://www.w3.org/2001/XMLSchema}"

    namespace = get_namespace(xmlDocTree.getroot())
    if debugON: formString += "namespace: " + namespace + "<br>"
    e = xmlDocTree.findall("./{0}element".format(namespace))

    if debugON: e = xmlDocTree.findall("{0}complexType/{0}choice/{0}element".format(namespace))
    if debugON: formString += "list size: " + str(len(e))

    if len(e) > 1:
        formString += "<b>" + e[0].attrib.get('name').capitalize() + "</b><br><ul><li>Choose:"
        for i in e:
            formString += "more than one: " + i.tag + "<br>"
    else:
        textCapitalized = e[0].attrib.get('name')[0].capitalize()  + e[0].attrib.get('name')[1:]
        newElement = etree.Element("b")
        newElement.text = textCapitalized
        xmlElement.append(newElement)
        newElement = etree.Element("br")
        xmlElement.append(newElement)
        formString += "<div xmlID='root'><b>" + textCapitalized + "</b><br>"
#        xmlDataTree = etree.Element(textCapitalized)
        if debugON: xmlString += "<" + textCapitalized + ">"
        xmlString += "<" + e[0].attrib.get('name') + ">"
        if debugON: formString += "<b>" + e[0].attrib.get('name').capitalize() + "</b><br>"
        formString += generateFormSubSection(e[0].attrib.get('type'),"",xmlElement)
        formString += "</div>"
        if debugON: xmlString += "</" + textCapitalized + ">"
        xmlString += "</" + e[0].attrib.get('name') + ">"
       
    # pretty string
#    s = etree.tostring(xmlDataTree) #, pretty_print=True)
#    print "xmlDataTree:\n" + s

    return formString

################################################################################
# 
# Function Name: generateXSDTreeForEnteringData(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#
################################################################################
@dajaxice_register
def generateXSDTreeForEnteringData(request):
    print 'BEGIN def generateXSDTreeForEnteringData(request)'

    global xmlString
    global formString
    global xmlDocTree
    global xmlDataTree

    dajax = Dajax()

    templateFilename = request.session['currentTemplate']
    templateID = request.session['currentTemplateID']
    print '>>>>' + templateFilename + ' is the current template in session'

    if xmlDocTree == "":
        setCurrentTemplate(request,templateFilename, templateID)

    if (formString == ""):

#    request.session.modified = True


        xmlString = ""
#    print "xsdDocTree: " + str(xmlDocTree)

        formString = "<form id=\"dataEntryForm\" name=\"xsdForm\">"
        newElement = etree.Element("form")
        newElement.attrib['id'] = "dataEntryForm"
        newElement.attrib['name'] = "xsdForm"
        xmlDataTree = etree.ElementTree(newElement)

        formString += generateForm("schema",xmlDataTree.getroot())

#    root = xmlDocTree.getroot()

#    for child in root:
#        print child.tag

        reparsed = minidom.parseString(xmlString)
#    print "xmlDataTree: " + reparsed.toprettyxml(indent="  ")
        formString += "</form>"

#    pretty_xml_as_string = xml.dom.minidom.parseString(xmlDocData).toprettyxml()

#    dajax.assign('#xsdForm', 'innerHTML', etree.ElementTree.tostring(xmlDataTree, encoding='utf8', method='xml'))
#    dajax.assign('#xsdForm', 'innerHTML', etree.tostring(xmlDataTree.getroot(),pretty_print=False))



    dajax.assign('#xsdForm', 'innerHTML', formString)

#    print etree.tostring(xmlDataTree.getroot(),pretty_print=True)

    pathFile = "{0}/static/resources/files/{1}"
    path = pathFile.format(settings.SITE_ROOT,"periodic.html")
    print 'path is ' + path
    periodicTableDoc = open(path,'r')
    periodicTableString = periodicTableDoc.read()

    dajax.assign('#periodicTable', 'innerHTML', periodicTableString)

#    dajax.assign('#xsdForm', 'innerHTML', pretty_xml_as_string)
#    dajax.alert(pretty_xml_as_string)
#    dajax.alert(xmlDocData)
 
    print 'END def generateXSDTreeForEnteringData(request)'
    return dajax.json()

################################################################################
# 
# Function Name: changeXMLSchema(request,operation,xpath,name)
# Inputs:        request - 
#                operation - 
#                xpath - 
#                name - 
# Outputs:       
# Exceptions:    None
# Description:   
#
################################################################################
@dajaxice_register
def changeXMLSchema(request,operation,xpath,name):
    print 'BEGIN def changeXMLSchema(request)'
    dajax = Dajax()

    global xmlString
    global xmlDocTree

    print "operation: " + operation
    print "xpath: " + xpath
    print "name: " + name


    if xmlDocTree == "":
        print "xmlDocTree is null"
        templateFilename = request.session['currentTemplate']
        pathFile = "{0}/xsdfiles/" + templateFilename
        path = pathFile.format(
            settings.SITE_ROOT)
        xmlDocTree = etree.parse(path)
        generateXSDTreeForEnteringData(request)
    else:
        print "xmlDocTree is not null"

    root = xmlDocTree.getroot()
    namespace = get_namespace(xmlDocTree.getroot())

    namespace = namespace[1:-1]

    print "root:"
    print root
    print "namespace: " + namespace

    e = xmlDocTree.xpath(xpath,namespaces={'xsd':namespace})

    print e[0].attrib.get('occurances')
    occurances = int(e[0].attrib.get('occurances'))
    if operation == "add":
        occurances += 1
    else:
        if occurances > 0:
            occurances -= 1
    print occurances
    e[0].attrib['occurances'] = str(occurances)
    
    formString = "<br><form id=\"dataEntryForm\">"
    formString += generateForm("schema","")
    formString += "</form>"
    dajax.assign('#xsdForm', 'innerHTML', formString)

#    generateXSDTreeForEnteringData(request)
    
    print 'END def changeXMLSchema(request)'
    return dajax.json()

