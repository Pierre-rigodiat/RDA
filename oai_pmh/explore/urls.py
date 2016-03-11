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
from django.conf.urls import patterns, url, include
from ajax import get_results_by_instance_keyword
urlpatterns = patterns(
    'oai_pmh.explore.views',
    url(r'^keyword',  'index_keyword', name='index-keyword'),
    url(r'^get_results_by_instance_keyword', get_results_by_instance_keyword),
    url(r'^get_metadata_formats', 'get_metadata_formats'),
)

