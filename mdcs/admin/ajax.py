################################################################################
#
# File Name: ajax.py
# Application: admin
# Purpose:    AJAX methods used for administration purposes
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

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import lxml.etree as etree
import json
from io import BytesIO
from mgi.models import Template, TemplateVersion, Instance, Request, Module, ModuleResource, Type, TypeVersion, Message, TermsOfUse, PrivacyPolicy
from django.core.files.temp import NamedTemporaryFile
import hashlib
import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import os
from django.conf import settings
from datetime import datetime

#Class definition

################################################################################
# 
# Class Name: ModuleResourceInfo
#
# Description: Store information about a resource for a module
#
################################################################################
class ModuleResourceInfo:
    "Class that store information about a resource for a module"
    
    def __init__(self, content = "", filename = ""):
        self.content = content
        self.filename = filename   

    def __to_json__(self):
        return json.dumps(self, default=lambda o:o.__dict__)


################################################################################
# 
# Function Name: uploadObject(request,objectName,objectFilename,objectContent, objectType)
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
        # 1) get the name from the file: type of the root or type of the root without namespace, check only one root
        elements = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}element")
        if (len(elements) != 1):
            dajax.script("""
                $("#objectNameErrorMessage").html("<font color='red'>Only templates with one root element can be uploaded as a type.</font><br/>");
            """)
            return dajax.json()
        else:
            elem = elements[0]
            if ('type' in elem.attrib):
                elementType = elem.attrib['type']
            else:
                dajax.script("""
                $("#objectNameErrorMessage").html("<font color='red'>The 'type' attribute should appear in the root element.</font><br/>");
                """)
                return dajax.json()
                                                                    
        # 2) check that the filename is not already in the database
        try:
            Type.objects.get(filename=objectFilename)
            dajax.script("""
            $("#objectNameErrorMessage").html("<font color='red'>A type with the same filename already exists.</font><br/>");
            """)
            return dajax.json()
        except:            
            # 3) Save the type
            objectVersions = TypeVersion(nbVersions=1, isDeleted=False).save()
            object = Type(title=elementType, filename=objectFilename, content=objectContent, version=1, typeVersion=str(objectVersions.id)).save()
    
    objectVersions.versions = [str(object.id)]
    objectVersions.current=str(object.id)
    objectVersions.save()    
    object.save()
    

    print 'END def uploadXMLSchema(request,xmlSchemaFilename,xmlSchemaContent)'
    return dajax.json()


################################################################################
# 
# Function Name: deleteObject(request, objectID, objectType)
# Inputs:        request - 
#                objectID - 
#                objectType - 
# Outputs:       JSON data 
# Exceptions:    None
# Description:   Delete an object (template or type).
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

    objectVersions.deletedVersions.append(str(object.id))    
    objectVersions.isDeleted = True
    objectVersions.save()


    print 'END def deleteXMLSchema(request,xmlSchemaID)'
    return dajax.json()

################################################################################
# 
# Function Name: setSchemaVersionContent(request, versionContent, versionFilename)
# Inputs:        request - 
#                versionContent -
#                versionFilename - 
# Outputs:       
# Exceptions:    None
# Description:   Save the name and content of uploaded schema before save
#
################################################################################
@dajaxice_register
def setSchemaVersionContent(request, versionContent, versionFilename):
    dajax = Dajax()
    
    request.session['xsdVersionContent'] = versionContent
    request.session['xsdVersionFilename'] = versionFilename
    
    return dajax.json()

################################################################################
# 
# Function Name: setTypeVersionContent(request, versionContent, versionFilename)
# Inputs:        request - 
#                versionContent -
#                versionFilename - 
# Outputs:       
# Exceptions:    None
# Description:   Save the name and content of uploaded type before save
#
################################################################################
@dajaxice_register
def setTypeVersionContent(request, versionContent, versionFilename):
    dajax = Dajax()
    
    request.session['typeVersionContent'] = versionContent
    request.session['typeVersionFilename'] = versionFilename
    
    return dajax.json()

