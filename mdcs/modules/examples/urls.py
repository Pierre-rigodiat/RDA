from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'positive-integer', 'modules.examples.views.positive_integer', name='Positive Integer'),
    # url(r'citation', 'modules.examples.views.citation', name='Citation'),
    url(r'autocomplete', 'modules.examples.views.example_autocomplete', name='Example autocomplete'),
    url(r'chemical-element-mapping', 'modules.examples.views.chemical_element_mapping', name='Chemical Element Mapping'),
    url(r'list-to-graph', 'modules.examples.views.list_to_graph', name='List to Graph'),
    url(r'siblings-accessor', 'modules.examples.views.siblings_accessor', name='Siblings Accessor'),
    url(r'flag-module', 'modules.examples.views.flag', name='Flags'),
)
