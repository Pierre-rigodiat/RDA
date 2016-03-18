################################################################################
#
# File Name: views.py
# Application: Informatics Core
# Description:
#
# Author: Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

# Responses
from rest_framework import status
from django.http.response import HttpResponseBadRequest
# Requests
import requests
from oai_pmh.forms import UpdateRegistryForm
import json
from mgi.settings import OAI_HOST_URI, OAI_USER, OAI_PASS
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
# Responses
from django.http import HttpResponse
# Requests
from oai_pmh.forms import RegistryForm, MyRegistryForm
from django.template import RequestContext, loader
from mgi.models import OaiRegistry, OaiSettings
from django.contrib.admin.views.decorators import staff_member_required
from mgi.models import Message, OaiMetadataFormat, OaiSet, OaiRecord
from oai_pmh.forms import Url
from django.utils.dateformat import DateFormat

################################################################################
#
# Function Name: check_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Check if the Registry is available
#
################################################################################
@login_required(login_url='/login')
def check_registry(request):
    try:
        form = Url(request.POST)
        if form.is_valid():
            #Call the identify function from the API.
            uri= OAI_HOST_URI + "/oai_pmh/api/identify"
            req = requests.post(uri, {"url":request.POST.get("url")}, auth=(OAI_USER, OAI_PASS))
            #IF the return status is HTTP_200_OK, the registry is available
            isAvailable = req.status_code == status.HTTP_200_OK
        else:
            isAvailable = False
    except:
        isAvailable = False
    return HttpResponse(json.dumps({'isAvailable' : isAvailable }), content_type='application/javascript')


################################################################################
#
# Function Name: add_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Client add registry page
#
################################################################################

@login_required(login_url='/login')
def add_registry(request):
    if request.method == 'POST':
        form = RegistryForm(request.POST)

        if form.is_valid():
            try:
                #We add the registry
                uri = OAI_HOST_URI + "/oai_pmh/api/add/registry"
                try:
                    url = request.POST.get('url')
                except ValueError:
                    return HttpResponseBadRequest('Please provide a URL.')

                #We retrieve information from the form
                if 'harvestrate' in request.POST:
                    harvestrate = request.POST.get('harvestrate')
                else:
                    harvestrate = ""
                if 'harvest' in request.POST:
                    harvest = True
                else:
                    harvest = False

                #Call to the API to add the registry
                try:
                    req = requests.post(uri, {"url":url,
                                              "harvestrate":harvestrate,
                                              "harvest":harvest},
                                        auth=(OAI_USER, OAI_PASS))
                    #If the status is OK, sucess message
                    if req.status_code == status.HTTP_201_CREATED:
                        messages.add_message(request, messages.SUCCESS, 'Data provider added with success.')
                        return HttpResponse('CREATED')
                    #Else, we return a bad request response with the message provided by the API
                    else:
                        data = json.loads(req.text)
                        return HttpResponseBadRequest(data['message'])
                except Exception as e:
                    return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
            except Exception as e:
                return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
        else:
            return HttpResponseBadRequest('Bad entries. Please enter a valid URL and a positive integer')


################################################################################
#
# Function Name: update_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH update one registry
#
# ################################################################################
@login_required(login_url='/login')
def update_registry(request):
    if request.method == 'POST':
        #UPDATE the registry
        try:
            uri = OAI_HOST_URI + "/oai_pmh/api/update/registry"
            #Get the ID
            if 'id' in request.POST:
                id = request.POST.get('id')
            else:
                return HttpResponseBadRequest('Please provide an ID in order to edit the data provider.')
            #Get all form information
            if 'harvestrate' in request.POST:
                harvestrate = request.POST.get('harvestrate')
            else:
                harvestrate = ''
            if 'edit_harvest' in request.POST:
                harvest = True
            else:
                harvest = False
            #Call the API to update the registry
            try:
                req = requests.put(uri,
                                   {"id":id,
                                    "harvestrate":harvestrate,
                                    "harvest": harvest},
                                   auth=(OAI_USER, OAI_PASS))
                #If the status is OK, sucess message
                if req.status_code == status.HTTP_201_CREATED:
                    messages.add_message(request, messages.INFO, 'Data Provider successfully edited.')
                    return HttpResponse(json.dumps({}), content_type='application/javascript')
                #Else, we return a bad request response with the message provided by the API
                else:
                    data = json.loads(req.text)
                    return HttpResponseBadRequest(data['message'])
            except Exception as e:
                return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
        except Exception as e:
            return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
    elif request.method == 'GET':
        #Build the template to render for the registry edition
        template = loader.get_template('oai_pmh/admin/form_registry_edit.html')
        registry_id = request.GET['registry_id']
        try:
            registry = OaiRegistry.objects.get(pk=registry_id)
            data = {'id': registry.id, 'harvestrate': registry.harvestrate,
                    'edit_harvest': registry.harvest}
            registry_form= UpdateRegistryForm(data)
        except:
            registry_form = UpdateRegistryForm()

        context = RequestContext(request, {
            'registry_form': registry_form,
        })

        return HttpResponse(json.dumps({'template': template.render(context)}), content_type='application/javascript')

