from modules.builtin.models import PopupModule
from django.conf import settings
import os


RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules/diffusion/resources/')


class PeriodicTableModule(PopupModule):
    
    def __init__(self):
        with open(RESOURCES_PATH + 'html/periodic.html', 'r') as periodic_file:        
            periodic_table = periodic_file.read()

        PopupModule.__init__(self, popup_content=periodic_table, button_label='Select Element')

    def get_default_display(self, request):
        return "No element selected"
        
    def get_default_result(self, request):
        return ""
    
    def process_data(self, request):
        pass