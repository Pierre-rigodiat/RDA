from models import PeriodicTableModule


def PeriodicTableView(request):
    return PeriodicTableModule().view(request)


