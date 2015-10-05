from django.conf.urls import patterns, url

urlpatterns = patterns('',
   url('', 'exporter.builtin.models.BasicExporter', name='XML'),
   url('', 'exporter.builtin.models.XSLTExporter', name='XSLT'),
)

