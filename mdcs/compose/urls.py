################################################################################
#
# File Name: urls.py
# Application: compose
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

from django.conf.urls import patterns, url

from compose import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^select-template', views.index),
    url(r'^build-template$', 'compose.views.compose_build_template', name='compose-build-template'),
    url(r'^download-XSD$', 'compose.views.compose_downloadxsd', name='compose-downloadxsd'),
)
