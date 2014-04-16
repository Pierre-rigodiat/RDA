################################################################################
#
# File Name: urls.py
# Application: mgi
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
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
    # Examples:
    # url(r'^$', 'mgi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'mgi.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('api.urls')),
#    url(r'^admin/$', 'mgi.views.admin', name='admin'),
#    url(r'^admin/xml-schemas', include('xml_schemas.html')), # include(admin.site.urls)),
#    url(r'^admin/xml-schemas', include(admin.site.urls)),
#    url(r'^admin/user-management', include(admin.site.urls)),
    url(r'^admin/xml-schemas$', 'mgi.views.xml_schemas', name='xml-schemas'),
    url(r'^admin/xml-schemas/current-model', 'mgi.views.xml_schemas', name='xml-schemas-current-model'),
    url(r'^admin/xml-schemas/manage-schemas', 'mgi.views.manage_schemas', name='xml-schemas-manage-schemas'),
    url(r'^admin/xml-schemas/manage-modules', 'mgi.views.manage_modules', name='xml-schemas-manage-modules'),
#    url(r'^admin/xml-schemas/manage-queries', 'mgi.views.manage_queries', name='xml-schemas-manage-queries'),
    url(r'^admin/xml-schemas/manage-ontologies', 'mgi.views.manage_ontologies', name='xml-schemas-manage-ontologies'),
    url(r'^admin/user-management', include(admin.site.urls)),
    url(r'^curate/', include('curate.urls')),
#    url(r'^curate$', 'mgi.views.curate', name='curate'),
    url(r'^curate/select-template', include('curate.urls')),
#    url(r'^curate/select-template', 'mgi.views.curate_select_template', name='curate-select-template'),
    url(r'^curate/enter-data$', 'mgi.views.curate_enter_data', name='curate-enter-data'),
    url(r'^curate/view-data$', 'mgi.views.curate_view_data', name='curate-view-data'),
    url(r'^curate/view-data/download-XML$', 'mgi.views.curate_view_data_downloadxml', name='curate-view-data-downloadxml'),
    url(r'^curate/view-data/download-XSD$', 'mgi.views.curate_view_data_downloadxsd', name='curate-view-data-downloadxsd'),
    url(r'^view-schema', 'mgi.views.view_schema', name='view-schema'),
    url(r'^explore/', include('explore.urls')),
#    url(r'^explore', 'mgi.views.explore', name='explore'),
    url(r'^explore/select-template', include('explore.urls')),
    url(r'^explore/customize-template$', 'mgi.views.explore_customize_template', name='expore-customize-template'),
    url(r'^explore/perform-search$', 'mgi.views.explore_perform_search', name='explore-perform-search'),
    url(r'^contribute', 'mgi.views.contribute', name='contribute'),
    url(r'^all-options', 'mgi.views.all_options', name='all-options'),
    url(r'^browse-all', 'mgi.views.browse_all', name='browse-all'),
    url(r'^login', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
#    url(r'^login', 'mgi.views.login_view', name='login'),
    url(r'^logout', 'mgi.views.logout_view', name='logout'),
    url(r'^my-profile$', 'mgi.views.my_profile', name='my-profile'),
    url(r'^my-profile/edit', 'mgi.views.my_profile_edit', name='my-profile-edit'),
    url(r'^my-profile/change-password', 'mgi.views.my_profile_change_password', name='my-profile-change-password'),
    url(r'^help', 'mgi.views.help', name='help'),
    url(r'^contact', 'mgi.views.contact', name='contact'),
    url(r'^about', 'mgi.views.about', name='about'),
    url(r'^privacy-policy', 'mgi.views.privacy_policy', name='privacy-policy'),
    url(r'^terms-of-use', 'mgi.views.terms_of_use', name='terms-of-use'),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')), # django-dajaxice
#    url(r'', include('multiuploader.urls')), # django-multiuploader
)

urlpatterns += staticfiles_urlpatterns()
