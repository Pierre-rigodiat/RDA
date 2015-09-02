from HTMLParser import HTMLParser
from modules.builtin.models import PopupModule, TextAreaModule
from modules.exceptions import ModuleError
from modules.curator.forms import BLOBHosterForm
from django.template import Context, Template
from django.conf import settings
import os
from mgi.settings import BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI
from utils.BLOBHoster.BLOBHosterFactory import BLOBHosterFactory
from lxml import etree
from lxml.etree import XMLSyntaxError

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

#         content_type = request.POST['contentType']
        uploaded_file = request.FILES['file']
        bh_factory = BLOBHosterFactory(BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI)
        blob_hoster = bh_factory.createBLOBHoster()
        self.handle = blob_hoster.save(blob=uploaded_file, filename=uploaded_file.name, contentType="")

        with open(RESOURCES_PATH + 'html/BLOBHosterDisplay.html', 'r') as display_file:
            display = display_file.read()
            template = Template(display)
            context = Context({'filename': uploaded_file.name, 'handle': self.handle})

        return template.render(context)

    def _post_result(self, request):
        return self.handle if self.handle is not None else ''


class RawXMLModule(TextAreaModule):
    def __init__(self):
        self.parser = HTMLParser()

        TextAreaModule.__init__(self, label="Raw XML")

    def _get_module(self, request):
        return TextAreaModule.get_module(self, request)

    def _get_display(self, request):
        data = request.GET['data'] if 'data' in request.GET else ''

        return self.disp(data)

    def disp(self, data):
        if data == '':
            return '<span class="notice">Please enter XML in the text area located above</span>'

        try:
            self.parse_data(data)
            return '<span class="success">XML entered is well-formed</span>'
        except XMLSyntaxError, e:
            return '<span class="error">XML error: ' + e.message + '</span>'

    def parse_data(self, data):
        xml_string = ''

        unescaped_data = self.parser.unescape(data)
        xml_data = etree.fromstring(unescaped_data)

        for xml_child in xml_data.getchildren():
            xml_string += etree.tostring(xml_child)

        return xml_string

    def _get_result(self, request):
        if 'data' not in request.GET:
            return ''

        try:
            return self.parse_data(request.GET['data'])
        except XMLSyntaxError:
            return ''

    def _is_data_valid(self, data):
        try:
            self.parse_data(data)
            return True
        except XMLSyntaxError:
            return False

    def _post_display(self, request):
        data = request.POST['data'] if 'data' in request.POST else ''
        return self.disp(data)

    def _post_result(self, request):
        if 'data' not in request.POST:
            return ''

        try:
            return self.parse_data(request.POST['data'])
        except XMLSyntaxError:
            return ''
