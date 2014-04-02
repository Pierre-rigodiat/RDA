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

def currentYear():
    return date.today().year

from django import forms

from mongoengine import *

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

class Template(Document):
    title = StringField(required=True)
    filename = StringField(required=True)

def index(request):
#    logout(request)
    template = loader.get_template('curate.html')
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        connect('mgi')
#        var c = db.user.find()
#        while ( c.hasNext() ) printjson( c.next() )

#        template1 = Template(title='HDF5 File', filename='HDF5-File.xsd').save()
#        template2 = Template(title='Basic Schema', filename='_basic_schema.xsd').save()
#        template3 = Template(title='Choice', filename='_choice.xsd').save()
#        template4 = Template(title='Module Pertable', filename='_module_pertable.xsd').save()
#        template5 = Template(title='Module Table', filename='_module_table.xsd').save()
#        template6 = Template(title='No Pertable', filename='_no_pertable.xsd').save()
#        template7 = Template(title='Restriction', filename='_restriction.xsd').save()
#        template8 = Template(title='Tree Multiplicity', filename='_tree_multiplicity.xsd').save()
#        template9 = Template(title='Demo Diffusion', filename='demo.diffusion.xsd').save()
#        template10 = Template(title='Demo Light', filename='demo.light.xsd').save()
#        template11 = Template(title='Demo Diffusion Data v2.0', filename='demoDiffusionData_v2.0.xsd').save()


        context = RequestContext(request, {
            'templates': Template.objects.order_by('title')
        })
#        for user in User.objects:
#          print user.first_name
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

