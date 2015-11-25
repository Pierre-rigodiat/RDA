

class ChemicalElementCheckboxesModule(CheckboxesModule):
    
    def __init__(self):
        self.options = {
            'Ac': 'Actinium',
            'Al': 'Aluminum',
            'Ag': 'Silver',
            'Am': 'Americium',
            'Ar': 'Argon',
            'As': 'Arsenic',
            'At': 'Astatine',
            'Au': 'Gold'
        }
                
        CheckboxesModule.__init__(self, options=self.options, label='Select elements', name='chemical')

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