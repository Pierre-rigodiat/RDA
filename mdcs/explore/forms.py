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
#         Pierre Francois RIGODIAT
#		  pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django import forms
from mgi.models import Template

class ExportForm(forms.Form):
    my_exporters = forms.MultipleChoiceField(label='', choices=[], widget=forms.CheckboxSelectMultiple())
    EXPORT_OPTIONS = []
    def __init__(self, templateId=""):
        self.EXPORT_OPTIONS = []
        #We retrieve exporters for this template
        exporters = Template.objects.get(pk=templateId).exporters
        for exporter in exporters:
            if exporter.name != 'XSLT':
                #We add them
                self.EXPORT_OPTIONS.append((exporter.url,exporter.name))

        super(ExportForm, self).__init__()
        self.fields['my_exporters'].choices = []
        self.fields['my_exporters'].choices = self.EXPORT_OPTIONS

class FormDataModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "XSLT: "+ obj.title

class UploadXSLTForm(forms.Form):
    my_xslts = forms.MultipleChoiceField(label='', choices=[], widget=forms.CheckboxSelectMultiple())
    EXPORT_OPTIONS = []
    def __init__(self, templateId=""):
        self.EXPORT_OPTIONS = []
        #We retrieve all XSLTFiles available for this template
        xslts = Template.objects.get(pk=templateId).XSLTFiles
        for xslt in xslts:
            #We add them
            self.EXPORT_OPTIONS.append((xslt.id, xslt.title))

        super(UploadXSLTForm, self).__init__()
        self.fields['my_xslts'].choices = []
        self.fields['my_xslts'].choices = self.EXPORT_OPTIONS