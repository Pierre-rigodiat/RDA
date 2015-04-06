################################################################################
#
# File Name: urls.py
# Application: admin
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


from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
    url(r'^user-management', include(admin.site.urls)),
    url(r'^backup-database$', 'admin.views.backup_database', name='backup_database'),
    url(r'^restore-database$', 'admin.views.restore_database', name='restore_database'),
    url(r'^user-requests$', 'admin.views.user_requests', name='user_requests'),
    url(r'^contact-messages$', 'admin.views.contact_messages', name='contact_messages'),
    url(r'^xml-schemas/module-management', 'admin.views.module_management', name='module_management'),
    url(r'^xml-schemas/module-add', 'admin.views.module_add', name='module_add'),
    url(r'^xml-schemas$', 'admin.views.manage_schemas', name='xml-schemas'),
    url(r'^xml-schemas/manage-schemas', 'admin.views.manage_schemas', name='xml-schemas-manage-schemas'),
    url(r'^manage-versions', 'admin.views.manage_versions', name='manage-versions'),
    url(r'^xml-schemas/manage-types', 'admin.views.manage_types', name='xml-schemas-manage-types'),
    url(r'^repositories$', 'admin.views.federation_of_queries', name='federation_of_queries'),
    url(r'^repositories/add-repository', 'admin.views.add_repository', name='add_repository'),
    url(r'^repositories/refresh-repository', 'admin.views.refresh_repository', name='refresh_repository'),
    url(r'^website$', 'admin.views.website', name='website'),
    url(r'^website/privacy-policy$', 'admin.views.privacy_policy_admin', name='privacy-policy-admin'),
    url(r'^website/terms-of-use$', 'admin.views.terms_of_use_admin', name='terms-of-use-admin'),
)
