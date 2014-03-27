################################################################################
#
# File Name: urls.py
# Application: Curate
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institue of Standards and Technology
#
################################################################################

from django.conf.urls import patterns, url

from curate import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
