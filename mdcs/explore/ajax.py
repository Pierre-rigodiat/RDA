################################################################################
#
# File Name: ajax.py
# Application: explore
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#        Guillaume Sousa Amaral
#        guillaume.sousa@nist.gov
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
from explore.models import XMLSchema 
from io import BytesIO
from lxml import html
from collections import OrderedDict
from pymongo import Connection
import xmltodict

#import xml.etree.ElementTree as etree
import lxml.etree as etree
import xml.dom.minidom as minidom

from mgi.models import Template, QueryResults, SparqlQueryResults, SavedQuery, Jsondata 

import sparqlPublisher

# Global Variables
# xmlString = ""
xmlDocTree = ""
formString = ""
customFormString = ""
# queryBuilderString = ""
savedQueryForm = ""
mapTagIDElementInfo = None
mapQueryInfo = dict()
mapCriterias = OrderedDict()
mapEnumIDChoices = dict()
debugON = 0
nbChoicesID = 0
defaultPrefix = ""
defaultNamespace = ""
criteriaID = ""
anyChecked = False


results = []
sparqlResults = ""
sparqlQuery = ""

#Class definition
class ElementInfo:    
    def __init__(self, type="", path=""):
        self.type = type
        self.path = path
        
class CriteriaInfo:
    def __init__(self, elementInfo=None, queryInfo=None):
        self.elementInfo = elementInfo
        self.queryInfo = queryInfo
        
class QueryInfo:
    def __init__(self, query="", displayedQuery=""):
        self.query = query
        self.displayedQuery = displayedQuery

class BranchInfo:
    def __init__(self, keepTheBranch, selectedLeave):
        self.keepTheBranch = keepTheBranch
        self.selectedLeave = selectedLeave


################################################################################
# 
# Function Name: setCurrentTemplate(request)
# Inputs:        request - 
#                templateFilename -  
#                templateID - 
# Outputs:       JSON data with success or failure
# Exceptions:    None
# Description:   Set the current template to input argument.  Template is read into
#                an xsdDocTree for use later.
#
################################################################################
@dajaxice_register
def setCurrentTemplate(request,templateFilename, templateID):
    print 'BEGIN def setCurrentTemplate(request)'
    
    global xmlDocTree
#     global xmlString
    global formString
    global customFormString

    # reset global variables
#     xmlString = ""
    formString = ""
    customFormString = ""
    
    request.session['exploreCurrentTemplate'] = templateFilename
    request.session['exploreCurrentTemplateID'] = templateID
    request.session.modified = True
    print '>>>>' + templateFilename + ' set as current template in session'
    dajax = Dajax()

    templateObject = Template.objects.get(filename=templateFilename)
    xmlDocData = templateObject.content

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
    if 'exploreCurrentTemplate' in request.session:
        print 'template is selected'
        templateSelected = 'yes'
    else:
        print 'template is not selected'
        templateSelected = 'no'
#     dajax = Dajax()

    print 'END def verifyTemplateIsSelected(request)'
    return simplejson.dumps({'templateSelected':templateSelected})

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
    request.session['exploreCurrentTemplate'] = modelFilename
    request.session.modified = True
    print '>>>>' + modelFilename
    dajax = Dajax()

    print 'END def setCurrentModel(request)'
    return dajax.json()


################################################################################
# 
# Function Name: generateFormSubSection(xpath,fullPath)
# Inputs:        xpath -
#                fullPath - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
#
################################################################################
def generateFormSubSection(xpath, elementName, fullPath):
    print 'BEGIN def generateFormSubSection(xpath, elementName, fullPath)'
    formString = ""
#     global xmlString
    global xmlDocTree
    global xmlDataTree
    global mapTagIDElementInfo
    global nbChoicesID
    global debugON
    global defaultNamespace
    global defaultPrefix
    
    
    
    p = re.compile('(\{.*\})?schema', re.IGNORECASE)

    if xpath is None:
        print "xpath is none"
        return formString;

    xpathFormated = "./*[@name='"+xpath+"']"
    if debugON: formString += "xpathFormated: " + xpathFormated.format(defaultNamespace)
    e = xmlDocTree.find(xpathFormated.format(defaultNamespace))

    if e is None:
        return formString

    if e.tag == "{0}complexType".format(defaultNamespace):
        if debugON: formString += "matched complexType" 
        print "matched complexType" + "<br>"
        complexTypeChild = e.find('*')

        if complexTypeChild is None:
            return formString

        fullPath += "." + elementName
        if complexTypeChild.tag == "{0}sequence".format(defaultNamespace):
            formString += "<ul>"
            if debugON: formString += "complexTypeChild:" + complexTypeChild.tag + "<br>"
            sequenceChildren = complexTypeChild.findall('*')            
            for sequenceChild in sequenceChildren:
                if debugON: formString += "SequenceChild:" + sequenceChild.tag + "<br>"
                print "SequenceChild: " + sequenceChild.tag 
                if sequenceChild.tag == "{0}element".format(defaultNamespace):
                    if 'type' not in sequenceChild.attrib:
                        pass
#                         if 'ref' in sequenceChild.attrib:
#                             if sequenceChild.attrib.get('ref') == "hdf5:HDF5-File":
#                                 formString += "<ul><li><i><div id='hdf5File'>" + sequenceChild.attrib.get('ref') + "</div></i> "
#                                 formString += "<div class=\"btn select-element\" onclick=\"selectHDF5File('hdf5:HDF5-File',this);\"><i class=\"icon-folder-open\"></i> Select HDF5 File</div>"
#                                 formString += "</li></ul>"
#                             elif sequenceChild.attrib.get('ref') == "hdf5:Field":
#                                 formString += "<ul><li><i><div id='hdf5Field'>" + sequenceChild.attrib.get('ref') + "</div></i> "
#                                 formString += "</li></ul>"
                    elif (sequenceChild.attrib.get('type') == "{0}:string".format(defaultPrefix)
                          or sequenceChild.attrib.get('type') == "{0}:double".format(defaultPrefix)
                          or sequenceChild.attrib.get('type') == "{0}:float".format(defaultPrefix)
                          or sequenceChild.attrib.get('type') == "{0}:integer".format(defaultPrefix)
                          or sequenceChild.attrib.get('type') == "{0}:anyURI".format(defaultPrefix)):                                                                
                        textCapitalized = sequenceChild.attrib.get('name')[0].capitalize()  + sequenceChild.attrib.get('name')[1:]                        
                        elementID = len(mapTagIDElementInfo.keys())
                        formString += "<li id='" + str(elementID) + "'>" + textCapitalized + " <input type='checkbox'>"                         
                        formString += "</li>"                    
                        elementInfo = ElementInfo(sequenceChild.attrib.get('type'),fullPath[1:] + "." + textCapitalized)
                        mapTagIDElementInfo[elementID] = elementInfo
                    else:                        
                        textCapitalized = sequenceChild.attrib.get('name')[0].capitalize()  + sequenceChild.attrib.get('name')[1:]    
                        elementID = len(mapTagIDElementInfo.keys())                        
                        isEnum = False
                        # look for enumeration
                        childElement = xmlDocTree.find("./*[@name='"+sequenceChild.attrib.get('type')+"']".format(defaultNamespace))
                        if (childElement is not None):
                            if(childElement.tag == "{0}simpleType".format(defaultNamespace)):
                                restrictionChild = childElement.find("{0}restriction".format(defaultNamespace))        
                                if restrictionChild is not None:                                    
                                    enumChildren = restrictionChild.findall("{0}enumeration".format(defaultNamespace))
                                    if enumChildren is not None:
                                        formString += "<li id='" + str(elementID) + "'>" + textCapitalized + " <input type='checkbox'>" + "</li>"
                                        elementInfo = ElementInfo("enum",fullPath[1:]+"." + textCapitalized)
                                        mapTagIDElementInfo[elementID] = elementInfo
                                        listChoices = []
                                        for enumChild in enumChildren:
                                            listChoices.append(enumChild.attrib['value'])
                                        mapEnumIDChoices[elementID] = listChoices
                                        isEnum = True
                                
                        if(isEnum is not True):                            
                            formString += "<li>" + textCapitalized + " "
                            formString += generateFormSubSection(sequenceChild.attrib.get('type'), textCapitalized,fullPath)
                            formString += "</li>"                        
                elif sequenceChild.tag == "{0}choice".format(defaultNamespace):
                    chooseID = nbChoicesID
                    chooseIDStr = 'choice' + str(chooseID)
                    nbChoicesID += 1
                    formString += "<li>Choose <select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"
                    choiceChildren = sequenceChild.findall('*')
