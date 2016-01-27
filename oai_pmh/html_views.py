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
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.shortcuts import redirect
# Requests
import requests
from oai_pmh.forms import Registry, AddRecord, GetRecord, Url, IdentifierForm, ListRecordForm
import json
import xmltodict
from mgi.settings import OAI_HOST_URI, OAI_USER, OAI_PASS


################################################################################
#
# Function Name: added_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Client added registry page
#
################################################################################

def added_registry(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = Registry(request.POST)

            if form.is_valid():

                try:
                    errors = []
                    uri=OAI_HOST_URI+"/oai_pmh/add/registry"
                    try:
                        name = request.POST.get('name')
                    except ValueError:
                        errors.append("Invalid Name")
                    try:
                        url = request.POST.get('url')
                    except ValueError:
                        errors.append("Invalid URL")
                    if 'harvestrate' in request.POST:
                        harvestrate = request.POST.get('harvestrate')
                    else:
                        harvestrate = ""
                    if 'metadataprefix' in request.POST:
                        metadataprefix = request.POST.get('metadataprefix')
                    else:
                        metadataprefix = ""
                    if 'identity' in request.POST:
                        identity = request.POST.get('identity')
                    else:
                        identity = {}
                    if 'sets' in request.POST:
                        sets = request.POST.get('sets')
                    else:
                        sets = {}
                    if 'description' in request.POST:
                        description = request.POST.get('description')
                    else:
                        description = ""
                    if len(errors) > 0:
                        print len(errors),' errors'

                    try:
                        req = requests.post(uri, {"name":name,
                                                  "url":url,
                                                  "metadataprefix":metadataprefix,
                                                  "sets":sets,
                                                  "description":description,
                                                  "identity":identity,
                                                  "harvestrate":harvestrate},
                                            auth=(OAI_USER, OAI_PASS))
                        if str(req.status_code) == "201":
                            return TemplateResponse(request, 'added_registry.html', {})
                        if str(req.status_code) == "400":
                            return TemplateResponse(request, 'existing_registry.html', {"form":form, "response":req.text})
                        if str(req.status_code) == "401":
                            return TemplateResponse(request, 'permission_denied.html', {"form":req.text})
                        else:
                            return HttpResponse(req.status_code)
                    except Exception as e:
                        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})
                except Exception as e:
                    print 'exception reading ',e
                    return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})
            else:
                print form.errors
        return render(request, 'added_registry.html', {})
    else:
        return redirect('/login')

################################################################################
#
# Function Name: addregistry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def addregistry(request):
    """
    GET GET http://localhost/client/add/registry
    """

    if request.user.is_authenticated():
        try:
            response = TemplateResponse(request, 'add_registry.html', {})
            return response
        except:
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
    else:
        return redirect('/login')

