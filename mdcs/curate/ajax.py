################################################################################
#
# File Name: ajax.py
# Application: curate
# Purpose:   
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
import sys
from xlrd import open_workbook
from argparse import ArgumentError
from cgi import FieldStorage
from cStringIO import StringIO
from django.core.servers.basehttp import FileWrapper
from mgi.models import Template, Htmlform, Xmldata, Hdf5file, Jsondata, XML2Download, TemplateVersion, Instance, Request, Module, ModuleResource, Type, TypeVersion
from django.contrib.auth.models import User
from datetime import datetime
from datetime import tzinfo
import requests
import xmltodict
from bson.objectid import ObjectId
from dateutil import tz
import hashlib
import json

#import xml.etree.ElementTree as etree
import lxml.html as html
import lxml.etree as etree
import xml.dom.minidom as minidom

# Specific to RDF
import rdfPublisher

#XSL file loading
import os
from json.decoder import JSONDecoder
from django.core.files.temp import NamedTemporaryFile

# SPARQL : URI for the project (http://www.example.com/)
projectURI = "http://www.example.com/"

# Global Variables
debugON = 0


class ModuleResourceInfo:
    "Class that store information about a resource for a module"
    
    def __init__(self, content = "", filename = ""):
        self.content = content
        self.filename = filename   

    def __to_json__(self):
        return json.dumps(self, default=lambda o:o.__dict__)

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
# Description:   
#                
#
################################################################################
@dajaxice_register
def getHDF5String(request):
#     print '>>>> BEGIN def getHDF5String(request)'
#     dajax = Dajax() 
# 
#     hdf5String = ""
#     try:
#         hdf5FileObject = Hdf5file.objects.get(title="hdf5file")
#         hdf5FileContent = hdf5FileObject.content
#         hdf5FileObject.delete()
#         hdf5String = hdf5FileContent.encode('utf-8')
#     except:
#         pass
#     
#     print hdf5String
# 
#     print '>>>> END def getHDF5String(request)'
#     return simplejson.dumps({'hdf5String':hdf5String})
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

    templateID = request.session['currentTemplateID']

    newHTMLForm = Htmlform(title=saveAs, schema=templateID, content=content).save()

    print '>>>> END def updateFormList(request)'
    return dajax.json()


################################################################################
#
# Function Name: validateXMLData(request, xmlString)
# Inputs:        request - 
#                xmlString - 
# Outputs:       
# Exceptions:    None
# Description:   Check if the current XML document is valid
#                
#
################################################################################
@dajaxice_register
def validateXMLData(request, xmlString):
    dajax = Dajax()
    
    templateID = request.session['currentTemplateID']
    
    request.session['xmlString'] = ""
    
    #TODO: XML validation           
    try:
        validateXMLDocument(templateID, xmlString)   
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
# Function Name: validateXMLDocument(templateID, xmlString)
# Inputs:        request - 
#                templateID - 
#                xmlString - 
# Outputs:       
# Exceptions:    None
# Description:   Check that the XML document is validated by the template
#                
#
################################################################################
def validateXMLDocument(templateID, xmlString):
    template = Template.objects.get(pk=templateID)
    xmlTree = etree.parse(StringIO(template.content.encode('utf-8')))
    
    imports = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}import")
    for import_el in imports:
        refTemplate = Template.objects.get(filename=import_el.attrib['schemaLocation'])
        f  = NamedTemporaryFile()
        f.write(refTemplate.content)
        f.flush()          
        import_el.attrib['schemaLocation'] = f.name.replace('\\', '/')
    
    includes = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}include")
    for include_el in includes:
        refTemplate = Template.objects.get(filename=include_el.attrib['schemaLocation'])
        f  = NamedTemporaryFile()
        f.write(refTemplate.content)
        f.flush()          
        include_el.attrib['schemaLocation'] = f.name.replace('\\', '/')
    
    xmlSchema = etree.XMLSchema(xmlTree)    
    xmlDoc = etree.fromstring(xmlString)
    prettyXMLString = etree.tostring(xmlDoc, pretty_print=True)  
    #xmlSchema.assertValid(etree.parse(StringIO(xmlString)))
    xmlSchema.assertValid(etree.parse(StringIO(prettyXMLString)))  
################################################################################
#
# Function Name: saveXMLDataToDB(request, saveAs)
# Inputs:        request - 
#                saveAs - title of the document
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

    xmlString = request.session['xmlString']
    templateID = request.session['currentTemplateID']

    #TODO: XML validation           
#     try:
#         validateXMLDocument(templateID, xmlString)   
#     except Exception, e:
#         message= e.message.replace('"','\'')
#         dajax.script("""
#             $("#saveErrorMessage").html(" """+ message + """ ");
#             saveXMLDataToDBError();
#         """)
#         return dajax.json()

    #newXMLData = Xmldata(title=saveAs, schema=templateID, content=xmlString).save()

    try:
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
        template = Template.objects.get(pk=templateID)
        xmlStr = xmlString.replace('>',' xmlns="' + projectURI + template.hash + '">', 1) #TODO: OR schema name...
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
# Description:   
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
# Description:   
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
#                into an xsdDocTree for use later.
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
# Function Name: uploadObject
# Inputs:        request - 
#                objectName - 
#                objectFilename - 
#                objectContent -
#                objectType -
# Outputs:       JSON data 
# Exceptions:    None
# Description:   Upload of an object (template or type)
# 
################################################################################
@dajaxice_register
def uploadObject(request,objectName,objectFilename,objectContent, objectType):
    print 'BEGIN def uploadXMLSchema(request,xmlSchemaFilename,xmlSchemaContent)'
    dajax = Dajax()

    #TODO: XML validation
    try:        
        xmlTree = etree.parse(BytesIO(objectContent.encode('utf-8')))
        try:
            imports = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}import")
            for import_el in imports:
                refTemplate = Template.objects.get(filename=import_el.attrib['schemaLocation'])
                f  = NamedTemporaryFile()
                f.write(refTemplate.content)
                f.flush()          
                import_el.attrib['schemaLocation'] = f.name.replace('\\', '/')
            
            includes = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}include")
            for include_el in includes:
                refTemplate = Template.objects.get(filename=include_el.attrib['schemaLocation'])
                f  = NamedTemporaryFile()
                f.write(refTemplate.content)
                f.flush()          
                include_el.attrib['schemaLocation'] = f.name.replace('\\', '/')
            
            xmlSchema = etree.XMLSchema(xmlTree)
        except Exception, e:
            dajax.script("""
                $("#objectNameErrorMessage").html("<font color='red'>Not a valid XML schema.</font><br/>"""+e.message.replace("'","") +""" ");
            """)
            return dajax.json()
    except Exception, e:
        #dajax.script("""alert('"""+e.message.replace("'","") +"""');""")
        dajax.script("""
                $("#objectNameErrorMessage").html("<font color='red'>Not a valid XML document.</font><br/>"""+e.message.replace("'","") +""" ");
            """)
        return dajax.json()     
    
    if objectType == "Template":
        objectVersions = TemplateVersion(nbVersions=1, isDeleted=False).save()
        hash = hashlib.sha1(objectContent)
        hex_dig = hash.hexdigest()
        object = Template(title=objectName, filename=objectFilename, content=objectContent, version=1, templateVersion=str(objectVersions.id), hash=hex_dig).save()
    else:
        objectVersions = TypeVersion(nbVersions=1, isDeleted=False).save()
        object = Type(title=objectName, filename=objectFilename, content=objectContent, version=1, typeVersion=str(objectVersions.id)).save()
    
