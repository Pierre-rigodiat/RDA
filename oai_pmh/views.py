################################################################################
#
# File Name: html_views.py
# Application: Informatics Core
# Description:
#
# Author: Marcus Newrock
#         marcus.newrock@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

# Responses
from rest_framework import status
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.shortcuts import redirect
# Requests
import requests
from oai_pmh.forms import UpdateRegistryForm, RegistryForm, AddRecord, GetRecord, Url, IdentifierForm, ListRecordForm
import json
import xmltodict
from mgi.settings import OAI_HOST_URI, OAI_USER, OAI_PASS
from django.contrib import messages
from django.template import RequestContext, loader
from mgi.models import Registry
from django.contrib.auth.decorators import login_required

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
                uri = OAI_HOST_URI + "/oai_pmh/add/registry"
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
            return HttpResponseBadRequest('Bad entries. Please verified your entry')


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
            uri = OAI_HOST_URI + "/oai_pmh/update/registry"
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
        template = loader.get_template('admin/oai_pmh/form_registry_edit.html')
        registry_id = request.GET['registry_id']
        try:
            registry = Registry.objects.get(pk=registry_id)
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
    uri = OAI_HOST_URI+"/oai_pmh/delete/registry"
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
            uri= OAI_HOST_URI + "/oai_pmh/identify"
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
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
@login_required(login_url='/login')
def add_record(request):
    try:
        response = TemplateResponse(request, 'oai_pmh/records/add_record.html', {})
        return response
    except Exception as e:
        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

@login_required(login_url='/login')
def add_record_result(request):
    if request.method == 'POST':
        form = AddRecord(request.POST)

        if form.is_valid():

            try:
                errors = []
                uri=OAI_HOST_URI+"/oai_pmh/add/record"
                try:
                    content = request.POST.get('content')
                except ValueError:
                    errors.append("Invalid Name")

                try:
                    req = requests.post(uri, {"content":content}, auth=(OAI_USER, OAI_PASS))
                    if str(req.status_code) == "201":
                        return TemplateResponse(request, 'add_record_result.html', {})
                    if str(req.status_code) == "400":
                        return TemplateResponse(request, 'existing_record.html', {"form":form, "record":req.text})
                    if str(req.status_code) == "401":
                        return TemplateResponse(request, 'permission_denied.html', {})
                    else:
                        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
                except Exception as e:
                    return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
            except Exception as e:
                print 'exception reading ',e
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})
        else:
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
    return render(request, 'added_registry.html', {"previouspage":"client/add/record"})


################################################################################
#
# Function Name: update_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
@login_required(login_url='/login')
def update_record(request):
    try:
        uri=OAI_HOST_URI+"/oai_pmh/update/record"
        errors = []
        try:
            identifier = request.POST.get('identifier')
        except ValueError:
            errors.append("Invalid identifier.")
        if len(errors):
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%str(errors)})
        try:
            content = request.POST.get('content')
        except ValueError:
            errors.append("Invalid identifier.")
        if len(errors):
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%str(errors)})

        try:
            req = requests.put(uri, {"identifier":identifier, "content":content}, auth=(OAI_USER, OAI_PASS))

            if str(req.status_code) == '201':
                return render(request, 'oai_pmh/records/update_record_result.html', {"record":req.text})
            if str(req.status_code) == '401':
                return TemplateResponse(request, 'permission_denied.html', {})
            if str(req.status_code) == '400':
                return render(request, 'error.html', {"message":req.text, "previouspage":"/update/record/select"})
        except Exception as e:
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
    except Exception as e:
        print 'exception reading ',e
        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

    return render(request, 'error.html', {})


################################################################################
#
# Function Name: getRecord(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
@login_required(login_url='/login')
def getRecord(request):
    try:
        form = GetRecord(request.POST)
        if form.is_valid():
            uri=OAI_HOST_URI+"/oai_pmh/getRecord"
            req = requests.post(uri, {"url":request.POST.get("url"), "identifier":request.POST.get("identifier"),
                                      "metadataprefix":request.POST.get("metadataprefix")}, auth=(OAI_USER, OAI_PASS))

            if str(req.status_code) == "200":
                response = xmltodict.parse( json.loads(req.text) )
                # pretty_print = pprint.PrettyPrinter(indent=4)
                # p_req = pretty_print.pformat(response)
                # pprint.pprint( p_req )
                return render(request, 'oai_pmh/client/getrecord.html', {"response":response, "code":"200"})
            if str(req.status_code) == "400":
                response = json.loads(req.text)['message']
                return render(request, 'error.html', {"response":response})
            if str(req.status_code) == "500":
                response = json.loads(req.text)['message']
                return render(request, 'error.html', {"response":response})

        return render(request, 'oai_pmh/client/getrecord.html', {})
    except:
        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
    return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})

