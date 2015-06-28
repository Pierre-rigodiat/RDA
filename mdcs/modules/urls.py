from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^diffusion/', include('modules.diffusion.urls')),
)