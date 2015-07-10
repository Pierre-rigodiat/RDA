from models import PositiveIntegerInputModule, ChemicalElementMappingModule, ListToGraphInputModule

def positive_integer(request):
    return PositiveIntegerInputModule().view(request)

def chemical_element_mapping(request):
    return ChemicalElementMappingModule().view(request)

def list_to_graph(request):
    return ListToGraphInputModule().view(request)