#                     selectedChild = choiceChildren[0]
                    for choiceChild in choiceChildren:
                        if choiceChild.tag == "{0}element".format(defaultNamespace):
                            textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                            formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
                    formString += "</select></nobr>"                    
                    for (counter, choiceChild) in enumerate(choiceChildren):
                        if choiceChild.tag == "{0}element".format(defaultNamespace):
                            if (choiceChild.attrib.get('type') == "{0}:string".format(defaultPrefix)
                              or choiceChild.attrib.get('type') == "{0}:double".format(defaultPrefix)
                              or choiceChild.attrib.get('type') == "{0}:float".format(defaultPrefix)
                              or choiceChild.attrib.get('type') == "{0}:integer".format(defaultPrefix)
                              or choiceChild.attrib.get('type') == "{0}:anyURI".format(defaultPrefix)):
                                textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                                elementID = len(mapTagIDElementInfo.keys())
                                if (counter > 0):
                                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li id='" + str(elementID) + "'>" + textCapitalized + " <input type='checkbox'>" + "</li></ul>"
                                else:                                      
                                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\"><li id='" + str(elementID) + "'>" + textCapitalized + " <input type='checkbox'>" + "</li></ul>"
                                elementInfo = ElementInfo(choiceChild.attrib.get('type'),fullPath[1:]+"." + textCapitalized)
                                mapTagIDElementInfo[elementID] = elementInfo
                            else:
                                textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                                if (counter > 0):
                                    formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li>" + textCapitalized
                                else:
                                    formString += "<ul id=\""  + chooseIDStr + "-" + str(counter) + "\"><li>" + textCapitalized
                                formString += generateFormSubSection(choiceChild.attrib.get('type'), textCapitalized, fullPath) + "</ul>"            
            formString += "</li></ul>"
        elif complexTypeChild.tag == "{0}choice".format(defaultNamespace):
            formString += "<ul>"
            if debugON: formString += "complexTypeChild:" + complexTypeChild.tag + "<br>"
            chooseID = nbChoicesID        
            chooseIDStr = 'choice' + str(chooseID)
            nbChoicesID += 1
            formString += "<li>Choose <select id='"+ chooseIDStr +"' onchange=\"changeChoice(this);\">"        
            choiceChildren = complexTypeChild.findall('*')
#             selectedChild = choiceChildren[0]
            for choiceChild in choiceChildren:
                if choiceChild.tag == "{0}element".format(defaultNamespace):
                    textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                    formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
            formString += "</select>"
            for (counter, choiceChild) in enumerate(choiceChildren):
                if choiceChild.tag == "{0}element".format(defaultNamespace):
                    if (choiceChild.attrib.get('type') == "{0}:string".format(defaultPrefix)
                      or choiceChild.attrib.get('type') == "{0}:double".format(defaultPrefix)
                      or choiceChild.attrib.get('type') == "{0}:float".format(defaultPrefix)
                      or choiceChild.attrib.get('type') == "{0}:integer".format(defaultPrefix)
                      or choiceChild.attrib.get('type') == "{0}:anyURI".format(defaultPrefix)):
                        textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                        elementID = len(mapTagIDElementInfo.keys())
                        if (counter > 0):
                            formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li id='" + str(elementID) + "'>" + textCapitalized + " <input type='checkbox'>" + "</li></ul>"
                        else:                                      
                            formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\"><li id='" + str(elementID) + "'>" + textCapitalized + " <input type='checkbox'>" + "</li></ul>"
                        elementInfo = ElementInfo(choiceChild.attrib.get('type'),fullPath[1:]+"." + textCapitalized)
                        mapTagIDElementInfo[elementID] = elementInfo
                    else:                                                    
                        textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                        if (counter > 0):
                            formString += "<ul id=\"" + chooseIDStr + "-" + str(counter) + "\" style=\"display:none;\"><li>" + textCapitalized
                        else:
                            formString += "<ul id=\""  + chooseIDStr + "-" + str(counter) + "\"><li>" + textCapitalized               
                        formString += generateFormSubSection(choiceChild.attrib.get('type'), textCapitalized, fullPath) + "</ul>"
            formString += "</li></ul>"
        elif complexTypeChild.tag == "{0}attribute".format(defaultNamespace):
            textCapitalized = complexTypeChild.attrib.get('name')[0].capitalize()  + complexTypeChild.attrib.get('name')[1:]
            formString += "<li>" + textCapitalized + "</li>"
    elif e.tag == "{0}simpleType".format(defaultNamespace):
        if debugON: formString += "matched simpleType" + "<br>"

        simpleTypeChildren = e.findall('*')
        
        if simpleTypeChildren is None:
            return formString

        for simpleTypeChild in simpleTypeChildren:
            if simpleTypeChild.tag == "{0}restriction".format(defaultNamespace):
                choiceChildren = simpleTypeChild.findall('*')
                for choiceChild in choiceChildren:
                    if choiceChild.tag == "{0}enumeration".format(defaultNamespace):
                        formString += "<input type='checkbox'>"
                        break

    print 'END def generateFormSubSection(xpath, elementName, fullPath)'
    return formString

################################################################################
# 
# Function Name: generateForm(key)
# Inputs:        key -
# Outputs:       rendered HTMl form
# Exceptions:    None
# Description:   Renders HTMl form for display.
#
################################################################################

def generateForm(key):
    print 'BEGIN def generateForm(key)'
    formString = ""
    global xmlDocTree
    global mapTagIDElementInfo
    global nbChoicesID
    global defaultNamespace
    global defaultPrefix

    mapTagIDElementInfo = dict()
    nbChoicesID = 0

    defaultNamespace = "http://www.w3.org/2001/XMLSchema"
    for prefix, url in xmlDocTree.getroot().nsmap.iteritems():
        if (url == defaultNamespace):            
            defaultPrefix = prefix
            break
    defaultNamespace = "{" + defaultNamespace + "}"
    if debugON: formString += "namespace: " + defaultNamespace + "<br>"
    e = xmlDocTree.findall("./{0}element".format(defaultNamespace))

    if debugON: e = xmlDocTree.findall("{0}complexType/{0}choice/{0}element".format(defaultNamespace))
    if debugON: formString += "list size: " + str(len(e))

#     if len(e) > 1:
    for element in e:
        textCapitalized = element.attrib.get('name')[0].capitalize()  + element.attrib.get('name')[1:]
        formString += "<b>" + textCapitalized + "</b><br>"
        if debugON: formString += "<b>" + element.attrib.get('name').capitalize() + "</b><br>"
        formString += generateFormSubSection(element.attrib.get('type'), textCapitalized, "")
#         formString += "<p style='color:red'> The schema is not valid ! </p>"
#     else:
#         textCapitalized = e[0].attrib.get('name')[0].capitalize()  + e[0].attrib.get('name')[1:]
#         formString += "<b>" + textCapitalized + "</b><br>"
#         if debugON: formString += "<b>" + e[0].attrib.get('name').capitalize() + "</b><br>"
#         formString += generateFormSubSection(e[0].attrib.get('type'), "")

    print 'END def generateForm(key)'

    return formString

################################################################################
# 
# Function Name: generateXSDTreeForQueryingData(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#
################################################################################
@dajaxice_register
def generateXSDTreeForQueryingData(request): 
    print 'BEGIN def generateXSDTreeForQueryingData(request)'

#     global xmlString
    global formString
    global xmlDocTree
    global xmlDataTree

    dajax = Dajax()
    templateFilename = request.session['exploreCurrentTemplate']
    templateID = request.session['exploreCurrentTemplateID']
    print '>>>> ' + templateFilename + ' is the current template in session'
    
    if xmlDocTree == "":
        setCurrentTemplate(request,templateFilename, templateID)
    if (formString == ""):
        formString = "<form id=\"dataQueryForm\" name=\"xsdForm\">"
        formString += generateForm("schema")        
        formString += "</form>"        
    
    dajax.assign('#xsdForm', 'innerHTML', formString)
 
    print 'END def generateXSDTreeForQueryingData(request)'
    return dajax.json()



################################################################################
# 
# Function Name: executeQuery(request, queryForm, queryBuilder)
# Inputs:        request - 
#                queryForm - 
#                queryBuilder - 
# Outputs:       
# Exceptions:    None
# Description:   execute a query in mongo db
#
################################################################################
@dajaxice_register
def executeQuery(request, queryForm, queryBuilder):
    print 'BEGIN def executeQuery(request, queryForm, queryBuilder)'        
    dajax = Dajax()
    global results
#     global queryBuilderString
    global savedQueryForm
    
