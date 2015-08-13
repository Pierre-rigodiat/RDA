from modules.builtin.models import PopupModule
from modules.exceptions import ModuleError
from modules.curator.forms import BLOBHosterForm
from django.template import Context, Template
from django.conf import settings
import os
from mgi.settings import BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI
from utils.BLOBHoster.BLOBHosterFactory import BLOBHosterFactory

RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules/curator/resources/')

class BlobHosterModule(PopupModule):
    def __init__(self):
        self.handle = None

        with open(RESOURCES_PATH + 'html/BLOBHoster.html', 'r') as blobhoster_file:        
            blobhoster = blobhoster_file.read()            
            template = Template(blobhoster)
            context = Context({'form': BLOBHosterForm()})
            popup_content = template.render(context)
        
        PopupModule.__init__(self, popup_content=popup_content, button_label='Upload File',
                             scripts=[os.path.join(RESOURCES_PATH, 'js/blobhoster.js')])

    def _get_module(self, request):
        return PopupModule.get_module(self, request)

    def _get_display(self, request):
        return 'No files selected'

    def _get_result(self, request):
        return ''

    def _is_data_valid(self, data):
        return True

    def _post_display(self, request):
        form = BLOBHosterForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ModuleError('Data not properly sent to server. Please set "contentType" and "file" in POST data.')

        content_type = request.POST['contentType']
        uploaded_file = request.FILES['file']
        bh_factory = BLOBHosterFactory(BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI)
        blob_hoster = bh_factory.createBLOBHoster()
        self.handle = blob_hoster.save(blob=uploaded_file, filename=uploaded_file.name, contentType=content_type)

        with open(RESOURCES_PATH + 'html/BLOBHosterDisplay.html', 'r') as display_file:
            display = display_file.read()
            template = Template(display)
            context = Context({'filename': uploaded_file.name, 'handle': self.handle})

        return template.render(context)

    def _post_result(self, request):
        return self.handle if self.handle is not None else ''
