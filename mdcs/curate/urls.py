################################################################################
#
# File Name: urls.py
# Application: curate
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

from curate import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^select-template', views.index),
    url(r'^select-hdf5file$', 'curate.views.curate_select_hdf5file', name='curate-select-hdf5file'),
    url(r'^upload-spreadsheet$', 'curate.views.curate_upload_spreadsheet', name='curate-upload-spreadsheet'),
    url(r'^enter-data$', 'curate.views.curate_enter_data', name='curate-enter-data'),
    url(r'^enter-data/download-XSD$', 'curate.views.curate_enter_data_downloadxsd', name='curate-enter-data-downloadxsd'),
    url(r'^enter-data/download-form$', 'curate.views.curate_enter_data_downloadform', name='curate-enter-data-downloadform'),
    url(r'^view-data$', 'curate.views.curate_view_data', name='curate-view-data'),
    url(r'^view-data/download-XML/$', 'curate.views.curate_view_data_downloadxml', name='curate-view-data-downloadxml'),
)