#     templateVersion = TemplateVersion(nbVersions=1, isDeleted=False).save()
#     newTemplate = Template(title=xmlSchemaName, filename=xmlSchemaFilename, content=xmlSchemaContent, version=1, templateVersion=str(templateVersion.id)).save()
    objectVersions.versions = [str(object.id)]
    objectVersions.current=str(object.id)
    objectVersions.save()    
    object.save()
    

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
def deleteObject(request, objectID, objectType):
    print 'BEGIN def deleteXMLSchema(request,xmlSchemaID)'
    dajax = Dajax()

    if objectType == "Template":
        object = Template.objects.get(pk=objectID)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectID)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)


#     for version in templateVersion.versions:
#         template = Template.objects.get(pk=version)
#         template.delete()
#     templateVersion.delete()
#     selectedSchema.delete()
    objectVersions.deletedVersions.append(str(object.id))    
    objectVersions.isDeleted = True
    objectVersions.save()


    print 'END def deleteXMLSchema(request,xmlSchemaID)'
    return dajax.json()

################################################################################
# 
# Function Name: uploadXMLType
# Inputs:        request - 
#                xmlTypeFilename - 
#                xmlTypeContent - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
# 
################################################################################
@dajaxice_register
def uploadXMLType(request,xmlTypeName,xmlTypeFilename,xmlTypeContent):
    print 'BEGIN def uploadXMType(request,xmlTypeFilename,xmlTypeContent)'
    dajax = Dajax()

    print 'xmlTypeName: ' + xmlTypeName
    print 'xmlTypeFilename: ' + xmlTypeFilename
    print 'xmlTypeContent: ' + xmlTypeContent

    newType = Type(title=xmlTypeName, filename=xmlTypeFilename, content=xmlTypeContent).save()

    print 'END def uploadXMLTypey(request,xmlTypeFilename,xmlTypeContent)'
    return dajax.json()

################################################################################
# 
# Function Name: deleteXMLType
# Inputs:        request - 
#                xmlTypeID - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
# 
################################################################################
@dajaxice_register
def deleteXMLType(request,xmlTypeID):
    print 'BEGIN def deleteXMLType(request,xmlTypeID)'
    dajax = Dajax()

    print 'xmlTypeID: ' + xmlTypeID

    selectedType = Type.objects(id=xmlTypeID)[0]
    selectedType.delete()

    print 'END def deleteXMLType(request,xmlTypeID)'
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
def generateFormSubSection(request, xpath, xmlTree, namespace):
    global debugON
    
    xsd_elements = request.session['xsd_elements']
    mapTagElement = request.session['mapTagElement']
#     mapModules = request.session['mapModules']
    namespaces = request.session['namespaces']
    nbChoicesID = int(request.session['nbChoicesID'])
    formString = ""

    if xpath is None:
        print "xpath is none"
        return formString;

    if type(xpath) is str:
        xpathFormated = "./*[@name='"+xpath+"']"
        if debugON: formString += "xpathFormated: " + xpathFormated.format(namespace)
        e = xmlTree.find(xpathFormated.format(namespace))
    else:
        e = xpath

    # e is None: no element found with the type
    # look for an included type
    if e is None:
        includedTypes = request.session['includedTypes']
        if xpath in includedTypes:
            includedType = Type.objects.get(pk=includedTypes[xpath])
            includedTypeTree = etree.parse(BytesIO(includedType.content.encode('utf-8')))
            element = includedTypeTree.find("{0}element".format(namespace))
            try:                                                    
                if((element.attrib.get('type') == "xsd:string".format(namespace))
                      or (element.attrib.get('type') == "xsd:double".format(namespace))
                      or (element.attrib.get('type') == "xsd:float".format(namespace)) 
                      or (element.attrib.get('type') == "xsd:integer".format(namespace)) 
                      or (element.attrib.get('type') == "xsd:anyURI".format(namespace))):
                    formString +=  "<input type='text'>"
                else:
                    formString += generateFormSubSection(request, element.attrib.get('type'), includedTypeTree, namespace)
                return formString
            except:
                return formString
        else:
            return formString    
        
    #TODOD: module
#     if e.attrib.get('name') in mapModules.keys():
#         formString += mapModules[e.attrib.get('name')]    
#         return formString
    
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
                            refNamespace = sequenceChild.attrib.get('ref').split(":")[0]
                            if refNamespace in namespaces.keys():
                                refTypeStr = sequenceChild.attrib.get('ref').split(":")[1]
                                try:
                                    addButton = False
                                    deleteButton = False
                                    nbOccurrences = 1
                                    refType = Type.objects.get(title=refTypeStr)
                                    refTypeTree = etree.parse(BytesIO(refType.content.encode('utf-8')))    
                                    e = refTypeTree.findall("./{0}element[@name='{1}']".format(namespace,refTypeStr))     
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
                                        formString += "<li id='" + str(tagID) + "'><nobr>" + refTypeStr
                                        if (addButton == True):                                
                                            formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"
                                        else:
                                            formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"                                                                             
                                        if (deleteButton == True):
                                            formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                                        else:
                                            formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                                        formString += generateFormSubSection(request, e[0].attrib.get('type'), refTypeTree, namespace)
                                        formString += "</nobr></li>"
                                    formString += "</ul>"
                                except:
                                    formString += "<ul><li>"+refTypeStr+"</li></ul>"
                                    print "Unable to find the following reference: " + sequenceChild.attrib.get('ref')
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
        if debugON: formString += "matched simpleType" + "<br>"

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
    


@dajaxice_register
def remove(request, tagID, xsdForm):
    dajax = Dajax()
    
    occurrences = request.session['occurrences']
    mapTagElement = request.session['mapTagElement']
    
    tagID = "element"+ str(tagID)
    elementID = mapTagElement[tagID]
