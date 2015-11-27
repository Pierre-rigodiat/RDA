from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'materialType', 'modules.registry.views.registry_checkboxes_materialType', name='Registry materialType Checkboxes'),
    url(r'structuralMorphology', 'modules.registry.views.registry_checkboxes_structuralMorphology', name='Registry structuralMorphology Checkboxes'),
    url(r'publisher-name-pid', 'modules.registry.views.publisher_name_pid', name='Publisher Name PID'),
    url(r'creator-name-pid', 'modules.registry.views.creator_name_pid', name='Creator Name PID'),
    url(r'contributor-name-pid', 'modules.registry.views.contributor_name_pid', name='Contributor Name PID'),
    url(r'name-name-pid', 'modules.registry.views.name_name_pid', name='Name Name PID'),
    url(r'type-name-pid', 'modules.registry.views.type_name_pid', name='Type Name PID'),
    url(r'ref-citation-name-pid', 'modules.registry.views.ref_citation_name_pid', name='Ref Citation Name PID'),
    url(r'title-name-pid', 'modules.registry.views.title_name_pid', name='Title Name PID'),
    url(r'relevant-date', 'modules.registry.views.relevant_date', name='Relevant Date'),
)

