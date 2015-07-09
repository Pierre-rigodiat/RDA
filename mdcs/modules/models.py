from django.http import HttpResponse
import json
from exceptions import ModuleError

from abc import ABCMeta, abstractmethod


class Module(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, scripts=None, styles=None):
        self.scripts = scripts
        self.styles = styles
        
    def view(self, request):
        module = None
        moduleDisplay = None
        moduleResult = None
        
        if request.method == 'GET':
            if 'type' in request.GET and request.GET['type'] == 'resources':            
                response = {
                    'moduleStyle': self.styles,
                    'moduleScript': self.scripts
                }
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
    
    def get_resources(self):
        """
        
        """
        moduleScripts = []
        moduleStyles = []
        
        if self.scripts is not None:
            try:
                for script in self.scripts:
                    external = False
                    try:
                        if script.startswith('http://') or script.startswith('https://'):
                            external = True
                    except:
                        raise ModuleError('Scripts should be string of characters. It can be a path to a resource or an URL.')
                                                            
                    if external:
                        script_tag = '<script src="' + script + '"></script>'    
                        moduleScripts.append(script_tag)
                    else:                        
                        with open(script, 'r') as script_file:
                            script_tag = '<script>' + script_file.read() + '</script>'    
                        moduleScripts.append(script_tag)
            except:
                raise ModuleError('An error occurred during the reading of resources. Make sure that you are only using urls to external resources or paths to resources inside the application.')
        
        if self.styles is not None:
            try:
                for style in self.styles:
                    external = False
                    try:
                        if style.startswith('http://') or style.startswith('https://'):
                            external = True
                    except:
                        raise ModuleError('Styles should be string of characters. It can be a path to a resource or an URL.')
                                                            
                    if external:
                        style_tag = '<link rel="stylesheet" type="text/css" href="' + style + '"></link>'    
                        moduleStyles.append(style_tag)
                    else:                        
                        with open(style, 'r') as style_file:
                            style_tag = '<style>' + style_file.read() + '</style>'    
                        moduleStyles.append(style_tag)
            except:
                raise ModuleError('An error occurred during the reading of resources. Make sure that you are only using urls to external resources or paths to resources inside the application.')
            
        return moduleScripts, moduleStyles
    



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


class ModuleManager(object):

    def load_scripts(self, scripts):
        module_scripts = []

        try:
            for script in reversed(list(scripts)):
                external = False
                try:
                    if script.startswith('http://') or script.startswith('https://'):
                        external = True
                except:
                    raise ModuleError('Scripts should be string of characters. It can be a path to a resource or an URL.')

                if external:
                    script_tag = '<script src="' + script + '"></script>'
                    module_scripts.append(script_tag)
                else:
                    with open(script, 'r') as script_file:
                        script_tag = '<script>' + script_file.read() + '</script>'
                    module_scripts.append(script_tag)
        except:
            raise ModuleError('An error occurred during the reading of resources. Make sure that you are only using urls to external resources or paths to resources inside the application.')

        return module_scripts

    def load_styles(self, styles):
        module_styles = []

        try:
            for style in reversed(list(styles)):
                external = False
                try:
                    if style.startswith('http://') or style.startswith('https://'):
                        external = True
                except:
                    raise ModuleError('Styles should be string of characters. It can be a path to a resource or an URL.')

                if external:
                    style_tag = '<link rel="stylesheet" type="text/css" href="' + style + '"></link>'
                    module_styles.append(style_tag)
                else:
                    with open(style, 'r') as style_file:
                        style_tag = '<style>' + style_file.read() + '</style>'
                    module_styles.append(style_tag)
        except:
            raise ModuleError('An error occurred during the reading of resources. Make sure that you are only using urls to external resources or paths to resources inside the application.')

        return module_styles