################################################################################
#
# File Name: ajax.py
# Application: compose
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
from mgi.models import Template, Type
import lxml.etree as etree
from io import BytesIO

# XSL file loading
import os

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

    request.session['currentComposeTemplate'] = templateFilename
    request.session['currentComposeTemplateID'] = templateID
    request.session.modified = True
    print '>>>>' + templateFilename + ' set as current template in session'
    dajax = Dajax()

    if templateID != "new":
        templateObject = Template.objects.get(pk=templateID)
        xmlDocData = templateObject.content
        request.session['xmlTemplateCompose'] = xmlDocData
    else:
        base_template_path = os.path.join(settings.SITE_ROOT, 'static/resources/xsd/new_base_template.xsd')
        base_template_file = open(base_template_path, 'r')
        base_template_content = base_template_file.read()
        request.session['xmlTemplateCompose'] = base_template_content

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
    if 'currentComposeTemplate' in request.session:
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
# Function Name: loadXML(request)
# Inputs:        request - 
# Outputs:       JSON data with templateSelected 
# Exceptions:    None
# Description:   Loads the XML data in the compose page. First transforms the data.
# 
################################################################################
@dajaxice_register
def loadXML(request):
    dajax = Dajax()
    
    xmlString = request.session['xmlTemplateCompose']
    
    xsltPath = os.path.join(settings.SITE_ROOT, 'static/resources/xsl/xsd2html.xsl')
    xslt = etree.parse(xsltPath)
    transform = etree.XSLT(xslt)
    xmlTree = ""
    if (xmlString != ""):
        request.session['namespacesCompose'] = get_namespaces(BytesIO(str(xmlString)))
        for prefix, url in request.session['namespacesCompose'].items():
            if (url == "{http://www.w3.org/2001/XMLSchema}"):            
                request.session['defaultPrefixCompose'] = prefix
                break
        dom = etree.parse(BytesIO(xmlString.encode('utf-8')))
        newdom = transform(dom)
        xmlTree = str(newdom)
    
    dajax.assign("#XMLHolder", "innerHTML", xmlTree)
    
    return dajax.json()

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
# Function Name: insertElementSequence(request, typeID, xpath)
# Inputs:        request - HTTP request
#                typeID - ID of the inserted type
#                xpath - xpath where the element is added
# Outputs:       JSON 
# Exceptions:    None
# Description:   insert the type in the original schema
# 
################################################################################
@dajaxice_register
def insertElementSequence(request, typeID, xpath, typeName):
    dajax = Dajax()
    
    defaultPrefix = request.session['defaultPrefixCompose']
    namespace = request.session['namespacesCompose'][defaultPrefix]
    
    xmlString = request.session['xmlTemplateCompose']
    dom = etree.parse(BytesIO(xmlString.encode('utf-8')))
    
    xpath = xpath.replace(defaultPrefix +":", namespace)
    dom.find(xpath).append(etree.Element(namespace+"element", attrib={'type':typeName, 'name':typeName}))
    request.session['xmlTemplateCompose'] = etree.tostring(dom) 
    print etree.tostring(dom)
    
    return dajax.json()
    