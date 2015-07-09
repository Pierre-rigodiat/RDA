from modules.builtin.models import InputModule, OptionsModule
from modules.exceptions import ModuleError

class PositiveIntegerInputModule(InputModule):
    
    def __init__(self):
        InputModule.__init__(self, label='Enter positive integer', default_value=1)

    def get_default_display(self, request):
        return "1 is a valid positive integer"
        
    def get_default_result(self, request):
        return 1
    
    def process_data(self, request):
        if 'value' in request.POST:
            moduleDisplay = ""
            moduleResult = "" 
            
            try:
                value = int(request.POST['value'])
                if value > 0:
                    moduleDisplay = str(value) + " is a valid positive integer"
                    moduleResult = value
                else:
                    moduleDisplay = str(value) + " is not a positive integer"
                    moduleResult = ""
            except:                            
                moduleDisplay = str(request.POST['value']) + " is not a positive integer"
                moduleResult = ""
                            
            return moduleDisplay, moduleResult
        else:
            raise ModuleError('Value not properly sent to server. Please set "value" in POST data.')
        

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
        