#     queryBuilderString = queryBuilder
    savedQueryForm = queryForm
    
    queryFormTree = html.fromstring(queryForm)
    errors = checkQueryForm(queryFormTree)
    if(len(errors)== 0):
        htmlTree = html.fromstring(queryForm)
        query = fieldsToQuery(htmlTree)
        results = Jsondata.executeQuery(query)
        dajax.script("resultsCallback();")
    else:
        errorsString = ""
        for error in errors:
            errorsString += "<p>" + error + "</p>"            
        dajax.assign('#listErrors', 'innerHTML', errorsString)
        dajax.script("displayErrors();")

    print 'END def executeQuery(request, queryForm, queryBuilder)'
    return dajax.json()


################################################################################
# 
# Function Name: getResults(request)
# Inputs:        request -  
# Outputs:       
# Exceptions:    None
# Description:   Get results of a query
#
################################################################################
@dajaxice_register
def getResults(request):
    print 'BEGIN def getResults(request)'
    dajax = Dajax()
    global results
    
    resultString = ""
    
    if len(results) > 0 :
        for result in results:
            resultString += "<textarea class='xmlResult' readonly='true'>"  
            resultString += str(xmltodict.unparse(result, pretty=True))
            resultString += "</textarea> <br/>"
    else:
        resultString = "<span style='font-style:italic; color:red;'> No Results found... </span>"
            
    dajax.assign("#results", "innerHTML", resultString)
    
    print 'END def getResults(request)'
    return dajax.json()


################################################################################
# 
# Function Name: intCriteria(path, comparison, value, isNot=False)
# Inputs:        path - 
#                comparison -
#                value -
#                isNot -
# Outputs:       a criteria
# Exceptions:    None
# Description:   Build a criteria for mongo db for the type integer
#
################################################################################
def intCriteria(path, comparison, value, isNot=False):
    print 'BEGIN def intCriteria(path, comparison, value, isNot=False)'
    criteria = dict()

    if(comparison == "="):
        if(isNot):
            criteria[path] = eval('{"$ne":' + value + '}')
        else:
            criteria[path] = int(value)
    else:
        if(isNot):
            criteria[path] = eval('{"$not":{"$' +comparison+ '":'+ value +'}}')
        else:
            criteria[path] = eval('{"$'+comparison+'":'+ value +'}')

    print 'END def intCriteria(path, comparison, value, isNot=False)'
    return criteria


################################################################################
# 
# Function Name: floatCriteria(path, comparison, value, isNot=False)
# Inputs:        path - 
#                comparison -
#                value -
#                isNot -
# Outputs:       a criteria
# Exceptions:    None
# Description:   Build a criteria for mongo db for the type float
#
################################################################################
def floatCriteria(path, comparison, value, isNot=False):
    criteria = dict()

    if(comparison == "="):
        if(isNot):
            criteria[path] = eval('{"$ne":' + value + '}')
        else:
            criteria[path] = float(value)
    else:
        if(isNot):
            criteria[path] = eval('{"$not":{"$' +comparison+ '":'+ value +'}}')
        else:
            criteria[path] = eval('{"$'+comparison+'":'+ value +'}')

    return criteria

################################################################################
# 
# Function Name: stringCriteria(path, comparison, value, isNot=False)
# Inputs:        path - 
#                comparison -
#                value -
#                isNot -
# Outputs:       a criteria
# Exceptions:    None
# Description:   Build a criteria for mongo db for the type string
#
################################################################################
def stringCriteria(path, comparison, value, isNot=False):
    criteria = dict()
    
    if (comparison == "is"):
        if(isNot):
            criteria[path] = eval('{"$ne":' + repr(value) + '}')
        else:
            criteria[path] = str(value)
    elif (comparison == "like"):
        if(isNot):
            criteria[path] = dict()
            criteria[path]["$not"] = re.compile(value)
        else:
            criteria[path] = re.compile(value)
    
    return criteria

################################################################################
# 
# Function Name: queryToCriteria(query, isNot=False)
# Inputs:        query - 
#                isNot -
# Outputs:       a criteria
# Exceptions:    None
# Description:   Build a criteria for mongo db for a query
#
################################################################################
def queryToCriteria(query, isNot=False):
    if(isNot):
        return invertQuery(query.copy())
    else:
        return query

################################################################################
# 
# Function Name: invertQuery(query)
# Inputs:        query - 
# Outputs:       
# Exceptions:    None
# Description:   Invert each field of the query to build NOT(query)
#
################################################################################
def invertQuery(query):
    for key, value in query.iteritems():
        if key == "$and" or key == "$or":
            for subValue in value:
                invertQuery(subValue)
        else:            
            #lt, lte, =, gte, gt, not, ne
            if isinstance(value,dict):                
                if value.keys()[0] == "$not" or value.keys()[0] == "$ne":
                    query[key] = (value[value.keys()[0]])                    
                else:
                    savedValue = value
                    query[key] = dict()
                    query[key]["$not"] = savedValue
            else:
                savedValue = value
                if isinstance(value, re._pattern_type):
                    query[key] = dict()
                    query[key]["$not"] = savedValue
                else:
                    query[key] = dict()
                    query[key]["$ne"] = savedValue
    return query

################################################################################
# 
# Function Name: enumCriteria(path, value, isNot=False)
# Inputs:        path -
#                value -
#                isNot -
# Outputs:       criteria
# Exceptions:    None
# Description:   Build a criteria for mongo db for an enumeration
#
################################################################################
def enumCriteria(path, value, isNot=False):
    criteria = dict()
    
    if(isNot):
        criteria[path] = eval('{"$ne":' + repr(value) + '}')
    else:
        criteria[path] = str(value)
            
    return criteria

################################################################################
# 
# Function Name: ANDCriteria(criteria1, criteria2)
# Inputs:        criteria1 -
#                criteria2 -
# Outputs:       criteria
# Exceptions:    None
# Description:   Build a criteria that is the result of criteria1 and criteria2
#
################################################################################
def ANDCriteria(criteria1, criteria2):
#     return criteria1.update(criteria2)
    ANDcriteria = dict()
    ANDcriteria["$and"] = []
    ANDcriteria["$and"].append(criteria1)
    ANDcriteria["$and"].append(criteria2)
    return ANDcriteria

################################################################################
# 
# Function Name: ORCriteria(criteria1, criteria2)
# Inputs:        criteria1 -
#                criteria2 -
# Outputs:       criteria
# Exceptions:    None
# Description:   Build a criteria that is the result of criteria1 or criteria2
#
################################################################################
def ORCriteria(criteria1, criteria2):
    ORcriteria = dict()
    ORcriteria["$or"] = []
    ORcriteria["$or"].append(criteria1)
    ORcriteria["$or"].append(criteria2)
    return ORcriteria

################################################################################
# 
# Function Name: buildCriteria(elemPath, comparison, value, elemType, isNot=False)
# Inputs:        elemPath -
#                comparison -
#                value -
#                elemType - 
#                isNot - 
# Outputs:       criteria
# Exceptions:    None
# Description:   Look at element type and route to the right function to build the criteria
#
################################################################################
def buildCriteria(elemPath, comparison, value, elemType, isNot=False):
    if (elemType == '{0}:integer'.format(defaultPrefix)):
        return intCriteria(elemPath, comparison, value, isNot)
    elif (elemType == '{0}:float'.format(defaultPrefix) or elemType == '{0}:double'.format(defaultPrefix)):
        return floatCriteria(elemPath, comparison, value, isNot)
    elif (elemType == '{0}:string'.format(defaultPrefix)):
        return stringCriteria(elemPath, comparison, value, isNot)
    else:
        return stringCriteria(elemPath, comparison, value, isNot)

################################################################################
# 
# Function Name: fieldsToQuery(htmlTree)
# Inputs:        htmlTree -
# Outputs:       query
# Exceptions:    None
# Description:   Take values from the html tree and create a query with them
#
################################################################################
def fieldsToQuery(htmlTree):
    fields = htmlTree.findall("./p")
    
    query = dict()
    for field in fields:        
        boolComp = field[0].value
        if (boolComp == 'NOT'):
            isNot = True
        else:
            isNot = False
            
        elemType = mapCriterias[field.attrib['id']].elementInfo.type
        if (elemType == "query"):
            queryValue = mapCriterias[field.attrib['id']].queryInfo.query
            criteria = queryToCriteria(queryValue, isNot)
        elif (elemType == "enum"):
            element = "content." + mapCriterias[field.attrib['id']].elementInfo.path
            value = field[2][0].value            
            criteria = enumCriteria(element, value, isNot)
        else:                
            element = "content." + mapCriterias[field.attrib['id']].elementInfo.path
            comparison = field[2][0].value
            value = field[2][1].value
            criteria = buildCriteria(element, comparison, value, elemType , isNot)
        
        if(boolComp == 'OR'):        
            query = ORCriteria(query, criteria)
        elif(boolComp == 'AND'):
            query = ANDCriteria(query, criteria)
        else:
            if(fields.index(field) == 0):
                query.update(criteria)
            else:
                query = ANDCriteria(query, criteria)
        
    return query

