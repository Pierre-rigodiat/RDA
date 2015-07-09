from models import PositiveIntegerInputModule, ChemicalElementMappingModule

def positive_integer(request):
    return PositiveIntegerInputModule().view(request)

def chemical_element_mapping(request):
    return ChemicalElementMappingModule().view(request)