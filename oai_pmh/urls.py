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
    url(r'^download-xml-build-req$', 'download_xml_build_req'),
    url(r'^(?i)listrecords$', 'listRecords'),
    url(r'^(?i)identify$', 'identify'),
    url(r'^(?i)listmetadataformats$', 'listMetadataFormats'),
    url(r'^(?i)listsets$', 'listSets'),
    url(r'^(?i)listidentifiers$', 'listIdentifiers'),
    url(r'^(?i)getrecord', 'getRecord'),
    url(r'^registry/(?P<registry>[-\w]+)/all_sets/$', 'all_sets'),
    url(r'^registry/(?P<registry>[-\w]+)/all_metadataprefix/$', 'all_metadataprefix'),
    url(r'^getdata/$', 'getData'),
)

