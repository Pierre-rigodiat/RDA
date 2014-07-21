################################################################################
#
# File Name: views.py
# Application: Curate
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
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
from mgi.models import Template

def currentYear():
    return date.today().year

from django import forms

from mongoengine import *

def index(request):
    template = loader.get_template('curate.html')
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        connect('mgi')

        titles = ['HDF5 File', 'Basic Schema', 'Choice', 'Module Pertable', 'Module Table', 'No pertable', 'Restriction', 'Tree Multiplicity', 'Demo Diffusion', 'Demo Light', 'Demo Difussion Data v2.0']
        filenames = ['HDF5-File.xsd','_basic_schema.xsd','_choice.xsd','_module_pertable.xsd','_module_table.xsd','_no_pertable.xsd','_restriction.xsd','_tree_multiplicity.xsd','demo.diffusion.xsd','demo.light.xsd','demoDiffusionData_v2.0.xsd']

        for title, filename in zip(titles, filenames):
            pathFile = "{0}/xsdfiles/{1}"
            path = pathFile.format(settings.SITE_ROOT,filename)
            print 'path is ' + path
            xmlDoc = open(path,'r')
            xmlString = xmlDoc.read()
#            newTemplate = Template(title=title, filename=filename, content=xmlString).save()

        context = RequestContext(request, {
            'templates': Template.objects.order_by('title')
        })

        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

