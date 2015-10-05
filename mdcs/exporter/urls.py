from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
   url('', include('exporter.builtin.urls')),
)

