from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^periodic-table', 'modules.builtin.views.PeriodicTableView'),
)