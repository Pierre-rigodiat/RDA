import json
from rest_framework import status
from models import ModuleManager
from django.http import HttpResponse

def load_resources_view(request):
    script_set = []
    style_set = []

    for script in request.POST.getlist('scripts[]'):
        if script not in script_set:
            script_set.append(script)

    for style in request.POST.getlist('styles[]'):
        if style not in style_set:
            style_set.append(style)

    response = {
        'styles': [],
        'scripts': []
    }

    m = ModuleManager()
    response['styles'] = m.load_styles(style_set)
    response['scripts'] = m.load_scripts(script_set)

    return HttpResponse(json.dumps(response), status=status.HTTP_200_OK)
