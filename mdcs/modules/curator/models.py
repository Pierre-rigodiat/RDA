from modules.builtin.models import PopupModule
from modules.exceptions import ModuleError
from modules.curator.forms import BLOBHosterForm
from django.template import Context, Template
from django.conf import settings
import os
from mgi.settings import BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI
from utils.BLOBHoster.BLOBHosterFactory import BLOBHosterFactory
RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules/utils/resources/')

class BlobHosterModule(PopupModule):
    def __init__(self):
        with open(RESOURCES_PATH + 'html/BLOBHoster.html', 'r') as blobhoster_file:        
            blobhoster = blobhoster_file.read()            
            template = Template(blobhoster)
            context = Context({'form': BLOBHosterForm()})
            popup_content = template.render(context)
        
        PopupModule.__init__(self, popup_content=popup_content, button_label='Upload File',
                             scripts=[os.path.join(RESOURCES_PATH, 'js/blobhoster.js')])

    def get_default_display(self, request):
        return "No file selected."
        
    def get_default_result(self, request):
        return ""
    
    def process_data(self, request):        
        moduleDisplay = ""
        moduleResult = ""
        form = BLOBHosterForm(request.POST, request.FILES)
        if form.is_valid():
            contentType = request.POST['contentType']
            file = request.FILES['file']
            blobHosterFactory = BLOBHosterFactory(BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI)
            blobHoster = blobHosterFactory.createBLOBHoster()
            handle = blobHoster.save(blob=file, filename=file.name, contentType=contentType)
            
            with open(RESOURCES_PATH + 'html/BLOBHosterDisplay.html', 'r') as display_file:        
                display = display_file.read()            
                template = Template(display)
                context = Context({'filename': file.name, 'handle': handle})
                
            moduleDisplay = template.render(context)
            moduleResult = handle
        else:
            raise ModuleError('Data not properly sent to server. Please set "contentType" and "file" in POST data.')
        return moduleDisplay, moduleResult