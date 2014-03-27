################################################################################
#
# File Name: views.py
# Application: mgi
# Description:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institue of Standards and Technology
#
################################################################################

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.shortcuts import redirect
from datetime import date

from django import forms

from django.core.servers.basehttp import FileWrapper
from django.conf import settings

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

from mongoengine import *
from operator import itemgetter

class Template(Document):
    title = StringField(required=True)
    filename = StringField(required=True)

def currentYear():
    return date.today().year

def home(request):
    template = loader.get_template('index.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def admin(request):
    template = loader.get_template('admin/index.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def xml_schemas(request):
    template = loader.get_template('admin/xml_schemas.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def manage_schemas(request):
    template = loader.get_template('admin/manage_schemas.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.all()
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def manage_modules(request):
    template = loader.get_template('admin/manage_modules.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def manage_queries(request):
    template = loader.get_template('admin/manage_queries.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def user_management(request):
    template = loader.get_template('admin/user_management.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

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
#        username = request.POST['username']
#        password = request.POST['password']
#        user = authenticate(username=username, password=password)
#        user = authenticate(username='materials', password='data123')
#        if user is not None:
            # the password verified for the user
#            if user.is_active:
#                login(request, user)
#                return HttpResponse(template.render(context))
#                return render_to_response('index.html', {'inhalt': 'sucessfully logged in'}, RequestContext(request))
#                return HttpResponse("HomePage: User is valid, active and authenticated")
#            else:
#                return HttpResponse("HomePage: The password is valid, but the account has been disabled!")
#        else:
            # the authentication system was unable to verify the username and password
#            return HttpResponse("HomePage: The username and password were incorrect.")

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

def curate_enter_data(request):
#    logout(request)
    template = loader.get_template('curate_enter_data.html')
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
        request.session['next'] = '/curate/enter-data'
        return redirect('/login')

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

def curate_view_data_downloadxml(request):
#    logout(request)

#    template = loader.get_template('curate_view_data.html2')
#    context = RequestContext(request, {
#        '': '',
#    })
#    request.session['currentYear'] = currentYear()
#    return HttpResponse(template.render(context))  # remove after testing
    templateFilename = request.session['currentTemplate']
    pathFile = "{0}/xsdfiles/" + templateFilename

    path = pathFile.format(
        settings.SITE_ROOT)
    xmlDoc = open(path,'r')
    response = HttpResponse(FileWrapper(xmlDoc), content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=mgiml.xml'
    return response
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

def curate_view_data_downloadxsd(request):
#    logout(request)

#    template = loader.get_template('curate_view_data.html2')
#    context = RequestContext(request, {
#        '': '',
#    })
#    request.session['currentYear'] = currentYear()
#    return HttpResponse(template.render(context))  # remove after testing
    templateFilename = request.session['currentTemplate']
    pathFile = "{0}/xsdfiles/" + templateFilename

    path = pathFile.format(
        settings.SITE_ROOT)
    xmlDoc = open(path,'r')
    response = HttpResponse(FileWrapper(xmlDoc), content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=mgiml.xml'
    return response
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

def all_options(request):
    template = loader.get_template('all-options.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def browse_all(request):
    template = loader.get_template('browse-all.html')
    connect('mgi')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('title')
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def login_view(request):
#    del request.session['loggedOut']

    template = loader.get_template('login.html')
    context = RequestContext(request, {
        'next': 'http://www.google.com',
    })
    request.session['currentYear'] = currentYear()
    request.session['next'] = 'http://www.google.com'
    return HttpResponse(template.render(context))

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

def about(request):
    template = loader.get_template('about.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def privacy_policy(request):
    template = loader.get_template('privacy-policy.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def terms_of_use(request):
    template = loader.get_template('terms-of-use.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

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

