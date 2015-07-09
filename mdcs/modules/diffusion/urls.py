from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^periodic-table$', 'modules.diffusion.views.periodic_table_view', name='Periodic Table'),
    url(r'^periodic-table-multiple', 'modules.diffusion.views.periodic_table_multiple_view',
        name='Periodic Table Multiple'),
)
