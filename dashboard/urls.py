################################################################################
#
# File Name: urls.py
# Application: dashboard
# Purpose:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#		  Xavier SCHMITT
#		  xavier.schmitt@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'dashboard.views.my_profile'),
    url(r'^my-profile$', 'dashboard.views.my_profile'),
    url(r'^my-profile/edit', 'dashboard.views.my_profile_edit'),
    url(r'^my-profile/change-password', 'dashboard.views.my_profile_change_password'),
    url(r'^forms', 'dashboard.views.dashboard_my_forms'),
    url(r'^resources$', 'dashboard.views.dashboard_resources'),
    url(r'^templates$', 'dashboard.views.dashboard_templates'),
    url(r'^types$', 'dashboard.views.dashboard_types'),
    url(r'^files$', 'dashboard.views.dashboard_files'),
    url(r'^toXML$', 'dashboard.ajax.dashboard_toXML'),
    url(r'^edit_information$', 'dashboard.ajax.edit_information'),
    url(r'^delete_object$', 'dashboard.ajax.delete_object'),
    url(r'^modules$', 'dashboard.views.dashboard_modules'),
    url(r'^detail$', 'dashboard.views.dashboard_detail_resource'),
)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += staticfiles_urlpatterns()