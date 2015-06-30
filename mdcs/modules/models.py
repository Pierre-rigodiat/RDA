from django.http import HttpResponse
import json
from exceptions import ModuleError

from abc import ABCMeta, abstractmethod


class Module(object):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.resources = {}
        self.resources['script'] = []
        self.resources['style'] = []
        
    def view(self, request):
        module = None
        moduleDisplay = None
        moduleResult = None
        
        if request.method == 'GET':
            if 'type' in request.GET and request.GET['type'] == 'resources':            
                response = {}
                self.get_resources()
                response['moduleStyle'] = self.resources['style']
                response['moduleScript'] = self.resources['script']
                return HttpResponse(json.dumps(response), content_type='application/javascript')
            else:
                try:
                    module = self.get_module(request)
                    moduleDisplay = self.get_default_display(request)
                    moduleResult = self.get_default_result(request)
                except Exception, e:
                    raise ModuleError('Something went wrong during module initialization: ' + e.message)
                
                # check returned values? 
                
                # module should be HTML and should not be null
                if module is None:
                    raise ModuleError('Module value cannot be None. Module initialization cannot be completed.')   
                else:
                    # check HTML or raise exception
                    pass
                
                if moduleDisplay is not None:
                    # check HTML or raise exception
                    pass
                
                if moduleResult is not None:
                    # check is value or valid XML or raise exception
                    pass
                
        elif request.method == 'POST':
            try:
                moduleDisplay, moduleResult = self.process_data(request)
            except Exception, e:
                raise ModuleError('Something went wrong during module execution: ' + e.message)
            # check returned values?
            if moduleDisplay is not None:
                # check HTML
                pass
            else:
                raise ModuleError('The module returned nothing to display.')
            
            if moduleResult is not None:
                # check is value or valid XML or raise exception
                pass
            else:
                raise ModuleError('The module returned no result.')
        else:
            raise ModuleError('Only GET and POST methods can be used to communicate with a module.')            
         
        response = {}
        if module is not None:
            response['module'] = module
        if moduleDisplay is not None:
            response['moduleDisplay'] = moduleDisplay
        if moduleResult is not None:
            response['moduleResult'] = moduleResult
        return HttpResponse(json.dumps(response), content_type='application/javascript')
    
    @abstractmethod
    def get_resources(self):
        pass
#         module_style = self.get_module_style()
#         
#         for style in module_style:
#             pass
#         
#         module_script = self.get_module_script()
#         
#         for script in module_script:
#             pass
    

    @abstractmethod
    def process_data(self, request):
        """
            Method:
                Process data received from the client and send back the result and what to display.
            Input:
                request: HTTP request
                request.POST['moduleDisplay']: value of moduleDisplay
                request.POST['moduleResult']: value of moduleResult
            Outputs:
                moduleDisplay: Value to display
                moduleResult: Result (can be a value or valid XML)
        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def get_module(self, request):
        """
            Method:
                Get the module to insert in the form.
            Outputs:
                module: input to be inserted in the form
        """
        raise NotImplementedError("This method is not implemented.")

    
    @abstractmethod
    def get_default_display(self, request):
        """
            Method:
                Get the default value to be displayed in the form.
            Outputs:
                default displayed value
        """
        raise NotImplementedError("This method is not implemented.")
    
    @abstractmethod
    def get_default_result(self, request):
        """
            Method:
                Get the default value to be stored in the form.
            Outputs:
                default result value
        """
        raise NotImplementedError("This method is not implemented.")