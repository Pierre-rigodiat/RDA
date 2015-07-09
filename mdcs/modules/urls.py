from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    url(r'^resources$', 'modules.views.load_resources_view'),
    url(r'^curator/', include('modules.curator.urls')),
    url(r'^diffusion/', include('modules.diffusion.urls')),    
    url(r'^test/', include('modules.test.urls')),
)