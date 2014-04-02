################################################################################
#
# File Name: urls.py
# Application: explore
# Description:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.conf.urls import patterns, url

from explore import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