################################################################################
#
# Function Name: selectallregistries(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH client select all registries
#
################################################################################
def selectallregistries(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/select/all/registries"

            try:
                req = requests.get(uri, auth=(OAI_USER, OAI_PASS))
                response = json.loads(req.text)
                if str(req.status_code) == '200':
                    return render(request, 'select_registry.html', {"registries":response})
                if str(req.status_code) == '401':
                    return TemplateResponse(request, 'permission_denied.html', {})
            except Exception as e:
                return 'e ',e.message
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

        return render(request, 'added_registry.html', {})
    else:
        return redirect('/login')

################################################################################
#
# Function Name: select_registry(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH client select registries
#
################################################################################
def select_registry(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/select/registry"
            errors = []
            try:
                name = request.POST.get('Registry')
            except ValueError:
                errors.append("Invalid Name")
            if len(errors):
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%str(errors)})
            try:
                req = requests.get(uri+"?name="+name, auth=(OAI_USER, OAI_PASS))

                response = json.loads(req.text)
                if str(req.status_code) == '200':
                    return render(request, 'view_registry.html', {"registry":response})
                if str(req.status_code) == '401':
                    return TemplateResponse(request, 'permission_denied.html', {})
            except Exception as e:
                return 'e ',e.message
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

        return render(request, 'added_registry.html', {})
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
################################################################################
def update_registry(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/select/all/registries"

            try:
                req = requests.get(uri, auth=(OAI_USER, OAI_PASS))
                response = json.loads(req.text)

                if str(req.status_code) == '200':
                    return render(request, 'update_registry.html', {"registries":response})
                if str(req.status_code) == '401':
                    return TemplateResponse(request, 'permission_denied.html', {})
            except Exception as e:
                return 'e ',e.message
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

        return render(request, 'added_registry.html', {})
    else:
        return render(request, 'login.html')

################################################################################
#
# Function Name: update_registry_select(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH returns page for selecting one registry
#
################################################################################
def update_registry_select(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/select/registry"
            errors = []
            try:
                name = request.POST.get('Registry')
            except ValueError:
                errors.append("Invalid Name")
            if len(errors):
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%str(errors)})

            try:
                req = requests.get(uri+"?name=%s"%name, auth=(OAI_USER, OAI_PASS))
                response = json.loads(req.text)
                if str(req.status_code) == '200':
                    identifier = name
                    response.update({"identifier":identifier})
                    return render(request, 'update_registry_select.html', {"registry":response})
                if str(req.status_code) == '401':
                    return TemplateResponse(request, 'permission_denied.html', {})
            except Exception as e:
                return 'e ',e.message
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

        return render(request, 'added_registry.html', {})
    else:
        return render(request, 'login.html')

def update_registry_result(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/update/registry"
            errors = []
            try:
                name = request.POST.get('name')
            except ValueError:
                errors.append("Invalid Name.")
            try:
                url = request.POST.get('url')
            except ValueError:
                errors.append("Invalid URL.")
            try:
                identifier = request.POST.get('identifier')
            except ValueError:
                errors.append("Invalid identifier.")

            harvestrate = request.POST.get('harvestrate')
            metadataprefix = request.POST.get('metadataprefix')

            if request.POST.get('sets') == "":
                sets = {}
            else:
                try:
                    sets = json.loads( request.POST.get('sets'))
                except Exception as e:
                    return TemplateResponse(request, e.message, '')

            if request.POST.get('identity') == "":
                identity = {}
            else:
                try:
                    identity = json.loads( request.POST.get('identity'))
                except Exception as e:
                    return TemplateResponse(request, e.message, '')

            description = request.POST.get('description')

            if len(errors):
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%str(errors)})

            try:
                req = requests.put(uri, {"identifier":identifier, "name":name, "url":url, "harvestrate":harvestrate, "metadataprefix":metadataprefix,
                                          "identity":identity, "sets":sets, "description":description}, auth=(OAI_USER, OAI_PASS))

                if str(req.status_code) == '201':
                    try:
                        uri=OAI_HOST_URI+"/oai_pmh/select/registry"
                        req = requests.get(uri+"?name="+name, auth=(OAI_USER, OAI_PASS))

                        response = json.loads(req.text)
                        if str(req.status_code) == '200':
                            return render(request, 'update_registry_result.html', {"registry":response})
                        if str(req.status_code) == '401':
                            return TemplateResponse(request, 'permission_denied.html', {})

                    except Exception as e:
                        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})
                if str(req.status_code) == '401':
                    return TemplateResponse(request, 'permission_denied.html', {})
            except Exception as e:
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})

def delete_registry(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/select/all/registries"

            try:
                req = requests.get(uri, auth=(OAI_USER, OAI_PASS))
                response = json.loads(req.text)
                if str(req.status_code) == '200':
                    return render(request, 'delete_registry.html', {"registries":response})
                if str(req.status_code) == '401':
                    return TemplateResponse(request, 'permission_denied.html', {})
            except Exception as e:
                return 'e ',e.message
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})