################################################################################
# 
# Function Name: checkQueryForm(htmlTree)
# Inputs:        htmlTree -
# Outputs:       query
# Exceptions:    None
# Description:   Check that values entered by the user match each element type
#
################################################################################
def checkQueryForm(htmlTree):
    global mapCriterias
    
    errors = []
    fields = htmlTree.findall("./p")
    if (len(mapCriterias) != len(fields)):
        errors.append("Some fields are empty !")
    else:
        for field in fields:
            elemType = mapCriterias[field.attrib['id']].elementInfo.type
            
            if (elemType == "{0}:float".format(defaultPrefix) or elemType == "{0}:double".format(defaultPrefix)):
                value = field[2][1].value
                try:
                    float(value)
                except ValueError:
                    elementPath = mapCriterias[field.attrib['id']].elementInfo.path
                    element = elementPath.split('.')[-1]
                    errors.append(element + " must be a number !")
                        
            elif (elemType == "{0}:integer".format(defaultPrefix)):
                value = field[2][1].value
                try:
                    int(value)
                except ValueError:
                    elementPath = mapCriterias[field.attrib['id']].elementInfo.path
                    element = elementPath.split('.')[-1]
                    errors.append(element + " must be an integer !")
                    
            elif (elemType == "{0}:string".format(defaultPrefix)):
                comparison = field[2][0].value
                value = field[2][1].value
                elementPath = mapCriterias[field.attrib['id']].elementInfo.path
                element = elementPath.split('.')[-1]
                if (comparison == "like"):
                    try:
                        re.compile(value)
                    except Exception, e:
                        errors.append(element + " must be a valid regular expression ! (" + str(e) + ")")
                    
    return errors
                    
################################################################################
# 
# Function Name: addField(request, htmlForm)
# Inputs:        request - 
#                htmlForm -
# Outputs:       
# Exceptions:    None
# Description:   Add an empty field to the query builder
#
################################################################################
@dajaxice_register
def addField(request, htmlForm):
    dajax = Dajax()
    htmlTree = html.fromstring(htmlForm)
    
    fields = htmlTree.findall("./p")    
    fields[-1].remove(fields[-1].find("./span[@class='icon add']"))      
    if (len(fields) == 1):
        criteriaID = fields[0].attrib['id']
        minusButton = html.fragment_fromstring("""<span class="icon remove" onclick="removeField('""" + str(criteriaID) +"""')"></span>""")
        fields[0].append(minusButton)
    
    # get the id of the last field (get the value of the increment, remove crit)
    lastID = fields[-1].attrib['id'][4:]
    tagID = int(lastID) + 1
    element = html.fragment_fromstring("""
        <p id='crit""" + str(tagID) + """'>
        """
        +
            renderANDORNOT() 
        +
        """
            <input onclick="showCustomTree('crit""" + str(tagID) + """')" readonly="readonly" type="text" class="elementInput">     
            <span id='ui"""+ str(tagID) +"""'>
            </span>  
            <span class="icon remove" onclick="removeField('crit""" + str(tagID) + """')"></span>
            <span class="icon add" onclick="addField()"></span>
        </p>
    """)
    
    #insert before the 3 buttons (save, clear, execute)
    htmlTree.insert(-3,element)   
    
    dajax.assign("#queryForm", "innerHTML", html.tostring(htmlTree))
    
#     dajax.script("""
#         makeInputsDroppable();
#     """);
    return dajax.json()

################################################################################
# 
# Function Name: removeField(request, queryForm, criteriaID)
# Inputs:        request -
#                htmlForm -
#                criteriaID -
# Outputs:       
# Exceptions:    None
# Description:   Remove a field from the query builder
#
################################################################################
@dajaxice_register
def removeField(request, queryForm, criteriaID):
    dajax = Dajax()
    global mapCriterias
    
    htmlTree = html.fromstring(queryForm)
    
    currentElement = htmlTree.get_element_by_id(criteriaID)
    fields = htmlTree.findall("./p")
    
    
    # suppress last element => give the + to the previous
    if(fields[-1].attrib['id'] == criteriaID):
        plusButton = html.fragment_fromstring("""<span class="icon add" onclick="addField()"></span>""")
        fields[-2].append(plusButton)
    # only one element left => remove the -
    if(len(fields) == 2):
        fields[-1].remove(fields[-1].find("./span[@class='icon remove']"))
        fields[-2].remove(fields[-2].find("./span[@class='icon remove']"))
        
    htmlTree.remove(currentElement)
    
    # replace the bool of the first element by the 2 choices input (YES/NOT) if it was an element with 3 inputs (AND/OR/NOT)
    fields = htmlTree.findall("./p")
    if(len(fields[0][0].value_options) is not 2):
        if (fields[0][0].value == 'NOT'):
            fields[0][0] = html.fragment_fromstring(renderYESORNOT())
            fields[0][0].value = 'NOT'
        else:
            fields[0][0] = html.fragment_fromstring(renderYESORNOT())
        
    try:
        del mapCriterias[criteriaID]
    except:
        pass
    
    dajax.assign("#queryForm", "innerHTML", html.tostring(htmlTree))
#     dajax.script("""
#         makeInputsDroppable();
#     """);
    return dajax.json()

################################################################################
# 
# Function Name: renderYESORNOT()
# Inputs:        
# Outputs:       Yes or Not select string
# Exceptions:    None
# Description:   Returns a string that represents an html select with yes or not options
#
################################################################################
def renderYESORNOT():
    return """
    <select>
      <option value=""></option>
      <option value="NOT">NOT</option>
    </select> 
    """

################################################################################
# 
# Function Name: renderANDORNOT()
# Inputs:        
# Outputs:       AND OR NOT select string
# Exceptions:    None
# Description:   Returns a string that represents an html select with AND, OR, NOT options
#
################################################################################
def renderANDORNOT():
    return """
    <select>
      <option value="AND">AND</option>
      <option value="OR">OR</option>
      <option value="NOT">NOT</option>
    </select> 
    """

################################################################################
# 
# Function Name: renderNumericSelect()
# Inputs:        
# Outputs:       numeric select string
# Exceptions:    None
# Description:   Returns a string that represents an html select with numeric comparisons
#
################################################################################
def renderNumericSelect():
    return """
    <select style="width:70px">
      <option value="lt">&lt;</option>
      <option value="lte">&le;</option>
      <option value="=">=</option>
      <option value="gte">&ge;</option>
      <option value="gt">&gt;</option>
    </select> 
    """

def renderValueInput():
    return """
    <input style="margin-left:4px;" type="text" class="valueInput"/>
    """

def renderStringSelect():
    return """
    <select>
      <option value="is">is</option>
      <option value="like">like</option>                      
    </select> 
    """

def renderEnum(fromElementID):
    enum = "<select class='selectInput'>"
    listOptions = mapEnumIDChoices[int(fromElementID)]
    for option in listOptions:
        enum += "<option value='" + option + "'>" + option + "</option>"    
    enum += "</select>"
    return enum

def renderSelectForm(tagID):
    pass

def buildPrettyCriteria(elementName, comparison, value, isNot=False):
    prettyCriteria = ""
    
    if (isNot):
        prettyCriteria += "NOT("
        
    prettyCriteria += elementName
    if(comparison == "lt"):
        prettyCriteria += " &lt; "
    elif (comparison == "lte"):
        prettyCriteria += " &le; "
    elif (comparison == "="):
        prettyCriteria += "="
    elif (comparison == "gte"):
        prettyCriteria += " &ge; "
    elif (comparison == "gt"):
        prettyCriteria += " &gt; "
    elif (comparison == "is"):
        prettyCriteria += " is "
    elif (comparison == "like"):
        prettyCriteria += " like "
    
    if value == "":
        prettyCriteria += '" "'
    else:
        prettyCriteria += str(value)        
    
    if(isNot):
        prettyCriteria += ")"
    
    return prettyCriteria

def queryToPrettyCriteria(queryValue, isNot):
    if(isNot):
        return "NOT(" + queryValue + ")"
    else:
        return queryValue
    
def enumToPrettyCriteria(element, value, isNot=False):
    if(isNot):
        return "NOT(" + str(element) + " is " + str(value) + ")"
    else:
        return str(element) + " is " + str(value)

def ORPrettyCriteria(query, criteria):
    return "(" + query + " OR " + criteria + ")"

