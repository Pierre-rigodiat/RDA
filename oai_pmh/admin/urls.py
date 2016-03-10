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

urlpatterns = patterns(
    'oai_pmh.admin.views',
    url(r'^check/registry$', 'check_registry'),
    url(r'^add/registry', 'add_registry'),
    url(r'^update/registry$', 'update_registry'),
    url(r'^update/my-registry$', 'update_my_registry'),
    url(r'^delete/registry$', 'delete_registry'),
    url(r'^oai-pmh$', 'oai_pmh', name='oai_pmh'),
    url(r'^oai-pmh-my-infos', 'oai_pmh_my_infos', name='oai_pmh_my_infos'),
    url(r'^oai-pmh-detail-registry$', 'oai_pmh_detail_registry', name='oai_pmh_detail_registry'),
    url(r'^update/all/records', 'update_all_records', name='update_all_records'),
)

