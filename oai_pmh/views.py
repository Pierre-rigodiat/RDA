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
from mgi.models import Registry, Set as SetModel
from sickle.models import Set
from oai_pmh.api.serializers import SetSerializer

################################################################################
#
# Function Name: add_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Client add registry page
#
################################################################################

def add_registry(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = RegistryForm(request.POST)

            if form.is_valid():
                try:
                    errors = []
                    #We retrieve repository information
                    try:
                        uri= OAI_HOST_URI + "/oai_pmh/identify"
                        req = requests.post(uri, {"url":request.POST.get("url")}, auth=(OAI_USER, OAI_PASS))
                        if req.status_code == status.HTTP_200_OK:
                            infos = json.loads( req.text )
                            try:
                                name = infos['message']['repositoryName'][0]
                            except:
                                name = ''
                            try:
                                description = infos['message']['description'][0]
                            except:
                                description = ""
                        else:
                            return HttpResponseBadRequest('Impossible to retrieve information from the repository.')
                    except:
                        return HttpResponseBadRequest('Impossible to retrieve information from the repository.')

                    #We retrieve set information
                    try:
                        uri= OAI_HOST_URI + "/oai_pmh/listobjectsets"
                        req = requests.post(uri, {"url":request.POST.get("url")}, auth=(OAI_USER, OAI_PASS))
                        if req.status_code == status.HTTP_200_OK:
                            sets = req.text
                        else:
                            return HttpResponseBadRequest('Impossible to retrieve information from the repository.')
                    except:
                        return HttpResponseBadRequest('Impossible to retrieve information from the repository.')

                    #We retrieve metadata formats information
                    try:
                        uri= OAI_HOST_URI + "/oai_pmh/listobjectmetadataformats"
                        req = requests.post(uri, {"url":request.POST.get("url")}, auth=(OAI_USER, OAI_PASS))
                        if req.status_code == status.HTTP_200_OK:
                            metadataformats = req.text
                        else:
                            return HttpResponseBadRequest('Impossible to retrieve information from the repository.')
                    except:
                        return HttpResponseBadRequest('Impossible to retrieve information from the repository.')

                    #We add the registry
                    uri = OAI_HOST_URI + "/oai_pmh/add/registry"
                    try:
                        url = request.POST.get('url')
                    except ValueError:
                        return HttpResponseBadRequest('Please provide a URL.')

                    if 'harvestrate' in request.POST:
                        harvestrate = request.POST.get('harvestrate')
                    else:
                        harvestrate = ""
                    if 'harvest' in request.POST:
                        harvest = True
                    else:
                        harvest = False

                    identity = {}
                    try:
                        req = requests.post(uri, {"name":name,
                                                  "url":url,
                                                  "metadataformats":metadataformats,
                                                  "sets":sets,
                                                  "description":description,
                                                  "identity":identity,
                                                  "harvestrate":harvestrate,
                                                  "harvest":harvest},
                                            auth=(OAI_USER, OAI_PASS))
                        if req.status_code == status.HTTP_201_CREATED:
                            messages.add_message(request, messages.SUCCESS, 'Registry {0} added with success.'.format(name.encode('utf-8')))
                            return HttpResponse('CREATED')
                        elif req.status_code == status.HTTP_400_BAD_REQUEST:
                            return HttpResponseBadRequest('An error occurred while trying to save the repository. Please contact your administrator.')
                        elif req.status_code == status.HTTP_401_UNAUTHORIZED:
                            return HttpResponseBadRequest('You don\'t have enough rights to do this add. Please contact your administrator.')
                        elif req.status_code == status.HTTP_409_CONFLICT:
                            return HttpResponseBadRequest('Unable to add the registry. The registry already exists')
                        else:
                            return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
                    except Exception as e:
                        return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
                except Exception as e:
                    return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
            else:
                return HttpResponseBadRequest('Bad entries. Please verified your entry')
    else:
        return redirect('/login')


################################################################################
#
# Function Name: update_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH update one registry
#
# ################################################################################
def update_registry(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            try:
                uri = OAI_HOST_URI + "/oai_pmh/update/registry"
                try:
                    id = request.POST.get('id')
                except ValueError:
                    return HttpResponseBadRequest('Please provide an ID in order to edit the registry.')

                if 'harvestrate' in request.POST:
                    harvestrate = request.POST.get('harvestrate')
                else:
                    harvestrate = ''
                if 'edit_harvest' in request.POST:
                    harvest = True
                else:
                    harvest = False

                try:
                    req = requests.put(uri,
                                       {"id":id,
                                        "harvestrate":harvestrate,
                                        "harvest": harvest},
                                       auth=(OAI_USER, OAI_PASS))

                    if req.status_code == status.HTTP_201_CREATED:
                        messages.add_message(request, messages.INFO, 'Registry edited with success.')
                        return HttpResponse(json.dumps({}), content_type='application/javascript')
                    elif req.status_code == status.HTTP_400_BAD_REQUEST:
                        return HttpResponseBadRequest('An error occurred. Please contact your administrator..')
                    elif req.status_code == status.HTTP_401_UNAUTHORIZED:
                        return HttpResponseBadRequest('You don\'t have enough rights to do this edition. Please contact your administrator.')
                    elif req.status_code == status.HTTP_409_CONFLICT:
                        return HttpResponseBadRequest('Unable to update the registry. The registry already exists. Please enter an other name.')
                    else:
                        return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
                except Exception as e:
                    return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
            except Exception as e:
                return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
        elif request.method == 'GET':
            template = loader.get_template('admin/oai_pmh/form_registry_edit.html')
            registry_id = request.GET['registry_id']
            try:
                registry = Registry.objects.get(pk=registry_id)
                data = {'id': registry.id, 'name': registry.name,
                        'url': registry.url, 'harvestrate': registry.harvestrate,
                        'edit_harvest': registry.harvest}
                registry_form= UpdateRegistryForm(data)
            except:
                registry_form = UpdateRegistryForm()

            context = RequestContext(request, {
                'registry_form': registry_form,
            })

            return HttpResponse(json.dumps({'template': template.render(context)}), content_type='application/javascript')
    else:
        return redirect('/login')

################################################################################
#
# Function Name: delete_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Delete Registry
#
################################################################################
def delete_registry(request):
    if request.user.is_authenticated():
        uri = OAI_HOST_URI+"/oai_pmh/delete/registry"
        try:
            id = request.POST.get('RegistryId')
        except ValueError:
            return HttpResponseBadRequest('Please provide an ID in order to delete the registry.')
        try:
            req = requests.post(uri, {"RegistryId":id}, auth=(OAI_USER, OAI_PASS))

            if req.status_code == status.HTTP_200_OK:
                messages.add_message(request, messages.INFO, 'Registry deleted with success.')
                return HttpResponse(json.dumps({}), content_type='application/javascript')
            elif req.status_code == status.HTTP_401_UNAUTHORIZED:
                return HttpResponseBadRequest('You don\'t have enough rights to do this edition. Please contact your administrator.')
            elif req.status_code == status.HTTP_400_BAD_REQUEST:
                return HttpResponseBadRequest('An error occurred. Impossible to delete the registry. Please contact your administrator.')
            else:
                return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
        except Exception as e:
            return HttpResponseBadRequest('An error occurred. Please contact your administrator.')
    else:
        return redirect('/login')

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def add_record(request):
    if request.user.is_authenticated():
        try:
            response = TemplateResponse(request, 'oai_pmh/records/add_record.html', {})
            return response
        except Exception as e:
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})
    else:
        return redirect('/login')

