################################################################################
#
# File Name: views.py
# Application: mgi
# Description: Django views used to render pages for the system.
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

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from datetime import date
from mongoengine import *
from operator import itemgetter
from cStringIO import StringIO
import sys
from xlrd import open_workbook
from argparse import ArgumentError
from cgi import FieldStorage
import zipfile
from mgi.models import Template, Database, Htmlform, Xmldata, Hdf5file, QueryResults, SparqlQueryResults, XML2Download, TemplateVersion, Instance, XMLSchema, Request, Module, Type, TypeVersion, SavedQuery, Message, TermsOfUse, PrivacyPolicy, Bucket
from bson.objectid import ObjectId
import lxml.etree as etree
import os
from dateutil import tz
from collections import OrderedDict
from xlrd import open_workbook
import requests
from datetime import datetime
from datetime import timedelta
from admin.forms import RepositoryForm, RefreshRepositoryForm, RequestAccountForm, EditProfileForm, ChangePasswordForm, ContactForm, PrivacyPolicyForm, TermsOfUseForm
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

################################################################################
#
# Function Name: currentYear(request)
# Inputs:        request - 
# Outputs:       Current Year
# Exceptions:    None
# Description:   Helper function - returns the current year
#
################################################################################
def currentYear():
    return date.today().year

