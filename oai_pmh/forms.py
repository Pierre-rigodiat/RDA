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
from django.core.validators import MinValueValidator
from mgi.models import OaiRegistry, OaiMetadataFormat, OaiSet, Template, TemplateVersion

VERBS = (('0', 'Pick one'),
         ('1', 'Identify'),
         ('2', 'Get Record'),
         ('3', 'List Records'),
         ('4', 'List Sets'),
         ('5', 'List Identifiers'),
         ('6', 'List Metadata Formats'))


class MyRegistryForm(forms.Form):
    """
        A my registry form
    """
    name = forms.CharField(label='Name', required=True)
    repo_identifier = forms.CharField(label='Repository Identifier', required=True)
    enable_harvesting = forms.BooleanField(label='Enable Harvesting ?', widget=forms.CheckboxInput(attrs={'class':'cmn-toggle cmn-toggle-round', 'visibility': 'hidden'}), required=False, initial=False)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)

class RegistryForm(forms.Form):
    """
        A registry form
    """
    name = forms.CharField(widget=forms.HiddenInput(), required=False)
    url = forms.URLField(label='URL', required=True)
    harvestrate = forms.IntegerField(label='Harvestrate (seconds)', required=False, validators=[MinValueValidator(0)])
    harvest = forms.BooleanField(label='Harvest ?', widget=forms.CheckboxInput(attrs={'class':'cmn-toggle cmn-toggle-round', 'visibility': 'hidden'}), required=False, initial=True)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)

class UpdateRegistryForm(forms.Form):
    """
        A registry update form
    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    harvestrate = forms.IntegerField(label='Harvestrate (seconds)', required=False)
    edit_harvest = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'cmn-toggle cmn-toggle-round'}), required=False)


class MyMetadataFormatForm(forms.Form):
    """
        A MyMetadataFormatForm form
    """
    metadataPrefix = forms.CharField(label='Metadata Prefix', required=True, widget=forms.TextInput(attrs={'placeholder': 'example: oai_dc'}))
    schema = forms.CharField(label='Schema URL', required=True)
    # metadataNamespace = forms.CharField(label='Namespace URL', required=True)
    # xmlSchema = forms.FileField(label='Select a file')


class FormDataModelChoiceFieldTemplateMF(forms.ModelChoiceField):
    #Used to return the name of the xslt file
    def label_from_instance(self, obj):
        return obj.title


class MyTemplateMetadataFormatForm(forms.Form):
    """
        A MyTemplateMetadataFormatForm form
    """
    metadataPrefix = forms.CharField(label='Metadata Prefix', required=True, widget=forms.TextInput(attrs={'placeholder': 'example: oai_dc'}))
    template = FormDataModelChoiceFieldTemplateMF(label='Template', queryset=[])

    def __init__(self, *args, **kwargs):
        templatesVersionID = Template.objects.distinct(field="templateVersion")
        templatesID = TemplateVersion.objects(pk__in=templatesVersionID, isDeleted=False).distinct(field="current")
        templates = Template.objects(pk__in=templatesID).all()
        super(MyTemplateMetadataFormatForm, self).__init__(*args, **kwargs)
        self.fields['template'].queryset = []
        self.fields['template'].queryset = templates

class MySetForm(forms.Form):
    """
        A MyMetadataFormatForm form
    """
    setSpec = forms.CharField(label='Set spec', required=True)
    setName = forms.CharField(label='Set name', required=True)

class UpdateMyMetadataFormatForm(forms.Form):
    """
        A UpdateMyMetadataFormatForm update form
    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    metadataPrefix = forms.CharField(label='Metadata Prefix', required=True)
    # schema = forms.CharField(label='Schema', required=True)
    # metadataNamespace = forms.CharField(label='Namespace', required=True)

class UpdateMySetForm(forms.Form):
    """
        A UpdateMySetForm update form
    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    setSpec = forms.CharField(label='Set spec', required=True)
    setName = forms.CharField(label='Set name', required=True)


class FormDataModelChoiceFieldMF(forms.ModelChoiceField):
    #Used to return the name of the xslt file
    def label_from_instance(self, obj):
        return obj.metadataPrefix


class FormDataModelChoiceFieldSet(forms.ModelChoiceField):
    #Used to return the name of the xslt file
    def label_from_instance(self, obj):
        return obj.setName


from django.contrib.admin.widgets import FilteredSelectMultiple

class SettingHarvestForm(forms.Form):
    """
        A UpdateMySetForm update form
    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    metadataFormats = FormDataModelChoiceFieldMF(label='Metadata Formats', queryset=[], widget=forms.CheckboxSelectMultiple(attrs={'class':'cmn-toggle cmn-toggle-round'}), empty_label=None, required=False)
    sets = FormDataModelChoiceFieldSet(label='Sets', queryset=[], required=False, widget=forms.CheckboxSelectMultiple(attrs={'class':'cmn-toggle cmn-toggle-round'}), empty_label=None)

    def __init__(self, *args, **kwargs):
        if 'id' in kwargs:
            registryId = kwargs.pop('id')

        metadataFormats = OaiMetadataFormat.objects(registry=str(registryId)).all()
        sets = OaiSet.objects(registry=str(registryId)).all()

        super(SettingHarvestForm, self).__init__(*args, **kwargs)
        self.fields['id'].initial = registryId
        self.fields['metadataFormats'].initial = [mf.id for mf in metadataFormats if mf.harvest]
        self.fields['metadataFormats'].queryset = []
        self.fields['metadataFormats'].queryset = metadataFormats
        self.fields['sets'].initial = [set.id for set in sets if set.harvest]
        self.fields['sets'].queryset = []
        self.fields['sets'].queryset = sets


class Url(forms.Form):
    """
        A record form
    """
    url = forms.URLField(label='url', required=True)

class RequestForm(forms.Form):
    """
        A request form
    """
    dataProvider= forms.ChoiceField(label='Data Provider', choices=[], required=False, widget=forms.Select(attrs={'style':'width:500px'}))
    verb = forms.ChoiceField(label='Verb', choices=VERBS, required=False, widget=forms.Select(attrs={'style':'width:500px'}))
    set = forms.ChoiceField(label='Set', choices=[], required=False, widget=forms.Select(attrs={'style':'width:500px', 'disabled':'true', 'class':'form-control'}))
    identifiers = forms.CharField(label='Identifier', required=False)
    metadataprefix = forms.ChoiceField(label='Matadata Prefix', choices=[], required=False, widget=forms.Select(attrs={'style':'width:500px', 'disabled':'true'}))
    From = forms.CharField(label='From', required=False, widget=forms.DateInput(attrs={'data-date-format':'yyyy-mm-ddThh:ii:00Z'}))
    until = forms.CharField(label='Until', required=False, widget=forms.DateInput(attrs={'data-date-format':'yyyy-mm-ddThh:ii:00Z'}))
    resumptionToken = forms.CharField(label='Resumption Token', required=False)

    def __init__ (self):
        super(RequestForm, self).__init__()
        self.dataproviders = []
        self.dataproviders.append(('0', 'Pick one'))
        self.fields['metadataprefix'].choices = self.dataproviders
        self.fields['set'].choices = self.dataproviders
        for o in OaiRegistry.objects.all():
            self.dataproviders.append((str(o.id)+'|'+o.url, str(o.name)))
        self.fields['dataProvider'].choices = self.dataproviders
