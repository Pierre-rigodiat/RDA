from django.conf import settings

def domain_context_processor(request):
    domain_params = {
        'CUSTOM_TITLE': settings.CUSTOM_TITLE,
        'CUSTOM_SUBTITLE': settings.CUSTOM_SUBTITLE,
        'CUSTOM_DATA': settings.CUSTOM_DATA,
        'CUSTOM_DESCRIPTION': settings.CUSTOM_DESCRIPTION,
    }
    return domain_params