from modules.models import Module, ModuleError
from django.conf import settings
import os
from django.template import Context, Template
from abc import abstractmethod


TEMPLATES_PATH = os.path.join(settings.SITE_ROOT, 'modules/builtin/resources/html/')


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
    def __init__(self, popup_content=None, button_label=None):
        Module.__init__(self)

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
    def __init__(self, label=None, default_value=None):
        Module.__init__(self)

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


class InputButtonModule(Module):
    def __init__(self, button_label=None, label=None, default_value=None):
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
    def __init__(self, options=None, label=None, default_value=None):
        Module.__init__(self)

        if options is None:
            raise ModuleError("'options' is required.")
        else:
            self.options = options

        self.label = label
        self.default_value = default_value

    def get_module(self, request):
        template = os.path.join(TEMPLATES_PATH, 'options.html')
        params = {"options": self.options}
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