#     sequenceChild = xsd_elements[elementID]
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
            #desactiver les couleurs etc pour elementX        
            dajax.script("""
                $('#add"""+str(tagID[7:])+"""').attr('style','');
                $('#remove"""+str(tagID[7:])+"""').attr('style','display:none');
                $("#"""+tagID+"""").prop("disabled",true);
                $("#"""+tagID+"""").css("color","#D8D8D8");
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
# Function Name: duplicate(tagID)
# Inputs:        xpath -
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
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
                $("#"""+tagID+"""").css("color","#000000");
                $("#"""+tagID+"""").children("ul").show(500);
            """)
        
        else:
            
            # render element
            namespace = namespaces[defaultPrefix]
            if 'type' not in sequenceChild.attrib:
                if 'ref' in sequenceChild.attrib:                    
                    refNamespace = sequenceChild.attrib.get('ref').split(":")[0]
                    if refNamespace in namespaces.keys():
                        refTypeStr = sequenceChild.attrib.get('ref').split(":")[1]
                        try:
                            refType = Type.objects.get(title=refTypeStr)
                            refTypeTree = etree.parse(BytesIO(refType.content.encode('utf-8')))    
                            e = refTypeTree.findall("./{0}element[@name='{1}']".format(namespace,refTypeStr))                                                             
                            newTagID = "element" + str(len(mapTagElement.keys()))  
                            mapTagElement[newTagID] = elementID 
                            formString += "<li id='" + str(newTagID) + "'><nobr>" + refTypeStr + " "
                            formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                            formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"           
                            formString += duplicateFormSubSection(request, e[0].attrib.get('type'), refTypeTree, namespace)  
                            formString += "</nobr></li>"  
                        except:
                            formString += "<ul><li>"+refTypeStr+"</li></ul>"
                            print "Unable to find the following reference: " + sequenceChild.attrib.get('ref')
                else:
                    textCapitalized = sequenceChild.attrib.get('name')
                    newTagID = "element" + str(len(mapTagElement.keys()))  
                    mapTagElement[newTagID] = elementID  
                    formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " "
                    formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                    formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"            
                    formString += duplicateFormSubSection(request, sequenceChild[0], xmlDocTree, namespace)
                    formString += "</nobr></li>"
            elif sequenceChild.attrib.get('type') == "xsd:string".format(namespace):
                textCapitalized = sequenceChild.attrib.get('name')                                     
                newTagID = "element" + str(len(mapTagElement.keys())) 
                mapTagElement[newTagID] = elementID
                formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " <input type='text'>"
                formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"         
                formString += "</nobr></li>"
            elif (sequenceChild.attrib.get('type') == "xsd:double".format(namespace)) or (sequenceChild.attrib.get('type') == "xsd:integer".format(namespace)) or (sequenceChild.attrib.get('type') == "xsd:anyURI".format(namespace)):
                textCapitalized = sequenceChild.attrib.get('name')
                newTagID = "element" + str(len(mapTagElement.keys()))  
                mapTagElement[newTagID] = elementID 
                formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " <input type='text'>"
                formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"        
                formString += "</nobr></li>"
            else:
                if sequenceChild.attrib.get('type') is not None:
                    xpathFormated = "./*[@name='"+sequenceChild.attrib['type']+"']"
                    elementType = xmlDocTree.find(xpathFormated.format(namespace))
                    if elementType is None:
                        includedTypes = request.session['includedTypes']
                        xpath = sequenceChild.attrib['type']
                        if xpath in includedTypes:
                            includedType = Type.objects.get(pk=includedTypes[xpath])
                            includedTypeTree = etree.parse(BytesIO(includedType.content.encode('utf-8')))
                            element = includedTypeTree.find("{0}element".format(namespace))
                            if 'name' in sequenceChild.attrib:
                                textCapitalized = sequenceChild.attrib.get('name')
                            else:
                                textCapitalized = sequenceChild.attrib.get('type').split(":")[1]
                            newTagID = "element" + str(len(mapTagElement.keys()))
                            mapTagElement[newTagID] = elementID
                            formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " "
                            formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                            formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"                        
                            e = includedTypeTree.find("./*[@type='{0}:{1}']".format(request.session['defaultPrefix'],xpath))
                            if e is not None:
                                if ((e.attrib['type'] == "xsd:string".format(namespace)) or 
                                    (e.attrib['type'] == "xsd:double".format(namespace)) or
                                    (e.attrib['type'] == "xsd:integer".format(namespace)) or
                                    (e.attrib['type'] == "xsd:anyURI".format(namespace))):
                                    formString += " <input type='text'>"
                            else:
                                formString += duplicateFormSubSection(request, sequenceChild.attrib['type'], includedTypeTree, namespace)
                            formString += "</nobr></li>"                            
#TODO: temporary solution before model change, look for the type in every type
#                     for externalType in Type.objects:
#                         refTypeTree = etree.parse(BytesIO(externalType.content.encode('utf-8')))    
#                         e = refTypeTree.findall("./{0}element[@name='{1}']".format(namespace,sequenceChild.attrib.get('type')))
#                         if e is not None:
#                             textCapitalized = sequenceChild.attrib.get('name')
#                             newTagID = "element" + str(len(mapTagElement.keys()))  
#                             mapTagElement[newTagID] = elementID 
#                             formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " "
#                             formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
#                             formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"            
#                             formString += duplicateFormSubSection(request, sequenceChild.attrib['type'], refTypeTree, namespace)
#                             formString += "</nobr></li>"
#                             break
                    else:                    
                        textCapitalized = sequenceChild.attrib.get('name')                      
                        newTagID = "element" + str(len(mapTagElement.keys()))  
                        mapTagElement[newTagID] = elementID 
                        formString += "<li id='" + str(newTagID) + "'><nobr>" + textCapitalized + " "
                        formString += "<span id='add"+ str(newTagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(newTagID[7:])+");\"></span>"
                        formString += "<span id='remove"+ str(newTagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(newTagID[7:])+");\"></span>"           
                        formString += duplicateFormSubSection(request, sequenceChild.attrib['type'], xmlDocTree, namespace)
                        formString += "</nobr></li>"            
                else:
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
# Function Name: duplicateFormSubSection(xpath)
# Inputs:        xpath -
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
#
################################################################################
def duplicateFormSubSection(request, xpath, xmlTree, namespace):
    print 'BEGIN def duplicateFormSubSection(xpath)'
    
    global debugON
    
    xsd_elements = request.session['xsd_elements']
    mapTagElement = request.session['mapTagElement']
#     mapModules = request.session['mapModules']
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
#     if e.attrib.get('name') in mapModules.keys():
#         formString += mapModules[e.attrib.get('name')]    
#         return formString 
    
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
        print "matched complexType" + "<br>"
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
                            if sequenceChild.attrib.get('ref') == "hdf5:HDF5-File":
#                                 formString += "<ul><li><i><div id='hdf5File'>Spreadsheet File</div></i> "
#                                 formString += "<div class=\"btn select-element\" onclick=\"selectHDF5File('Spreadsheet File',this);\"><i class=\"icon-folder-open\"></i> Upload Spreadsheet </div>"
#                                 formString += "</li></ul>"
                                formString += "<div class='module' style='display: inline'>"
                                formString += "<div class=\"btn select-element\" onclick=\"selectHDF5File('Spreadsheet File',this);\"><i class=\"icon-folder-open\"></i> Upload Spreadsheet </div>"
                                formString += "<div class='moduleDisplay'></div>"
                                formString += "<div class='moduleResult' style='display: none'></div>"
                                formString += "</div>"
                            elif sequenceChild.attrib.get('ref') == "hdf5:Field":
                                formString += "<ul><li><i><div id='hdf5Field'>" + sequenceChild.attrib.get('ref') + "</div></i> "
                                formString += "</li></ul>"
                            else:
                                refNamespace = sequenceChild.attrib.get('ref').split(":")[0]
                                if refNamespace in namespaces.keys():
                                    refTypeStr = sequenceChild.attrib.get('ref').split(":")[1]
                                    try:
                                        addButton = False
                                        deleteButton = False
                                        nbOccurrences = 1
                                        refType = Type.objects.get(title=refTypeStr)
                                        refTypeTree = etree.parse(BytesIO(refType.content.encode('utf-8')))    
                                        e = refTypeTree.findall("./{0}element[@name='{1}']".format(namespace,refTypeStr))     
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
                                            formString += "<li id='" + str(tagID) + "'><nobr>" + refTypeStr
                                            if (addButton == True):                                
                                                formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"
                                            else:
                                                formString += "<span id='add"+ str(tagID[7:]) +"' class=\"icon add\" style=\"display:none;\" onclick=\"changeHTMLForm('add',this,"+str(tagID[7:])+");\"></span>"                                                                             
                                            if (deleteButton == True):
                                                formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                                            else:
                                                formString += "<span id='remove"+ str(tagID[7:]) +"' class=\"icon remove\" style=\"display:none;\" onclick=\"changeHTMLForm('remove',this,"+str(tagID[7:])+");\"></span>"
                                            formString += duplicateFormSubSection(request, e[0].attrib.get('type'), refTypeTree, namespace) 
                                            formString += "</nobr></li>"
                                        formString += "</ul>"
                                    except:
                                        formString += "<ul><li>"+refTypeStr+"</li></ul>"
                                        print "Unable to find the following reference: " + sequenceChild.attrib.get('ref')
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
        if debugON: formString += "matched simpleType" + "<br>"

        simpleTypeChildren = e.findall('*')
        
        if simpleTypeChildren is None:
            return formString

        #TODO: modules
#         if e.attrib.get('name') == "ChemicalElement":
# #            formString += "<div id=\"periodicTable\"></div>"
#             formString += "<div class=\"btn select-element\" onclick=\"selectElement('None',this,"+str(nbSelectedElement)+");\"><i class=\"icon-folder-open\"></i> Select Chemical Element</div>"
#             formString += "<div id=\"elementSelected"+ str(nbSelectedElement) +"\">Current Selection: None</div>"
#             nbSelectedElement += 1
#             return formString

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

def getIncludedTypes(xmlTreeStr, namespace):
    includedTypes = dict()
    
    xmlTree = etree.fromstring(xmlTreeStr)
    listIncludes = xmlTree.findall("{0}include".format(namespace))
    if (len(listIncludes) > 0):
        for include in listIncludes:
            if 'schemaLocation' in include.attrib:
                try:
                    includedType = Type.objects.get(filename=include.attrib['schemaLocation'])
                    includedTypes[includedType.title] = str(includedType.id)
                except:
                    pass
    
    return includedTypes
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

def loadModuleResources(templateID):
    modules = Module.objects(template=templateID)
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
# Description:   
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
    modules = Module.objects(template=templateID)  
    for module in modules:
        mapModules[module.tag] = module.htmlTag
    request.session['mapModules'] = mapModules    
    
    # find the namespaces
    request.session['namespaces'] = get_namespaces(BytesIO(str(xmlDocTree)))
    for prefix, url in request.session['namespaces'].items():
        if (url == "{http://www.w3.org/2001/XMLSchema}"):            
            request.session['defaultPrefix'] = prefix
            break
    
    # load included types from the database
    if 'includedTypes' in request.session:
        del request.session['includedTypes']
    includedTypes = getIncludedTypes(xmlDocTree, request.session['namespaces'][request.session['defaultPrefix']]);
    request.session['includedTypes'] = includedTypes
    
    if (formString == ""):                
        formString = "<form id=\"dataEntryForm\" name=\"xsdForm\">"
        formString += generateForm(request)
        formString += "</form>"
        request.session['originalForm'] = formString

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


@dajaxice_register
def downloadXML(request):
    dajax = Dajax()

    xmlString = request.session['xmlString']
    
    xml2download = XML2Download(xml=xmlString).save()
    xml2downloadID = str(xml2download.id)
    
    dajax.redirect("/curate/view-data/download-XML?id="+xml2downloadID)
    
    return dajax.json()


@dajaxice_register
def manageVersions(request, objectID, objectType):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectID)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectID)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
#     template = Template.objects.get(pk=schemaID)
#     templateVersions = TemplateVersion.objects.get(pk=template.templateVersion)
    
    htmlVersionsList = "<p><b>upload new version:</b>"
    htmlVersionsList += "<input type='file' id='fileVersion' name='files[]'></input>"
    htmlVersionsList += "<span class='btn' id='updateVersionBtn' versionid='"+str(objectVersions.id)+"' objectType='"+ objectType +"' onclick='uploadVersion()'>upload</span></p>"
    htmlVersionsList += "<div id='versionNameErrorMessage'></div>"
    htmlVersionsList += "<table>"    
    
    
    i = len(objectVersions.versions)
    for obj_versionID in reversed(objectVersions.versions):
        if objectType == "Template":
            obj = Template.objects.get(pk=obj_versionID)
        else:
            obj = Type.objects.get(pk=obj_versionID)
