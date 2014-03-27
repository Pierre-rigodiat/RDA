################################################################################
#
# File Name: urls.py
# Application: explore
# Description:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institue of Standards and Technology
#
################################################################################

from django.conf.urls import patterns, url

from explore import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
