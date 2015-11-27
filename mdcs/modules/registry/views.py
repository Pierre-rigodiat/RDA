from modules.registry.models import RegistryCheckboxesModule, NamePIDModule


def registry_checkboxes_materialType(request):
    return RegistryCheckboxesModule(xml_tag='_materialType').render(request)

def registry_checkboxes_structuralMorphology(request):
    return RegistryCheckboxesModule(xml_tag='_structuralMorphology').render(request)

def name_pid(request):
    return NamePIDModule().render(request)