def ANDPrettyCriteria(query, criteria):
    return "(" + query + " AND " + criteria + ")"

def fieldsToPrettyQuery(queryFormTree):
    fields = queryFormTree.findall("./p")
    
    query = ""
#     criteriaIterator = 0
    for field in fields:        
        boolComp = field[0].value
        if (boolComp == 'NOT'):
            isNot = True
        else:
            isNot = False
                
        elemType = mapCriterias[field.attrib['id']].elementInfo.type
        if (elemType == "query"):
            queryValue = mapCriterias[field.attrib['id']].queryInfo.displayedQuery
#             criteriaIterator += 1
            criteria = queryToPrettyCriteria(queryValue, isNot)
        elif (elemType == "enum"):
            elementPath = mapCriterias[field.attrib['id']].elementInfo.path
            element = elementPath.split('.')[-1]
#             criteriaIterator += 1
            value = field[2][0].value            
            criteria = enumToPrettyCriteria(element, value, isNot)
        else:                 
            elementPath = mapCriterias[field.attrib['id']].elementInfo.path
            element = elementPath.split('.')[-1]
#             criteriaIterator += 1
            comparison = field[2][0].value
            value = field[2][1].value
            criteria = buildPrettyCriteria(element, comparison, value, isNot)
        
        if(boolComp == 'OR'):        
            query = ORPrettyCriteria(query, criteria)
        elif(boolComp == 'AND'):
            query = ANDPrettyCriteria(query, criteria)
        else:
            if(fields.index(field) == 0):
                query += criteria
            else:
                query = ANDPrettyCriteria(query, criteria)
        
    return query    

@dajaxice_register
def saveQuery(request, queryForm, queriesTable):
    dajax = Dajax()
    queryFormTree = html.fromstring(queryForm)

    # Check that the user can save a query
    errors = []
    if '_auth_user_id' in request.session:
        userID = request.session['_auth_user_id']
        if 'exploreCurrentTemplateID' in request.session:
            templateID = request.session['exploreCurrentTemplateID'] 
        else:
            errors = ['You have to select a template before you can save queries (Step 1 : Select Template).']
    else:
        errors = ['You have to login to save a query.']
    
    if(len(errors)== 0): 
        # Check that the query is valid      
        errors = checkQueryForm(queryFormTree)
        if(len(errors)== 0):
            query = fieldsToQuery(queryFormTree)    
            displayedQuery = fieldsToPrettyQuery(queryFormTree) 
        
            #save the query in the data base
            connect('mgi')
            
            ListRegex = []
            ListPattern = []
            manageRegexBeforeSave(query, ListRegex, ListPattern)
            savedQuery = SavedQuery(str(userID),str(templateID), str(query),displayedQuery,ListRegex, ListPattern)
            savedQuery.save()
            
            #add the query to the table        
#             queriesTree = html.fromstring(queriesList)
#             queriesTable = queriesTree.find("./[@id=queriesTable]")
            queriesTableTree = html.fromstring(queriesTable)
            tr = queriesTableTree.find("./tbody/tr[@id='noqueries']")
            if(tr is not None):
                # removes the row         
                queriesTableTree.find("./tbody").remove(tr) 
    
#             linesInTable = queriesTable.findall("./tbody")
#             if (len(linesInTable) == 1): #th
#                 queryID = 0
#             else:
#                 queryID = int(linesInTable[-1][0].attrib['id'][5:]) + 1
#                 pass
#             mapQueryInfo[queryID] = QueryInfo(query, displayedQuery)
            mapQueryInfo[str(savedQuery.id)] = QueryInfo(query, displayedQuery)
            
            element = html.fragment_fromstring(renderSavedQuery(str(displayedQuery),savedQuery.id))
            queriesTableTree.find("./tbody").append(element)
            dajax.assign('#queriesTable', 'innerHTML', html.tostring(queriesTableTree))
        else:
            errorsString = ""
            for error in errors:
                errorsString += "<p>" + error + "</p>"            
            dajax.assign('#listErrors', 'innerHTML', errorsString)
            dajax.script("displayErrors();")
    else:
        errorsString = ""
        for error in errors:
            errorsString += "<p>" + error + "</p>"            
        dajax.assign('#listErrors', 'innerHTML', errorsString)
        dajax.script("displayErrors();")

    return dajax.json()


def manageRegexBeforeSave(query, ListRegex, ListPattern):
#     for key, value in query.iteritems():
#         if isinstance(value, dict):
#             manageRegexBeforeSave(value)
#         else:
#             if isinstance(value, re._pattern_type):
#                 query[key] = "re.compile(" + value.pattern + ")"
    for key, value in query.iteritems():
        if key == "$and" or key == "$or":
            for subValue in value:
                manageRegexBeforeSave(subValue, ListRegex, ListPattern)
        elif isinstance(value, re._pattern_type):
            ListRegex.append(str(value))
            ListPattern.append(value.pattern)
        elif isinstance(value, dict):
            manageRegexBeforeSave(value, ListRegex, ListPattern)
#                 DictRegex[str(value).replace(".", "")] = value.pattern

@dajaxice_register
def deleteQuery(request, queriesTable, savedQueryID):
    dajax = Dajax()
    global mapQueryInfo
    
#     queriesTree = html.fromstring(queriesList)
#     queriesTable = queriesTree.find(".//table")
#     lineToDelete = queriesTable.find(".//tr/[@id='"+ savedQueryID +"']")
#     queriesTable.remove(lineToDelete)
    
    # finds all lines in the table exept the first one : headers
    queriesTableTree = html.fromstring(queriesTable)
    tr = queriesTableTree.find("./tbody/tr[@id='"+ savedQueryID +"']")
    if(tr is not None):
        # removes the row         
        queriesTableTree.find("./tbody").remove(tr)   
#     # finds all lines in the table exept the first one : headers
#     for tbody in queriesTableTree.findall('./tbody')[1:]:
#         tr = tbody.find("./tr/[@id='"+ savedQueryID +"']")
#         if(tr is not None):
#             # removes the row         
#             queriesTableTree.remove(tbody)   
#             break
    
    connect('mgi')
    SavedQuery(id=savedQueryID[5:]).delete()
    del mapQueryInfo[savedQueryID[5:]]
    if '_auth_user_id' in request.session and 'exploreCurrentTemplateID' in request.session:
        userID = request.session['_auth_user_id']
        templateID = request.session['exploreCurrentTemplateID']
        connect('mgi')
        userQueries = SavedQuery.objects(user=str(userID),template=str(templateID))        
        if(len(userQueries) == 0):
            queriesTableTree = html.fragment_fromstring(
            """<table>
                <tr>                    
                    <th width="15px">Add to Builder</th>
                    <th>Queries</th>
                    <th width="15px">Delete</th>
                </tr>                
            </table>""")
            element = html.fragment_fromstring(renderNoQueries())
            queriesTableTree.append(element)
    dajax.assign("#queriesTable", "innerHTML", html.tostring(queriesTableTree))
#     dajax.script(""" 
#         makeInputsDroppable();    
#     """);
    return dajax.json()
    
    
def renderSavedQuery(query, queryID):
    return """
        <tr id=query"""+ str(queryID) +""">
            <td><span class="icon upload" onclick="addSavedQueryToForm('query"""+ str(queryID) +"""')"></span></td>
            <td>""" + query +  """</td>
            <td><span class="icon invalid" onclick="deleteQuery('query"""+ str(queryID) +"""')"></span></td>
        </tr>
    """

# def checkTypes(queryFormTree, errors):
#     areTypesOK = True
#       
#     for criteria in queryFormTree.findall("./p"):
#         type = mapCriterias[criteria.attrib['id']].elementInfo.type
#         if (type == "integer"):
#             try:
#                 int(criteria[2][1].value)
#             except:
#                 errors.append(criteria[1].value + " must be of type : " + type)
#         elif (type == "string"):
#             pass
#         elif (type == "double"):
#             pass
#         elif (type == "query"):
#             pass
#         
#     return areTypesOK