#         tpl = Template.objects.get(pk=tpl_versionID)        
        htmlVersionsList += "<tr>"
        htmlVersionsList += "<td>Version " + str(obj.version) + "</td>"
        if str(obj.id) == str(objectVersions.current):
            htmlVersionsList += "<td style='font-weight:bold;color:green'>Current</td>"
            htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>"
        elif str(obj.id) in objectVersions.deletedVersions:
            htmlVersionsList += "<td style='color:red'>Deleted</td>"
            htmlVersionsList += "<td><span class='icon legend retrieve' id='restore"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='restoreVersion(restore"+str(i)+")'>Restore</span></td>"
        else:
            htmlVersionsList += "<td><span class='icon legend long' id='setcurrent"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='setCurrentVersion(setcurrent"+str(i)+")'>Set Current</span></td>"
            htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>"        
        objectid = ObjectId(obj.id)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        datetimeUTC = objectid.generation_time
        datetimeUTC = datetimeUTC.replace(tzinfo=from_zone)
        datetimeLocal = datetimeUTC.astimezone(to_zone)
        htmlVersionsList += "<td>" + datetimeLocal.strftime('%m/%d/%Y %H&#58;%M&#58;%S') + "</td>"
        htmlVersionsList += "</tr>"
        i -= 1
    htmlVersionsList += "</table>"     
    if objectType == "Template":
        handler = "handleSchemaVersionUpload"
    else:
        handler = "handleTypeVersionUpload"
    dajax.script("""
        $("#object_versions").html(" """+ htmlVersionsList +""" ");    
        $("#delete_custom_message").html("");
        $(function() {
            $("#dialog-manage-versions").dialog({
              modal: true,
              width: 500,
              buttons: {
                Ok: function() {
                  $( this ).dialog( "close" );
                  $('#model_selection').load(document.URL +  ' #model_selection', function() {
                      loadUploadManagerHandler();
                  });                  
                },
                Cancel: function() {
                  $( this ).dialog( "close" );  
                  $('#model_selection').load(document.URL +  ' #model_selection', function() {
                      loadUploadManagerHandler();
                  });                
                }
              }
            });            
          });
        document.getElementById('fileVersion').addEventListener('change',"""+ handler +""", false);
    """)
    return dajax.json()


@dajaxice_register
def setSchemaVersionContent(request, versionContent, versionFilename):
    dajax = Dajax()
    
    request.session['xsdVersionContent'] = versionContent
    request.session['xsdVersionFilename'] = versionFilename
    
    return dajax.json()

@dajaxice_register
def setTypeVersionContent(request, versionContent, versionFilename):
    dajax = Dajax()
    
    request.session['typeVersionContent'] = versionContent
    request.session['typeVersionFilename'] = versionFilename
    
    return dajax.json()

@dajaxice_register
def uploadVersion(request, objectVersionID, objectType):
    dajax = Dajax()    
        
    if objectType == "Template":      
        if ('xsdVersionContent' in request.session 
        and 'xsdVersionFilename' in request.session 
        and request.session['xsdVersionContent'] != "" 
        and request.session['xsdVersionFilename'] != ""):
            objectVersions = TemplateVersion.objects.get(pk=objectVersionID)
            object = Template.objects.get(pk=objectVersions.current)
            versionContent = request.session['xsdVersionContent']
            versionFilename = request.session['xsdVersionFilename']
            
            try:        
                xmlTree = etree.parse(BytesIO(versionContent.encode('utf-8')))
                try:
                    imports = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}import")
                    for import_el in imports:
                        refTemplate = Template.objects.get(filename=import_el.attrib['schemaLocation'])
                        f  = NamedTemporaryFile()
                        f.write(refTemplate.content)
                        f.flush()          
                        import_el.attrib['schemaLocation'] = f.name.replace('\\', '/')
                    
                    includes = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}include")
                    for include_el in includes:
                        refTemplate = Template.objects.get(filename=include_el.attrib['schemaLocation'])
                        f  = NamedTemporaryFile()
                        f.write(refTemplate.content)
                        f.flush()          
                        include_el.attrib['schemaLocation'] = f.name.replace('\\', '/')
                    
                    xmlSchema = etree.XMLSchema(xmlTree)
                except Exception, e:
                    dajax.script("""
                        $("#versionNameErrorMessage").html("<font color='red'>Not a valid XML schema.</font><br/>"""+e.message.replace("'","") +""" ");
                    """)
                    return dajax.json()
            except Exception, e:
                dajax.script("""
                        $("#versionNameErrorMessage").html("<font color='red'>Not a valid XML document.</font><br/>"""+e.message.replace("'","") +""" ");
                    """)
                return dajax.json()
        else:
            return dajax.json()
    else:
        if ('typeVersionContent' in request.session 
        and 'typeVersionFilename' in request.session 
        and request.session['typeVersionContent'] != "" 
        and request.session['typeVersionFilename'] != ""):
            objectVersions = TypeVersion.objects.get(pk=objectVersionID)
            object = Type.objects.get(pk=objectVersions.current)
            versionContent = request.session['typeVersionContent']
            versionFilename = request.session['typeVersionFilename']
        else:
            return dajax.json()

    if versionContent != "" and versionFilename != "":
