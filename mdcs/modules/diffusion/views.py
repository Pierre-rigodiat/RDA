from models import PeriodicTableModule


def periodic_table_view(request):
    return PeriodicTableModule().view(request)


