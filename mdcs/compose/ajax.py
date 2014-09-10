################################################################################
#
# File Name: ajax.py
# Application: compose
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
from mgi.models import XMLSchema 
import sys
from xlrd import open_workbook
from argparse import ArgumentError
from cgi import FieldStorage
from cStringIO import StringIO
from django.core.servers.basehttp import FileWrapper
from mgi.models import Template, Ontology, Htmlform, Xmldata, Hdf5file, Jsondata, XML2Download, TemplateVersion

#import xml.etree.ElementTree as etree
import lxml.html as html
import lxml.etree as etree
import xml.dom.minidom as minidom

#XSL file loading
import os
from explore.ajax import formString
#from django.conf.settings import PROJECT_ROOT


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

    templateObject = Template.objects.get(pk=templateID)
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
    if 'currentComposeTemplate' in request.session:
      print 'template is selected'
      templateSelected = 'yes'
    else:
      print 'template is not selected'
      templateSelected = 'no'
    dajax = Dajax()

    print 'END def verifyTemplateIsSelected(request)'
    return simplejson.dumps({'templateSelected':templateSelected})


