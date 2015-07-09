from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'positive-integer', 'modules.test.views.positive_integer', name='Positive Integer'),
    url(r'chemical-element-mapping', 'modules.test.views.chemical_element_mapping', name='Chemical Element Mapping'),
)