from modules.registry.models import RegistryCheckboxesModule, NamePIDModule, \
    RelevantDateModule


def registry_checkboxes_materialType(request):
    return RegistryCheckboxesModule(xml_tag='materialType').render(request)


def registry_checkboxes_structuralMorphology(request):
    return RegistryCheckboxesModule(xml_tag='structuralMorphology').render(request)


def registry_checkboxes_propertyClass(request):
    return RegistryCheckboxesModule(xml_tag='propertyClass').render(request)


def name_pid(request):
    return NamePIDModule().render(request)


def relevant_date(request):
    return RelevantDateModule().render(request)