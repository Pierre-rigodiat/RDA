from modules.models import Module, ModuleError
from django.conf import settings
import os
from django.template import Context, Template
from abc import abstractmethod


RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules/builtin/resources/')
TEMPLATES_PATH = os.path.join(RESOURCES_PATH, 'html/')


def render_module(template, params):
    """
        Purpose:
            renders the template with its context
        Input:
            template: path to HTML template to render
            params: parameters to create a context for the template
    """
    with open(template, 'r') as template_file:
        template_content = template_file.read()
        template = Template(template_content)
        context = Context(params)
        module = template.render(context)
        return module


class PopupModule(Module):
    def __init__(self, scripts=None, styles=None, popup_content=None, button_label=None):
        input_script = os.path.join(RESOURCES_PATH, 'js/popup.js')

        if scripts is not None:
            scripts.insert(0, input_script)
        else:
            scripts = [input_script]

        Module.__init__(self, scripts=scripts, styles=styles)

        if popup_content is None or button_label is None:
            raise ModuleError("'popup_content' and 'button_label' are required.")
        else:
            self.popup_content = popup_content
            self.button_label = button_label

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'popup.html')
        params = {
            "popup_content": self.popup_content,
            "button_label": self.button_label
            }

        return render_module(template, params)

    @abstractmethod
    def get_default_display(self, request):
        pass

    @abstractmethod
    def get_default_result(self, request):
        pass

    @abstractmethod
    def process_data(self, request):
        pass


class InputModule(Module):
    def __init__(self, scripts=None, styles=None, label=None, default_value=None):
        input_script = os.path.join(RESOURCES_PATH, 'js/input.js')
        
        if scripts is not None:
            scripts.append(input_script)
        else:
            scripts =[input_script]
        
        Module.__init__(self, scripts=scripts, styles=styles)

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

    @abstractmethod
    def get_default_display(self, request):
        pass

    @abstractmethod
    def get_default_result(self, request):
        pass

    @abstractmethod
    def process_data(self, request):
        pass


class AsyncInputModule(Module):
    def __init__(self, scripts=None, styles=None, label=None, default_value=None, modclass=None):
        input_script = os.path.join(RESOURCES_PATH, 'js/async_input.js')
        
        if modclass is None:
            raise ModuleError("'modclass' is required.")
        else:
            self.modclass = modclass
        
        if scripts is not None:
            scripts.append(input_script)
        else:
            scripts =[input_script]
        
        Module.__init__(self, scripts=scripts, styles=styles)

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

    @abstractmethod
    def get_default_display(self, request):
        pass

    @abstractmethod
    def get_default_result(self, request):
        pass

    @abstractmethod
    def process_data(self, request):
        pass


class InputButtonModule(Module):
    def __init__(self, scripts=None, styles=None, button_label=None, label=None, default_value=None):
        Module.__init__(self)

        if button_label is None:
            raise ModuleError("'button_label' is required.")
        else:
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


    @abstractmethod
    def get_default_display(self, request):
        pass

    @abstractmethod
    def get_default_result(self, request):
        pass

    @abstractmethod
    def process_data(self, request):
        pass


class OptionsModule(Module):
    def __init__(self, scripts=None, styles=None, label=None, opt_values=None, opt_labels=None):
        options_script = os.path.join(RESOURCES_PATH, 'js/options.js')
        
        if scripts is not None:
            scripts.append(options_script)
        else:
            scripts =[options_script]
        
        Module.__init__(self, scripts=scripts, styles=styles)

        if opt_values is None or opt_labels is None:
            raise ModuleError("'opt_values' and 'opt_labels' are required.")
        else:
            if len(opt_values) != len(opt_labels):
                raise ModuleError("'opt_values' and 'opt_labels' should have the same size.")
            else:
                self.opt_values = opt_values
                self.opt_labels = opt_labels

        self.label = label

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'options.html')
        options = ""
        for i in range(0, len(self.opt_values)):
            options += "<option value='" + self.opt_values[i] + "'>" + self.opt_labels[i] +"</option>"
        
        params = {"options": options}
        if self.label is not None:
            params.update({"label": self.label})
        return render_module(template, params)

    @abstractmethod
    def get_default_display(self, request):
        pass

    @abstractmethod
    def get_default_result(self, request):
        pass

    @abstractmethod
    def process_data(self, request):
        pass


class AutoCompleteModule(Module):
    def __init__(self, scripts=None, styles=None, label=None):
        input_script = os.path.join(RESOURCES_PATH, 'js/autocomplete.js')

        if scripts is not None:
            scripts.insert(0, input_script)
        else:
            scripts = [input_script]

        Module.__init__(self, scripts=scripts, styles=styles)

        self.label = label

    def get_module(self, request):
        if 'term' in request.GET:
            return self.process_data(request)

        template = os.path.join(TEMPLATES_PATH, 'autocomplete.html')
        params = {}

        if self.label is not None:
            params.update({"label": self.label})

        return render_module(template, params)

    @abstractmethod
    def get_default_display(self, request):
        pass

    @abstractmethod
    def get_default_result(self, request):
        pass

    @abstractmethod
    def process_data(self, request):
        pass
