################################################################################
#
# File Name: url.py
# Application: Informatics Core
# Description:
#
# Author: Marcus Newrock
#         marcus.newrock@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'oai_pmh.views',
    url(r'^add/registry', 'add_registry'),
    url(r'^update/registry$', 'update_registry'),
    url(r'^delete/registry$', 'delete_registry'),
    url(r'^add/record$', 'add_record'),
    url(r'^update/record$', 'update_record'),
    url(r'^check/registry$', 'check_registry'),
    # url(r'^delete/record$', 'delete_record'),
    url(r'^(?i)listrecords$', 'listRecords'),
    url(r'^(?i)identify$', 'identify'),
    url(r'^(?i)listmetadataformats$', 'listMetadataFormats'),
    url(r'^(?i)listsets$', 'listSets'),
    url(r'^(?i)listidentifiers$', 'listIdentifiers'),
    url(r'^(?i)getrecord', 'getRecord'),


    # url(r'^update/record/select$', 'update_record_select'),
    # url(r'^update/record/result$', 'update_record_result'),
    # url(r'^view/record$', 'view_record'),
    # url(r'^view/record/result$', 'view_record_result'),
    # url(r'^delete/registry/select$', 'delete_registry_select'),
    # url(r'^delete/registry/result$', 'delete_registry_result'),
    # url(r'^update/registry/select$', 'update_registry_select'),
    # url(r'^update/registry/result$', 'update_registry_result'),
    # url(r'^select/all/registries$', 'selectallregistries'),
    # url(r'^select/registry$', 'selectallregistries'),
    # url(r'^view/registry$', 'select_registry'),
    # url(r'^add/registry$', 'addregistry'),
)