################################################################################
#
# Function Name: delete_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Delete Registry
#
################################################################################
@login_required(login_url='/login')
def delete_registry(request):
    uri = OAI_HOST_URI+"/oai_pmh/api/delete/registry"
    try:
        id = request.POST.get('RegistryId')
    except ValueError:
        return HttpResponseBadRequest('Please provide an ID in order to delete the data provider.')
    try:
        req = requests.post(uri, {"RegistryId":id}, auth=(OAI_USER, OAI_PASS))

        #If the status is OK, sucess message
        if req.status_code == status.HTTP_200_OK:
            messages.add_message(request, messages.INFO, 'Data provider deleted with success.')
            return HttpResponse(json.dumps({}), content_type='application/javascript')
        #Else, we return a bad request response with the message provided by the API
        else:
            data = json.loads(req.text)
            return HttpResponseBadRequest(data['message'])
    except Exception as e:
        return HttpResponseBadRequest('An error occurred. Please contact your administrator.')


################################################################################
#
# Function Name: oai_pmh(request)
# Inputs:        request -
# Outputs:       OAI-PMH Page
# Exceptions:    None
# Description:   Page that allows to manage OAI-PMH
#
################################################################################
@staff_member_required
def oai_pmh(request):
    template = loader.get_template('oai_pmh/admin/oai_pmh.html')

    registry_form = RegistryForm();
    registries = OaiRegistry.objects.all()
    context = RequestContext(request, {
        'contacts': Message.objects,
        'registry_form': registry_form,
        'registries': registries,
    })

    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: oai_pmh(request)
# Inputs:        request -
# Outputs:       OAI-PMH Page
# Exceptions:    None
# Description:   Page that allows to manage OAI-PMH
#
################################################################################
@staff_member_required
def oai_pmh_my_infos(request):
    template = loader.get_template('oai_pmh/admin/oai_pmh_my_infos.html')
    information = OaiSettings.objects.get()
    if information:
        name = information.repositoryName
        repoIdentifier = information.repositoryIdentifier
        enableHarvesting = information.enableHarvesting
    else:
        name = settings.OAI_NAME
        repoIdentifier = settings.OAI_REPO_IDENTIFIER
        enableHarvesting = False

    data_provider = {
            'name': name,
            'baseURL': settings.OAI_HOST_URI +"/oai_pmh/server/",
            'protocole_version': settings.OAI_PROTOCOLE_VERSION,
            'admins': (email for name, email in settings.OAI_ADMINS),
            # 'earliest_date': self.getEarliestDate(),   # placeholder
            'deleted': settings.OAI_DELETED_RECORD,  # no, transient, persistent
            'granularity': settings.OAI_GRANULARITY,  # or YYYY-MM-DD
            'identifier_scheme': settings.OAI_SCHEME,
            'repository_identifier': repoIdentifier,
            'identifier_delimiter': settings.OAI_DELIMITER,
            'sample_identifier': settings.OAI_SAMPLE_IDENTIFIER,
            'enable_harvesting': enableHarvesting,
        }

    context = RequestContext(request, {
        'data_provider': data_provider,
    })

    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: oai_pmh(request)
