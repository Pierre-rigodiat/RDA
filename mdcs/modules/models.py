from HTMLParser import HTMLParser
import importlib
import os
from django.conf import settings
from django.http import HttpResponse
import json
from django.http.request import QueryDict
from django.utils.html import escape
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST
from exceptions import ModuleError

from abc import ABCMeta, abstractmethod
from modules.utils import sanitize
# from mdcs.modules.urls import urlpatterns
# from mgi import models
from modules import render_module


class Module(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, scripts=list(), styles=list()):
        self.scripts = scripts
        self.styles = styles

        self.template = os.path.join(settings.SITE_ROOT, 'templates/module.html')


    def add_scripts(self, scripts):
        pass

    def add_styles(self, styles):
        pass

    def render(self, request):
        if request.method == 'GET':
            if 'resources' in request.GET:
                return self._get_resources()
            else:
                return self._get(request)
        elif request.method == 'POST':
            return self._post(request)
        else:
            raise ModuleError('Only GET and POST methods can be used to communicate with a module.')

    def _get(self, request):
        # FIXME add additional check
        #   > TODO in get we only need url and data(optional)
        #   > TODO parameters needs to be sanitized
        if 'data' in request.GET:
            request.GET = {
                'data': sanitize(request.GET['data']),
                'url': request.GET['url']
            }

            if not self._is_data_valid(request.GET['data']):
                print 'Data ' + str(request.GET['data']) + ' is not valid'
                del request.GET['data']

        template_data = {
            'module': '',
            'display': '',
            'result': '',
            'url': request.GET['url']
        }

        try:
            template_data['module'] = self._get_module(request)
            template_data['display'] = self._get_display(request)
            template_data['result'] = self._get_result(request)
        except Exception, e:
            raise ModuleError('Something went wrong during module initialization: ' + e.message)

        # TODO Add additional checks
        for key, val in template_data.items():
            if val is None:
                raise ModuleError('Variable '+key+' cannot be None. Module initialization cannot be completed.')

        # Apply tags to the template
        html_code = render_module(self.template, template_data)
        return HttpResponse(html_code, status=HTTP_200_OK)

    def _post(self, request):
        # Sanitzing data from the request
        post_data = {}
        for key, value in request.POST.items():
            post_data[key] = sanitize(value)

        request.POST = post_data

        if not self._is_data_well_formed(request.POST['data']):
            return HttpResponse(status=HTTP_400_BAD_REQUEST)

        template_data = {
            'module': '',
            'display': '',
            'result': '',
            'url': ''
        }

        try:
            # template_data['module'] = self._post_module(request)
            template_data['display'] = self._post_display(request)
            template_data['result'] = self._post_result(request)

            html_parser = HTMLParser()
            for key in template_data.keys():
                template_data[key] = html_parser.unescape(template_data[key])
        except Exception, e:
            raise ModuleError('Something went wrong during module initialization: ' + e.message)

        html_code = render_module(self.template, template_data)
        return HttpResponse(html_code, status=HTTP_200_OK)
    
    def _get_resources(self):
        """
        
        """
        response = {
            'scripts': self.scripts,
            'styles': self.styles
        }

        return HttpResponse(json.dumps(response), status=HTTP_200_OK)

    def _is_data_well_formed(self, data):
        # TODO Implement this function
        return True

    @abstractmethod
    def _is_data_valid(self, data):
        """
            Method:
                Get the default value to be stored in the form.
            Outputs:
                default result value
        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def _get_module(self, request):
        """
            Method:
                Get the default value to be stored in the form.
            Outputs:
                default result value
        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def _get_display(self, request):
        """
            Method:
                Get the default value to be stored in the form.
            Outputs:
                default result value
        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def _get_result(self, request):
        """
            Method:
                Get the default value to be stored in the form.
            Outputs:
                default result value
        """
        raise NotImplementedError("This method is not implemented.")

    # @abstractmethod
    # def _post_module(self, request):
    #     """
    #         Method:
    #             Get the default value to be stored in the form.
    #         Outputs:
    #             default result value
    #     """
    #     raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def _post_display(self, request):
        """
            Method:
                Get the default value to be stored in the form.
            Outputs:
                default result value
        """
        raise NotImplementedError("This method is not implemented.")

    @abstractmethod
    def _post_result(self, request):
        """
            Method:
                Get the default value to be stored in the form.
            Outputs:
                default result value
        """
        raise NotImplementedError("This method is not implemented.")

    # @abstractmethod
    # def process_data(self, request):
    #     """
    #         Method:
    #             Process data received from the client and send back the result and what to display.
    #         Input:
    #             request: HTTP request
    #             request.POST['moduleDisplay']: value of moduleDisplay
    #             request.POST['moduleResult']: value of moduleResult
    #         Outputs:
    #             moduleDisplay: Value to display
    #             moduleResult: Result (can be a value or valid XML)
    #     """
    #     raise NotImplementedError("This method is not implemented.")
    #
    # @abstractmethod
    # def get_module(self, request):
    #     """
    #         Method:
    #             Get the module to insert in the form.
    #         Outputs:
    #             module: input to be inserted in the form
    #     """
    #     raise NotImplementedError("This method is not implemented.")
    #
    #
    # @abstractmethod
    # def get_default_display(self, request):
    #     """
    #         Method:
    #             Get the default value to be displayed in the form.
    #         Outputs:
    #             default displayed value
    #     """
    #     raise NotImplementedError("This method is not implemented.")
    #
    # @abstractmethod
    # def get_default_result(self, request):
    #     """
    #         Method:
    #             Get the default value to be stored in the form.
    #         Outputs:
    #             default result value
    #     """
    #     raise NotImplementedError("This method is not implemented.")