#         templateVersions = TemplateVersion.objects.get(pk=templateVersionID)
#         currentTemplate = Template.objects.get(pk=templateVersions.current)
        objectVersions.nbVersions += 1
        if objectType == "Template": 
            hash = hashlib.sha1(versionContent)
            hex_dig = hash.hexdigest()
            newObject = Template(title=object.title, filename=versionFilename, content=versionContent, templateVersion=objectVersionID, version=objectVersions.nbVersions, hash=hex_dig).save()
        else:
            newObject = Type(title=object.title, filename=versionFilename, content=versionContent, typeVersion=objectVersionID, version=objectVersions.nbVersions).save()
        objectVersions.versions.append(str(newObject.id))
        objectVersions.save()
        
        htmlVersionsList = "<p><b>upload new version:</b>"
        htmlVersionsList += "<input type='file' id='fileVersion' name='files[]'></input>"
        htmlVersionsList += "<span class='btn' id='updateVersionBtn' versionid='"+str(objectVersions.id)+"' objectType='"+ objectType +"' onclick='uploadVersion()'>upload</span></p>"
        htmlVersionsList += "<div id='versionNameErrorMessage'></div>"
        htmlVersionsList += "<table>"    
        
        
        i = len(objectVersions.versions)
        for obj_versionID in reversed(objectVersions.versions):
            if objectType == "Template":
                obj = Template.objects.get(pk=obj_versionID)
            else:
                obj = Ttype.objects.get(pk=obj_versionID)
            htmlVersionsList += "<tr>"
            htmlVersionsList += "<td>Version " + str(obj.version) + "</td>"
            if str(obj.id) == str(objectVersions.current):
                htmlVersionsList += "<td style='font-weight:bold;color:green'>Current</td>"
                htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>"
            elif str(obj.id) in objectVersions.deletedVersions:
                htmlVersionsList += "<td style='color:red'>Deleted</td>"
                htmlVersionsList += "<td><span class='icon legend retrieve' id='restore"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='restoreVersion(restore"+str(i)+")'>Restore</span></td>"
            else:
                htmlVersionsList += "<td><span class='icon legend long' id='setcurrent"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='setCurrentVersion(setcurrent"+str(i)+")'>Set Current</span></td>"
                htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>" 
            objectid = ObjectId(obj.id)
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            datetimeUTC = objectid.generation_time
            datetimeUTC = datetimeUTC.replace(tzinfo=from_zone)
            datetimeLocal = datetimeUTC.astimezone(to_zone)
            htmlVersionsList += "<td>" + datetimeLocal.strftime('%m/%d/%Y %H&#58;%M&#58;%S') + "</td>"         
            htmlVersionsList += "</tr>"
            i -= 1
        htmlVersionsList += "</table>"     
        if objectType == "Template":
            handler = "handleSchemaVersionUpload"
        else:
            handler = "handleTypeVersionUpload"
        dajax.script("""
            $("#object_versions").html(" """+ htmlVersionsList +""" ");    
            $("#delete_custom_message").html("");
            document.getElementById('fileVersion').addEventListener('change',"""+ handler +""", false);
        """)
    else:
        dajax.script("""showUploadErrorDialog();""");
    
    if objectType == "Template":
        request.session['xsdVersionContent'] = ""
        request.session['xsdVersionFilename'] = ""
    else:
        request.session['typeVersionContent'] = ""
        request.session['typeVersionFilename'] = ""
        
    return dajax.json()


@dajaxice_register
def setCurrentVersion(request, objectid, objectType):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
    
#     selectedTemplate = Template.objects.get(pk=schemaid)
#     templateVersions = TemplateVersion.objects.get(pk=selectedTemplate.templateVersion)
    objectVersions.current = str(object.id)
    objectVersions.save()
    
    htmlVersionsList = "<p><b>upload new version:</b>"
    htmlVersionsList += "<input type='file' id='fileVersion' name='files[]'></input>"
    htmlVersionsList += "<span class='btn' id='updateVersionBtn' versionid='"+str(objectVersions.id)+"' objectType='"+ objectType +"' onclick='uploadVersion()'>upload</span></p>"
    htmlVersionsList += "<div id='versionNameErrorMessage'></div>"
    htmlVersionsList += "<table>"    
    
    
    i = len(objectVersions.versions)
    for obj_versionID in reversed(objectVersions.versions):
        if objectType == "Template":
            obj = Template.objects.get(pk=obj_versionID)
        else:
            obj = Type.objects.get(pk=obj_versionID)
        htmlVersionsList += "<tr>"
        htmlVersionsList += "<td>Version " + str(obj.version) + "</td>"
        if str(obj.id) == str(objectVersions.current):
            htmlVersionsList += "<td style='font-weight:bold;color:green'>Current</td>"
            htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>"
        elif str(obj.id) in objectVersions.deletedVersions:
            htmlVersionsList += "<td style='color:red'>Deleted</td>"
            htmlVersionsList += "<td><span class='icon legend retrieve' id='restore"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='restoreVersion(restore"+str(i)+")'>Restore</span></td>"
        else:
            htmlVersionsList += "<td><span class='icon legend long' id='setcurrent"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='setCurrentVersion(setcurrent"+str(i)+")'>Set Current</span></td>"
            htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>"          
        objectid = ObjectId(obj.id)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        datetimeUTC = objectid.generation_time
        datetimeUTC = datetimeUTC.replace(tzinfo=from_zone)
        datetimeLocal = datetimeUTC.astimezone(to_zone)
        htmlVersionsList += "<td>" + datetimeLocal.strftime('%m/%d/%Y %H&#58;%M&#58;%S') + "</td>"
        htmlVersionsList += "</tr>"
        i -= 1
    htmlVersionsList += "</table>"     
    
    if objectType == "Template":
        handler = "handleSchemaVersionUpload"
    else:
        handler = "handleTypeVersionUpload"

    dajax.script("""
        $("#object_versions").html(" """+ htmlVersionsList +""" ");    
        $("#delete_custom_message").html("");
        document.getElementById('fileVersion').addEventListener('change',"""+ handler +""", false);
    """)
    
    return dajax.json()

@dajaxice_register
def deleteVersion(request, objectid, objectType, newCurrent):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
    
#     selectedTemplate = Template.objects.get(pk=schemaid)
#     templateVersions = TemplateVersion.objects.get(pk=selectedTemplate.templateVersion)    

    if len(objectVersions.versions) == 1 or len(objectVersions.versions) == len(objectVersions.deletedVersions) + 1:
#         selectedTemplate.delete()
        objectVersions.deletedVersions.append(str(object.id))    
#         templateVersions.delete()
        objectVersions.isDeleted = True
        objectVersions.save()
        dajax.script("""
        $("#delete_custom_message").html("");
        $("#dialog-manage-versions").dialog( "close" );
        $('#model_selection').load(document.URL +  ' #model_selection', function() {
          loadUploadManagerHandler();
        });    
        """)
    else:
        if newCurrent != "": 
            objectVersions.current = newCurrent
