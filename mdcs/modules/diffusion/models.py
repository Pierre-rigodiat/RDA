from modules.builtin.models import PopupModule
from django.conf import settings
import os
from modules.exceptions import ModuleError
import json
from modules.diffusion.forms import ExcelUploaderForm
from django.template import Context, Template
import lxml.etree as etree
from xlrd import open_workbook

RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules/diffusion/resources/')


class PeriodicTableModule(PopupModule):
    
    def __init__(self):
        with open(RESOURCES_PATH + 'html/periodic.html', 'r') as periodic_file:        
            periodic_table = periodic_file.read()

        PopupModule.__init__(self, popup_content=periodic_table, button_label='Select Element',
                             styles=[os.path.join(RESOURCES_PATH, 'css/periodic.css')],
                             scripts=[os.path.join(RESOURCES_PATH, 'js/periodic.js')])

    def _get_module(self, request):
        return PopupModule.get_module(self, request)

    def _get_display(self, request):
        if 'data' in request.GET:
            return 'Chosen element: ' + str(request.GET['data'])
        return 'No selected element.'

    def _get_result(self, request):
        if 'data' in request.GET:
            return str(request.GET['data'])
        return ''

    def _post_display(self, request):
        if 'selectedElement' not in request.POST:
            return self._get_display(request)
        else:
            return 'Chosen element: ' + request.POST['selectedElement']

    def _post_result(self, request):
        if 'selectedElement' not in request.POST:
            return self._get_result(request)

        return request.POST['selectedElement']


class PeriodicTableMultipleModule(PopupModule):

    def __init__(self):
        with open(RESOURCES_PATH + 'html/periodic_multiple.html', 'r') as periodic_file:
            periodic_table = periodic_file.read()

        PopupModule.__init__(self, popup_content=periodic_table, button_label='Select Elements',
                             styles=[os.path.join(RESOURCES_PATH, 'css/periodic.css'),
                                     os.path.join(RESOURCES_PATH, 'css/periodic_multiple.css')],
                             scripts=[os.path.join(RESOURCES_PATH, 'js/periodic_multiple.js')])

    def _get_module(self, request):
        return PopupModule.get_module(self, request)

    def _get_display(self, request):
        if 'data' in request.GET:
            constituents = etree.XML(request.GET['data'])
            
            if len(constituents) == 0:
                return 'No element selected.'
            else:
                constituents_disp = '<table class="table table-striped element-list">'
                constituents_disp += '<thead><tr>'
                constituents_disp += '<th>Element</th>'
                constituents_disp += '<th>Quantity</th>'
                constituents_disp += '<th>Purity</th>'
                constituents_disp += '<th>Error</th>'
                constituents_disp += '</tr></thead>'
                constituents_disp += '<tbody>'

                for constituent in constituents:
                    constituent_elements = list(constituent)
                    name = ""
                    quantity = ""
                    purity = ""
                    error = ""
                    for constituent_element in constituent_elements:
                        if constituent_element.tag == 'element':
                            if constituent_element.text is None:
                                name = ''
                            else:
                                name = constituent_element.text
                        elif constituent_element.tag == 'quantity':
                            if constituent_element.text is None:
                                quantity = ''
                            else:
                                quantity = constituent_element.text
                        elif constituent_element.tag == 'purity':
                            if constituent_element.text is None:
                                purity = ''
                            else:
                                purity = constituent_element.text
                        elif constituent_element.tag == 'error':
                            if constituent_element.text is None:
                                error = ''
                            else:
                                error = constituent_element.text
                
                    constituents_disp += '<tr>'
                    constituents_disp += "<td>" + name + "</td>"
                    constituents_disp += "<td>" + quantity + "</td>"
                    constituents_disp += "<td>" + purity + "</td>"
                    constituents_disp += "<td>" + error + "</td>"
                    constituents_disp += '</tr>'

                constituents_disp += '</tbody>'
                constituents_disp += '</table>'

            return constituents_disp
        return 'No element selected.'

    def _get_result(self, request):
        if 'data' in request.GET:
            result = ''
            constituents = etree.XML(request.GET['data'])
            for constituent in constituents:
                result += etree.tostring(constituent)
            return result
        return ''

    def _post_display(self, request):
        if 'elementList' in request.POST:
            element_list = json.loads(request.POST['elementList'])

            if len(element_list) == 0:
                return 'No element selected.'
            else:
                element_list_disp = '<table class="table table-striped element-list">'
                element_list_disp += '<thead><tr>'
                element_list_disp += '<th>Element</th>'
                element_list_disp += '<th>Quantity</th>'
                element_list_disp += '<th>Purity</th>'
                element_list_disp += '<th>Error</th>'
                element_list_disp += '</tr></thead>'
                element_list_disp += '<tbody>'

                for element in element_list:
                    element_list_disp += '<tr>'
                    element_list_disp += "<td>" + element['name'] + "</td>"
                    element_list_disp += "<td>" + element['qty'] + "</td>"
                    element_list_disp += "<td>" + element['pur'] + "</td>"
                    element_list_disp += "<td>" + element['err'] + "</td>"
                    element_list_disp += '</tr>'

                element_list_disp += '</tbody>'
                element_list_disp += '</table>'

            return element_list_disp
        else:
            return self._get_display(request)

    def _post_result(self, request):
        if 'elementList' in request.POST:
            element_list = json.loads(request.POST['elementList'])

            if len(element_list) == 0:
                element_list_xml = self._get_result(request)
            else:
                element_list_xml = ""

                for element in element_list:
                    element_list_xml += '<constituent>'
                    element_list_xml += "<element>" + element['name'] + "</element>"
                    element_list_xml += "<quantity>" + element['qty'] + "</quantity>"
                    element_list_xml += "<purity>" + element['pur'] + "</purity>"
                    element_list_xml += "<error>" + element['err'] + "</error>"
                    element_list_xml += '</constituent>'

            return element_list_xml
        else:
            return self._get_result(request)

    # def get_default_display(self, request):
    #     return "No elements selected"
    #
    # def get_default_result(self, request):
    #     return ""

    # def process_data(self, request):
    #     if 'elementList' in request.POST:
    #         element_list = json.loads(request.POST['elementList'])
    #
    #         if len(element_list) == 0:
    #             element_list_disp = self.get_default_display(request)
    #             element_list_xml = ""
    #         else:
    #             element_list_disp = '<table class="table table-striped element-list">'
    #             element_list_disp += '<thead><tr>'
    #             element_list_disp += '<th>Element</th>'
    #             element_list_disp += '<th>Quantity</th>'
    #             element_list_disp += '<th>Purity</th>'
    #             element_list_disp += '<th>Error</th>'
    #             element_list_disp += '</tr></thead>'
    #             element_list_disp += '<tbody>'
    #
    #             element_list_xml = ""
    #
    #             for element in element_list:
    #                 element_list_xml += '<constituent>'
    #                 element_list_xml += "<element>" + element['name'] + "</element>"
    #                 element_list_xml += "<quantity>" + element['qty'] + "</quantity>"
    #                 element_list_xml += "<purity>" + element['pur'] + "</purity>"
    #                 element_list_xml += "<error>" + element['err'] + "</error>"
    #                 element_list_xml += '</constituent>'
    #
    #                 element_list_disp += '<tr>'
    #                 element_list_disp += "<td>" + element['name'] + "</td>"
    #                 element_list_disp += "<td>" + element['qty'] + "</td>"
    #                 element_list_disp += "<td>" + element['pur'] + "</td>"
    #                 element_list_disp += "<td>" + element['err'] + "</td>"
    #                 element_list_disp += '</tr>'
    #
    #             element_list_disp += '</tbody>'
    #             element_list_disp += '</table>'
    #
    #         return element_list_disp, element_list_xml
    #     else:
    #         raise ModuleError('Selected Element not properly sent to server. '
    #                           'Please set "selectedElement" in POST data.')


