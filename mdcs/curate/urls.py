################################################################################
#
# File Name: urls.py
# Application: Curate
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.conf.urls import patterns, url

from curate import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
