from models import PeriodicTableModule, PeriodicTableMultipleModule


def periodic_table_view(request):
    return PeriodicTableModule().view(request)


def periodic_table_multiple_view(request):
    return PeriodicTableMultipleModule().view(request)
