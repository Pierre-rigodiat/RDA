################################################################################
#
# File Name: urls.py
# Application: api
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

from django.conf.urls import patterns, url, include
# from api.views import JsonDataList
from api.views import docs

urlpatterns = patterns(
    'api.views',
    url(r'^savedqueries/$','savedQuery_list', name='savedQuery_list'),
    url(r'^savedqueries/(?P<pk>([0-9]|[a-z])+)$', 'savedQuery_detail'),
#     url(r'^data/$',JsonDataList.as_view(),name='jsonData_list'),
    url(r'^data/$','jsonData_list', name='jsonData_list'),
    url(r'^data/(?P<pk>([0-9]|[a-z])+)$', 'jsonData_detail'),
    url(r'^curate$', 'curate', name='curate'),
    url(r'^explore/select/all$', 'explore', name='explore'),
    url(r'^explore/query-by-example$', 'query_by_example', name='query_by_example'),
    url(r'^explore/sparql-query$', 'sparql_query', name='sparql_query'),
    url(r'^schema/add$','add_schema', name='add_schema'),
    url(r'^schema/select$','select_schema'),
    url(r'^schema/delete$','delete_schema'),
    url(r'^schema/select/all$','select_all_schemas'),
    url(r'^.*$', include([url(r'^.*$', docs)], namespace='error_redirect'))
)


