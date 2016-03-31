################################################################################
#
# File Name: forms.py
# Application: Informatics Core
# Description:
#
# Author: Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from django import forms
from mgi.models import OaiXslt

class UploadOaiPmhXSLTForm(forms.Form):
    """
    Form to upload a new XSLT for OAI-PMH purpose
    """
    oai_name = forms.CharField(label='Enter XSLT name', max_length=100, required=True)
    oai_pmh_xslt_file = forms.FileField(label='Select a file',required=True)


class FormDataModelChoiceField(forms.ModelChoiceField):
    #Used to return the name of the xslt file
    def label_from_instance(self, obj):
        return obj.name

class AssociateXSLT(forms.Form):
    """
    Associate XSLTs to a metadata formats (per template)
    """

    def clean(self):
        #Check if an XSLT file is provided when the Metadata Format is activated
        cleaned_data = super(AssociateXSLT, self).clean()
        name = cleaned_data.get("oai_name")
        activated = cleaned_data.get("activated")
        xslt_file = cleaned_data.get("oai_pmh_xslt_file")
        #If not, raise validation error
        if activated and not xslt_file:
            raise forms.ValidationError("Please provide an XSLT File for the '%s' Metadata Format." % name)

    template_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    oai_my_mf_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    oai_name = forms.CharField(label='Enter XSLT name', max_length=100, required=True, widget=forms.TextInput(attrs={'readonly':'readonly', 'style': 'background-color:transparent;border:none'}))
    oai_pmh_xslt_file = FormDataModelChoiceField(queryset=OaiXslt.objects().all(), required=False, widget=forms.Select(attrs={'style':'width:500px'}))
    activated = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'cmn-toggle cmn-toggle-round'}), required=False)
