from modules.builtin.models import InputModule, OptionsModule, AsyncInputModule, AutoCompleteModule
from modules.exceptions import ModuleError
from django.conf import settings
import os

RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules/examples/resources/')

class PositiveIntegerInputModule(InputModule):
    
    def __init__(self):
        InputModule.__init__(self, label='Enter positive integer', default_value=1)

    def _get_module(self, request):
        if 'data' in request.GET:
            self.default_value = request.GET['data']

        return InputModule.get_module(self, request)

    def _is_data_valid(self, data):
        try:
            value = int(data)
            if value > 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def _get_display(self, request):
        if 'data' in request.GET:
            self.default_value = request.GET['data']

        return str(self.default_value)+" is a valid positive integer"

    def _get_result(self, request):
        return ''

    # def _post_module(self, request):
    #     return ''

    def _post_display(self, request):
        data = str(request.POST['data'])

        return data + " is a positive integer" if self._is_data_valid(data) else data + " is not a positive integer"

    def _post_result(self, request):
        return ''


class ChemicalElementMappingModule(OptionsModule):
    
    def __init__(self):
        self.values = ['Ac', 
                  'Al', 
                  'Ag',
                  'Am', 
                  'Ar', 
                  'As', 
                  'At', 
                  'Au']
        self.labels = ['Actinium', 
                  'Aluminum',
                  'Silver', 
                  'Americium', 
                  'Argon', 
                  'Arsenic', 
                  'Astatine', 
                  'Gold']
                
        OptionsModule.__init__(self, opt_values=self.values, opt_labels=self.labels, label='Select an element')

    def get_default_display(self, request):
        return self.labels[0] + " is selected"
        
    def get_default_result(self, request):
        return self.values[0]
    
    def process_data(self, request):
        if 'value' in request.POST:
            try:
                value = request.POST['value']
                idxValue = self.values.index(value)
                label = self.labels[idxValue]
            except:
                raise ModuleError('Bad value sent to server.')
            moduleDisplay = label  + " is selected"
            moduleResult = value
            
            return moduleDisplay, moduleResult
        else:
            raise ModuleError('Value not properly sent to server. Please set "value" in POST data.')



class ListToGraphInputModule(AsyncInputModule):
    
    def __init__(self):
        AsyncInputModule.__init__(self, label='Enter a list of numbers', modclass='list_to_graph',
                             styles=[os.path.join(RESOURCES_PATH, 'css/list_to_graph.css')],
                             scripts=["https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js",
                                      os.path.join(RESOURCES_PATH, 'js/list_to_graph.js')])

    def get_default_display(self, request):
        return ""
        
    def get_default_result(self, request):
        return ""
    
    def process_data(self, request):
        if 'value' in request.POST:
            moduleDisplay = "<div class='chart'></div>"
            moduleResult = request.POST['value']
            
            post_value = request.POST['value']
            values = post_value.split(' ')
            
            for value in values:
                try:
                    int(value)
                except:
                    moduleDisplay = "<b style='color:red;'>Expecting a list of integer values separated by spaces.</b>"
                    moduleResult = ""            
                            
            return moduleDisplay, moduleResult
        else:
            raise ModuleError('Value not properly sent to server. Please set "value" in POST data.')
        


class ExampleAutoCompleteModule(AutoCompleteModule):

    def __init__(self):
        self.data = [
            'Plastic',
            'Concrete',
            'Cement',
            'Material1',
            'Material2',
            'Material3',
            'Others'
        ]

        AutoCompleteModule.__init__(self, label='Material Name', scripts=[os.path.join(RESOURCES_PATH,
                                                                                       'js/example_autocomplete.js')])

    def get_default_display(self, request):
        return ""

    def get_default_result(self, request):
        return ""

    def process_data(self, request):
        if 'term' in request.GET:
            response_list = []

            for d in self.data:
                if request.GET['term'].lower() in d.lower():
                    response_list.append(d)

            return response_list
        else:
            pass