################################################################################
# 
# Function Name: uploadVersion(request, objectVersionID, objectType)
# Inputs:        request - 
#                objectVersionID -
#                objectType - 
# Outputs:       
# Exceptions:    None
# Description:   Upload the object (template or type)
#
################################################################################
@dajaxice_register
def uploadVersion(request, objectVersionID, objectType):
    dajax = Dajax()    
    
    # Templates
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
    else: #Types
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
        
        # check if a type with the same name already exists
        testFilenameObjects = Type.objects(filename=versionFilename)    
        if len(testFilenameObjects) == 1: # 0 is ok, more than 1 can't happen
            dajax.script("""
                showErrorEditType();
            """)
            return dajax.json()

        objectVersions.nbVersions += 1
        if objectType == "Template": 
            hash = hashlib.sha1(versionContent)
            hex_dig = hash.hexdigest()
            newObject = Template(title=object.title, filename=versionFilename, content=versionContent, templateVersion=objectVersionID, version=objectVersions.nbVersions, hash=hex_dig).save()
        else:
            newObject = Type(title=object.title, filename=versionFilename, content=versionContent, typeVersion=objectVersionID, version=objectVersions.nbVersions).save()
        objectVersions.versions.append(str(newObject.id))
        objectVersions.save()
                
        dajax.script("""
            $("#delete_custom_message").html("");
            $('#model_version').load(document.URL +  ' #model_version', function() {}); 
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

################################################################################
# 
# Function Name: setCurrentVersion(request, objectid, objectType)
# Inputs:        request - 
#                objectid -
#                objectType - 
# Outputs:       
# Exceptions:    None
# Description:   Set the current version of the object (template or type)
#
################################################################################
@dajaxice_register
def setCurrentVersion(request, objectid, objectType):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
    
    objectVersions.current = str(object.id)
    objectVersions.save()
     
    dajax.script("""
        $("#delete_custom_message").html("");   
        $('#model_version').load(document.URL +  ' #model_version', function() {});      
    """)
    
    return dajax.json()

################################################################################
# 
# Function Name: deleteVersion(request, objectid, objectType, newCurrent)
# Inputs:        request - 
#                objectid -
#                objectType - 
#                newCurrent - 
# Outputs:       
# Exceptions:    None
# Description:   Delete a version of the object (template or type) by adding it to the list of deleted
#
################################################################################
@dajaxice_register
def deleteVersion(request, objectid, objectType, newCurrent):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
      

    if len(objectVersions.versions) == 1 or len(objectVersions.versions) == len(objectVersions.deletedVersions) + 1:
        objectVersions.deletedVersions.append(str(object.id))    
        objectVersions.isDeleted = True
        objectVersions.save()
        dajax.script("""
            $("#delete_custom_message").html("");
            window.parent.versionDialog.dialog("close");  
        """)
    else:
        if newCurrent != "": 
            objectVersions.current = newCurrent
        objectVersions.deletedVersions.append(str(object.id))   
        objectVersions.save()        
    
        dajax.script("""
            $("#delete_custom_message").html("");   
            $('#model_version').load(document.URL +  ' #model_version', function() {}); 
        """)
    
    return dajax.json()

################################################################################
# 
# Function Name: assignDeleteCustomMessage(request, objectid, objectType)
# Inputs:        request - 
#                objectid -
#                objectType - 
# Outputs:       
# Exceptions:    None
# Description:   Assign a message to the dialog box regarding the situation of the version that is about to be deleted
#
################################################################################
@dajaxice_register
def assignDeleteCustomMessage(request, objectid, objectType):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)  
    
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
    
    dajax.script("""
                    $('#delete_custom_message').html(" """+ message +""" ");
                 """)
    
    return dajax.json()

################################################################################
# 
# Function Name: editInformation(request, objectid, objectType, newName, newFilename)
# Inputs:        request - 
#                objectid -
#                objectType - 
#                newName - 
#                newFileName -
# Outputs:       
# Exceptions:    None
# Description:   Edit information of an object (template or type)
#
################################################################################
@dajaxice_register
def editInformation(request, objectid, objectType, newName, newFilename):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:        
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
        # check if a type with the same name already exists
        testFilenameObjects = Type.objects(filename=newFilename)    
        if len(testFilenameObjects) == 1: # 0 is ok, more than 1 can't happen
            #check that the type with the same filename is the current one
            if testFilenameObjects[0].id != object.id:
                dajax.script("""
                    showErrorEditType();
                """)
                return dajax.json()
    
    # change the name of every version but only the filename of the current
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


################################################################################
# 
# Function Name: restoreObject(request, objectid, objectType)
# Inputs:        request - 
#                objectid -
#                objectType - 
# Outputs:       
# Exceptions:    None
# Description:   Restore an object previously deleted (template or type)
#
################################################################################
@dajaxice_register
def restoreObject(request, objectid, objectType):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
        
    objectVersions.isDeleted = False
    del objectVersions.deletedVersions[objectVersions.deletedVersions.index(objectVersions.current)]
    objectVersions.save()
    
    dajax.script("""
        $('#model_selection').load(document.URL +  ' #model_selection', function() {
              loadUploadManagerHandler();
        });
    """)
    
    return dajax.json()

################################################################################
# 
# Function Name: restoreVersion(request, objectid, objectType)
# Inputs:        request - 
#                objectid -
#                objectType - 
# Outputs:       
# Exceptions:    None
# Description:   Restore a version of an object previously deleted (template or type)
#
################################################################################
@dajaxice_register
def restoreVersion(request, objectid, objectType):
    dajax = Dajax()
    
    if objectType == "Template":
        object = Template.objects.get(pk=objectid)
        objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
    else:
        object = Type.objects.get(pk=objectid)
        objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
        
    del objectVersions.deletedVersions[objectVersions.deletedVersions.index(objectid)]
    objectVersions.save()
       
    dajax.script("""
        $("#delete_custom_message").html("");
        $('#model_version').load(document.URL +  ' #model_version', function() {}); 
    """)
    
    return dajax.json()

################################################################################
# 
# Function Name: addInstance(request, name, protocol, address, port, user, password)
# Inputs:        request - 
#                name -
#                protocol - 
#                address - 
#                port - 
#                user - 
#                password - 
# Outputs:       
# Exceptions:    None
# Description:   Register a remote instance for the federation of queries
#
################################################################################
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
            url = protocol + "://" + address + ":" + port + "/rest/ping"
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

################################################################################
# 
# Function Name: retrieveInstance(request, instanceid)
# Inputs:        request - 
#                instanceid - 
# Outputs:       
# Exceptions:    None
# Description:   Retrieve an instance to edit it
#
################################################################################
@dajaxice_register
def retrieveInstance(request, instanceid):
    dajax = Dajax()
    
    instance = Instance.objects.get(pk=instanceid)
    dajax.script("editInstanceCallback('"+ str(instance.name) +"','"+ str(instance.protocol) +"','"+ str(instance.address) +"','"+ str(instance.port) +"','"+ str(instance.user) +"','"+ str(instance.password) +"','"+ str(instanceid) +"');")
    
    return dajax.json()

################################################################################
# 
# Function Name: editInstance(request, instanceid, name, protocol, address, port, user, password)
# Inputs:        request -
#                instanceid - 
#                name -
#                protocol - 
#                address - 
#                port - 
#                user - 
#                password - 
# Outputs:       
# Exceptions:    None
# Description:   Edit the instance information
#
################################################################################
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
            url = protocol + "://" + address + ":" + port + "/rest/ping"
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

################################################################################
# 
# Function Name: deleteInstance(request, instanceid)
# Inputs:        request -
#                instanceid -  
# Outputs:       
# Exceptions:    None
# Description:   Delete an instance
#
################################################################################
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

################################################################################
# 
# Function Name: requestAccount(request, username, password, firstname, lastname, email)
# Inputs:        request - 
#                username - 
#                password - 
#                firstname - 
#                lastname - 
#                email - 
# Outputs:        
# Exceptions:    None
# Description:   Submit a request for an user account for the system.
# 
################################################################################
@dajaxice_register
def requestAccount(request, username, password, firstname, lastname, email):
    dajax = Dajax()
    try:
        user = User.objects.get(username=username)
        dajax.script("showErrorRequestDialog();")
    except:
        Request(username=username, password=password ,first_name=firstname, last_name=lastname, email=email).save()
        dajax.script("showSentRequestDialog();")
    return dajax.json()

################################################################################
# 
# Function Name: acceptRequest(request, requestid)
# Inputs:        request - 
#                requestid - 
# Outputs:        
# Exceptions:    None
# Description:   Accepts a request and creates the user account
# 
################################################################################
@dajaxice_register
def acceptRequest(request, requestid):
    dajax = Dajax()
    userRequest = Request.objects.get(pk=requestid)
    try:
        existingUser = User.objects.get(username=userRequest.username)
        dajax.script("showErrorRequestDialog();")        
    except:
        user = User.objects.create_user(username=userRequest.username, password=userRequest.password, first_name=userRequest.first_name, last_name=userRequest.last_name, email=userRequest.email)
        user.save()
        userRequest.delete()
        dajax.script("showAcceptedRequestDialog();")
        
    return dajax.json()

################################################################################
# 
# Function Name: denyRequest(request, requestid)
# Inputs:        request - 
#                requestid - 
# Outputs:        
# Exceptions:    None
# Description:   Denies a request
# 
################################################################################
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

################################################################################
# 
# Function Name: initModuleManager(request)
# Inputs:        request - 
#                requestid - 
# Outputs:        
# Exceptions:    None
# Description:   Empties the list of resource when come to the module manager
# 
################################################################################
@dajaxice_register
def initModuleManager(request):
    dajax = Dajax()
    
    request.session['listModuleResource'] = []
    
    return dajax.json()

################################################################################
# 
# Function Name: addModuleResource(request, resourceContent, resourceFilename)
# Inputs:        request - 
#                resourceContent - 
#                resourceFilename - 
# Outputs:        
# Exceptions:    None
# Description:   Add a resource for the module. Save the content and name before save.
# 
################################################################################
@dajaxice_register
def addModuleResource(request, resourceContent, resourceFilename):
    dajax = Dajax()
    
    request.session['currentResourceContent'] = resourceContent
    request.session['currentResourceFilename'] = resourceFilename    
    
    return dajax.json()


################################################################################
# 
# Function Name: uploadResource(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Upload the resource
# 
################################################################################
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

################################################################################
# 
# Function Name: addModule(request, template, name, tag, HTMLTag)
# Inputs:        request - 
#                template - 
#                name - 
#                tag - 
#                HTMLTag - 
# Outputs:        
# Exceptions:    None
# Description:   Add a module in mongo db
# 
################################################################################
@dajaxice_register
def addModule(request, templates, name, tag, HTMLTag):
    dajax = Dajax()    
    
    module = Module(name=name, templates=templates, tag=tag, htmlTag=HTMLTag)
    listModuleResource = request.session['listModuleResource']
    for resource in listModuleResource: 
        resource = eval(resource)        
        moduleResource = ModuleResource(name=resource['filename'], content=resource['content'], type=resource['filename'].split(".")[-1])
        module.resources.append(moduleResource)
    
    module.save()

    return dajax.json()

################################################################################
# 
# Function Name: deleteModule(request, objectid)
# Inputs:        request - 
#                objectid - 
# Outputs:        
# Exceptions:    None
# Description:   Delete a module
# 
################################################################################
@dajaxice_register
def deleteModule(request, objectid):
    dajax = Dajax()    
    
    module = Module.objects.get(pk=objectid)
    module.delete()

    return dajax.json()

################################################################################
# 
# Function Name: createBackup(request, mongodbPath)
# Inputs:        request - 
#                mongoPath -  
# Outputs:        
# Exceptions:    None
# Description:   Runs the mongo db command to create a backup of the current mongo instance
# 
################################################################################
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
    dajax.script("showBackupDialog();")
    return dajax.json()

################################################################################
# 
# Function Name: restoreBackup(request, mongodbPath, backup)
# Inputs:        request - 
#                mongoPath -  
#                backup - 
# Outputs:        
# Exceptions:    None
# Description:   Runs the mongo db command to restore a backup to the current mongo instance
# 
################################################################################
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
    dajax.script("showBackupDialog();")
    return dajax.json()

################################################################################
# 
# Function Name: restoreBackup(request, backup)
# Inputs:        request -   
#                backup - 
# Outputs:        
# Exceptions:    None
# Description:   Deletes a backup from the list
# 
################################################################################
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

################################################################################
# 
# Function Name: saveUserProfile(request, userid, username, firstname, lastname, email)
# Inputs:        request -   
#                userid - 
#                username - 
#                firstname -
#                lastname -
#                email - 
# Outputs:        
# Exceptions:    None
# Description:   saves the user profile with the updated information
# 
################################################################################
@dajaxice_register
def saveUserProfile(request, userid, username, firstname, lastname, email):
    dajax = Dajax()
    
    user = User.objects.get(id=userid)
    errors = ""
    if username != user.username:
        try:
            user = User.objects.get(username=username)
            errors += "A user with the same username already exists.<br/>"
            dajax.script("showEditErrorDialog('"+errors+"');")
            return dajax.json()
        except:
            user.username = username
    
    user.first_name = firstname
    user.last_name = lastname
    user.email = email
    user.save()
    dajax.script("showSavedProfileDialog();")
    
    return dajax.json()


################################################################################
# 
# Function Name: changePassword(request, userid, old_password, password)
# Inputs:        request -   
#                userid - 
#                old_password - 
#                password - 
# Outputs:        
# Exceptions:    None
# Description:   Changes the password of the user
# 
################################################################################
@dajaxice_register
def changePassword(request, userid, old_password, password):
    dajax = Dajax()
    
    errors = ""
    user = User.objects.get(id=userid)
    auth_user = authenticate(username=user.username, password=old_password)
    if auth_user is None:
        errors += "The old password is incorrect."
        dajax.script("showChangePasswordErrorDialog('"+ errors +"')")
        return dajax.json()
    else:        
        user.set_password(password)
        user.save()
        dajax.script("showPasswordChangedDialog();")

    
    return dajax.json()

################################################################################
# 
# Function Name: pingRemoteAPI(request, name, protocol, address, port, user, password)
# Inputs:        request -
#                name - 
#                protocol -
#                address - 
#                port -
#                user -
#                password - 
# Outputs:       
# Exceptions:    None
# Description:   Ping a remote instance to see if it is reachable with the given parameters
#
################################################################################
@dajaxice_register
def pingRemoteAPI(request, name, protocol, address, port, user, password):
    dajax = Dajax()
    
    try:
        url = protocol + "://" + address + ":" + port + "/rest/ping"
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
# Function Name: contact(request, name, email, message)
# Inputs:        request -
#                name - 
#                email -
#                message - 
# Outputs:       
# Exceptions:    None
# Description:   Send a message to the Administrator
#
################################################################################
@dajaxice_register
def contact(request, name, email, message):
    dajax = Dajax()
    
    Message(name=name, email=email, content=message).save()
    
    return dajax.json()

################################################################################
# 
# Function Name: removeMessage(request, messageid)
# Inputs:        request -
#                messageid - 
# Outputs:       
# Exceptions:    None
# Description:   Remove a message from Contact form
#
################################################################################
@dajaxice_register
def removeMessage(request, messageid):
    dajax = Dajax()
    
    message = Message.objects.get(pk=messageid)
    message.delete()
        
    return dajax.json()

################################################################################
# 
# Function Name: saveTermsOfUse(request, content)
# Inputs:        request -
#                content - 
# Outputs:       
# Exceptions:    None
# Description:   Saves the terms of use
#
################################################################################
@dajaxice_register
def saveTermsOfUse(request, content):
    dajax = Dajax()
    
    for term in TermsOfUse.objects:
        term.delete()
    
    if (content != ""):
        newTerms = TermsOfUse(content = content)
        newTerms.save()
    
    return dajax.json()


################################################################################
# 
# Function Name: savePrivacyPolicy(request, content)
# Inputs:        request -
#                content - 
# Outputs:       
# Exceptions:    None
# Description:   Saves the privacy policy
#
################################################################################
@dajaxice_register
def savePrivacyPolicy(request, content):
    dajax = Dajax()
    
    for privacy in PrivacyPolicy.objects:
        privacy.delete()
    
    if (content != ""):
        newPrivacy = PrivacyPolicy(content = content)
        newPrivacy.save()
    
    return dajax.json()

