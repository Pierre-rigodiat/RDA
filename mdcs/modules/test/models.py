from modules.builtin.models import InputModule
from modules.exceptions import ModuleError

class PositiveIntegerInputModule(InputModule):
    
    def __init__(self):
        InputModule.__init__(self, label='Enter positive integer', default_value=1)

    
    
    def get_resources(self):
        InputModule.get_resources(self)
         
        


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
            except:                            
                moduleDisplay = str(value) + " is not a positive integer"
                moduleResult = ""
                            
            return moduleDisplay, moduleResult
        else:
            raise ModuleError('Value not properly sent to server. Please set "value" in POST data.')