from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^builtin/', include('modules.builtin.urls')),
)