def add_record_result(request):
    if request.user.is_authenticated():
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
    else:
        return redirect('/login')


################################################################################
#
# Function Name: update_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def update_record(request):
    if request.user.is_authenticated():
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
    else:
        return redirect('/login')


################################################################################
#
# Function Name: check_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Check if the Registry is available
#
################################################################################
def check_registry(request):
    if request.user.is_authenticated():
        try:
            form = Url(request.POST)
            if form.is_valid():
                uri= OAI_HOST_URI + "/oai_pmh/identify"
                req = requests.post(uri, {"url":request.POST.get("url")}, auth=(OAI_USER, OAI_PASS))
                isAvailable = str(req.status_code) == "200"
            else:
                isAvailable = False
        except:
            req= {}
            isAvailable = False

        return HttpResponse(json.dumps({'isAvailable' : isAvailable }), content_type='application/javascript')
    else:
        return redirect('/login')

################################################################################
#
# Function Name: getRecord(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def getRecord(request):
    if request.user.is_authenticated():

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
    else:
        return redirect('/login')

################################################################################
#
# Function Name: identify(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def identify(request):
    if request.user.is_authenticated():
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

    else:
        return redirect('/login')

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def listMetadataFormats(request):
    if request.user.is_authenticated():
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

    else:
        return redirect('/login')

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def listSets(request):
    if request.user.is_authenticated():
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

    else:
        return redirect('/login')

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def listIdentifiers(request):
    if request.user.is_authenticated():
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

    else:
        return redirect('/login')

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def listRecords(request):
    if request.user.is_authenticated():
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

    else:
        return redirect('/login')