#         del templateVersions.versions[templateVersions.versions.index(schemaid)]
        objectVersions.deletedVersions.append(str(object.id))   
        objectVersions.save()
#         selectedTemplate.delete()
        
        htmlVersionsList = "<p><b>upload new version:</b>"
        htmlVersionsList += "<input type='file' id='fileVersion' name='files[]'></input>"
        htmlVersionsList += "<span class='btn' id='updateVersionBtn' versionid='"+str(objectVersions.id)+"' objectType='"+ objectType +"' onclick='uploadVersion()'>upload</span></p>"
        htmlVersionsList += "<div id='versionNameErrorMessage'></div>"
        htmlVersionsList += "<table>"    
        
        
        i = len(objectVersions.versions)
        for obj_versionID in reversed(objectVersions.versions):
            if objectType == "Template":
                obj = Template.objects.get(pk=obj_versionID)
            else:
                obj = Type.objects.get(pk=obj_versionID)
            htmlVersionsList += "<tr>"
            htmlVersionsList += "<td>Version " + str(obj.version) + "</td>"
            if str(obj.id) == str(objectVersions.current):
                htmlVersionsList += "<td style='font-weight:bold;color:green'>Current</td>"
                htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>"
            elif str(obj.id) in objectVersions.deletedVersions:
                htmlVersionsList += "<td style='color:red'>Deleted</td>"
                htmlVersionsList += "<td><span class='icon legend retrieve' id='restore"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='restoreVersion(restore"+str(i)+")'>Restore</span></td>"
            else:
                htmlVersionsList += "<td><span class='icon legend long' id='setcurrent"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='setCurrentVersion(setcurrent"+str(i)+")'>Set Current</span></td>"
                htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>"     
            objectid = ObjectId(obj.id)
            from_zone = tz.tzutc()
            to_zone = tz.tzlocal()
            datetimeUTC = objectid.generation_time
            datetimeUTC = datetimeUTC.replace(tzinfo=from_zone)
            datetimeLocal = datetimeUTC.astimezone(to_zone)
            htmlVersionsList += "<td>" + datetimeLocal.strftime('%m/%d/%Y %H&#58;%M&#58;%S') + "</td>"
            htmlVersionsList += "</tr>"
            i -= 1
        htmlVersionsList += "</table>"    
        if objectType == "Template":
            handler = "handleSchemaVersionUpload"
        else:
            handler = "handleTypeVersionUpload"
        
        dajax.script("""
            $("#object_versions").html(" """+ htmlVersionsList +""" "); 
            $("#delete_custom_message").html("");   
            document.getElementById('fileVersion').addEventListener('change',"""+ handler +""", false);
        """)
    
    return dajax.json()

@dajaxice_register
def assignDeleteCustomMessage(request, objectid, objectType):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
        
#     selectedTemplate = Template.objects.get(pk=schemaid)
#     templateVersions = TemplateVersion.objects.get(pk=selectedTemplate.templateVersion)    
    
    message = ""

    if len(objectVersions.versions) == 1:
        message = "<span style='color:red'>You are about to delete the only version of this "+ objectType +". The "+ objectType +" will be deleted from the "+ objectType +" manager.</span>"
    elif objectVersions.current == str(object.id) and len(objectVersions.versions) == len(objectVersions.deletedVersions) + 1:
        message = "<span style='color:red'>You are about to delete the last version of this "+ objectType +". The "+ objectType +" will be deleted from the "+ objectType +" manager.</span>"
    elif objectVersions.current == str(object.id):
        message = "<span>You are about to delete the current version. If you want to continue, please select a new current version: <select id='selectCurrentVersion'>"
        for version in objectVersions.versions:
            if version != objectVersions.current and version not in objectVersions.deletedVersions:
                if objectType == "Template":
                    obj = Template.objects.get(pk=version)
                else:
                    obj = Type.objects.get(pk=version)
                message += "<option value='"+version+"'>Version " + str(obj.version) + "</option>"
        message += "</select></span>"
    
    dajax.assign("#delete_custom_message", "innerHTML", message)
    
    return dajax.json()

@dajaxice_register
def editInformation(request, objectid, objectType, newName, newFilename):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
    
#     selectedTemplate = Template.objects.get(pk=schemaid)       
#     templateVersions = TemplateVersion.objects.get(pk=selectedTemplate.templateVersion)
    
    for version in objectVersions.versions:
        if objectType == "Template":
            obj = Template.objects.get(pk=version)
        else:
            obj = Type.objects.get(pk=version)
        obj.title = newName
        if version == objectid:
            obj.filename = newFilename
        obj.save()
    
    dajax.script("""
        $("#dialog-edit-info").dialog( "close" );
        $('#model_selection').load(document.URL +  ' #model_selection', function() {
              loadUploadManagerHandler();
        });
    """)
    
    return dajax.json()

@dajaxice_register
def restoreObject(request, objectid, objectType):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
    
#     selectedTemplate = Template.objects.get(pk=schemaid)       
#     templateVersions = TemplateVersion.objects.get(pk=selectedTemplate.templateVersion)
    objectVersions.isDeleted = False
    del objectVersions.deletedVersions[objectVersions.deletedVersions.index(objectVersions.current)]
    objectVersions.save()
    
    dajax.script("""
        $('#model_selection').load(document.URL +  ' #model_selection', function() {
              loadUploadManagerHandler();
        });
    """)
    
    return dajax.json()

@dajaxice_register
def restoreVersion(request, objectid, objectType):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
    
#     selectedTemplate = Template.objects.get(pk=schemaid)
#     templateVersions = TemplateVersion.objects.get(pk=selectedTemplate.templateVersion)
    del objectVersions.deletedVersions[objectVersions.deletedVersions.index(objectid)]
    objectVersions.save()
    
    htmlVersionsList = "<p><b>upload new version:</b>"
    htmlVersionsList += "<input type='file' id='fileVersion' name='files[]'></input>"
    htmlVersionsList += "<span class='btn' id='updateVersionBtn' versionid='"+str(objectVersions.id)+"' objectType='"+ objectType +"' onclick='uploadVersion()'>upload</span></p>"
    htmlVersionsList += "<div id='versionNameErrorMessage'></div>"
    htmlVersionsList += "<table>"    
    
    
    i = len(objectVersions.versions)
    for obj_versionID in reversed(objectVersions.versions):
        if objectType == "Template":
            obj = Template.objects.get(pk=obj_versionID)
        else:
            obj = Type.objects.get(pk=obj_versionID)
        htmlVersionsList += "<tr>"
        htmlVersionsList += "<td>Version " + str(obj.version) + "</td>"
        if str(obj.id) == str(objectVersions.current):
            htmlVersionsList += "<td style='font-weight:bold;color:green'>Current</td>"
            htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>"
        elif str(obj.id) in objectVersions.deletedVersions:
            htmlVersionsList += "<td style='color:red'>Deleted</td>"
            htmlVersionsList += "<td><span class='icon legend retrieve' id='restore"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='restoreVersion(restore"+str(i)+")'>Restore</span></td>"
        else:
            htmlVersionsList += "<td><span class='icon legend long' id='setcurrent"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='setCurrentVersion(setcurrent"+str(i)+")'>Set Current</span></td>"
            htmlVersionsList += "<td><span class='icon legend delete' id='delete"+str(i)+"' objectid='"+str(obj.id)+"' objectType='"+ objectType +"' onclick='deleteVersion(delete"+str(i)+")'>Delete</span></td>"          
        objectid = ObjectId(obj.id)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        datetimeUTC = objectid.generation_time
        datetimeUTC = datetimeUTC.replace(tzinfo=from_zone)
        datetimeLocal = datetimeUTC.astimezone(to_zone)
        htmlVersionsList += "<td>" + datetimeLocal.strftime('%m/%d/%Y %H&#58;%M&#58;%S') + "</td>"
        htmlVersionsList += "</tr>"
        i -= 1
    htmlVersionsList += "</table>"     
    if objectType == "Template":
        handler = "handleSchemaVersionUpload"
    else:
        handler = "handleTypeVersionUpload"
    dajax.script("""
        $("#object_versions").html(" """+ htmlVersionsList +""" ");    
        $("#delete_custom_message").html("");
        document.getElementById('fileVersion').addEventListener('change',"""+ handler +""", false);
    """)
    
    return dajax.json()

