from models import PositiveIntegerInputModule, ExampleAutoCompleteModule, ChemicalElementMappingModule, ListToGraphInputModule

def positive_integer(request):
    return PositiveIntegerInputModule().render(request)

def example_autocomplete(request):
    return ExampleAutoCompleteModule().render(request)

def chemical_element_mapping(request):
    return ChemicalElementMappingModule().render(request)

def list_to_graph(request):
    return ListToGraphInputModule().render(request)

