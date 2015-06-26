from modules.models import Module
from django.conf import settings
import os


RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules/builtin/resources/')


class PeriodicTableModule(Module):
    
    def __init__(self, template=None, params=None):
        with open(RESOURCES_PATH + 'html/periodic.html', 'r') as periodic_file:        
            periodic_table = periodic_file.read()
            
        template ='popup'
        params = {
                  'popup_content': periodic_table,
                  'button_label': 'Select Element'
                  }
        
        Module.__init__(self, template, params)
        
    def get_default_display(self):
        return "No element selected"
        
    def get_default_result(self):
        return ""
    
    def post(self, request):
        pass