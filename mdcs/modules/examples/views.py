from models import PositiveIntegerInputModule, ExampleAutoCompleteModule, ChemicalElementMappingModule, \
    ListToGraphInputModule, CitationRefIdModule, SiblingsAccessorModule, FlagModule

def positive_integer(request):
    return PositiveIntegerInputModule().render(request)

def citation(request):
    return CitationRefIdModule().render(request)

def example_autocomplete(request):
    return ExampleAutoCompleteModule().render(request)

def chemical_element_mapping(request):
    return ChemicalElementMappingModule().render(request)

def list_to_graph(request):
    return ListToGraphInputModule().render(request)

def siblings_accessor(request):
    return SiblingsAccessorModule().render(request)

def flag(request):
    return FlagModule().render(request)

