from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'materialType', 'modules.registry.views.registry_checkboxes_materialType', name='Registry materialType Checkboxes'),
    url(r'structuralMorphology', 'modules.registry.views.registry_checkboxes_structuralMorphology', name='Registry structuralMorphology Checkboxes'),
    url(r'name-pid', 'modules.registry.views.name_pid', name='Name PID'),
)
