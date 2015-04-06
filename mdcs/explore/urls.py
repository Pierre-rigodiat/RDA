################################################################################
#
# File Name: urls.py
# Application: explore
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume Sousa Amaral
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.conf.urls import patterns, url

from explore import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^select-template', views.index),
    url(r'^customize-template$', 'explore.views.explore_customize_template', name='expore-customize-template'),
    url(r'^perform-search$', 'explore.views.explore_perform_search', name='explore-perform-search'),
    url(r'^results$', 'explore.views.explore_results', name='explore-results'),
    url(r'^results/download-results/$', 'explore.views.explore_download_results', name='explore-download-results'),
    url(r'^sparqlresults$', 'explore.views.explore_sparqlresults', name='explore-sparqlresults'),
    url(r'^results/download-sparqlresults/$', 'explore.views.explore_download_sparqlresults', name='explore-download-sparqlresults'),
)
