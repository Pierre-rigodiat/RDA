################################################################################
#
# File Name: views.py
# Application: mgi
# Description: Django views used to render pages for the system.
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django import forms
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from datetime import date
from mongoengine import *
from operator import itemgetter
from cStringIO import StringIO
from curate.models import XMLSchema 

import lxml.etree as etree

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class Template(Document):
    title = StringField(required=True)
    filename = StringField(required=True)
    content = StringField(required=True)

class Ontology(Document):
    title = StringField(required=True)
    filename = StringField(required=True)
    content = StringField(required=True)

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
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: admin(request)
# Inputs:        request - 
# Outputs:       Administrative Dashboard page
# Exceptions:    None
# Description:   renders the admin page from template (admin/index.html)
#
################################################################################
def admin(request):
    template = loader.get_template('admin/index.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: xml_schemas(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def xml_schemas(request):
    template = loader.get_template('admin/xml_schemas.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: manage_schemas(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def manage_schemas(request):
    template = loader.get_template('admin/manage_schemas.html')
    connect('mgi')

    context = RequestContext(request, {
#        'templates': Template.objects.all()
        'templates': Template.objects.order_by('-id')
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: manage_modules(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def manage_modules(request):
    template = loader.get_template('admin/manage_modules.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: manage_queries(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def manage_queries(request):
    template = loader.get_template('admin/manage_queries.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: manage_ontologies(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def manage_ontologies(request):
    template = loader.get_template('admin/manage_ontologies.html')
    connect('mgi')

    context = RequestContext(request, {
        'ontologies': Ontology.objects.order_by('-id')
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: user_management(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def user_management(request):
    template = loader.get_template('admin/user_management.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: curate(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate(request):
#    logout(request)
    template = loader.get_template('curate.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: curate_select_template(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate_select_template(request):
#    logout(request)
    template = loader.get_template('curate.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/select-template'
        return redirect('/login')

################################################################################
#
# Function Name: curate_enter_data(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate_enter_data(request):
    print "BEGIN curate_enter_data(request)"
#    logout(request)
    template = loader.get_template('curate_enter_data.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
#    return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
        if 'currentTemplate' not in request.session:
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
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate_view_data(request):
#    logout(request)
    template = loader.get_template('curate_view_data.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
        if 'currentTemplate' not in request.session:
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
        if 'currentTemplate' not in request.session:
            return redirect('/curate/select-template')
        else:
            templateFilename = request.session['currentTemplate']
            pathFile = "{0}/mdcs/xsdfiles/" + templateFilename

            path = pathFile.format(
                settings.SITE_ROOT)
            xmlDoc = open(path,'r')
            response = HttpResponse(FileWrapper(xmlDoc), content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=mgiml.xml'
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
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
def curate_view_data_downloadxsd(request):
    if request.user.is_authenticated():
        if 'currentTemplate' not in request.session:
            return redirect('/curate/select-template')
        else:
            templateFilename = request.session['currentTemplate']
            print 'currentTemplate: ' + templateFilename

            templateObject = Template.objects.get(filename=templateFilename)

            print templateObject
#            xsdDocData = templateObject.content
            print XMLSchema.tree
            root = XMLSchema.tree.getroot()
            xsdDocData = etree.tostring(root,pretty_print=True)

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
# Function Name: view_schema(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def view_schema(request):
#    logout(request)
    template = loader.get_template('view_schema.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
        if 'currentTemplate' not in request.session:
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
# Function Name: explore(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore(request):
#    logout(request)
    template = loader.get_template('explore.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')
#        user = authenticate(username='materials', password='data123')
#        if user is not None:
            # the password verified for the user
#            if user.is_active:
#                return HttpResponse(template.render(context))
#                return HttpResponse("HomePage: User is valid, active and authenticated")
#            else:
#                return HttpResponse("HomePage: The password is valid, but the account has been disabled!")
#        else:
            # the authentication system was unable to verify the username and password
#            return HttpResponse("HomePage: The username and password were incorrect.")

################################################################################
#
# Function Name: explore_select_template(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore_select_template(request):
#    logout(request)
    template = loader.get_template('explore.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
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
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore_customize_template(request):
#    logout(request)
    template = loader.get_template('explore_customize_template.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
        if 'currentTemplate' not in request.session:
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
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore_perform_search(request):
#    logout(request)
    template = loader.get_template('explore_perform_search.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
        if 'currentTemplate' not in request.session:
            return redirect('/explore/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore/perform-search'
        return redirect('/login')

################################################################################
#
# Function Name: contribute(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def contribute(request):
    template = loader.get_template('contribute.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: all_options(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
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
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def browse_all(request):
    template = loader.get_template('browse-all.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('title')
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: login_view(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def login_view(request):
#    del request.session['loggedOut']

    template = loader.get_template('login.html')
    context = RequestContext(request, {
        'next': 'http://www.google.com',
    })
    request.session['currentYear'] = currentYear()
    request.session['next'] = 'http://www.google.com'
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: logout_view(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
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
#    template = loader.get_template('login.html')
#    context = RequestContext(request, {
#        '': '',
#    })
#    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: my_profile(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def my_profile(request):
    template = loader.get_template('my_profile.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/my-profile'
        return redirect('/login')

################################################################################
#
# Function Name: my_profile_edit(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def my_profile_edit(request):
    template = loader.get_template('my_profile_edit.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/my-profile'
        return redirect('/login')

################################################################################
#
# Function Name: my_profile_change_password(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def my_profile_change_password(request):
    template = loader.get_template('my_profile_change_password.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
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
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })
#    template = loader.get_template('contact.html')
#    context = RequestContext(request, {
#        '': '',
#    })
#    request.session['currentYear'] = currentYear()
#    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: about(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def about(request):
    template = loader.get_template('about.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: privacy_policy(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def privacy_policy(request):
    template = loader.get_template('privacy-policy.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: terms_of_use(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def terms_of_use(request):
    template = loader.get_template('terms-of-use.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: help(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def help(request):
    template = loader.get_template('help.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

#    if request.user.is_authenticated():
#        return HttpResponse("HomePage: User is authenticated")
#    else:
#        user = authenticate(username='materials', password='data123')
#        if user is not None:
#            # the password verified for the user
#            if user.is_active:
#                return HttpResponse("HomePage: User is valid, active and authenticated")
#            else:
#                return HttpResponse("HomePage: The password is valid, but the account has been disabled!")
#        else:
#            # the authentication system was unable to verify the username and password
#            return HttpResponse("HomePage: The username and password were incorrect.")