@dajaxice_register
def addInstance(request, name, protocol, address, port, user, password):
    dajax = Dajax()
    
    errors = ""
    
    # test if the name is "Local"
    if (name == "Local"):
        errors += "By default, the instance named Local is the instance currently running."
    else:
        # test if an instance with the same name exists
        instance = Instance.objects(name=name)
        if len(instance) != 0:
            errors += "An instance with the same name already exists.<br/>"
    
    # test if new instance is not the same as the local instance
    if address == request.META['REMOTE_ADDR'] and port == request.META['SERVER_PORT']:
        errors += "The address and port you entered refer to the instance currently running."
    else:
        # test if an instance with the same address/port exists
        instance = Instance.objects(address=address, port=port)
        if len(instance) != 0:
            errors += "An instance with the address/port already exists.<br/>"
    
    # If some errors display them, otherwise insert the instance
    if(errors == ""):
        status = "Unreachable"
        try:
            url = protocol + "://" + address + ":" + port + "/api/ping"
            r = requests.get(url, auth=(user, password))
            if r.status_code == 200:
                status = "Reachable"
        except Exception, e:
            pass
        
        Instance(name=name, protocol=protocol, address=address, port=port, user=user, password=password, status=status).save()
        dajax.script("""
        $("#dialog-add-instance").dialog("close");
        $('#model_selection').load(document.URL +  ' #model_selection', function() {
              loadFedOfQueriesHandler();
        });
        """)
    else:
        dajax.assign("#instance_error", "innerHTML", errors)
    
    return dajax.json()

@dajaxice_register
def retrieveInstance(request, instanceid):
    dajax = Dajax()
    
    instance = Instance.objects.get(pk=instanceid)
    dajax.script(
    """
    $("#edit-instance-name").val('"""+ instance.name +"""');
    $("#edit-instance-protocol").val('"""+ instance.protocol +"""');
    $("#edit-instance-address").val('"""+ instance.address +"""');
    $("#edit-instance-port").val('"""+ str(instance.port) +"""');
    $("#edit-instance-user").val('"""+ str(instance.user) +"""');
    $("#edit-instance-password").val('"""+ str(instance.password) +"""');
    $(function() {
        $( "#dialog-edit-instance" ).dialog({
            modal: true,
            height: 450,
            width: 275,
            buttons: {
                Edit: function() {
                    name = $("#edit-instance-name").val()
                    protocol = $("#edit-instance-protocol").val()
                    address = $("#edit-instance-address").val()
                    port = $("#edit-instance-port").val()     
                    user = $("#edit-instance-user").val()
                    password = $("#edit-instance-password").val()
                    
                    errors = checkFields(protocol, address, port, user, password);
                    
                    if (errors != ""){
                        $("#edit_instance_error").html(errors)
                    }else{
                        Dajaxice.curate.editInstance(Dajax.process,{"instanceid":'"""+instanceid+"""',"name":name, "protocol": protocol, "address":address, "port":port, "user": user, "password": password});
                    }
                },
                Cancel: function() {                        
                    $( this ).dialog( "close" );
                }
            }
        });
    });
    """             
    )
    
    return dajax.json()

@dajaxice_register
def editInstance(request, instanceid, name, protocol, address, port, user, password):
    dajax = Dajax()
    
    errors = ""
    
    # test if the name is "Local"
    if (name == "Local"):
        errors += "By default, the instance named Local is the instance currently running."
    else:   
        # test if an instance with the same name exists
        instance = Instance.objects(name=name)
        if len(instance) != 0 and str(instance[0].id) != instanceid:
            errors += "An instance with the same name already exists.<br/>"
    
    # test if new instance is not the same as the local instance
    if address == request.META['REMOTE_ADDR'] and port == request.META['SERVER_PORT']:
        errors += "The address and port you entered refer to the instance currently running."
    else:
        # test if an instance with the same address/port exists
        instance = Instance.objects(address=address, port=port)
        if len(instance) != 0 and str(instance[0].id) != instanceid:
            errors += "An instance with the address/port already exists.<br/>"
    
    # If some errors display them, otherwise insert the instance
    if(errors == ""):
        status = "Unreachable"
        try:
            url = protocol + "://" + address + ":" + port + "/api/ping"
            r = requests.get(url, auth=(user, password))
            if r.status_code == 200:
                status = "Reachable"
        except Exception, e:
            pass
        
        instance = Instance.objects.get(pk=instanceid)
        instance.name = name
        instance.protocol = protocol
        instance.address = address
        instance.port = port
        instance.user = user
        instance.password = password
        instance.status = status
        instance.save()
        dajax.script("""
        $("#dialog-edit-instance").dialog("close");
        $('#model_selection').load(document.URL +  ' #model_selection', function() {
              loadFedOfQueriesHandler();
        });
        """)
    else:
        dajax.assign("#edit_instance_error", "innerHTML", errors)
    
    return dajax.json()

@dajaxice_register
def deleteInstance(request, instanceid):
    dajax = Dajax()
    
    instance = Instance.objects.get(pk=instanceid)
    instance.delete()
    
    dajax.script("""
        $("#dialog-deleteinstance-message").dialog("close");
        $('#model_selection').load(document.URL +  ' #model_selection', function() {
              loadFedOfQueriesHandler();
        });
    """)
    
    return dajax.json()

@dajaxice_register
def clearFields(request):
    dajax = Dajax()
    
    # get the original version of the form
    originalForm = request.session['originalForm']
    
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
    
    
    # assign the form to the page
    dajax.assign('#xsdForm', 'innerHTML', originalForm)
    
    return dajax.json()


@dajaxice_register
def pingRemoteAPI(request, name, protocol, address, port, user, password):
    dajax = Dajax()
    
    try:
        url = protocol + "://" + address + ":" + port + "/api/ping"
        r = requests.get(url, auth=(user, password))
        if r.status_code == 200:
            dajax.assign("#instance_error", "innerHTML", "<b style='color:green'>Remote API reached with success.</b>")
        else:
            if 'detail' in eval(r.content):
                dajax.assign("#instance_error", "innerHTML", "<b style='color:red'>Error: " + eval(r.content)['detail'] + "</b>")
            else:
                dajax.assign("#instance_error", "innerHTML", "<b style='color:red'>Error: Unable to reach the remote API.</b>")
    except Exception, e:
        dajax.assign("#instance_error", "innerHTML", "<b style='color:red'>Error: Unable to reach the remote API.</b>")
        
    
    return dajax.json()

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