def delete_registry_select(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/select/registry"
            errors = []
            try:
                name = request.POST.get('Registry')
            except ValueError:
                errors.append("Invalid Name")
            if len(errors):
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%str(errors)})

            try:
                req = requests.get(uri+"?name="+name, auth=(OAI_USER, OAI_PASS))
                response = json.loads(req.text)

                if str(req.status_code) == '200':
                    return render(request, 'delete_registry_select.html', {"registry":response})
                if str(req.status_code) == '401':
                    return TemplateResponse(request, 'permission_denied.html', {})
            except Exception as e:
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. %s."%e.message})

        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
    else:
        return redirect('/login')

def delete_registry_result(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/delete/registry"
            errors = []
            try:
                name = request.POST.get('identifier')
            except ValueError:
                errors.append("Invalid Name")
            if len(errors):
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%str(errors)})

            try:
                req = requests.post(uri, {"name":name}, auth=(OAI_USER, OAI_PASS))

                if str(req.status_code) == '204':
                    return render(request, 'delete_registry_result.html', {"registry":{"name":name}})
                if str(req.status_code) == '401':
                    return render(request, 'permission_denied.html', {})
                if str(req.status_code) == '400':
                    print req.text
                    return render(request, 'error.html', {})
            except Exception as e:
                return 'e ',e.message
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

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
# Function Name: view_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def view_record(request):
    if request.user.is_authenticated():
        try:
            return render(request, 'oai_pmh/records/view_record.html', {})
        except Exception as e:
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})
    else:
        return redirect('/login')

################################################################################
#
# Function Name: view_record_result(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def view_record_result(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/select/record"
            errors = []
            try:
                identifier = request.POST.get('identifier')
            except ValueError:
                errors.append("Invalid identifier")
            if len(errors):
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%str(errors)})
            try:
                req = requests.post(uri, {"identifier":identifier}, auth=(OAI_USER, OAI_PASS))
                response = json.loads(req.text)
                # response = parseString( dicttoxml.dicttoxml( json.loads(req.text) ) ).toprettyxml()
                print response
                if str(req.status_code) == '200':
                    return render(request, 'oai_pmh/records/view_record_result.html', {"record":response})
                if str(req.status_code) == '401':
                    return TemplateResponse(request, 'permission_denied.html', {})
            except Exception as e:
                return 'e ',e.message
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

        return render(request, 'error.html', {"previouspage":"/client/view/record"})
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
            return render(request, 'oai_pmh/records/update_record.html', {})
        except:
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
    else:
        return redirect('/login')

################################################################################
#
# Function Name: update_record_select(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def update_record_select(request):
    if request.user.is_authenticated():
        try:
            uri=OAI_HOST_URI+"/oai_pmh/select/record"
            errors = []
            try:
                identifier = request.POST.get('identifier')
            except ValueError:
                errors.append("Invalid identifier.")
            if len(errors):
                return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%str(errors)})

            try:
                req = requests.post(uri, {"identifier":identifier}, auth=(OAI_USER, OAI_PASS))
                # pretty_print = pprint.PrettyPrinter(indent=4)
                # p_req = pretty_print.pformat(req.text)

                if str(req.status_code) == '200':
                    return render(request, 'oai_pmh/records/update_record_select.html', {"record":req.text, "identifier":identifier} )
                if str(req.status_code) == '401':
                    return TemplateResponse(request, 'permission_denied.html', {})
            except Exception as e:
                return 'e ',e.message
        except Exception as e:
            print 'exception reading ',e
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator. %s"%e.message})

        return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
    else:
        return redirect('/login')

################################################################################
#
# Function Name: update_record_select(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def update_record_result(request):
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
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   OAI-PMH Add Registry
#
################################################################################
def delete_record(request):
    if request.user.is_authenticated():
        try:
            return render(request, 'oai_pmh/records/delete_record.html', {})
        except:
            return render(request, 'error.html', {"response":"An error occurred. Please contact your administrator."})
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
# Function Name: add_record(request)
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
                uri=OAI_HOST_URI+"/oai_pmh/listmetadataformats"
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
                req = requests.post(uri, {"url":request.POST.get("url"), "setH":request.POST.get("set"),
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
                                          "setH":request.POST.get("set"),
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
