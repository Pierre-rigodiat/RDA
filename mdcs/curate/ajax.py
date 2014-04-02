################################################################################
#
# File Name: ajax.py
# Application: Curate
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

#import xml.etree.ElementTree as etree
import lxml.etree as etree
import xml.dom.minidom as minidom

# Global Variables
xmlString = ""
xmlDocTree = ""
debugON = 0

################################################################################
#
# Function Name: getXsdString(request)
# Inputs:        request - 
# Outputs:       XML Schema of the current template
# Exceptions:    None
# Description:   Returns an XML Schema of the current template.
#                The template is possibly modified.
#
################################################################################
@dajaxice_register
def getXsdString(request):
    print 'BEGIN def getXmlString(request)'
    dajax = Dajax()

    templateFilename = request.session['currentTemplate']
    pathFile = "{0}/xsdfiles/" + templateFilename

    path = pathFile.format(
        settings.SITE_ROOT)
    xmlDoc = open(path,'r')
    xmlString = xmlDoc.read()

    print 'END def getXmlString(request)'
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
    print 'BEGIN def getXmlString(request)'
    dajax = Dajax()

    global xmlString

    print 'END def getXmlString(request)'
    return simplejson.dumps({'xmlString':xmlString})


    return simplejson.dumps({'xmlString':xmlstring})

