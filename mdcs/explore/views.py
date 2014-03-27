################################################################################
#
# File Name: views.py
# Application: explore
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

def currentYear():
    return date.today().year

from django import forms

from mongoengine import *

class Template(Document):
    title = StringField(required=True)
    filename = StringField(required=True)

def index(request):
#    logout(request)
    template = loader.get_template('explore.html')
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        connect('mgi')
#        var c = db.user.find()
#        while ( c.hasNext() ) printjson( c.next() )

        context = RequestContext(request, {
                'templates': Template.objects,
                })
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')


#    if request.user.is_authenticated():
#        return HttpResponse("Explore: User is authenticated")
#    else:
#        user = authenticate(username='materials', password='data123')
#        if user is not None:
#            # the password verified for the user
#            if user.is_active:
#                return HttpResponse("Explore: User is valid, active and authenticated")
#            else:
#                return HttpResponse("Explore: The password is valid, but the account has been disabled!")
#        else:
#            # the authentication system was unable to verify the username and password
#            return HttpResponse("Explore: The username and password were incorrect.")