@dajaxice_register
def updateUserInputs(request, htmlForm, fromElementID, criteriaID):   
    dajax = Dajax()
    global mapTagIDElementInfo
    toCriteriaID = "crit" + str(criteriaID)
    
    mapCriterias[toCriteriaID] = CriteriaInfo()
    mapCriterias[toCriteriaID].elementInfo = mapTagIDElementInfo[int(fromElementID)]
    
    htmlTree = html.fromstring(htmlForm)
    currentCriteria = htmlTree.get_element_by_id(toCriteriaID)  
    
    try:
        currentCriteria[1].attrib['class'] = currentCriteria[1].attrib['class'].replace('queryInput','elementInput') 
    except:
        pass
    # criteria id = crit%d  
    criteriaIDIncr = toCriteriaID[4:]
    userInputs = currentCriteria.find("./span/[@id='ui"+ str(criteriaIDIncr) +"']")
    
    for element in userInputs.findall("*"):
        userInputs.remove(element) 
    
    if (mapCriterias[toCriteriaID].elementInfo.type == "{0}:integer".format(defaultPrefix) 
        or mapCriterias[toCriteriaID].elementInfo.type == "{0}:double".format(defaultPrefix)
        or mapCriterias[toCriteriaID].elementInfo.type == "{0}:float".format(defaultPrefix)):
        form = html.fragment_fromstring(renderNumericSelect())
        inputs = html.fragment_fromstring(renderValueInput()) 
        userInputs.append(form)
        userInputs.append(inputs) 
    elif (mapCriterias[toCriteriaID].elementInfo.type == "enum"):
        form = html.fragment_fromstring(renderEnum(fromElementID))
        userInputs.append(form)
    else:
        form = html.fragment_fromstring(renderStringSelect())
        inputs = html.fragment_fromstring(renderValueInput())
        userInputs.append(form)
        userInputs.append(inputs)
        

#     userInputs.getparent()[1].attrib['class'] = "elementInput ui-droppable"
    
    dajax.assign("#queryForm", "innerHTML", html.tostring(htmlTree))
#     dajax.script("""
#         makeInputsDroppable();    
#     """);
    return dajax.json()
    
    
@dajaxice_register
def addSavedQueryToForm(request, queryForm, savedQueryID):
    dajax = Dajax()
    queryTree = html.fromstring(queryForm)
    
    fields = queryTree.findall("./p")
    fields[-1].remove(fields[-1].find("./span[@class='icon add']"))      
    if (len(fields) == 1):
        criteriaID = fields[0].attrib['id']
        minusButton = html.fragment_fromstring("""<span class="icon remove" onclick="removeField('""" + str(criteriaID) +"""')"></span>""")
        fields[0].append(minusButton)
        
    lastID = fields[-1].attrib['id'][4:]
    query = mapQueryInfo[savedQueryID[5:]].displayedQuery
    if (len(fields)== 1 and fields[0][1].value == ""):
        queryTree.remove(fields[0])
        tagID = int(lastID)
        element = html.fragment_fromstring("""
        <p id='crit""" + str(tagID) + """'>
        """
        +
            renderYESORNOT() 
        +
        """
            <input onclick="showCustomTree('crit""" + str(tagID) + """')" readonly="readonly" type="text" class="queryInput" value=" """+ str(query) +""" ">     
            <span id="ui"""+ str(tagID) +"""">
            </span>              
            <span class="icon add" onclick=addField()> </span>
        </p>
        """)
    else:
        tagID = int(lastID) + 1
        element = html.fragment_fromstring("""
            <p id='crit""" + str(tagID) + """'>
            """
            +
                renderANDORNOT() 
            +
            """
                <input onclick="showCustomTree('crit""" + str(tagID) + """')" readonly="readonly" type="text" class="queryInput" value=" """+ str(query) +""" ">     
                <span id="ui"""+ str(tagID) +"""">
                </span>  
                <span class="icon remove" onclick="removeField('crit"""+ str(tagID) +"""')"></span>
                <span class="icon add" onclick="addField()"> </span>
            </p>
        """)  
#             break
    
    #insert before the 3 buttons (save, clear, execute)
    queryTree.insert(-3,element)
    
    mapCriterias['crit'+ str(tagID)] = CriteriaInfo()
    mapCriterias['crit'+ str(tagID)].queryInfo = mapQueryInfo[savedQueryID[5:]]
    mapCriterias['crit'+ str(tagID)].elementInfo = ElementInfo("query") 
    dajax.assign("#queryForm", "innerHTML", html.tostring(queryTree))
#     dajax.script("""    
#         makeInputsDroppable();    
#     """);
    return dajax.json()
    

def renderInitialForm():
    return """
    <p id="crit0">
        <select>
          <option value=""></option>
          <option value="NOT">NOT</option>
        </select> 
        <input onclick="showCustomTree('crit0')" readonly="readonly" type="text" class="elementInput"/>
        <span id="ui0">
        </span>                        
        <span class="icon add" onclick="addField()"></span>                                
    </p>
    """

@dajaxice_register
def clearCriterias(request, queryForm):
    """ Reset Saved Criterias """
    dajax = Dajax()
    global mapCriterias
    
    # Load the criterias tree     
    queryTree = html.fromstring(queryForm)
    
    fields = queryTree.findall("./p")
    for field in fields:
        queryTree.remove(field)
    
    initialForm = html.fragment_fromstring(renderInitialForm())
    queryTree.insert(0,initialForm)  
    
    mapCriterias.clear()
      
    dajax.assign("#queryForm", "innerHTML", html.tostring(queryTree))
#     dajax.script("""   
#         makeInputsDroppable();    
#     """);
    return dajax.json()
    
@dajaxice_register
def clearQueries(request):
    """ Reset Saved Queries """
    dajax = Dajax()
    
    global mapQueryInfo
    
#     queriesTableTree = html.fromstring(queriesTable)
#         
#     # finds all lines in the table exept the first one : headers
#     for tr in queriesTableTree.findall('./tbody/tr')[1:]:
#         # removes existing rows         
#         queriesTableTree.find("./tbody").remove(tr)    
    connect('mgi')
    for queryID in mapQueryInfo.keys():
        SavedQuery(id=queryID).delete()
            
    mapQueryInfo.clear()
    
    if '_auth_user_id' in request.session and 'exploreCurrentTemplateID' in request.session:
        userID = request.session['_auth_user_id']
        templateID = request.session['exploreCurrentTemplateID']
        connect('mgi')
        userQueries = SavedQuery.objects(user=str(userID),template=str(templateID))
        queriesTableTree = html.fragment_fromstring(
            """<table>
                <tr>                    
                    <th width="15px">Add to Builder</th>
                    <th>Queries</th>
                    <th width="15px">Delete</th>
                </tr>                
            </table>""")
        if(len(userQueries) == 0):
            element = html.fragment_fromstring(renderNoQueries())
            queriesTableTree.append(element)
        
        
    dajax.assign("#queriesTable", "innerHTML", html.tostring(queriesTableTree))
    # render table again     
#     dajax.script("""  
#         makeInputsDroppable();    
#     """);
    return dajax.json()

def renderNoQueries():
    return "<tr id='noqueries'><td colspan='3' style='color:red;'>No Saved Queries for now.</td></tr>"


@dajaxice_register
def getCustomForm(request):
    dajax = Dajax()
    
#     if 'currentExploreTab' in request.session and request.session['currentExploreTab'] == "tab-1":
        
    global customFormString
    global mapQueryInfo
    global savedQueryForm
    
    #delete criterias if user comes from another page than results
    if 'keepCriterias' in request.session:
        del request.session['keepCriterias']
        if savedQueryForm != "" :
            dajax.assign("#queryForm", "innerHTML", savedQueryForm)
            savedQueryForm = ""
    else:
        mapCriterias.clear()
    
    #Get saved queries of an user
    mapQueryInfo.clear()
    if '_auth_user_id' in request.session and 'exploreCurrentTemplateID' in request.session:
        userID = request.session['_auth_user_id']
        templateID = request.session['exploreCurrentTemplateID']
        connect('mgi')
        userQueries = SavedQuery.objects(user=str(userID),template=str(templateID))
        queriesTable = html.fragment_fromstring(
            """<table>
                <tr>                    
                    <th width="15px">Add to Builder</th>
                    <th>Queries</th>
                    <th width="15px">Delete</th>
                </tr>                
            </table>""")
        if(len(userQueries) == 0):
            element = html.fragment_fromstring(renderNoQueries())
            queriesTable.append(element)
        else:
            for query in userQueries:
                for i in range(0, len(query.ListRegex)):
                    query.query = query.query.replace(query.ListRegex[i], "re.compile('" + query.ListPattern[i] + "')")
                    
                mapQueryInfo[str(query.id)] = QueryInfo(eval(query.query), query.displayedQuery)
                element = html.fragment_fromstring(renderSavedQuery(query.displayedQuery, query.id))            
                queriesTable.append(element)
        dajax.assign('#queriesTable', 'innerHTML', html.tostring(queriesTable))
        
    if (customFormString != ""):
        if 'currentExploreTab' in request.session and request.session['currentExploreTab'] == "tab-1":
            dajax.assign('#customForm', 'innerHTML', customFormString)
            dajax.assign('#sparqlCustomForm', 'innerHTML', "")
        elif 'currentExploreTab' in request.session and request.session['currentExploreTab'] == "tab-2":
            dajax.assign('#sparqlCustomForm', 'innerHTML', customFormString)
            dajax.assign('#customForm', 'innerHTML', "")
    else:
        customFormErrorMsg = "<p style='color:red;'>You should customize the template first. <a href='/explore/customize-template' style='color:red;font-weight:bold;'>Go back to Step 2 </a> and select the elements that you want to use in your queries.</p>"
        dajax.assign('#customForm', 'innerHTML', customFormErrorMsg)
        dajax.assign('#sparqlCustomForm', 'innerHTML', customFormErrorMsg)
    
