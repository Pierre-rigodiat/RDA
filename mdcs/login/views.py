################################################################################
#
# File Name: views.py
# Application: login
# Description:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth import authenticate#, logout
from django.template import RequestContext, loader

def index(request):
    #logout(request)

    template = loader.get_template('login.html')
    context = RequestContext(request, {
        '': '',
    })
    return HttpResponse(template.render(context))

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
