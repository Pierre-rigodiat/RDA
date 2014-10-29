################################################################################
#
# File Name: views.py
# Application: Compose
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

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.shortcuts import redirect
from datetime import date
from django.conf import settings
from mgi.models import Template, TemplateVersion

def currentYear():
    return date.today().year

from django import forms

from mongoengine import *

def index(request):
    template = loader.get_template('compose.html')
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
    
        currentTemplateVersions = []
        for tpl_version in TemplateVersion.objects():
            currentTemplateVersions.append(tpl_version.current)
        
        currentTemplates = dict()
        for tpl_version in currentTemplateVersions:
            tpl = Template.objects.get(pk=tpl_version)
            templateVersions = TemplateVersion.objects.get(pk=tpl.templateVersion)
            currentTemplates[tpl] = templateVersions.isDeleted
    
        context = RequestContext(request, {
           'templates':currentTemplates
        })

        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose'
        return redirect('/login')
