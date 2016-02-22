################################################################################
#
# File Name: forms.py
# Application: Informatics Core
# Description:
#
# Author: Marcus Newrock
#         marcus.newrock@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from django import forms
from django.core.validators import MinValueValidator, URLValidator

PROTOCOLS = (('http', 'HTTP'),
            ('https', 'HTTPS'))

class RegistryForm(forms.Form):
    """
        A registry form
    """
    name = forms.CharField(widget=forms.HiddenInput(), required=False)
    url = forms.URLField(label='URL', required=True)
    harvestrate = forms.IntegerField(label='Harvestrate (seconds)', required=False, validators=[MinValueValidator(0)])
    harvest = forms.BooleanField(label='Harvest ?', widget=forms.CheckboxInput(attrs={'class':'cmn-toggle cmn-toggle-round'}), required=False, initial=True)
    id = forms.CharField(widget=forms.HiddenInput(), required=False)

class UpdateRegistryForm(forms.Form):
    """
        A registry update form
    """
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    harvestrate = forms.IntegerField(label='Harvestrate (seconds)', required=False)
    edit_harvest = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'cmn-toggle cmn-toggle-round'}), required=False)

class AddRecord(forms.Form):
    """
        Add record form
    """
    content = forms.CharField(label='content', required=True)

class Record(forms.Form):
    """
        A record form
    """
    identifier = forms.CharField(label='identifier', required=True)

class GetRecord(forms.Form):
    """
        A record form
    """
    url = forms.URLField(label='identifier', required=True)
    identifier = forms.CharField(label='identifier', required=True)
    metadataprefix = forms.CharField(label='metadataprefix', required=True)

class Url(forms.Form):
    """
        A record form
    """
    url = forms.URLField(label='url', required=True)

class IdentifierForm(forms.Form):
    """
        A registry form
    """
    url = forms.CharField(label='url', required=True)
    metadataprefix = forms.CharField(label='metadataprefix', required=True)
    sets = forms.CharField(label='sets', required=False)

class ListRecordForm(forms.Form):
    """
        A registry form
    """
    url = forms.CharField(label='url', required=True)
    metadataprefix = forms.CharField(label='metadataprefix', required=True)
    sets = forms.CharField(label='sets', required=False)
    resumptionToken = forms.CharField(label='resumptiontoken', required=False)
    fromDate = forms.DateField(label='fromdate', required=False)
    untilDate = forms.DateField(label='untildate', required=False)
