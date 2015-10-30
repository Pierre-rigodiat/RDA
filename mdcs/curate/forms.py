################################################################################
#
# File Name: forms.py
# Application: curate
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django import forms
from mgi.models import FormData


class NewForm(forms.Form):
    document_name = forms.CharField(label='', max_length=100, required=True)

class FormDataModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class OpenForm(forms.Form):
    forms = FormDataModelChoiceField(label='', queryset=FormData.objects().none())

    def __init__(self, *args, **kwargs):
        if 'forms' in kwargs:
            qs = kwargs.pop('forms')
        else:
            qs = FormData.objects().none()   
        super(OpenForm, self).__init__(*args, **kwargs)
        self.fields['forms'].queryset = qs

class UploadForm(forms.Form):
    file = forms.FileField(label='')

ADVANCED_OPTIONS = (
                    ('min_tree','Minimum Tree'),
                    ('siblings_mod','Siblings Modules'),
                    )

class AdvancedOptionsForm(forms.Form):
    options = forms.MultipleChoiceField(label='', required=False, widget=forms.CheckboxSelectMultiple, choices=ADVANCED_OPTIONS)
    
class SaveDataForm(forms.Form):

    def is_valid(self):
        return super(SaveDataForm, self).is_valid() and self.data['title'].strip() != ""

    title = forms.CharField(label='Save As', min_length=1, max_length=100, required=True)