class ExcelUploaderModule(PopupModule):
    def __init__(self):
        self.xml = None
        
        with open(RESOURCES_PATH + 'html/ExcelUploader.html', 'r') as excel_uploader_file:        
            excel_uploader = excel_uploader_file.read()            
            template = Template(excel_uploader)
            context = Context({'form': ExcelUploaderForm()})
            popup_content = template.render(context)
        
        PopupModule.__init__(self, popup_content=popup_content, button_label='Upload Excel File',
                             scripts=[os.path.join(RESOURCES_PATH, 'js/exceluploader.js')])

    def _get_module(self, request):
        return PopupModule.get_module(self, request)

    def _get_display(self, request):
        if 'data' in request.GET:
            return 'Data uploaded.'
        return 'No file selected'

    def _get_result(self, request):
        if 'data' in request.GET:
            result = ''
            elements = etree.XML(request.GET['data'])
            for element in elements:
                result += etree.tostring(element)
            return result
        return ''

    def _post_display(self, request):
        form = ExcelUploaderForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ModuleError('Data not properly sent to server. Please set "file" in POST data.')

        
        try:
            input_excel = request.FILES['file']
            book = open_workbook(file_contents=input_excel.read())
        
            root = etree.Element("table")
            root.set("name", str(input_excel))
            header = etree.SubElement(root, "headers")
            values = etree.SubElement(root, "rows")
        
            for sheet in book.sheets():
                for rowIndex in range(sheet.nrows):
                    if rowIndex != 0:
                        row = etree.SubElement(values, "row")
                        row.set("id", str(rowIndex))
        
                    for colIndex in range(sheet.ncols):
                        if rowIndex == 0:
                            col = etree.SubElement(header, "column")
                        else:
                            col = etree.SubElement(row, "column")
        
                        col.set("id", str(colIndex))
                        col.text = str(sheet.cell(rowIndex, colIndex).value)
        
            xmlString = etree.tostring(header)
            xmlString += etree.tostring(values)
        
            self.xml = xmlString
            
            return input_excel.name + ' uploaded with success.'
        except:
            return 'Something went wrong. Be sure to upload an Excel file, with correct format.' 

    def _post_result(self, request):
        return self.xml if self.xml is not None else ''
    