# Inputs:        request -
# Outputs:       OAI-PMH Page
# Exceptions:    None
# Description:   Page that allows to manage OAI-PMH
#
################################################################################
@staff_member_required
def oai_pmh_detail_registry(request):
    result_id = request.GET['id']
    template = loader.get_template('oai_pmh/admin/oai_pmh_detail_registry.html')
    context = RequestContext(request, {
        'registry': OaiRegistry.objects.get(pk=result_id),
        'metadataformats': OaiMetadataFormat.objects(registry=result_id),
        'sets': OaiSet.objects(registry=result_id),
        'nbRecords': OaiRecord.objects(registry=result_id).count(),
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: update_my_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH update my registry
#
# ################################################################################
@login_required(login_url='/login')
def update_my_registry(request):
    if request.method == 'POST':
        #UPDATE the registry
        try:
            uri = OAI_HOST_URI + "/oai_pmh/api/update/my-registry"
            #Get all form information
            if 'name' in request.POST:
                name = request.POST.get('name')
            else:
                name = ''
            if 'enable_harvesting' in request.POST:
                enable_harvesting = True
            else:
                enable_harvesting = False
            #Call the API to update the registry
            try:
                req = requests.put(uri,
                                   {"repositoryName": name,
                                    # "repositoryIdentifier": repo_identifier,
                                    "enableHarvesting": enable_harvesting},
                                   auth=(OAI_USER, OAI_PASS))
                #If the status is OK, sucess message
                if req.status_code == status.HTTP_201_CREATED:
                    messages.add_message(request, messages.INFO, 'Data provider edited with success.')
                    return HttpResponse(json.dumps({}), content_type='application/javascript')
                #Else, we return a bad request response with the message provided by the API
                else:
                    data = json.loads(req.text)
                    return HttpResponseBadRequest(data['message'])
            except Exception as e:
                return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
        except Exception as e:
            return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
    elif request.method == 'GET':
        #Build the template to render for the registry edition
        template = loader.get_template('oai_pmh/admin/form_my_registry_edit.html')
        try:
            information = OaiSettings.objects.get()
            data = {'name': information.repositoryName, 'repo_identifier': information.repositoryIdentifier,
                    'enable_harvesting': information.enableHarvesting}
            registry_form= MyRegistryForm(data)
        except:
            registry_form = MyRegistryForm()

        context = RequestContext(request, {
            'registry_form': registry_form,
        })

        return HttpResponse(json.dumps({'template': template.render(context)}), content_type='application/javascript')


################################################################################
#
# Function Name: update_my_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH update my registry
#
# ################################################################################
@login_required(login_url='/login')
def update_all_records(request):
    if request.method == 'POST':
        try:
            #Get the ID
            registry_id = request.POST['registry_id']
            uri = OAI_HOST_URI + "/oai_pmh/api/update/all/records"

            #Call the API to update all records for this registry
            try:
                req = requests.post(uri,
                                   {"registry_id": registry_id},
                                   auth=(OAI_USER, OAI_PASS))
                #If the status is OK, sucess message
                # if req.status_code == status.HTTP_201_CREATED:
                #     messages.add_message(request, messages.INFO, 'Data provider edited with success.')
                #     return HttpResponse(json.dumps({}), content_type='application/javascript')
                # #Else, we return a bad request response with the message provided by the API
                # else:
                #     data = json.loads(req.text)
                #     return HttpResponseBadRequest(data['message'])
                return HttpResponse(json.dumps({}), content_type='application/javascript')
            except Exception as e:
                return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
        except Exception as e:
            return HttpResponseBadRequest('An error occurred. Please contact your administrator.')

################################################################################
#
# Function Name: check_harvest_data(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Return the state of the registries (isHarvesting)
#
# ################################################################################
@login_required(login_url='/login')
def check_harvest_data(request):
    if request.method == 'POST':
        try:
            resultsByKeyword = []
            #Get all registries
            registries = OaiRegistry.objects.only('id', 'isHarvesting', 'lastUpdate').all()
            #Build array with registry id and isHarvesting value
            for registry in registries:
                result_json = {}
                result_json['registry_id'] = str(registry.id)
                result_json['isHarvesting'] = registry.isHarvesting
                if registry.lastUpdate:
                    df =  DateFormat(registry.lastUpdate)
                    lastUpdate = df.format('F j, Y, g:i a')
                else:
                    lastUpdate = ''
                result_json['lastUpdate'] = lastUpdate
                resultsByKeyword.append(result_json)

            return HttpResponse(json.dumps(resultsByKeyword), content_type='application/javascript')
        except Exception as e:
            return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