################################################################################
# 
# Function Name: setCurrentTemplate(request)
# Inputs:        request - 
#                templateFilename -  
# Outputs:       JSON data with success or failure
# Exceptions:    None
# Description:   Set the current template to input argument.  Template is read into
#                an xsdDocTree for use later.
#
################################################################################
@dajaxice_register
def setCurrentTemplate(request,templateFilename):
    print 'BEGIN def setCurrentTemplate(request)'
    
    global xmlDocTree

    request.session['currentTemplate'] = templateFilename
    request.session.modified = True
    print '>>>>' + templateFilename + ' set as current template in session'
    dajax = Dajax()

    pathFile = "{0}/xsdfiles/" + templateFilename

    path = pathFile.format(
        settings.SITE_ROOT)
    xmlDoc = open(path,'r')
    xmlDocData = xmlDoc.read()
    print "xsdData: " + xmlDocData
    xmlDocTree2 = etree.XML(xmlDocData)
    print "xsdDocTree: " + str(xmlDocTree2)

    xmlDocTree = etree.parse(path)

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
# Function Name: generateFormSubSection(xpath,selected,xmlDataTree)
# Inputs:        xpath -
#                selected -
#                xmlDatatree - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   
#
################################################################################
def generateFormSubSection(xpath,selected,xmlDataTree):
    formString = ""
    global xmlString
    global xmlDocTree
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
        if debugON: formString += "matched complexType" + "<br>"
        complexTypeChild = e.find('*')

        if complexTypeChild is None:
            return formString

        if complexTypeChild.tag == "{0}sequence".format(namespace):
            if debugON: formString += "complexTypeChild:" + complexTypeChild.tag + "<br>"
            sequenceChildren = complexTypeChild.findall('*')
            for sequenceChild in sequenceChildren:
                if debugON: formString += "SequenceChild:" + sequenceChild.tag + "<br>"
                if sequenceChild.tag == "{0}element".format(namespace):
                    if sequenceChild.attrib.get('type') == "xsd:string".format(namespace):
                        textCapitalized = sequenceChild.attrib.get('name')[0].capitalize()  + sequenceChild.attrib.get('name')[1:]
                        newElement = etree.Element(textCapitalized)
                        newElement.text = ""
                        xmlDataTree.append(newElement)
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
                            formString += "<ul><li><nobr>" + textCapitalized + " <input type='text' disabled>" 
                            xmlString += "<" + sequenceChild.attrib.get('name') + ">" + "</" + sequenceChild.attrib.get('name') + ">"
                            if sequenceChild.attrib.get('maxOccurs') is not None:
                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                            elif sequenceChild.attrib.get('minOccurs') is not None:
                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                            formString += "</nobr></li></ul>"
                        else:
                            for x in range (0,occurances):
                                formString += "<ul><li><nobr>" + textCapitalized + " <input type='text'>"
                                xmlString += "<" + sequenceChild.attrib.get('name') + ">" + "</" + sequenceChild.attrib.get('name') + ">"
                                if sequenceChild.attrib.get('maxOccurs') is not None:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                    if (sequenceChild.attrib.get('maxOccurs') == "unbounded") or (int(sequenceChild.attrib.get('maxOccurs')) != occurances):
                                        currentXPath = xmlDocTree.getpath(sequenceChild)
                                        formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                elif sequenceChild.attrib.get('minOccurs') is not None:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                formString += "</nobr></li></ul>"
                    elif (sequenceChild.attrib.get('type') == "xsd:double".format(namespace)) or (sequenceChild.attrib.get('type') == "xsd:integer".format(namespace)) or (sequenceChild.attrib.get('type') == "xsd:anyURI".format(namespace)):
                        textCapitalized = sequenceChild.attrib.get('name')[0].capitalize()  + sequenceChild.attrib.get('name')[1:]
                        newElement = etree.Element(textCapitalized)
                        newElement.text = ""
                        xmlDataTree.append(newElement)
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
                            formString += "<ul><li><nobr>" + textCapitalized + " <input type='text' disabled>"
                            xmlString += "<" + sequenceChild.attrib.get('name') + ">" + "</" + sequenceChild.attrib.get('name') + ">"
                            if sequenceChild.attrib.get('maxOccurs') is not None:
                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                            elif sequenceChild.attrib.get('minOccurs') is not None:
                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                            formString += "</nobr></li></ul>"
                        else:
                            formString += "<ul><li><nobr>" + textCapitalized + " <input type='text'>"
                            xmlString += "<" + sequenceChild.attrib.get('name') + ">" + "</" + sequenceChild.attrib.get('name') + ">"
                            for x in range (0,occurances):
                                if sequenceChild.attrib.get('maxOccurs') is not None:
                                    if sequenceChild.attrib.get('maxOccurs') != "unbounded":
                                        maxOccurs = int(sequenceChild.attrib.get('maxOccurs'))
                                        if maxOccurs == 0:
                                            currentXPath = xmlDocTree.getpath(sequenceChild)
                                            formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                    else:
                                        currentXPath = xmlDocTree.getpath(sequenceChild)
                                        formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                if sequenceChild.attrib.get('minOccurs') is not None:
                                    minOccurs = int(sequenceChild.attrib.get('minOccurs'))
                                    if minOccurs == 0:
                                        currentXPath = xmlDocTree.getpath(sequenceChild)
                                        formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                            formString += "</nobr></li></ul>"
                    else:
                        if sequenceChild.attrib.get('type') is not None:
                            textCapitalized = sequenceChild.attrib.get('name')[0].capitalize()  + sequenceChild.attrib.get('name')[1:]
                            newElement = etree.Element(textCapitalized)
                            xmlDataTree.append(newElement)
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
                                formString += "<ul><li><nobr>" + textCapitalized + " "
                                xmlString += "<" + sequenceChild.attrib.get('name') + ">" 
                                if sequenceChild.attrib.get('maxOccurs') is not None:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    if (sequenceChild.attrib.get('maxOccurs') == "unbounded"):
                                        formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                        if sequenceChild.attrib.get('minOccurs') is not None:
                                            if (occurances > sequenceChild.attrib.get('minOccurs')):
                                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                                formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                        else:
                                            if (occurances > 1):
                                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                                formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                    else:
                                        if (int(sequenceChild.attrib.get('maxOccurs')) > occurances):
                                            formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                        if sequenceChild.attrib.get('minOccurs') is not None:
                                            print "occurances: " + str(occurances)
                                            print "minOccurs: " + str(sequenceChild.attrib.get('minOccurs'))
                                            if (occurances > int(sequenceChild.attrib.get('minOccurs'))):
                                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                                formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                        else:
                                            if (occurances > 1):
                                                currentXPath = xmlDocTree.getpath(sequenceChild)
                                                formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                elif sequenceChild.attrib.get('minOccurs') is not None:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
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
                            newElement = etree.Element(textCapitalized)
                            xmlDataTree.append(newElement)
                            formString += "<ul><li><nobr>" + textCapitalized + " "
                            xmlString += "<" + sequenceChild.attrib.get('name') + ">" 
                            if sequenceChild.attrib.get('occurances') is None:
                                sequenceChild.attrib['occurances'] = '1'
                            if sequenceChild.attrib.get('maxOccurs') is not None:
                                if sequenceChild.attrib.get('maxOccurs') != "unbounded":
                                    maxOccurs = int(sequenceChild.attrib.get('maxOccurs'))
                                    if maxOccurs == 0:
                                        currentXPath = xmlDocTree.getpath(sequenceChild)
                                        formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                                else:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    formString += "<span class=\"icon add\" onclick=\"changeXMLSchema('add','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                            if sequenceChild.attrib.get('minOccurs') is not None:
                                minOccurs = int(sequenceChild.attrib.get('minOccurs'))
                                if minOccurs == 0:
                                    currentXPath = xmlDocTree.getpath(sequenceChild)
                                    formString += "<span class=\"icon remove\" onclick=\"changeXMLSchema('remove','" + currentXPath + "','" + sequenceChild.attrib.get('name') + "');\"></span>"
                            formString += generateFormSubSection(sequenceChild.attrib.get('type'),selected,newElement)
                            xmlString += "</" + sequenceChild.attrib.get('name') + ">"
                            formString += "</nobr></li></ul>"
                elif sequenceChild.tag == "{0}choice".format(namespace):
                    formString += "<ul><li><nobr>Choose <select onchange=\"alert('change to ' + this.value);\">"
                    choiceChildren = sequenceChild.findall('*')
                    selectedChild = choiceChildren[0]
                    xmlString += "<" + selectedChild.attrib.get('name') + "/>"
                    for choiceChild in choiceChildren:
                        if choiceChild.tag == "{0}element".format(namespace):
                            textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                            newElement = etree.Element(textCapitalized)
                            newElement.text = ""
                            xmlDataTree.append(newElement)
                            formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
                        formString += "</select>"
                    if selected == "":
                        choiceFirstChild = complexTypeChild[0]
                        if choiceFirstChild.tag == "{0}element".format(namespace):
                            if choiceFirstChild.attrib.get('type') != "xsd:string".format(namespace):
                                textCapitalized = choiceFirstChild.attrib.get('name')[0].capitalize()  + choiceFirstChild.attrib.get('name')[1:]
                                newElement = etree.Element(textCapitalized)
                                xmlDataTree.append(newElement)
                                formString += "<ul><li><nobr>" + textCapitalized
                                xmlString += "<" + textCapitalized + ">" 
                                formString += generateFormSubSection(choiceFirstChild.attrib.get('type'),selected,newElement) + "</nobr></li></ul>"
                                xmlString += "</" + textCapitalized + ">"
                            else:
                                formString += "<ul><li><nobr>" + choiceFirstChild.attrib.get('name').capitalize() + " <input type='text'>" + "</nobr></li></ul>"
                    else:
                        formString += "selected not empty"
                    formString += "</nobr></li></ul>"
        elif complexTypeChild.tag == "{0}choice".format(namespace):
            if debugON: formString += "complexTypeChild:" + complexTypeChild.tag + "<br>"
            formString += "<ul><li><nobr>Choose <select onchange=\"alert('change to ' + this.value);\">"
            choiceChildren = complexTypeChild.findall('*')
            selectedChild = choiceChildren[0]
            xmlString += "<" + selectedChild.attrib.get('name') + "/>"
            for choiceChild in choiceChildren:
                if choiceChild.tag == "{0}element".format(namespace):
                    textCapitalized = choiceChild.attrib.get('name')[0].capitalize()  + choiceChild.attrib.get('name')[1:]
                    newElement = etree.Element(textCapitalized)
                    newElement.text = ""
                    xmlDataTree.append(newElement)
                    formString += "<option value='" + textCapitalized + "'>" + textCapitalized + "</option></b><br>"
            formString += "</select>"
            if selected == "":
                choiceFirstChild = complexTypeChild[0]
                if choiceFirstChild.tag == "{0}element".format(namespace):
                    if choiceFirstChild.attrib.get('type') != "xsd:string".format(namespace):
                        textCapitalized = choiceFirstChild.attrib.get('name')[0].capitalize()  + choiceFirstChild.attrib.get('name')[1:]
                        newElement = etree.Element(textCapitalized)
                        xmlDataTree.append(newElement)
                        formString += "<ul><li><nobr>" + textCapitalized
                        xmlString += "<" + textCapitalized + ">" 
                        formString += generateFormSubSection(choiceFirstChild.attrib.get('type'),selected,newElement) + "</nobr></li></ul>"
                        xmlString += "</" + textCapitalized + ">"
                    else:
                        formString += "<ul><li><nobr>" + choiceFirstChild.attrib.get('name').capitalize() + " <input type='text'>" + "</nobr></li></ul>"
            else:
                formString += "selected not empty"
            formString += "</nobr></li></ul>"
        elif complexTypeChild.tag == "{0}attribute".format(namespace):
            textCapitalized = complexTypeChild.attrib.get('name')[0].capitalize()  + complexTypeChild.attrib.get('name')[1:]
            newElement = etree.Element(textCapitalized)
            newElement.text = ""
            xmlDataTree.append(newElement)
            formString += "<li>" + textCapitalized + "</li>"
            xmlString += "<" + textCapitalized + ">" 
            xmlString += "</" + textCapitalized + ">"
    elif e.tag == "{0}simpleType".format(namespace):
        if debugON: formString += "matched simpleType" + "<br>"

        simpleTypeChildren = e.findall('*')
        
        if simpleTypeChildren is None:
            return formString

        for simpleTypeChild in simpleTypeChildren:
            if simpleTypeChild.tag == "{0}restriction".format(namespace):
                formString += "<select>"
                choiceChildren = simpleTypeChild.findall('*')
                selectedChild = choiceChildren[0]
                xmlString += selectedChild.attrib.get('value')
                for choiceChild in choiceChildren:
                    if choiceChild.tag == "{0}enumeration".format(namespace):
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
# Function Name: generateForm(key,xmlDataTree)
# Inputs:        key -
#                xmlDatatree -
# Outputs:       rendered HTMl form
# Exceptions:    None
# Description:   Renders HTMl form for display.
#
################################################################################
def generateForm(key,xmlDataTree):
    formString = ""
    global xmlString
    global xmlDocTree

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
        formString += "<b>" + textCapitalized + "</b><br>"
        xmlDataTree = etree.Element(textCapitalized)
        if debugON: xmlString += "<" + textCapitalized + ">"
        xmlString += "<" + e[0].attrib.get('name') + ">"
        if debugON: formString += "<b>" + e[0].attrib.get('name').capitalize() + "</b><br>"
        formString += generateFormSubSection(e[0].attrib.get('type'),"",xmlDataTree)
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
    global xmlDocTree

    templateFilename = request.session['currentTemplate']
#    request.session.modified = True
    print '>>>>' + templateFilename + ' is the current template in session'
    dajax = Dajax()

    pathFile = "{0}/xsdfiles/" + templateFilename

    path = pathFile.format(
        settings.SITE_ROOT)
    xmlDoc = open(path,'r')
    xmlDocData = xmlDoc.read()
#    print "xsdDocData: " + xmlDocData
#    xmlDocTree = etree.XML(xmlDocData)

#   xmlDocTree = etree.parse(path)
    xmlDataTree = ""
    xmlString = ""
#    print "xsdDocTree: " + str(xmlDocTree)

    formString = "<br><form id=\"dataEntryForm\">"

    formString += generateForm("schema",xmlDataTree)

#    root = xmlDocTree.getroot()

#    for child in root:
#        print child.tag

    reparsed = minidom.parseString(xmlString)
#    print "xmlDataTree: " + reparsed.toprettyxml(indent="  ")
    formString += "</form>"

#    pretty_xml_as_string = xml.dom.minidom.parseString(xmlDocData).toprettyxml()

    dajax.assign('#xsdForm', 'innerHTML', formString)
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

