from modules.builtin.models import CheckboxesModule

class RegistryCheckboxesModule(CheckboxesModule):
    
    def __init__(self):                
        CheckboxesModule.__init__(self, options={}, label='Select elements', name='chemical')

    def _get_module(self, request):
        return CheckboxesModule.get_module(self, request)

    def _get_display(self, request):
        return ''

    def _get_result(self, request):
        return ''

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        if 'data[]' in request.POST:
            return str(request.POST['data[]'])