from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'blob-hoster', 'modules.curator.views.blob_hoster', name='BLOB Hoster'),
    url(r'raw-xml', 'modules.curator.views.raw_xml', name='Raw XML'),
    url(r'handle', 'modules.curator.views.handle', name='Handle'),
)
