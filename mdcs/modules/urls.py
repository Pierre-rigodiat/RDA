from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^resources$', 'modules.views.load_resources_view', name='load_resources'),
)

excluded = ['load_resources']