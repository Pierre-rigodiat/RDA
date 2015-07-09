from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'blob-hoster', 'modules.curator.views.blob_hoster', name='BLOB Hoster'),
)