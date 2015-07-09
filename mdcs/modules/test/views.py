from models import PositiveIntegerInputModule

def positive_integer(request):
    return PositiveIntegerInputModule().view(request)