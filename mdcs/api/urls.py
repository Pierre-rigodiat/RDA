################################################################################
#
# File Name: urls.py
# Application: api
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.conf.urls import patterns, url
# from api.views import JsonDataList

urlpatterns = patterns(
    'api.views',
    url(r'^savedqueries/$','savedQuery_list', name='savedQuery_list'),
    url(r'^savedqueries/(?P<pk>([0-9]|[a-z])+)$', 'savedQuery_detail'),
#     url(r'^data/$',JsonDataList.as_view(),name='jsonData_list'),
    url(r'^data/$','jsonData_list',name='jsonData_list'),
    url(r'^data/(?P<pk>([0-9]|[a-z])+)$', 'jsonData_detail'),
    url(r'^tasks/$', 'task_list', name='task_list'),
    url(r'^tasks/(?P<pk>[0-9]+)$', 'task_detail', name='task_detail'),
)
