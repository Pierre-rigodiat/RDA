from modules.registry.models import RegistryCheckboxesModule, NamePIDModule, \
    RelevantDateModule


def registry_checkboxes_materialType(request):
    return RegistryCheckboxesModule(xml_tag='materialType').render(request)


def registry_checkboxes_structuralMorphology(request):
    return RegistryCheckboxesModule(xml_tag='structuralMorphology').render(request)


def publisher_name_pid(request):
    return NamePIDModule('publisher').render(request)


def creator_name_pid(request):
    return NamePIDModule('creator').render(request)


def contributor_name_pid(request):
    return NamePIDModule('contributor').render(request)


def name_name_pid(request):
    return NamePIDModule('name').render(request)


def type_name_pid(request):
    return NamePIDModule('type').render(request)


def ref_citation_name_pid(request):
    return NamePIDModule('referenceCitation').render(request)


def title_name_pid(request):
    return NamePIDModule('title').render(request)


def relevant_date(request):
    return RelevantDateModule(xml_tag='date').render(request)