################################################################################
#
# Function Name: identify(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
@login_required(login_url='/login')
def identify(request):
    try:
        form = Url(request.POST)
        if form.is_valid():

            uri=OAI_HOST_URI+"/oai_pmh/identify"
            req = requests.post(uri, {"url":request.POST.get("url")}, auth=(OAI_USER, OAI_PASS))
            if str(req.status_code) == "200":
                return render(request, 'oai_pmh/client/identify.html', {"response":req.text, "code":"200"})
        else:
            return render(request, 'oai_pmh/client/identify.html', {"response":"invalid"})

        return render(request, 'oai_pmh/client/identify.html', {"response":""})
    except:
        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
@login_required(login_url='/login')
def listMetadataFormats(request):
    try:
        form = Url(request.POST)
        if form.is_valid():
            uri= OAI_HOST_URI + "/oai_pmh/listmetadataformats"
            req = requests.post(uri, {"url":request.POST.get("url")}, auth=(OAI_USER, OAI_PASS))
            if str(req.status_code) == "200":
                return render(request, 'oai_pmh/client/listmetadataformats.html', {"response":req.text, "code":"200"})
            else:
                print render(request, 'error.html', {})
        else:
            return render(request, 'oai_pmh/client/listmetadataformats.html', {"response":"invalid"})

        return render(request, 'oai_pmh/client/listmetadataformats.html', {"response":""})
    except:
        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
@login_required(login_url='/login')
def listSets(request):
    try:
        form = Url(request.POST)
        if form.is_valid():
            uri=OAI_HOST_URI+"/oai_pmh/listSets"
            req = requests.post(uri, {"url":request.POST.get("url")}, auth=(OAI_USER, OAI_PASS))
            if str(req.status_code) == "200":
                return render(request, 'oai_pmh/client/listsets.html', {"response":req.text, "code":"200"})
            if str(req.status_code) == "400":
                print req.text
        else:
            return render(request, 'oai_pmh/client/listsets.html', {"response":"invalid"})
        return render(request, 'oai_pmh/client/listsets.html', {"response":""})
    except:
        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
@login_required(login_url='/login')
def listIdentifiers(request):
    try:
        form = IdentifierForm(request.POST)
        if form.is_valid():
            uri=OAI_HOST_URI+"/oai_pmh/listIdentifiers"
            req = requests.post(uri, {"url":request.POST.get("url"), "set":request.POST.get("set"),
                                      "metadataprefix":request.POST.get("metadataprefix")}, auth=(OAI_USER, OAI_PASS))
            print request.POST.get("url")
            print request.POST.get("set")
            print request.POST.get("metadataprefix")
            print req.status_code
            if str(req.status_code) == "200":
                return render(request, 'oai_pmh/client/listidentifiers.html', {"response":req.text, "code":"200"})
        else:
            return render(request, 'oai_pmh/client/listidentifiers.html', {"response":"invalid"})

        return render(request, 'oai_pmh/client/listidentifiers.html', {"response":""})
    except:
        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
@login_required(login_url='/login')
def listRecords(request):
    try:
        form = ListRecordForm(request.POST)
        if form.is_valid():
            uri=OAI_HOST_URI+"/oai_pmh/listIdentifiers"
            req = requests.post(uri, {"url":request.POST.get("url"),
                                      "set":request.POST.get("set"),
                                      "metadataprefix":request.POST.get("metadataprefix"),
                                      "resumptionToken":request.POST.get("resumptionToken"),
                                      "fromDate":request.POST.get("fromDate"),
                                      "untilDate":request.POST.get("untilDate"),
                                      }, auth=(OAI_USER, OAI_PASS))
            print request.POST.get("url")
            print request.POST.get("set")
            print request.POST.get("metadataprefix")
            print req.status_code
            if str(req.status_code) == "200":
                return render(request, 'oai_pmh/client/listrecords.html', {"response":req.text, "code":"200"})
        else:
            return render(request, 'oai_pmh/client/listrecords.html', {"response":"invalid"})

        return render(request, 'oai_pmh/client/listrecords.html', {"response":""})
    except:
        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})

