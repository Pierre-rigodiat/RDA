from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^positive-integer', 'modules.test.views.positive_integer'),
)