#     elif 'currentExploreTab' in request.session and request.session['currentExploreTab'] == "tab-2":
        
    global sparqlQuery
    
    if sparqlQuery != "" :
        
        dajax.assign('#SPARQLqueryBuilder .SPARQLTextArea', 'innerHTML', sparqlQuery)
        sparqlQuery = ""
    
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
def saveCustomData(request,formContent):
    print '>>>>  BEGIN def saveCustomData(request,formContent)'
    dajax = Dajax()

#     global xmlString
    global customFormString
    global formString
    global anyChecked
    
#     global queryBuilderString
    
#     queryBuilderString = ""

#     xmlString = xmlContent
    formString = formContent

    # modify the form string to only keep the selected elements
    htmlTree = html.fromstring(formContent)
    createCustomTreeForQuery(htmlTree)
    if (anyChecked):
        customFormString = html.tostring(htmlTree)
    else:
        customFormString = ""
    
    anyChecked = False 
#     + """
#     <script>
#     $("#customForm").find("li[draggable=true]").draggable({
#         helper: "clone",
#     });
#     
#     $( "#queryForm input[droppable=true]" ).droppable({
#         hoverClass: "ui-state-hover",
#         drop: function( event, ui ) {
#             $(this).val(ui.draggable.text());
#             updateUserInputs(ui.draggable.attr('id'),$(this).parent().attr('id')); 
#         }
#     });
#     </script>
#     """

    print '>>>> END def saveCustomData(request,formContent)'
    return dajax.json()  

def createCustomTreeForQuery(htmlTree):
    global anyChecked
    anyChecked = False
    for li in htmlTree.findall("./ul/li"):
        manageLiForQuery(li)

def manageUlForQuery(ul):
    branchInfo = BranchInfo(keepTheBranch = False, selectedLeave = None)
#     hasOnlyLeaves = True
    selectedLeaves = []
    for li in ul.findall("./li"):
        liBranchInfo = manageLiForQuery(li)
        if(liBranchInfo.keepTheBranch == True):
            branchInfo.keepTheBranch = True
#         if(liBranchInfo.branchType == "branch"):
#             hasOnlyLeaves = False
        if (liBranchInfo.selectedLeave is not None):
            selectedLeaves.append(liBranchInfo.selectedLeave)
             
    if(not branchInfo.keepTheBranch):
        ul.attrib['style'] = "display:none;"
#     elif(hasOnlyLeaves and nbSelectedLeaves >1): # starting at 2 because 1 is the regular case
    elif(len(selectedLeaves) >1):
        parent = ul.getparent()
        parent.attrib['style'] = "color:purple;font-weight:bold;cursor:pointer;"
        leavesID = ""
        for leave in selectedLeaves[:-1]:
            leavesID += leave + " "
        leavesID += selectedLeaves[-1]
#         parent.attrib['onclick'] = "selectParent('"+ leavesID +"')"
        parent.insert(0, html.fragment_fromstring("""<span onclick="selectParent('"""+ leavesID +"""')">"""+ parent.text +"""</span>"""))
        parent.text = ""
    return branchInfo

            
def manageLiForQuery(li):
    listUl = li.findall("./ul")
    branchInfo = BranchInfo(keepTheBranch = False, selectedLeave = None)
    if (len(listUl) != 0):
        for ul in listUl:
            ulBranchInfo = manageUlForQuery(ul)
            if(ulBranchInfo.keepTheBranch == True):
                branchInfo.keepTheBranch = True
        if(not branchInfo.keepTheBranch):
            li.attrib['style'] = "display:none;"
        return branchInfo
    else:
        try:
            checkbox = li.find("./input[@type='checkbox']")
            if(checkbox.attrib['value'] == 'false'):
                li.attrib['style'] = "display:none;"
                return branchInfo
            else:
                global anyChecked
                anyChecked = True
                # remove the checkbox and make the element clickable
                li.attrib['style'] = "color:orange;font-weight:bold;cursor:pointer;"
                li.attrib['onclick'] = "selectElement("+ li.attrib['id'] +")"
                checkbox.attrib['style'] = "display:none;"   
                # tells to keep this branch until this leave
                branchInfo.keepTheBranch = True
                branchInfo.selectedLeave = li.attrib['id']          
                return branchInfo
        except:
            return branchInfo
  


@dajaxice_register
def downloadResults(request):
    print '>>>>  BEGIN def downloadResults(request)'
    dajax = Dajax()

    global results

    connect('mgi')
    
    if (len(results) > 0):
        xmlResults = []
        for result in results:
            xmlResults.append(str(xmltodict.unparse(result)))
        
        savedResults = QueryResults(results=xmlResults).save()
        savedResultsID = str(savedResults.id)
    
        dajax.redirect("/explore/results/download-results?id="+savedResultsID)
    
    print '>>>> END def downloadResults(request)'
    return dajax.json()
  

@dajaxice_register
def backToQuery(request):
    dajax = Dajax()
    global savedQueryForm
     
    request.session['keepCriterias'] = True

    return dajax.json()


@dajaxice_register
def redirectExplore(request):
    dajax = Dajax()
    
    request.session['currentExploreTab'] = "tab-2"
    dajax.redirect("/explore")
    
    return dajax.json()

@dajaxice_register
def redirectExploreTabs(request):
    dajax = Dajax()
       
    if 'currentExploreTab' in request.session and request.session['currentExploreTab'] == "tab-2":
        dajax.script("redirectSPARQLTab();")
    else:
        dajax.script("switchTabRefresh();")
    
    return dajax.json()

@dajaxice_register
def switchExploreTab(request,tab):
    dajax = Dajax()
    
    request.session["currentExploreTab"] = tab
    
    global customFormString
    
    if (customFormString != ""):
        if 'currentExploreTab' in request.session and request.session['currentExploreTab'] == "tab-1":
            dajax.assign('#customForm', 'innerHTML', customFormString)
            dajax.assign('#sparqlCustomForm', 'innerHTML', "")
        elif 'currentExploreTab' in request.session and request.session['currentExploreTab'] == "tab-2":
            dajax.assign('#sparqlCustomForm', 'innerHTML', customFormString)
            dajax.assign('#customForm', 'innerHTML', "")
    
    return dajax.json()


@dajaxice_register
def setCurrentCriteria(request, currentCriteriaID):
    dajax = Dajax()
    
    global criteriaID
    criteriaID = currentCriteriaID
    
    return dajax.json()

@dajaxice_register
def selectElement(request, elementID, elementName): 
    dajax = Dajax()
    
    if 'currentExploreTab' in request.session and request.session['currentExploreTab'] == "tab-1":
        global criteriaID    
        dajax.script("""
            $($("#"""+ criteriaID +"""").children()[1]).val('"""+ elementName +"""');
            $($("#"""+ criteriaID +"""").children()[1]).attr("class","elementInput");
            updateUserInputs("""+ str(elementID) +""", """+ str(criteriaID[4:]) +"""); 
            $("#dialog-customTree").dialog("close");    
        """)
        
        criteriaID = ""
    elif 'currentExploreTab' in request.session and request.session['currentExploreTab'] == "tab-2":
        global mapTagIDElementInfo
        elementPath = mapTagIDElementInfo[elementID].path
        elementPath = elementPath.replace(".","/tpl:")
        elementPath = "tpl:" + elementPath
        
        queryExample = """SELECT ?""" + elementName + """Value
WHERE {
?s """ + elementPath + """ ?o .
?o rdf:value ?""" + elementName + """Value .
}
"""
        dajax.script("""
            $("#sparqlElementPath").val('"""+ elementPath + """');
        """)
        dajax.assign("#sparqlExample", "innerHTML", queryExample)
    return dajax.json()

@dajaxice_register
def executeSPARQLQuery(request, queryStr, sparqlFormatIndex):
    print 'BEGIN def executeSPARQLQuery(request, queryStr, sparqlFormatIndex)'        
    dajax = Dajax()
    
    global sparqlResults
    global sparqlQuery
    
    sparqlQuery = queryStr
    sparqlResults = sparqlPublisher.sendSPARQL(str(sparqlFormatIndex) + queryStr)
    if sparqlResults is not None :
        dajax.script("sparqlResultsCallback();")

    print 'END def executeSPARQLQuery(request, queryStr, sparqlFormatIndex)'
    return dajax.json()