################################################################################
#
# Function Name: home(request)
# Inputs:        request - 
# Outputs:       Materials Data Curation System homepage
# Exceptions:    None
# Description:   renders the main home page from template (index.html)
#
################################################################################
def home(request):
    template = loader.get_template('index.html')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

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
    request.session['currentYear'] = currentYear()
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
    request.session['currentYear'] = currentYear()
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
        request.session['currentYear'] = currentYear()
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
    request.session['currentYear'] = currentYear()
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
    request.session['currentYear'] = currentYear()
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
# Function Name: backup_database(request)
# Inputs:        request - 
# Outputs:       Backup Page
# Exceptions:    None
# Description:   Page that allows to create a MongoDB backup 
#
################################################################################
def backup_database(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/backup-database.html')
        backupsDir = settings.SITE_ROOT + '/data/backups/'
            
        context = RequestContext(request, {
            'backups' : os.listdir(backupsDir)
        })
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')

################################################################################
#
# Function Name: restore_database(request)
# Inputs:        request - 
# Outputs:       Backup Page
# Exceptions:    None
# Description:   Page that allows to restore a MongoDB backup 
#
################################################################################
def restore_database(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/restore-database.html')

        backupsDir = settings.SITE_ROOT + '/data/backups/'
            
        context = RequestContext(request, {
            'backups' : os.listdir(backupsDir)
        })
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
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
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')

################################################################################
#
# Function Name: manage_modules(request)
# Inputs:        request - 
# Outputs:       Manage Modules Page
# Exceptions:    None
# Description:   Page that allows to list all existing modules
#
################################################################################
def module_management(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/manage_modules.html')

        context = RequestContext(request, {
            'modules': Module.objects
        })
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')

################################################################################
#
# Function Name: module_add(request)
# Inputs:        request - 
# Outputs:       Add Module Page
# Exceptions:    None
# Description:   Page that allows to add a new module
#
################################################################################
def module_add(request):
    if request.user.is_authenticated() and request.user.is_staff:
        template = loader.get_template('admin/add_module.html')
        
        context = RequestContext(request, {
            'templates':Template.objects
        })
        request.session['currentYear'] = currentYear()
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
        request.session['currentYear'] = currentYear()
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
        request.session['currentYear'] = currentYear()
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
    request.session['currentYear'] = currentYear()
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
                            url = request.POST["protocol"] + "://" + request.POST["ip_address"] + ":" + request.POST["port"] + "/oauth2/access_token/"                            
                            data="client_id=" + request.POST["client_id"] + "&client_secret=" + request.POST["client_secret"] + "&grant_type=password&username=" + request.POST["username"] + "&password=" + request.POST["password"]
                            headers = {'content-type': 'application/x-www-form-urlencoded'}
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
    request.session['currentYear'] = currentYear()
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
                    url = instance.protocol + "://" + instance.address + ":" + str(instance.port) + "/oauth2/access_token/"                            
                    data="client_id=" + request.POST["client_id"] + "&client_secret=" + request.POST["client_secret"] + "&grant_type=refresh_token&refresh_token=" + instance.refresh_token
                    headers = {'content-type': 'application/x-www-form-urlencoded'}
                    r = requests.post(url=url, data=data, headers=headers, timeout=int(request.POST["timeout"]))
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
# Function Name: curate(request)
# Inputs:        request - 
# Outputs:       Main Page of Curate Application
# Exceptions:    None
# Description:   Redirects to Curate Application        
#
################################################################################
def curate(request):
    if request.user.is_authenticated():
        template = loader.get_template('curate.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: curate_select_template(request)
# Inputs:        request - 
# Outputs:       Main Page of Curate Application
# Exceptions:    None
# Description:   Page that allows to select a template to start curating data
#                
#
################################################################################
def curate_select_template(request):
    if request.user.is_authenticated():
        template = loader.get_template('curate.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/select-template'
        return redirect('/login')


################################################################################
#
# Function Name: curate_select_hdf5file(request)
# Inputs:        request - 
# Outputs:       Select Spreadsheet page
# Exceptions:    None
# Description:   Page that allows to select an Excel Spreadsheet 
#                
#
################################################################################
def curate_select_hdf5file(request):
    if request.user.is_authenticated():
        template = loader.get_template('curate_select_hdf5file.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/select-template'
        return redirect('/login')

################################################################################
#
# Function Name: curate_upload_hdf5file(request)
# Inputs:        request - 
# Outputs:       Result of the upload
# Exceptions:    None
# Description:   Transforms the spreadsheet into XML and displays a success or error message
#
################################################################################
def curate_upload_spreadsheet(request):
    if request.user.is_authenticated():
        template = loader.get_template('curate_upload_successful.html')
    
        context = RequestContext(request, {
            '': '',
        })
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            if request.method == 'POST':
                try:
                    print request.FILES
                    input_excel = request.FILES['excelSpreadsheet']
                    print input_excel
                    book = open_workbook(file_contents=input_excel.read())
                    
                    root = etree.Element("table")
                    root.set("name", str(input_excel))
                    header = etree.SubElement(root, "headers")
                    values = etree.SubElement(root, "rows")
                    
                    for sheet in book.sheets():
                        for rowIndex in range(sheet.nrows):
                    
                            if rowIndex != 0:
                                row = etree.SubElement(values, "row")
                                row.set("id", str(rowIndex))
                    
                            for colIndex in range(sheet.ncols):
                                if rowIndex == 0:
                                    col = etree.SubElement(header, "column")
                                else:
                                    col = etree.SubElement(row, "column")
                    
                                col.set("id", str(colIndex))
                                col.text = str(sheet.cell(rowIndex, colIndex).value)                    
    
#                     xmlString = etree.tostring(root)
                    xmlString = etree.tostring(header)
                    xmlString += etree.tostring(values)
                    
                    request.session['spreadsheetXML'] = xmlString                    
                except:
                    templateError = loader.get_template('curate_upload_failed.html')
                    return HttpResponse(templateError.render(context))

            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/enter-data'
        return redirect('/login')


################################################################################
#
# Function Name: curate_enter_data(request)
# Inputs:        request - 
# Outputs:       Enter Data Page
# Exceptions:    None
# Description:   Page that allows to fill XML document data using an HTML form
#                
#
################################################################################
def curate_enter_data(request):
    print "BEGIN curate_enter_data(request)"
    if request.user.is_authenticated():
        template = loader.get_template('curate_enter_data.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/enter-data'
        return redirect('/login')

################################################################################
#
# Function Name: curate_view_data(request)
# Inputs:        request - 
# Outputs:       View Data Page
# Exceptions:    None
# Description:   Page that allows to view XML data to be curated                
#
################################################################################
def curate_view_data(request):    
    if request.user.is_authenticated():
        template = loader.get_template('curate_view_data.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/view-data'
        return redirect('/login')

################################################################################
#
# Function Name: curate_view_data_downloadxsd(request)
# Inputs:        request - 
# Outputs:       XSD representation of the current form instance
# Exceptions:    None
# Description:   Returns an XSD representation of the current form instance.
#                Used when user wants to download the form / xml schema.
#
################################################################################
def curate_enter_data_downloadxsd(request):
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            templateFilename = request.session['currentTemplate']
            templateID = request.session['currentTemplateID']

            
            templateObject = Template.objects.get(pk=ObjectId(templateID))
                
            print templateObject
            xsdDocData = templateObject.content

            xsdEncoded = xsdDocData.encode('utf-8')
            fileObj = StringIO(xsdEncoded)

            response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=' + templateFilename
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: curate_view_data_downloadxml(request)
# Inputs:        request - 
# Outputs:       XML representation of the current data instance
# Exceptions:    None
# Description:   Returns an XML representation of the current data instance.
#                Used when user wants to download the XML file.
#
################################################################################
def curate_enter_data_downloadform(request):
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            htmlFormId = request.GET.get('id','')          
            htmlFormObject = Htmlform.objects.get(pk=htmlFormId)

            formStringEncoded = htmlFormObject.content.encode('utf-8') 
            fileObj = StringIO(formStringEncoded)

            htmlFormObject.delete()

            response = HttpResponse(FileWrapper(fileObj), content_type='text/html')
            response['Content-Disposition'] = 'attachment; filename=' + "form.html" 
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: curate_view_data_downloadxml(request)
# Inputs:        request - 
# Outputs:       XML representation of the current data instance
# Exceptions:    None
# Description:   Returns an XML representation of the current data instance.
#                Used when user wants to download the XML file.
#
################################################################################
def curate_view_data_downloadxml(request):
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            xml2downloadID = request.GET.get('id','')
            xmlDataObject = XML2Download.objects.get(pk=xml2downloadID)
            

            xmlStringEncoded = xmlDataObject.xml.encode('utf-8') 
            fileObj = StringIO(xmlStringEncoded)

            xmlDataObject.delete()

            response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=' + "data.xml" #templateFilename
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')


################################################################################
#
# Function Name: explore(request)
# Inputs:        request - 
# Outputs:       Main Page of Explore Application
# Exceptions:    None
# Description:   Redirects to the Explore Application
#
################################################################################
def explore(request):
    if request.user.is_authenticated():
        template = loader.get_template('explore.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')

################################################################################
#
# Function Name: explore_select_template(request)
# Inputs:        request - 
# Outputs:       Main Page of Explore Application
# Exceptions:    None
# Description:   Page that allows to select a template to start Exploring
#
################################################################################
def explore_select_template(request):
    if request.user.is_authenticated():
        template = loader.get_template('explore.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/select-template'
        return redirect('/login')

################################################################################
#
# Function Name: explore_customize_template(request)
# Inputs:        request - 
# Outputs:       Customize Template Page
# Exceptions:    None
# Description:   Page that allows to select fields being used during Exploration
#
################################################################################
def explore_customize_template(request):
    if request.user.is_authenticated():
        template = loader.get_template('explore_customize_template.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore/customize-template'
        return redirect('/login')

################################################################################
#
# Function Name: explore_perform_search(request)
# Inputs:        request - 
# Outputs:       Perform Search Page
# Exceptions:    None
# Description:   Page that allows to submit queries
#
################################################################################
def explore_perform_search(request):
    try:
        if request.user.is_authenticated():
            template = loader.get_template('explore_perform_search.html')
            instances = Instance.objects()   
            if 'HTTPS' in request.META['SERVER_PROTOCOL']:
                protocol = "https"
            else:
                protocol = "http"
            local = Instance(name="Local", protocol=protocol, address=request.META['REMOTE_ADDR'], port=request.META['SERVER_PORT'])
            listInstances = [local]
            for instance in instances:
                listInstances.append(instance) 
                
            template_hash = Template.objects.get(pk=request.session['exploreCurrentTemplateID']).hash
            
            queries = SavedQuery.objects(user=str(request.user.id), template=str(request.session['exploreCurrentTemplateID']))
            context = RequestContext(request, {
                'instances': listInstances,
                'template_hash': template_hash,
                'queries':queries,
            })
            request.session['currentYear'] = currentYear()
            if 'exploreCurrentTemplateID' not in request.session:
                return redirect('/explore/select-template')
            else:
                return HttpResponse(template.render(context))
        else:
            if 'loggedOut' in request.session:
                del request.session['loggedOut']
            request.session['next'] = '/explore/perform-search'
            return redirect('/login')
    except:
        return redirect("/explore")

################################################################################
#
# Function Name: explore_results(request)
# Inputs:        request - 
# Outputs:       Query results page
# Exceptions:    None
# Description:   Page that allows to see results from a query
#
################################################################################
def explore_results(request):
    if request.user.is_authenticated():
        template = loader.get_template('explore_results.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore/results'
        return redirect('/login')
    
################################################################################
#
# Function Name: explore_sparqlresults(request)
# Inputs:        request - 
# Outputs:       SPARQL Results Page
# Exceptions:    None
# Description:   Page that allows to see SPARQL results
#
################################################################################
def explore_sparqlresults(request):
    if request.user.is_authenticated():
        template = loader.get_template('explore_sparqlresults.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore/sparqlresults'
        return redirect('/login')

################################################################################
#
# Function Name: explore_download_results(request)
# Inputs:        request - 
# Outputs:       results of a query as xml files
# Exceptions:    None
# Description:   Download XML results in a ZIP file
#
################################################################################
def explore_download_results(request):
    if request.user.is_authenticated():
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:          
            savedResultsID = request.GET.get('id','')
            ResultsObject = QueryResults.objects.get(pk=savedResultsID)

            in_memory = StringIO()
            zip = zipfile.ZipFile(in_memory, "a")
            
            resultNumber = 1
            for result in ResultsObject.results:
                zip.writestr("result"+str(resultNumber)+".xml", result)
                resultNumber += 1
                
            # fix for Linux zip files read in Windows  
            for xmlFile in zip.filelist:  
                xmlFile.create_system = 0 
            
            zip.close()
            
            ResultsObject.delete()

            response = HttpResponse(mimetype="application/zip")  
            response["Content-Disposition"] = "attachment; filename=results.zip"  
              
            in_memory.seek(0)      
            response.write(in_memory.read())  
              
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')


################################################################################
#
# Function Name: explore_download_sparqlresults(request)
# Inputs:        request - 
# Outputs:       Results of a sparql query
# Exceptions:    None
# Description:   Download SPARQL results
#
################################################################################
def explore_download_sparqlresults(request):
    if request.user.is_authenticated():
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:          
            savedResultsID = request.GET.get('id','')
            sparqlResults = SparqlQueryResults.objects.get(pk=savedResultsID)

            sparqlResultsEncoded = sparqlResults.results.encode('utf-8')
            fileObj = StringIO(sparqlResultsEncoded)

            response = HttpResponse(FileWrapper(fileObj), content_type='application/text')
            response['Content-Disposition'] = 'attachment; filename=sparql_results.txt'
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')

################################################################################
#
# Function Name: compose(request)
# Inputs:        request - 
# Outputs:       Main Page of the Composer Application 
# Exceptions:    None
# Description:   Redirects to the main page of the composer
#                
################################################################################
def compose(request):
    template = loader.get_template('compose.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose'
        return redirect('/login')

################################################################################
#
# Function Name: compose_select_template(request)
# Inputs:        request - 
# Outputs:       Main Page of Composer Application
# Exceptions:    None
# Description:   Page that allows to select a template to start composing
#
################################################################################
def compose_select_template(request):
    template = loader.get_template('compose.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose/select-template'
        return redirect('/login')

################################################################################
#
# Function Name: compose_build_template(request)
# Inputs:        request - 
# Outputs:       Build Template Page
# Exceptions:    None
# Description:   Page that allows to Compose the Template
#
################################################################################
def compose_build_template(request):
    template = loader.get_template('compose_build_template.html')
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
               
        # 1) user types: list of ids
        userTypes = []
        for user_type in Type.objects(user=request.user.id):
            userTypes.append(user_type)
                       
        # 2) buckets: label -> list of type that are not deleted
        # 3) nobuckets: list of types that are not assigned to a specific bucket
        bucketsTypes = dict()        
        nobucketsTypes = []
        
        buckets = Bucket.objects
        
        for type_version in TypeVersion.objects():
            if type_version.isDeleted == False:
                hasBucket = False
                for bucket in buckets:
                    if str(type_version.id) in bucket.types:
                        if bucket not in bucketsTypes.keys():
                            bucketsTypes[bucket] = []
                        bucketsTypes[bucket].append(Type.objects.get(pk=type_version.current))
                        hasBucket = True
                if hasBucket == False:
                    nobucketsTypes.append(Type.objects.get(pk=type_version.current))
        
        context = RequestContext(request, {
           'bucketsTypes': bucketsTypes,
           'nobucketsTypes': nobucketsTypes,
           'userTypes': userTypes,
        })
        
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose/build-template'
        return redirect('/login')

################################################################################
#
# Function Name: all_options(request)
# Inputs:        request - 
# Outputs:       All Options Page
# Exceptions:    None
# Description:   Page that allows to access every features of the System   
#
################################################################################
def all_options(request):
    template = loader.get_template('all-options.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: browse_all(request)
# Inputs:        request - 
# Outputs:       Browse All Page
# Exceptions:    None
# Description:   Page that allows to access the list of all existing templates
#
################################################################################
def browse_all(request):
    template = loader.get_template('browse-all.html')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('title')
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: request_new_account(request)
# Inputs:        request - 
# Outputs:       Request New Account Page
# Exceptions:    None
# Description:   Page that allows to request a user account
#
################################################################################
def request_new_account(request):
    request.session['currentYear'] = currentYear()
    
    if request.method == 'POST':
        form = RequestAccountForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=request.POST["username"])
                message = "This username already exists. Please choose another username."
                return render(request, 'request_new_account.html', {'form':form, 'action_result':message})
            except:
                Request(username=request.POST["username"], password=request.POST["password1"],first_name=request.POST["firstname"], last_name=request.POST["lastname"], email=request.POST["email"]).save()
                messages.add_message(request, messages.INFO, 'User Account Request sent to the administrator.')
                return redirect('/')
                
    else:
        form = RequestAccountForm()
    
    return render(request, 'request_new_account.html', {'form':form})

################################################################################
#
# Function Name: logout_view(request)
# Inputs:        request - 
# Outputs:       Login Page
# Exceptions:    None
# Description:   Page that redirects to login page
#                
#
################################################################################
def logout_view(request):
    logout(request)
    if 'loggedOut' in request.session:
        request.session['loggedOut'] = 'true'
    request.session['next'] = '/'
    request.session['currentYear'] = currentYear()
    return redirect('/login')

################################################################################
#
# Function Name: my_profile(request)
# Inputs:        request - 
# Outputs:       My Profile Page
# Exceptions:    None
# Description:   Page that allows to look at user's profile information
#
################################################################################
def my_profile(request):
    if request.user.is_authenticated():
        template = loader.get_template('my_profile.html')
        context = RequestContext(request, {
            '': '',
        })
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/my-profile'
        return redirect('/login')

################################################################################
#
# Function Name: my_profile_edit(request)
# Inputs:        request - 
# Outputs:       Edit My Profile Page
# Exceptions:    None
# Description:   Page that allows to edit a profile
#
################################################################################
def my_profile_edit(request):   
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = EditProfileForm(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.user.id)
                if request.POST['username'] != user.username:
                    try:
                        user = User.objects.get(username=request.POST['username'])
                        message = "A user with the same username already exists."
                        return render(request, 'my_profile_edit.html', {'form':form, 'action_result':message})
                    except:
                        user.username = request.POST['username']
                
                user.first_name = request.POST['firstname']
                user.last_name = request.POST['lastname']
                user.email = request.POST['email']
                user.save()                
                messages.add_message(request, messages.INFO, 'Profile information edited with success.')
                return redirect('/my-profile')
        else:
            user = User.objects.get(id=request.user.id)
            data = {'firstname':user.first_name, 
                    'lastname':user.last_name,
                    'username':user.username,
                    'email':user.email}
            form = EditProfileForm(data)
        
        return render(request, 'my_profile_edit.html', {'form':form})
    
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/my-profile'
        return redirect('/login')

################################################################################
#
# Function Name: my_profile_change_password(request)
# Inputs:        request - 
# Outputs:       Change Password Page
# Exceptions:    None
# Description:   Page that allows to change a password
#
################################################################################
def my_profile_change_password(request):
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(id=request.user.id)
                auth_user = authenticate(username=user.username, password=request.POST['old'])
                if auth_user is None:
                    message = "The old password is incorrect."
                    return render(request, 'my_profile_change_password.html', {'form':form, 'action_result':message})
                else:        
                    user.set_password(request.POST['new1'])
                    user.save()
                    messages.add_message(request, messages.INFO, 'Password changed with success.')
                    return redirect('/my-profile')
        else:
            form = ChangePasswordForm()
        
        return render(request, 'my_profile_change_password.html', {'form':form})
    
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/my-profile'
        return redirect('/login')

################################################################################
#
# Function Name: contact(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Message(name=request.POST['name'], email=request.POST['email'], content=request.POST['message']).save()
            messages.add_message(request, messages.INFO, 'Your message was sent to the administrator.')
            return redirect('/')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form':form})

################################################################################
#
# Function Name: privacy_policy(request)
# Inputs:        request - 
# Outputs:       Privacy Policy Page
# Exceptions:    None
# Description:   Page that provides privacy policy     
#
################################################################################
def privacy_policy(request):
    template = loader.get_template('privacy-policy.html')
    policy = None
    if len(PrivacyPolicy.objects) != 0:
        policy = PrivacyPolicy.objects[0] 

    context = RequestContext(request, { 
        'policy': policy
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: terms_of_use(request)
# Inputs:        request - 
# Outputs:       Terms of Use page
# Exceptions:    None
# Description:   Page that provides terms of use
#
################################################################################
def terms_of_use(request):
    template = loader.get_template('terms-of-use.html')
    terms = None
    if len(TermsOfUse.objects) != 0:
        terms = TermsOfUse.objects[0] 

    context = RequestContext(request, { 
        'terms': terms
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: help(request)
# Inputs:        request - 
# Outputs:       Help Page
# Exceptions:    None
# Description:   Page that provides FAQ
#
################################################################################
def help(request):
    template = loader.get_template('help.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: compose_downloadxsd(request)
# Inputs:        request - 
# Outputs:       XSD representation of the current data instance
# Exceptions:    None
# Description:   Returns an XSD representation of the current data instance.
#                Used when user wants to download the XML file.
#
################################################################################
def compose_downloadxsd(request):
    if request.user.is_authenticated():                  
        xml2downloadID = request.GET.get('id','')
        xmlDataObject = XML2Download.objects.get(pk=xml2downloadID)
        

        xmlStringEncoded = xmlDataObject.xml.encode('utf-8') 
        fileObj = StringIO(xmlStringEncoded)

        xmlDataObject.delete()

        response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=' + "new_template.xsd"
        return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose'
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
        
        id = request.GET.get('id','')
        objectType = request.GET.get('type','')
        
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
        request.session['currentYear'] = currentYear()
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/'
        return redirect('/login')

            
        
        
        
        