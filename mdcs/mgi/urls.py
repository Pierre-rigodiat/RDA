################################################################################
#
# File Name: urls.py
# Application: mgi
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

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',

    url(r'^$', 'mgi.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^rest/', include('api.urls')),
    url(r'^docs/api', include('rest_framework_swagger.urls')),
    url(r'^admin/backup-database$', 'mgi.views.backup_database', name='backup_database'),
    url(r'^admin/restore-database$', 'mgi.views.restore_database', name='restore_database'),
    url(r'^admin/user-requests$', 'mgi.views.user_requests', name='user_requests'),
    url(r'^admin/xml-schemas/module-management', 'mgi.views.module_management', name='module_management'),
    url(r'^admin/xml-schemas/module-add', 'mgi.views.module_add', name='module_add'),
    url(r'^admin/xml-schemas$', 'mgi.views.manage_schemas', name='xml-schemas'),    
    url(r'^admin/xml-schemas/manage-schemas', 'mgi.views.manage_schemas', name='xml-schemas-manage-schemas'),
    url(r'^admin/manage-versions', 'mgi.views.manage_versions', name='manage-versions'),
    url(r'^admin/xml-schemas/manage-types', 'mgi.views.manage_types', name='xml-schemas-manage-types'),
    url(r'^admin/user-management', include(admin.site.urls)),
    url(r'^admin/federation-of-queries', 'mgi.views.federation_of_queries', name='federation_of_queries'),
    url(r'^curate/', include('curate.urls')),
    url(r'^curate/select-template', include('curate.urls')),
    url(r'^curate/select-hdf5file$', 'mgi.views.curate_select_hdf5file', name='curate-select-hdf5file'),
    url(r'^curate/upload-spreadsheet$', 'mgi.views.curate_upload_spreadsheet', name='curate-upload-spreadsheet'),
    url(r'^curate/enter-data$', 'mgi.views.curate_enter_data', name='curate-enter-data'),
    url(r'^curate/enter-data/download-XSD$', 'mgi.views.curate_enter_data_downloadxsd', name='curate-enter-data-downloadxsd'),
    url(r'^curate/enter-data/download-form$', 'mgi.views.curate_enter_data_downloadform', name='curate-enter-data-downloadform'),
    url(r'^curate/view-data$', 'mgi.views.curate_view_data', name='curate-view-data'),
    url(r'^curate/view-data/download-XML/$', 'mgi.views.curate_view_data_downloadxml', name='curate-view-data-downloadxml'),
    url(r'^explore/', include('explore.urls')),
    url(r'^explore/select-template', include('explore.urls')),
    url(r'^explore/customize-template$', 'mgi.views.explore_customize_template', name='expore-customize-template'),
    url(r'^explore/perform-search$', 'mgi.views.explore_perform_search', name='explore-perform-search'),
    url(r'^explore/results$', 'mgi.views.explore_results', name='explore-results'),
    url(r'^explore/results/download-results/$', 'mgi.views.explore_download_results', name='explore-download-results'),
    url(r'^explore/sparqlresults$', 'mgi.views.explore_sparqlresults', name='explore-sparqlresults'),
    url(r'^explore/results/download-sparqlresults/$', 'mgi.views.explore_download_sparqlresults', name='explore-download-sparqlresults'),   
    url(r'^compose/', include('compose.urls')),
    url(r'^compose/select-template', include('compose.urls')),
    url(r'^compose/build-template$', 'mgi.views.compose_build_template', name='compose-build-template'),
    url(r'^compose/download-XSD$', 'mgi.views.compose_downloadxsd', name='compose-downloadxsd'),
    url(r'^all-options', 'mgi.views.all_options', name='all-options'),
    url(r'^browse-all', 'mgi.views.browse_all', name='browse-all'),
    url(r'^login', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    url(r'^request-new-account', 'mgi.views.request_new_account', name='request-new-account'),   
    url(r'^logout', 'mgi.views.logout_view', name='logout'),
    url(r'^my-profile$', 'mgi.views.my_profile', name='my-profile'),
    url(r'^my-profile/edit', 'mgi.views.my_profile_edit', name='my-profile-edit'),
    url(r'^my-profile/change-password', 'mgi.views.my_profile_change_password', name='my-profile-change-password'),
    url(r'^help', 'mgi.views.help', name='help'),
    url(r'^contact', 'mgi.views.contact', name='contact'),
    url(r'^privacy-policy', 'mgi.views.privacy_policy', name='privacy-policy'),
    url(r'^terms-of-use', 'mgi.views.terms_of_use', name='terms-of-use'),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')), # django-dajaxice
)

urlpatterns += staticfiles_urlpatterns()
