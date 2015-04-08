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
    url(r'^create_backup', 'admin.ajax.create_backup'),
    url(r'^restore_backup', 'admin.ajax.restore_backup'),
    url(r'^delete_backup', 'admin.ajax.delete_backup'),
    url(r'^remove_message', 'admin.ajax.remove_message'),
    url(r'^edit_instance', 'admin.ajax.edit_instance'),
    url(r'^delete_instance', 'admin.ajax.delete_instance'),
    url(r'^delete_module', 'admin.ajax.delete_module'),
    url(r'^init_module_manager', 'admin.ajax.init_module_manager'),
    url(r'^add_module_resource', 'admin.ajax.add_module_resource'),
    url(r'^upload_resource', 'admin.ajax.upload_resource'),
    url(r'^add_module', 'admin.ajax.add_module'),
    url(r'^accept_request', 'admin.ajax.accept_request'),
    url(r'^deny_request', 'admin.ajax.deny_request'),
    url(r'^set_schema_version_content', 'admin.ajax.set_schema_version_content'),
    url(r'^set_type_version_content', 'admin.ajax.set_type_version_content'),
    url(r'^upload_version', 'admin.ajax.upload_version'),
    url(r'^set_current_version', 'admin.ajax.set_current_version'),
    url(r'^assign_delete_custom_message', 'admin.ajax.assign_delete_custom_message'),
    url(r'^delete_version', 'admin.ajax.delete_version'),
    url(r'^restore_object', 'admin.ajax.restore_object'),
    url(r'^restore_version', 'admin.ajax.restore_version'),
    url(r'^edit_information', 'admin.ajax.edit_information'),
    url(r'^delete_object', 'admin.ajax.delete_object'),
    url(r'^clear_object', 'admin.ajax.clear_object'),
    url(r'^save_object', 'admin.ajax.save_object'),
    url(r'^save_version', 'admin.ajax.save_version'),
    url(r'^resolve_dependencies', 'admin.ajax.resolve_dependencies'),
    url(r'^add_bucket', 'admin.ajax.add_bucket'),
    url(r'^delete_bucket', 'admin.ajax.delete_bucket'),
    url(r'^upload_object', 'admin.ajax.upload_object'),
)
