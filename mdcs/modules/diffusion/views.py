from models import PeriodicTableModule, PeriodicTableMultipleModule


def periodic_table_view(request):
    return PeriodicTableModule().render(request)


def periodic_table_multiple_view(request):
    return PeriodicTableMultipleModule().render(request)
