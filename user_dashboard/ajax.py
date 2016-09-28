################################################################################
#
# File Name: ajax.py
# Application: dashboard
# Description:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Xavier SCHMITT
#         xavier.schmitt@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.contrib.auth.decorators import login_required
from django.conf import settings
from mgi.settings import BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI
from utils.BLOBHoster.BLOBHosterFactory import BLOBHosterFactory
from django.http import HttpResponse
from mgi.models import Template, XMLdata, Type, delete_template, delete_type, FormData
from django.contrib import messages
import lxml.etree as etree
from io import BytesIO
import json
from mgi.common import send_mail_to_managers
from utils.XSDParser.parser import delete_branch_from_db
import os
from django.utils.importlib import import_module
settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
MDCS_URI = settings.MDCS_URI


################################################################################
#
# Function Name: edit_information(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Edit information of an object (template or type)
#
################################################################################
@login_required(login_url='/login')
def edit_information(request):
    object_id = request.POST['objectID']
    object_type = request.POST['objectType']
    new_name = request.POST['newName']
    new_filename = request.POST['newFilename']

    if object_type == "Template":
        object = Template.objects.get(pk=object_id)
        testFilenameObjects = Template.objects(filename=new_filename.strip())
        testNameObjects = Template.objects(title=new_name.strip())
    else:
        object = Type.objects.get(pk=object_id)
        testFilenameObjects = Type.objects(filename=new_filename.strip())
        testNameObjects = Type.objects(title=new_name.strip())

    if len(testNameObjects) == 1: # 0 is ok, more than 1 can't happen
            #check that the type with the same filename is the current one
        if testNameObjects[0].id != object.id:
            response_dict = {'name': 'True'}
            return HttpResponse(json.dumps(response_dict), content_type='application/javascript')

    if len(testFilenameObjects) == 1: # 0 is ok, more than 1 can't happen
            #check that the type with the same filename is the current one
        if testFilenameObjects[0].id != object.id:
            response_dict = {'filename': 'True'}
            return HttpResponse(json.dumps(response_dict), content_type='application/javascript')

    object.title = new_name.strip()
    object.filename = new_filename.strip()
    object.save()

    return HttpResponse(json.dumps({}), content_type='application/javascript')

################################################################################
#
# Function Name: delete_object(request)
# Inputs:        request -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Delete an object (template or type).
#
################################################################################
@login_required(login_url='/login')
def delete_object(request):
    print 'BEGIN def delete_object(request)'
    objects_id = request.POST.getlist('objectID[]')
    object_type = request.POST['objectType']

    listObject = ''
    if object_type == "Template":
        for object_id in objects_id:
            listObject = delete_template(object_id)

    elif object_type == "Type":
        for object_id in objects_id:
            listObject = delete_type(object_id)

    else:
        url = request.POST['url']
        bh_factory = BLOBHosterFactory(BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI)
        blob_hoster = bh_factory.createBLOBHoster()
        for object_id in objects_id:
            blob_hoster.delete(url+"/rest/blob?id="+object_id)
        messages.add_message(request, messages.INFO, 'File deleted with success.')
        print 'END def delete_object(request)'
        return HttpResponse(json.dumps({}), content_type='application/javascript')

    if listObject is not None and listObject != '':
        response_dict = {object_type: listObject}
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        messages.add_message(request, messages.INFO, object_type+' deleted with success.')

    print 'END def delete_object(request)'
    return HttpResponse(json.dumps({}), content_type='application/javascript')

################################################################################
#
# Function Name: dashboard_toXML(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Page that display XML
#
################################################################################
@login_required(login_url='/login')
def dashboard_toXML(request):
    xmlString = request.POST['xml']

    xsltPath = os.path.join(settings.SITE_ROOT, 'static', 'resources', 'xsl', 'xsd2html.xsl')
    xslt = etree.parse(xsltPath)
    transform = etree.XSLT(xslt)
    xmlTree = ""
    if (xmlString != ""):

        dom = etree.parse(BytesIO(xmlString.encode('utf-8')))
        annotations = dom.findall(".//{http://www.w3.org/2001/XMLSchema}annotation")
        for annotation in annotations:
            annotation.getparent().remove(annotation)
        newdom = transform(dom)
        xmlTree = str(newdom)

    response_dict = {'XMLHolder': xmlTree}
    return HttpResponse(json.dumps(response_dict), content_type='application/javascript')


################################################################################
#
# Function Name: delete_result(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Delete a list of XML document from the database
#
################################################################################
def delete_result(request):
    result_ids = request.POST.getlist('result_id[]')
    for result_id in result_ids:
        try:
            XMLdata.delete(result_id)
            messages.add_message(request, messages.INFO, 'Resource deleted with success.')
        except:
            # XML can't be found
            pass
    return HttpResponse(json.dumps({}), content_type='application/javascript')

################################################################################
#
# Function Name: update_publish(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Publish and update the publish date of an XMLdata
#
################################################################################
def update_publish(request):
    XMLdata.update_publish(request.GET['result_id'])
    resource = XMLdata.get(request.GET['result_id'])

    # Send mail to the user and the admin
    context = {'URI': MDCS_URI,
               'title': resource['title'],
               'publicationdate': resource['publicationdate'],
               'user': request.user.username}

    send_mail_to_managers(subject='Resource Published',
                                pathToTemplate='dashboard/email/resource_published.html',
                                context=context)
    return HttpResponse(json.dumps({}), content_type='application/javascript')

################################################################################
#
# Function Name: update_unpublish(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Unpublish an XMLdata
#
################################################################################
def update_unpublish(request):
    XMLdata.update_unpublish(request.GET['result_id'])
    return HttpResponse(json.dumps({}), content_type='application/javascript')

################################################################################
#
# Function Name: delete-forms(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Deletes a saved form
#
################################################################################
def delete_forms(request):
    formsID = request.POST.getlist('formsID[]')
    for formID in formsID:
        try:
            form_data = FormData.objects().get(pk=formID)
            # TODO: check if need to delete all SchemaElements
            if form_data.schema_element_root is not None:
                delete_branch_from_db(form_data.schema_element_root.pk)
            form_data.delete()
        except Exception, e:
            return HttpResponse(json.dumps({}), status=400)
    messages.add_message(request, messages.INFO, 'Form deleted with success.')
    return HttpResponse(json.dumps({}), content_type='application/javascript')

################################################################################
#
# Function Name: change_owner_forms(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Change the list of form's owner
#
################################################################################
def change_owner_forms(request):
    if 'formID[]' in request.POST and 'userID' in request.POST:
        form_data_ids = request.POST.getlist('formID[]')
        user_id = request.POST['userID']
        for form_data_id in form_data_ids:
            try:
                form_data = FormData.objects().get(pk=form_data_id)
                form_data.user = user_id
                form_data.save()
            except Exception, e:
                return HttpResponse(json.dumps({}),status=400)
        messages.add_message(request, messages.INFO, 'Form Owner changed with success !')
    return HttpResponse(json.dumps({}), content_type='application/javascript')
