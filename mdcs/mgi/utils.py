
import lxml.etree as etree
from mgi.models import MetaSchema, Template
from cStringIO import StringIO

################################################################################
# 
# Function Name: checkValidForMDCS(xmlTree, type)
# Inputs:        request - 
#                xmlTree - 
#                type - 
# Outputs:       errors
# Exceptions:    None
# Description:   Check that the format of the the schema is supported by the current version of the MDCS
# 
################################################################################
def getValidityErrorsForMDCS(xmlTree, type):
    errors = []
    
    # General Tests
    
    # get the imports
    imports = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}import")
    # get the includes
    includes = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}include")
    # get the elements
    elements = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}element")
    
    if len(imports) != 0 or len(includes) != 0:
        # V1: Only includes        
        if len(imports) != 0:
            errors.append("Import statements are not supported.")
        else:
            for el_include in includes:
                if 'schemaLocation' not in el_include.attrib:
                    errors.append("The attribute schemaLocation of include is required but missing.")
                elif ' ' in el_include.attrib['schemaLocation']:
                    errors.append("The use of namespace in include elements is not supported.")

    # Templates Tests

    if type == "Template":
        # Tests for templates
        if len(elements) < 1 :
            errors.append("Only templates with at least one root element are supported.")

    # Types Tests
    
    elif type == "Type":        
        elements = xmlTree.findall("*")
        # only simpleType, complexType or include
        for element in elements:
            if 'complexType' not in element.tag and 'simpleType' not in element.tag and 'include' not in element.tag:
                errors.append("A type should be a valid XML schema containing only one type definition (Allowed tags are: simpleType or complexType and include).")
                break
        # only one type
        for element in elements:
            cptType = 0 
            if 'complexType' in element.tag or 'simpleType' in element.tag:
                cptType += 1
                if cptType > 1:
                    errors.append("A type should be a valid XML schema containing only one type definition (only one simpleType or complexType).")
                    break

    return errors

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
    
    if templateID in MetaSchema.objects.all().values_list('schemaId'):
        meta = MetaSchema.objects.get(schemaId=templateID)
        xmlDocData = meta.flat_content
    else:
        templateObject = Template.objects.get(pk=templateID)
        xmlDocData = templateObject.content
    
    xmlTree = etree.parse(StringIO(xmlDocData.encode('utf-8')))
    
    xmlSchema = etree.XMLSchema(xmlTree)    
    xmlDoc = etree.fromstring(xmlString)
    prettyXMLString = etree.tostring(xmlDoc, pretty_print=True)  
    xmlSchema.assertValid(etree.parse(StringIO(prettyXMLString)))  

################################################################################
#
# Function Name: getXSDTypes(prefix)
# Inputs:        request - 
#                prefix - Namespace prefix 
# Outputs:       
# Exceptions:    None
# Description:   Returns the list of all supported XSD types
#
################################################################################
def getXSDTypes(prefix):
    return ["{0}:string".format(prefix), 
            "{0}:normalizedString".format(prefix),
            "{0}:token".format(prefix),
            "{0}:date".format(prefix),
            "{0}:dateTime".format(prefix),
            "{0}:duration".format(prefix),
            "{0}:gDay".format(prefix),
            "{0}:gMonth".format(prefix),
            "{0}:gMonthDay".format(prefix),
            "{0}:gYear".format(prefix),
            "{0}:gYearMonth".format(prefix),
            "{0}:gYearMonth".format(prefix),
            "{0}:time".format(prefix), 
            "{0}:byte".format(prefix),
            "{0}:decimal".format(prefix),
            "{0}:int".format(prefix),
            "{0}:integer".format(prefix),
            "{0}:long".format(prefix),
            "{0}:negativeInteger".format(prefix),
            "{0}:nonNegativeInteger".format(prefix),
            "{0}:nonPositiveInteger".format(prefix),
            "{0}:positiveInteger".format(prefix), 
            "{0}:short".format(prefix), 
            "{0}:unsignedLong".format(prefix), 
            "{0}:unsignedInt".format(prefix), 
            "{0}:unsignedShort".format(prefix), 
            "{0}:unsignedByte".format(prefix), 
            "{0}:anyURI".format(prefix), 
            "{0}:base64Binary".format(prefix), 
            "{0}:boolean".format(prefix), 
            "{0}:double".format(prefix),  
            "{0}:float".format(prefix),
            "{0}:hexBinary".format(prefix),
            "{0}:QName".format(prefix)]