from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'positive-integer', 'modules.test.views.positive_integer', name='Positive Integer'),
    url(r'autocomplete', 'modules.test.views.example_autocomplete', name='Example autocomplete'),
    url(r'chemical-element-mapping', 'modules.test.views.chemical_element_mapping', name='Chemical Element Mapping'),
    url(r'list-to-graph', 'modules.test.views.list_to_graph', name='List to Graph'),

)
