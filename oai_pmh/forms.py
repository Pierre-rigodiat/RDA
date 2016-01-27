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

PROTOCOLS = (('http', 'HTTP'),
            ('https', 'HTTPS'))

class Registry(forms.Form):
    """
        A registry form
    """
    name           = forms.CharField(label='name', required=True)
    url            = forms.CharField(label='url', required=True)
    harvestrate    = forms.CharField(label='harvestrate', required=False)
    metadataprefix = forms.CharField(label='metadataprefix', required=False)
    identity       = forms.CharField(label='identity', required=False)
    sets           = forms.CharField(label='sets', required=False)
    description    = forms.CharField(label='description', required=False)

class AddRecord(forms.Form):
    """
        Add record form
    """
    content        = forms.CharField(label='content', required=True)

class Record(forms.Form):
    """
        A record form
    """
    identifier     = forms.CharField(label='identifier', required=True)

class GetRecord(forms.Form):
    """
        A record form
    """
    url     = forms.URLField(label='identifier', required=True)
    identifier     = forms.CharField(label='identifier', required=True)
    metadataprefix     = forms.CharField(label='metadataprefix', required=True)

class Url(forms.Form):
    """
        A record form
    """
    url     = forms.URLField(label='url', required=True)

class IdentifierForm(forms.Form):
    """
        A registry form
    """
    url            = forms.CharField(label='url', required=True)
    metadataprefix = forms.CharField(label='metadataprefix', required=True)
    sets           = forms.CharField(label='sets', required=False)

class ListRecordForm(forms.Form):
    """
        A registry form
    """
    url             = forms.CharField(label='url', required=True)
    metadataprefix  = forms.CharField(label='metadataprefix', required=True)
    sets            = forms.CharField(label='sets', required=False)
    resumptionToken = forms.CharField(label='resumptiontoken', required=False)
    fromDate        = forms.DateField(label='fromdate', required=False)
    untilDate       = forms.DateField(label='untildate', required=False)
