################################################################################
#
# File Name: views.py
# Application: admin_mdcs
# Purpose:   
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

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import redirect
from datetime import date
from mgi.models import Request, Message, PrivacyPolicy, TermsOfUse, Template, TemplateVersion, Type, TypeVersion, \
    Module, Bucket, Instance
from forms import PrivacyPolicyForm, TermsOfUseForm, RepositoryForm, RefreshRepositoryForm
from django.contrib import messages
import os
from django.conf import settings
import requests
from datetime import datetime
from datetime import timedelta
from bson.objectid import ObjectId
from dateutil import tz
from collections import OrderedDict
import lxml.etree as etree
from io import BytesIO
from mgi import common


################################################################################
#
# Function Name: user_requests(request)
# Inputs:        request -
# Outputs:       User Request Page
# Exceptions:    None
# Description:   Page that allows to accept or deny user requests
#
################################################################################
def user_requests(request):
    template = loader.get_template('admin/user_requests.html')

    context = RequestContext(request, {
        'requests': Request.objects
    })
    
    if request.user.is_authenticated() and request.user.is_staff:
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: contact_messages(request)
# Inputs:        request -
# Outputs:       User Request Page
# Exceptions:    None
# Description:   Page that allows to read messages from the contact page
#
################################################################################
def contact_messages(request):
    template = loader.get_template('admin/contact_messages.html')

    context = RequestContext(request, {
        'contacts': Message.objects
    })
    
    if request.user.is_authenticated() and request.user.is_staff:
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: website(request)
# Inputs:        request -
# Outputs:       User Request Page
# Exceptions:    None
# Description:   Page that allows to edit website pages
#
################################################################################
def website(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/website.html')

        context = RequestContext(request, {
        })

        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: privacy_policy_admin(request)
# Inputs:        request -
# Outputs:       User Request Page
# Exceptions:    None
# Description:   Page that allows to edit Privacy Policy
#
################################################################################
def privacy_policy_admin(request):
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST':
            form = PrivacyPolicyForm(request.POST)
            if form.is_valid():
                for privacy in PrivacyPolicy.objects:
                    privacy.delete()

                if (request.POST['content'] != ""):
                    newPrivacy = PrivacyPolicy(content = request.POST['content'])
                    newPrivacy.save()
                messages.add_message(request, messages.INFO, 'Privacy Policy saved with success.')
                return redirect('/admin/website')
        else:
            if len(PrivacyPolicy.objects) != 0:
                policy = PrivacyPolicy.objects[0]
                data = {'content':policy.content}
                form = PrivacyPolicyForm(data)
            else:
                form = PrivacyPolicyForm()

        return render(request, 'admin/privacy_policy.html', {'form':form})
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: terms_of_use_admin(request)
# Inputs:        request -
# Outputs:       User Request Page
# Exceptions:    None
# Description:   Page that allows to edit Terms of Use
#
################################################################################
def terms_of_use_admin(request):
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST':
            form = TermsOfUseForm(request.POST)
            if form.is_valid():
                for terms in TermsOfUse.objects:
                    terms.delete()

                if (request.POST['content'] != ""):
                    newTerms = TermsOfUse(content = request.POST['content'])
                    newTerms.save()
                messages.add_message(request, messages.INFO, 'Terms of Use saved with success.')
                return redirect('/admin/website')
        else:
            if len(TermsOfUse.objects) != 0:
                terms = TermsOfUse.objects[0]
                data = {'content':terms.content}
                form = TermsOfUseForm(data)
            else:
                form = TermsOfUseForm()

        return render(request, 'admin/terms_of_use.html', {'form':form})
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: manage_schemas(request)
# Inputs:        request -
# Outputs:       Manage Templates Page
# Exceptions:    None
# Description:   Page that allows to upload new schemas and manage the existing ones
#
################################################################################
def manage_schemas(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/manage_uploads.html')

        currentTemplateVersions = []
        for tpl_version in TemplateVersion.objects():
            currentTemplateVersions.append(tpl_version.current)

        currentTemplates = dict()
        for tpl_version in currentTemplateVersions:
            tpl = Template.objects.get(pk=tpl_version)
            templateVersions = TemplateVersion.objects.get(pk=tpl.templateVersion)
            currentTemplates[tpl] = templateVersions.isDeleted

        context = RequestContext(request, {
            'objects':currentTemplates,
            'objectType': "Template"
        })
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: manage_types(request)
# Inputs:        request -
# Outputs:       Manage Types Page
# Exceptions:    None
# Description:   Page that allows to upload new types and manage the existing ones
#
################################################################################
def manage_types(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/manage_uploads.html')

        currentTypeVersions = []
        for type_version in TypeVersion.objects():
            currentTypeVersions.append(type_version.current)

        currentTypes = dict()
        for type_version in currentTypeVersions:
            type = Type.objects.get(pk=type_version)
            typeVersions = TypeVersion.objects.get(pk=type.typeVersion)
            currentTypes[type] = typeVersions.isDeleted

        context = RequestContext(request, {
            'objects':currentTypes,
            'objectType': "Type",
            'buckets': Bucket.objects

        })
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: federation_of_queries(request)
# Inputs:        request -
# Outputs:       Repositories Management Page
# Exceptions:    None
# Description:   Page that allows to add instance of repositories and manage existing ones
#
#
################################################################################
def federation_of_queries(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/federation_of_queries.html')

        context = RequestContext(request, {
            'instances': Instance.objects.order_by('-id')
        })
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: add_repository(request)
# Inputs:        request -
# Outputs:       Page that allows to add a repository
# Exceptions:    None
# Description:   Page that allows to add instance of a repository
#
#
################################################################################
def add_repository(request):
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST':


            form = RepositoryForm(request.POST)

            if form.is_valid():
                if request.POST["action"] == "Register":
                    errors = ""

                    # test if the name is "Local"
                    if (request.POST["name"].upper() == "LOCAL"):
                        errors += "By default, the instance named Local is the instance currently running."
                    else:
                        # test if an instance with the same name exists
                        instance = Instance.objects(name=request.POST["name"])
                        if len(instance) != 0:
                            errors += "An instance with the same name already exists.<br/>"

                    # test if new instance is not the same as the local instance
                    if request.POST["ip_address"] == request.META['REMOTE_ADDR'] and request.POST["port"] == request.META['SERVER_PORT']:
                        errors += "The address and port you entered refer to the instance currently running."
                    else:
                        # test if an instance with the same address/port exists
                        instance = Instance.objects(address=request.POST["ip_address"], port=request.POST["port"])
                        if len(instance) != 0:
                            errors += "An instance with the address/port already exists.<br/>"

                    # If some errors display them, otherwise insert the instance
                    if(errors == ""):
                        try:
                            url = request.POST["protocol"] + "://" + request.POST["ip_address"] + ":" + request.POST["port"] + "/o/token/"
#                             data="grant_type=password&username=" + request.POST["username"] + "&password=" + request.POST["password"]
                            headers = {'content-type': 'application/x-www-form-urlencoded'}
                            data={
                                'grant_type': 'password',
                                'username': request.POST["username"],
                                'password': request.POST["password"],
                                'client_id': request.POST["client_id"],
                                'client_secret': request.POST["client_secret"]
                            }
                            r = requests.post(url=url, data=data, headers=headers, timeout=int(request.POST["timeout"]))
                            if r.status_code == 200:
                                now = datetime.now()
                                delta = timedelta(seconds=int(eval(r.content)["expires_in"]))
                                expires = now + delta
                                Instance(name=request.POST["name"], protocol=request.POST["protocol"], address=request.POST["ip_address"], port=request.POST["port"], access_token=eval(r.content)["access_token"], refresh_token=eval(r.content)["refresh_token"], expires=expires).save()
                                messages.add_message(request, messages.INFO, 'Repository registered with success.')
                                return redirect('/admin/repositories')
                            else:
                                message = "Unable to get access to the remote instance using these parameters."
                                return render(request, 'admin/add_repository.html', {'form':form, 'action_result':message})
                        except Exception, e:
                            message = "Unable to get access to the remote instance using these parameters."
                            return render(request, 'admin/add_repository.html', {'form':form, 'action_result':message})

                    else:
                        return render(request, 'admin/add_repository.html', {'form':form, 'action_result':errors})

                elif request.POST["action"] == "Ping":
                    try:
                        url = request.POST["protocol"] + "://" + request.POST["ip_address"] + ":" + request.POST["port"] + "/rest/ping"
                        r = requests.get(url, auth=(request.POST["username"], request.POST["password"]), timeout=int(request.POST["timeout"]))
                        if r.status_code == 200:
                            message = "Remote API reached with success."
                        else:
                            if 'detail' in eval(r.content):
                                message = "Error: " + eval(r.content)['detail']
                            else:
                                message = "Error: Unable to reach the remote API."
                    except Exception, e:
                        message = "Error: Unable to reach the remote API."

                    return render(request, 'admin/add_repository.html', {'form':form, 'action_result':message})
        else:
            form = RepositoryForm()

        return render(request, 'admin/add_repository.html', {'form':form})
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: refresh_repository(request)
# Inputs:        request -
# Outputs:       Page that allows to refresh a repository token
# Exceptions:    None
# Description:   Page that allows to refresh a repository token
#
#
################################################################################
def refresh_repository(request):
    if request.user.is_authenticated() and request.user.is_staff:
        if request.method == 'POST':

            form = RefreshRepositoryForm(request.POST)

            if form.is_valid():
                try:
                    id = request.session['refreshInstanceID']
                    instance = Instance.objects.get(pk=ObjectId(id))
                except:
                    message = "Error: Unable to access the registered instance."
                    return render(request, 'admin/refresh_repository.html', {'form':form, 'action_result':message})

                try:
                    url = instance.protocol + "://" + instance.address + ":" + str(instance.port) + "/o/token/"
                    data="&grant_type=refresh_token&refresh_token=" + instance.refresh_token
                    headers = {'content-type': 'application/x-www-form-urlencoded'}
                    r = requests.post(url=url, data=data, headers=headers, auth=(request.POST["client_id"], request.POST["client_secret"]), timeout=int(request.POST["timeout"]))
                    if r.status_code == 200:
                        now = datetime.now()
                        delta = timedelta(seconds=int(eval(r.content)["expires_in"]))
                        expires = now + delta
                        instance.access_token=eval(r.content)["access_token"]
                        instance.refresh_token=eval(r.content)["refresh_token"]
                        instance.expires=expires
                        instance.save()
                        return HttpResponseRedirect('/admin/repositories')
                    else:
                        message = "Unable to get access to the remote instance using these parameters."
                        return render(request, 'admin/refresh_repository.html', {'form':form, 'action_result':message})
                except Exception, e:
                    message = "Unable to get access to the remote instance using these parameters."
                    return render(request, 'admin/refresh_repository.html', {'form':form, 'action_result':message})


        else:
            form = RefreshRepositoryForm()
            request.session['refreshInstanceID'] = request.GET['id']

        return render(request, 'admin/refresh_repository.html', {'form':form})
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: manage_versions(request)
# Inputs:        request -
# Outputs:       Manage Version Page
# Exceptions:    None
# Description:   Redirects to the version manager of a given object
#
################################################################################
def manage_versions(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/manage_versions.html')

        id = request.GET.get('id', None)
        objectType = request.GET.get('type', None)
        
        if id is not None and objectType is not None:
            try:
                if objectType == "Template":
                    object = Template.objects.get(pk=id)
                    objectVersions = TemplateVersion.objects.get(pk=object.templateVersion)
                else:
                    object = Type.objects.get(pk=id)
                    objectVersions = TypeVersion.objects.get(pk=object.typeVersion)
        
                versions = OrderedDict()
                reversedVersions = list(reversed(objectVersions.versions))
                for version_id in reversedVersions:
                    if objectType == "Template":
                        version = Template.objects.get(pk=version_id)
                    else:
                        version = Type.objects.get(pk=version_id)
                    objectid = ObjectId(version.id)
                    from_zone = tz.tzutc()
                    to_zone = tz.tzlocal()
                    datetimeUTC = objectid.generation_time
                    datetimeUTC = datetimeUTC.replace(tzinfo=from_zone)
                    datetimeLocal = datetimeUTC.astimezone(to_zone)
                    datetime = datetimeLocal.strftime('%m/%d/%Y %H&#58;%M&#58;%S')
                    versions[version] = datetime
        
        
                context = RequestContext(request, {
                    'versions': versions,
                    'objectVersions': objectVersions,
                    'objectType': objectType,
                })
                return HttpResponse(template.render(context))
            except:
                return redirect('/')
        else:
            return redirect('/')
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')


################################################################################
#
# Function Name: modules(request)
# Inputs:        request -
# Outputs:       User Request Page
# Exceptions:    None
# Description:   Page that allows to add modules to a template
#
################################################################################
def modules(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/modules.html')
        id = request.GET.get('id', None)
        if id is not None:
            try:
                object = Template.objects.get(pk=id)
                xsltPath = os.path.join(settings.SITE_ROOT, 'static/resources/xsl/xsd2html4modules.xsl')
                xslt = etree.parse(xsltPath)
                transform = etree.XSLT(xslt)            

                dom = etree.parse(BytesIO(object.content.encode('utf-8')))
                annotations = dom.findall(".//{http://www.w3.org/2001/XMLSchema}annotation")
                for annotation in annotations:
                    annotation.getparent().remove(annotation)
                newdom = transform(dom)
                xsdTree = str(newdom)
                
                request.session['moduleTemplateID'] = id
                request.session['moduleTemplateContent'] = object.content
                
                request.session['moduleNamespaces'] = common.get_namespaces(BytesIO(str(object.content)))
                for prefix, url in request.session['moduleNamespaces'].items():
                    if (url == "{http://www.w3.org/2001/XMLSchema}"):            
                        request.session['moduleDefaultPrefix'] = prefix
                        break
                
                context = RequestContext(request, {
                    'xsdTree': xsdTree,      
                    'modules': Module.objects              
                })
                
                
                return HttpResponse(template.render(context))
            except:
                return redirect('/')
        else:
            return redirect('/')
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')
    
    