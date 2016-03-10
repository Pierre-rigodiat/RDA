################################################################################
#
# File Name: rest_urls.py
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
    'oai_pmh.api.views',
    url(r'^add/registry$', 'add_registry'),
    url(r'^add/record$', 'add_record'),
    url(r'^select/all/registries$', 'select_all_registries'),
    url(r'^select/all/records', 'select_all_records'),
    url(r'^select/registry$', 'select_registry'),
    url(r'^select/record$', 'select_record'),
    url(r'^update/registry$', 'update_registry'),
    url(r'^update/my-registry$', 'update_my_registry'),
    url(r'^update/record$', 'update_record'),
    url(r'^delete/registry$', 'delete_registry'),
    url(r'^delete/record$', 'delete_record'),
    url(r'^(?i)listobjectallrecords$', 'listObjectAllRecords'),
    url(r'^(?i)identify$', 'identify'),
    url(r'^(?i)objectidentify$', 'objectIdentify'),
    url(r'^(?i)listmetadataformats$', 'listMetadataFormats'),
    url(r'^(?i)listobjectmetadataformats$', 'listObjectMetadataFormats'),
    url(r'^(?i)listsets$', 'listSets'),
    url(r'^(?i)listobjectsets$', 'listObjectSets'),
    url(r'^(?i)listidentifiers$', 'listIdentifiers'),
    url(r'^(?i)getrecord', 'getRecord'),
    url(r'^getdata/$', 'getData'),

    url(r'^update/all/records$', 'update_all_records'),
)