@dajaxice_register
def getSparqlResults(request):
    dajax = Dajax()
    
    global sparqlResults
    
    displayedSparqlResults = sparqlResults.replace("<", "&#60;")
    displayedSparqlResults = displayedSparqlResults.replace(">", "&#62;")
    resultString = ""
    resultString += "<pre class='sparqlResult' readonly='true'>"
#     resultString += "<pre>"  
    resultString += displayedSparqlResults
#     resultString += "</pre>"
    resultString += "</pre>"    
            
    dajax.assign("#results", "innerHTML", resultString)
    
    return dajax.json()

@dajaxice_register
def downloadSparqlResults(request):
    print '>>>>  BEGIN def downloadSparqlResults(request)'
    dajax = Dajax()

    global sparqlResults

    connect('mgi')
    
    if (sparqlResults is not None):
        
        savedResults = SparqlQueryResults(results=sparqlResults).save()
        savedResultsID = str(savedResults.id)
    
        dajax.redirect("/explore/results/download-sparqlresults?id="+savedResultsID)
    
    print '>>>> END def downloadSparqlResults(request)'
    return dajax.json()

@dajaxice_register
def prepareSubElementQuery(request, leavesID):
    print '>>>>  BEGIN def prepareSubElementQuery(request, leavesID)'
    dajax = Dajax()
    
    global mapTagIDElementInfo
    
    listLeavesId = leavesID.split(" ")
    firstElementPath = mapTagIDElementInfo[int(listLeavesId[0])].path
    parentPath = ".".join(firstElementPath.split(".")[:-1])
    parentName = parentPath.split(".")[-1]
    
    subElementQueryBuilderStr = "<p><b>" +parentName+ "</b></p>"
    subElementQueryBuilderStr += "<ul>"
    for leaveID in listLeavesId:
        elementInfo = mapTagIDElementInfo[int(leaveID)]
        elementName = elementInfo.path.split(".")[-1]
        subElementQueryBuilderStr += "<li><input type='checkbox' style='margin-right:4px;margin-left:2px;' checked/>"
        subElementQueryBuilderStr += renderYESORNOT()
        subElementQueryBuilderStr += elementName + ": "
        if (elementInfo.type == "{0}:integer".format(defaultPrefix) 
        or elementInfo.type == "{0}:double".format(defaultPrefix)
        or elementInfo.type == "{0}:float".format(defaultPrefix)):
            subElementQueryBuilderStr += renderNumericSelect()
            subElementQueryBuilderStr += renderValueInput()
        elif (elementInfo.type == "enum"):
            subElementQueryBuilderStr += renderEnum(leaveID)
        else:
            subElementQueryBuilderStr += renderStringSelect()
            subElementQueryBuilderStr += renderValueInput()
        subElementQueryBuilderStr += "</li><br/>"
    subElementQueryBuilderStr += "</ul>"
    
    dajax.assign("#subElementQueryBuilder", "innerHTML", subElementQueryBuilderStr)    
    
    print '>>>>  END def prepareSubElementQuery(request, leavesID)'
    return dajax.json()

@dajaxice_register
def insertSubElementQuery(request, leavesID, form):
    print '>>>>  BEGIN def insertSubElementQuery(request, leavesID, form)'
    dajax = Dajax()
    
    global mapTagIDElementInfo
    
    htmlTree = html.fromstring(form)
    listLi = htmlTree.findall("ul/li")
    listLeavesId = leavesID.split(" ")
    
    i = 0
    nbSelected = 0
    errors = []
    for li in listLi:
        if (li[0].attrib['value'] == 'true'):
            nbSelected += 1
            elementInfo = mapTagIDElementInfo[int(listLeavesId[i])]
            elementName = elementInfo.path.split(".")[-1]
            elementType = elementInfo.type
            error = checkSubElementField(li, elementName, elementType)
            if (error != ""):
                errors.append(error)
        i += 1
    
    if (nbSelected < 2):
        errors = ["Please select at least two elements."]
    
    if(len(errors) == 0):
        query = subElementfieldsToQuery(listLi, listLeavesId)
        prettyQuery = subElementfieldsToPrettyQuery(listLi, listLeavesId)
        mapCriterias[criteriaID] = CriteriaInfo()
        mapCriterias[criteriaID].queryInfo = QueryInfo(query, prettyQuery)
        mapCriterias[criteriaID].elementInfo = ElementInfo("query")
        global criteriaID
        uiID = "ui" + criteriaID[4:]
        dajax.script("""
            // insert the pretty query in the query builder
            $($("#"""+ criteriaID +"""").children()[1]).attr("value",'"""+ prettyQuery +"""');
            var field = $("#"""+ criteriaID +"""").children()[1]
            // replace the pretty by an encoded version
            $(field).attr("value",$(field).html($(field).attr("value")).text())
            // set the class to query
            $($("#"""+ criteriaID +"""").children()[1]).attr("class","queryInput");
            // remove all other existing inputs
            $("#"""+uiID+"""").children().remove();
            // close the dialog
            $("#dialog-subElementQuery").dialog("close");    
        """)        
    else:
        errorsString = ""
        for error in errors:
            errorsString += "<p>" + error + "</p>"            
        dajax.assign('#listErrors', 'innerHTML', errorsString)
        dajax.script("displayErrors();")
            
    
    print '>>>>  END def insertSubElementQuery(request, leavesID, form)'
    return dajax.json()

def checkSubElementField(liElement, elementName, elementType):   
    error = ""
       
    if (elementType == "{0}:float".format(defaultPrefix) or elementType == "{0}:double".format(defaultPrefix)):
        value = liElement[3].value
        try:
            float(value)
        except ValueError:
            error = elementName + " must be a number !"
                
    elif (elementType == "{0}:integer".format(defaultPrefix)):
        value = liElement[3].value
        try:
            int(value)
        except ValueError:
            error = elementName + " must be an integer !"
            
    elif (elementType == "{0}:string".format(defaultPrefix)):
        comparison = liElement[2].value
        value = liElement[3].value
        if (comparison == "like"):
            try:
                re.compile(value)
            except Exception, e:
                error = elementName + " must be a valid regular expression ! (" + str(e) + ")"    

    return error

def subElementfieldsToQuery(liElements, listLeavesId):
    global mapTagIDElementInfo
    
    elemMatch = dict()
    i = 0
    
    firstElementPath = mapTagIDElementInfo[int(listLeavesId[i])].path
    parentPath = "content." + ".".join(firstElementPath.split(".")[:-1])
    
    for li in liElements:        
        if (li[0].attrib['value'] == 'true'):
            boolComp = li[1].value
            if (boolComp == 'NOT'):
                isNot = True
            else:
                isNot = False
                
            elementInfo = mapTagIDElementInfo[int(listLeavesId[i])]
            elementType = elementInfo.type
            elementName = elementInfo.path.split(".")[-1]
            if (elementType == "enum"):
                value = li[2].value            
                criteria = enumCriteria(elementName, value, isNot)
            else:                
                comparison = li[2].value
                value = li[3].value
                criteria = buildCriteria(elementName, comparison, value, elementType , isNot)
             
        
            elemMatch.update(criteria)
                
        i += 1
         
    query = dict()
    query[parentPath] = dict()
    query[parentPath]["$elemMatch"] = elemMatch
    
    
    return query


def subElementfieldsToPrettyQuery(liElements, listLeavesId):
    query = ""
    
    elemMatch = "("
    i = 0
    
    for li in liElements:        
        if (li[0].attrib['value'] == 'true'):
            boolComp = li[1].value
            if (boolComp == 'NOT'):
                isNot = True
            else:
                isNot = False
                
            elementInfo = mapTagIDElementInfo[int(listLeavesId[i])]
            elementType = elementInfo.type
            elementName = elementInfo.path.split(".")[-1]
            if (elementType == "enum"):
                value = li[2].value
                criteria = enumToPrettyCriteria(elementName, value, isNot)
            else:                 
                comparison = li[2].value
                value = li[3].value
                criteria = buildPrettyCriteria(elementName, comparison, value, isNot)
            
            if (elemMatch != "("):
                elemMatch += ", "
            elemMatch += criteria       
        i += 1
        
    elemMatch += ")"
    firstElementPath = mapTagIDElementInfo[int(listLeavesId[0])].path
    parentName = firstElementPath.split(".")[-2]
    
    query =  parentName + elemMatch
        
    return query 