@dajaxice_register
def requestAccount(request, username, password, firstname, lastname, email):
    dajax = Dajax()
    try:
        user = User.objects.get(username=username)
        dajax.script(
         """
            $("#listErrors").html("This user already exist. Please choose another username.");
            $(function() {
                $( "#dialog-errors-message" ).dialog({
                  modal: true,
                  buttons: {
                    Ok: function() {
                      $( this ).dialog( "close" );
                    }
                  }
                });
              });
         """)
    except:
        Request(username=username, password=password ,first_name=firstname, last_name=lastname, email=email).save()
        dajax.script(
         """
            $(function() {
                $( "#dialog-request-sent" ).dialog({
                  modal: true,
                  buttons: {
                    Ok: function() {
                      $( this ).dialog( "close" );
                      window.location = "/";
                    }
                  }
                });
              });
         """)
    return dajax.json()

@dajaxice_register
def acceptRequest(request, requestid):
    dajax = Dajax()
    userRequest = Request.objects.get(pk=requestid)
    try:
        existingUser = User.objects.get(username=userRequest.username)
        dajax.script(
        """
            $(function() {
                $( "#dialog-error-request" ).dialog({
                  modal: true,
                  buttons: {
                    Ok: function() {
                      $( this ).dialog( "close" );
                    }
                  }
                });
              });              
        """)        
    except:
        user = User.objects.create_user(username=userRequest.username, password=userRequest.password, first_name=userRequest.first_name, last_name=userRequest.last_name, email=userRequest.email)
        user.save()
        userRequest.delete()
        dajax.script(
        """
            $(function() {
                $( "#dialog-accepted-request" ).dialog({
                  modal: true,
                  buttons: {
                    Ok: function() {
                      $( this ).dialog( "close" );
                    }
                  }
                });
              });
              $('#model_selection').load(document.URL +  ' #model_selection', function() {
                  loadUserRequestsHandler();
              });
        """)
        
    return dajax.json()

@dajaxice_register
def denyRequest(request, requestid):
    dajax = Dajax()
    userRequest = Request.objects.get(pk=requestid)
    userRequest.delete()
    dajax.script(
    """
      $('#model_selection').load(document.URL +  ' #model_selection', function() {
          loadUserRequestsHandler();
      });
    """)
    return dajax.json()

@dajaxice_register
def initModuleManager(request):
    dajax = Dajax()
    
    request.session['listModuleResource'] = []
    
    return dajax.json()

@dajaxice_register
def addModuleResource(request, resourceContent, resourceFilename):
    dajax = Dajax()
    
    request.session['currentResourceContent'] = resourceContent
    request.session['currentResourceFilename'] = resourceFilename    
    
    return dajax.json()


@dajaxice_register
def uploadResource(request):
    dajax = Dajax()
    
    if ('currentResourceContent' in request.session 
        and request.session['currentResourceContent'] != "" 
        and 'currentResourceFilename' in request.session 
        and request.session['currentResourceFilename'] != ""):
            request.session['listModuleResource'].append(ModuleResourceInfo(content=request.session['currentResourceContent'],filename=request.session['currentResourceFilename']).__to_json__())
            dajax.append("#uploadedResources", "innerHTML", request.session['currentResourceFilename'] + "<br/>")
            dajax.script("""$("#moduleResource").val("");""")
            request.session['currentResourceContent'] = ""
            request.session['currentResourceFilename'] = ""
    
    return dajax.json()

@dajaxice_register
def addModule(request, template, name, tag, HTMLTag):
    dajax = Dajax()    
    
    module = Module(name=name, template=template, tag=tag, htmlTag=HTMLTag)
    listModuleResource = request.session['listModuleResource']
    for resource in listModuleResource: 
        resource = eval(resource)        
        moduleResource = ModuleResource(name=resource['filename'], content=resource['content'], type=resource['filename'].split(".")[-1])
        module.resources.append(moduleResource)
    
    module.save()

    return dajax.json()

@dajaxice_register
def createBackup(request, mongodbPath):
    dajax = Dajax()
    
    backupsDir = settings.SITE_ROOT + '/data/backups/'
    
    now = datetime.now()
    backupFolder = now.strftime("%Y_%m_%d_%H_%M_%S")
    
    backupCommand = mongodbPath + "/mongodump --out " + backupsDir + backupFolder
    retvalue = os.system(backupCommand)
#     result = subprocess.check_output(backupCommand, shell=True)
    if retvalue == 0:
        result = "Backup created with success."
    else:
        result = "Unable to create the backup."
        
    dajax.assign("#backup-message", 'innerHTML', result)
    dajax.script(
    """
        $(function() {
            $( "#dialog-backup" ).dialog({
                modal: true,
                width: 520,
                buttons: {
                    OK: function() {    
                        $( this ).dialog( "close" );
                        }
                }      
            });
        });
      $('#model_selection').load(document.URL +  ' #model_selection', function() {});
    """)
    return dajax.json()


@dajaxice_register
def restoreBackup(request, mongodbPath, backup):
    dajax = Dajax()
    
    backupsDir = settings.SITE_ROOT + '/data/backups/'
    
    backupCommand = mongodbPath + "/mongorestore " + backupsDir + backup
    retvalue = os.system(backupCommand)
    
    if retvalue == 0:
        result = "Backup restored with success."
    else:
        result = "Unable to restore the backup."
        
    dajax.assign("#backup-message", 'innerHTML', result)
    dajax.script(
    """
        $(function() {
            $( "#dialog-backup" ).dialog({
                modal: true,
                width: 520,
                buttons: {
                    OK: function() {    
                        $( this ).dialog( "close" );
                        }
                }      
            });
        });
    """)
    return dajax.json()


@dajaxice_register
def deleteBackup(request, backup):
    dajax = Dajax()
    
    backupsDir = settings.SITE_ROOT + '/data/backups/'
    
    for root, dirs, files in os.walk(backupsDir + backup, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(backupsDir + backup)
    
    dajax.script(
    """
      $('#model_selection').load(document.URL +  ' #model_selection', function() {});
    """)
    
    return dajax.json()


@dajaxice_register
def saveUserProfile(request, userid, username, firstname, lastname, email):
    dajax = Dajax()
    
    user = User.objects.get(id=userid)
    errors = ""
    if username != user.username:
        try:
            user = User.objects.get(username=username)
            errors += "A user with the same username already exists.<br/>"
            dajax.script(
            """
            $("#edit-errors").html('"""+errors+"""');
            $(function() {
                $( "#dialog-errors-message" ).dialog({
                  modal: true,
                  buttons: {
                    Ok: function() {
                      $( this ).dialog( "close" );
                    }
                  }
                });
              });
              """)
            return dajax.json()
        except:
            user.username = username
    
    user.first_name = firstname
    user.last_name = lastname
    user.email = email
    user.save()
    dajax.script(
    """
    $(function() {
        $( "#dialog-saved-message" ).dialog({
            modal: true,
            buttons: {
                    Ok: function() {                        
                    $( this ).dialog( "close" );
                }
            }
        });
    });
    """)
    
    return dajax.json()

from django.contrib.auth import authenticate

@dajaxice_register
def changePassword(request, userid, old_password, password):
    dajax = Dajax()
    
    errors = ""
    user = User.objects.get(id=userid)
    auth_user = authenticate(username=user.username, password=old_password)
    if auth_user is None:
        errors += "The old password is incorrect"
        dajax.script(
        """
        $("#list-errors").html('"""+errors+"""');
        $(function() {
            $( "#dialog-errors-message" ).dialog({
              modal: true,
              buttons: {
                Ok: function() {
                  $( this ).dialog( "close" );
                }
              }
            });
          });
          """)
        return dajax.json()
    else:        
        user.set_password(password)
        user.save()
        dajax.script(
        """
        $(function() {
            $( "#dialog-saved-message" ).dialog({
                modal: true,
                buttons: {
                        Ok: function() {                        
                        $( this ).dialog( "close" );
                    }
                }
            });
        });
        """)

    
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