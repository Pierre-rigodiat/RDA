from django.http import HttpResponse
import json
from exceptions import ModuleError
from django.template import Context, Template


from abc import ABCMeta, abstractmethod
from django.conf import settings
import os


class Module(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, template=None, params={}):
        if template is None:
            raise ModuleError('No base template selected. Provide a template to the module constructor. Available templates are: ' + str(TEMPLATES.keys()))
        
        self.template = template
        self.params = params
    
    def view(self, request):
        module = None
        moduleDisplay = None
        moduleResult = None
        
        if request.method == 'GET':
            try:
#                 self.params.update(self.set_params())
                module = self.get_module()
                moduleDisplay = self.get_default_display()
                moduleResult = self.get_default_result()                
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
                if 'moduleDisplay' not in request.POST or 'moduleResult' not in request.POST:
                    raise ModuleError('Current values of display and results should be sent in JSON body.')
                moduleDisplay, moduleResult = self.post(request)
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
        #return HttpResponse(module)
        return HttpResponse(json.dumps(response), content_type='application/javascript')

    
#     @abstractmethod
#     def get(self, request):
#         """
#             Method:
#                 Get the module to insert in the form and default values
#             Input:
#                 request: HTTP request
#             Outputs:
#                 module: input to be inserted in the form
#                 moduleDisplay: Default value to display (can be None)
#                 moduleResult: Default result (can be None)
#         """
#         raise NotImplementedError("This method is not implemented.")    
    
    @abstractmethod
    def post(self, request):
        """
            Method:
                Send data to the server (called before editing or saving)
            Input:
                request: HTTP request
                request.POST['moduleDisplay']: value of moduleDisplay
                request.POST['moduleResult']: value of moduleResult
            Outputs:
                moduleDisplay: Value to display
                moduleResult: Result (can be a value or valid XML)
        """
        raise NotImplementedError("This method is not implemented.")

    def get_module(self):
        """
            Method:
                Get the module to insert in the form.
            Outputs:
                module: input to be inserted in the form
        """
        # check template in available templates
        if self.template in TEMPLATES.keys():
            # check parameters in template's parameters
            for param_name in self.params.keys():                
                if (param_name not in TEMPLATES[self.template]['parameters']['required'] and
                   param_name not in TEMPLATES[self.template]['parameters']['optional']):                    
                    raise ModuleError('At least one of the parameters provided to the template is not expected. Required parameters: ' + str(TEMPLATES[self.template]['parameters']['required']) + ', Optional parameters: ' + str(TEMPLATES[self.template]['parameters']['optional']) )                                
            # check that all required parameters are present
            for required_param in TEMPLATES[self.template]['parameters']['required']:
                if required_param not in self.params.keys():
                    raise ModuleError('One of the required parameters is missing. Required parameters are: ' + str(TEMPLATES[self.template]['parameters']['required']))
                
            # load template with context
            with open(TEMPLATES[self.template]['path'], 'r') as template_file:
                template_content = template_file.read()
                template = Template(template_content)
                context = Context(self.params) 
                module = template.render(context)
                return module       
        else:
            raise ModuleError('The selected template does not exist. Available templates are: ' + str(TEMPLATES.keys()))

#     @abstractmethod
#     def set_params(self):   
#         """
#             Method:
#                 Set parameters for template. Allows actions on the server.
#             Input:
# 
#             Outputs:
#                 params: dict = {"param_name": "param_value"}
#         """
#         return dict()
    
    @abstractmethod
    def get_default_display(self):
        """
            Method:
                Get the default value to be displayed in the form.
            Outputs:
                default displayed value
        """
        raise NotImplementedError("This method is not implemented.")
    
    @abstractmethod
    def get_default_result(self):
        """
            Method:
                Get the default value to be stored in the form.
            Outputs:
                default result value
        """
        raise NotImplementedError("This method is not implemented.")
    


TEMPLATES_PATH = os.path.join(settings.SITE_ROOT, 'modules/templates/')
TEMPLATES = {
             "input": 
                {
                "path": TEMPLATES_PATH + "input.html",
                "parameters":
                    {
                    "required" : [],
                    "optional" : ["label","default_value"]
                    }
                },
             "input_button": 
                {
                "path": TEMPLATES_PATH + "input_button.html",
                "parameters":
                    {
                    "required" : ["button_label"],
                    "optional" : ["label","default_value"], 
                    }
                },
             "options":
                {
                "path": TEMPLATES_PATH + "options.html",
                "parameters":
                    {
                    "required" : [],
                    "optional" : ["label","default_value"], 
                    }
                }, 
             "popup":
                {
                "path": TEMPLATES_PATH + "popup.html",
                "parameters":
                    {
                    "required" : ["popup_content", "button_label"],
                    "optional" : [], 
                    }
                }, 
             "free":
                {
                "path": TEMPLATES_PATH + "free.html",
                "parameters":
                    {
                    "required" : ["content"],
                    "optional" : [], 
                    }
                }, 
             }
    
    
