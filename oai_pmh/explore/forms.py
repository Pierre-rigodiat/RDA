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
from django.core.validators import MinValueValidator
from mgi.models import OaiRegistry, OaiMetadataFormat
from django.forms.extras.widgets import SelectDateWidget
from itertools import groupby

class KeywordForm(forms.Form):
    """
    Create the form for the keyword search: input and checkboxes
    """
    my_registries = forms.MultipleChoiceField(label='', choices=[], widget=forms.CheckboxSelectMultiple(attrs={"checked":""}))
    search_entry = forms.CharField(widget=forms.TextInput(attrs={'class': 'research'}))

    REGISTRIES_OPTIONS = []
    def __init__(self, userId=""):
        self.SCHEMAS_OPTIONS = []
        self.REGISTRIES_OPTIONS = []

        #We retrieve all registries (data providers)
        registries = OaiRegistry.objects()

        for registry in registries:
            #We add them
            self.REGISTRIES_OPTIONS.append((registry.id, registry.name))
        super(KeywordForm, self).__init__()
        self.fields['my_registries'].choices = []
        self.fields['my_registries'].choices = self.REGISTRIES_OPTIONS
        self.my_registries_nb = len(self.REGISTRIES_OPTIONS)

class MetadataFormatsForm(forms.Form):
    """
    Create the form for the keyword search: input and checkboxes
    """
    my_schemas = forms.MultipleChoiceField(label='', choices=[], widget=forms.CheckboxSelectMultiple(attrs={"checked":""}))
    my_schemas_nb = 0
    SCHEMAS_OPTIONS = []

    def __init__(self, listRegistriesId=[]):
        self.SCHEMAS_OPTIONS = []
        #Retrieve registries name
        registriesName = {}
        for registryId in listRegistriesId:
            obj = OaiRegistry.objects(pk=registryId).get()
            registriesName[str(registryId)] = obj.name

        #We retrieve all common schemas
        schemas = OaiMetadataFormat.objects(registry__in=listRegistriesId)
        groups = []
        uniquekeys = []
        for k, g in groupby(schemas, lambda x: x.hash):
            groups.append(list(g))      # Store group iterator as a list
            uniquekeys.append(k)
        #TODO Group by HASH + First Name (Cacher tous sauf le premier) Premier checkbox pr tous + collapse avec les checkbox des autres

        # for schema in schemas:
        #     #We add them
        #     self.SCHEMAS_OPTIONS.append((schema.id, schema.metadataPrefix))
        for group in groups:
            name = group[0].metadataPrefix
            listValues = []
            for elt in group:
                listValues.append((str(elt.id), elt.metadataPrefix + ' (' + registriesName[str(elt.registry)] +")"))

            self.SCHEMAS_OPTIONS.append(((name, ( listValues ) )))
            # self.SCHEMAS_OPTIONS.append((('Library', ( ('vinyl', 'Vinyl'),('cd', 'CD') ) )))

        super(MetadataFormatsForm, self).__init__()
        self.fields['my_schemas'].choices = []
        self.fields['my_schemas'].choices = self.SCHEMAS_OPTIONS

        self.my_schemas_nb = len(self.SCHEMAS_OPTIONS)
