from modules.models import Module, ModuleError
from django.conf import settings
import os
# from django.template import Context, Template
# from abc import abstractmethod
from modules import render_module

RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules/builtin/resources/')
TEMPLATES_PATH = os.path.join(RESOURCES_PATH, 'html/')
SCRIPTS_PATH = os.path.join(RESOURCES_PATH, 'js/')
STYLES_PATH = os.path.join(RESOURCES_PATH, 'css/')

class InputModule(Module):
    def __init__(self, scripts=list(), styles=list(), label=None, default_value=None):
        Module.__init__(self)

        self.add_scripts([os.path.join(SCRIPTS_PATH, 'input.js')])
        self.add_scripts(scripts)

        self.add_styles(styles)

        self.label = label
        self.default_value = default_value

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'input.html')
        params = {}

        if self.label is not None:
            params.update({"label": self.label})

        if self.default_value is not None:
            params.update({"default_value": self.default_value})

        return render_module(template, params)


class OptionsModule(Module):
    def __init__(self, scripts=list(), styles=list(), label=None, options=dict()):
        Module.__init__(self)

        self.add_scripts([os.path.join(SCRIPTS_PATH, 'options.js')])
        self.add_scripts(scripts)

        self.add_styles(styles)

        if len(options) == 0:
            raise ModuleError("'options' variablie is required.")

        self.options = options
        self.label = label

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'options.html')
        options_html = ""

        for key, val in self.options.items():
            options_html += "<option value='" + key + "'>" + val + "</option>"

        params = {"options": options_html}

        if self.label is not None:
            params.update({"label": self.label})

        return render_module(template, params)


class PopupModule(Module):
    def __init__(self, scripts=list(), styles=list(), popup_content=None, button_label='Save'):
        Module.__init__(self)

        self.add_scripts([os.path.join(SCRIPTS_PATH, 'popup.js')])
        self.add_scripts(scripts)

        self.add_styles(styles)

        if popup_content is None:
            raise ModuleError("'popup_content' and is required. Cannot instantiate an empty popup")

        self.popup_content = popup_content
        self.button_label = button_label

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'popup.html')
        params = {
            "popup_content": self.popup_content,
            "button_label": self.button_label
        }

        return render_module(template, params)


class AsyncInputModule(Module):
    def __init__(self, scripts=list(), styles=list(), label=None, default_value=None, modclass=None):
        Module.__init__(self)

        self.add_scripts([os.path.join(SCRIPTS_PATH, 'async_input.js')])
        self.add_scripts(scripts)

        self.add_styles(styles)

        if modclass is None:
            raise ModuleError("'modclass' is required.")

        self.modclass = modclass
        self.label = label
        self.default_value = default_value

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'async_input.html')
        params = {'class': self.modclass}
        if self.label is not None:
            params.update({"label": self.label})
        if self.default_value is not None:
            params.update({"default_value": self.default_value})
        return render_module(template, params)


class InputButtonModule(Module):
    def __init__(self, scripts=list(), styles=list(), button_label='Send', label=None, default_value=None):
        Module.__init__(self)

        # self.add_scripts([os.path.join(SCRIPTS_PATH, 'async_input.js')])
        self.add_scripts(scripts)
        self.add_styles(styles)

        # if button_label is None:
        #     raise ModuleError("'button_label' is required.")
        # else:
        self.button_label = button_label
        self.label = label
        self.default_value = default_value

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'input_button.html')
        params = {"button_label": self.button_label}
        if self.label is not None:
            params.update({"label": self.label})
        if self.default_value is not None:
            params.update({"default_value": self.default_value})
        return render_module(template, params)


class TextAreaModule(Module):
    def __init__(self, scripts=list(), styles=list(), label=None):
        Module.__init__(self)

        self.add_scripts([os.path.join(SCRIPTS_PATH, 'textarea.js')])
        self.add_scripts(scripts)

        self.add_styles([os.path.join(STYLES_PATH, 'textarea.css')])
        self.add_styles(styles)

        if label is None:
            raise ModuleError("'label' is required.")

        self.label = label

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'textarea.html')

        params = {"label": self.label, "data": "Insert XML here..."}

        if 'data' in request.GET:
            params['data'] = request.GET['data']

        return render_module(template, params)


class AutoCompleteModule(Module):
    def __init__(self, scripts=list(), styles=list(), label=None):
        Module.__init__(self)

        self.add_scripts([os.path.join(SCRIPTS_PATH, 'autocomplete.js')])
        self.add_scripts(scripts)

        self.add_styles(styles)

        self.label = label

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'autocomplete.html')
        params = {}

        if self.label is not None:
            params.update({"label": self.label})

        return render_module(template, params)
