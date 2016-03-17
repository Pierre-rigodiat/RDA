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
from mgi.models import Template, FormData, XMLdata, Type
from django.contrib import messages
import lxml.etree as etree
from io import BytesIO
import os
import json


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
        testFilenameObjects = Template.objects(filename=new_filename)
        testNameObjects = Template.objects(title=new_name)
    else:
        object = Type.objects.get(pk=object_id)
        testFilenameObjects = Type.objects(filename=new_filename)
        testNameObjects = Type.objects(title=new_name)

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

    object.title = new_name
    object.filename = new_filename
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
    object_id = request.POST['objectID']
    object_type = request.POST['objectType']

    listObject = ''
    if object_type == "Template":
        object = Template.objects.get(pk=object_id)
        dependenciesData = XMLdata.find({'schema' : str(object_id)})
        dependenciesForm = list(FormData.objects(template=object_id))
        if len(dependenciesData) >= 1:
            for temp in dependenciesData:
                listObject += temp['title'] + ', '
        if len(dependenciesForm):
            for temp in dependenciesForm:
                listObject += temp.name + ', '

    elif object_type == "Type":
        object = Type.objects.get(pk=object_id)
        dependenciesTemplate = list(Template.objects(dependencies=object_id))
        dependenciesType = list(Type.objects(dependencies=object_id))
        if len(dependenciesType) >= 1:
            for temp in dependenciesType:
                listObject += temp.title + ', '
        if len(dependenciesTemplate) >= 1:
            for temp in dependenciesTemplate:
                listObject += temp.title + ', '

    else:
        url = request.POST['url']
        bh_factory = BLOBHosterFactory(BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI)
        blob_hoster = bh_factory.createBLOBHoster()
        blob_hoster.delete(url+"/rest/blob?id="+object_id)
        messages.add_message(request, messages.INFO, 'File deleted with success.')
        print 'END def delete_object(request)'
        return HttpResponse(json.dumps({}), content_type='application/javascript')

    if listObject != '':
        response_dict = {object_type: listObject[:-2]}
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    else:
        messages.add_message(request, messages.INFO, object_type+' deleted with success.')
        object.delete()

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