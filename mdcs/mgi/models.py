################################################################################
#
# File Name: models.py
# Application: mgi
# Description: 
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django import forms
from django.db import models
from mongoengine import *

# Specific to MongoDB ordered inserts
from collections import OrderedDict
from pymongo import Connection
import xmltodict

# Create your models here.

# Class definitions
class Template(Document):
    title = StringField(required=True)
    filename = StringField(required=True)
    content = StringField(required=True)

class Ontology(Document):
    title = StringField(required=True)
    filename = StringField(required=True)
    content = StringField(required=True)

class Htmlform(Document):
    title = StringField(required=True)
    schema = StringField(required=True)
    content = StringField(required=True)

class Xmldata(Document):
    title = StringField(required=True)
    schema = StringField(required=True)
    content = StringField(required=True)

class Hdf5file(Document):
    title = StringField(required=True)
    schema = StringField(required=True)
    content = StringField(required=True)

class Database(Document):
    title = StringField(required=True)
    timestamp = StringField(required=True)
    content = StringField(required=True)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

class queryResults(Document):
    results = ListField(required=True) 
    
class sparqlQueryResults(Document):
    results = StringField(required=True)

# ORDERED DICT : Used by the Wrapper to insert numeric values as numbers (and not string)
def postprocessor(path, key, value):
    try:
        return key, int(value)
    except (ValueError, TypeError):
        try:
            return key, float(value)
        except (ValueError, TypeError):
            return key, value
        
# ORDERED DICT : Wrapper to insert ordered dict into mongoDB, using mongoengine syntax                                                                                                                                        
class Jsondata():
    """                                                                                                                                                                                                                       
        Wrapper to manage JSON Documents, like mongoengine would have manage them (but with ordered data)                                                                                                                     
    """

    def __init__(self, schemaID=None, xml=None, title=""):
        """                                                                                                                                                                                                                   
            initialize the object                                                                                                                                                                                             
            schema = ref schema (Document)                                                                                                                                                                                    
            xml = xml string 
            title = title of the document                                                                                                                                                                                                 
        """
        # create a connection                                                                                                                                                                                                 
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        self.xmldata = db['xmldata']
        # create a new dict to keep the mongoengine order                                                                                                                                                                     
        self.content = OrderedDict()
        # insert the ref to schema                                                                                                                                                                                            
        self.content['schema'] = schemaID
        # insert the title                                                                                                                                                                                                    
        self.content['title'] = title
        # insert the json content after                                                                                                                                                                                       
        self.content['content'] = xmltodict.parse(xml, postprocessor=postprocessor)

    def save(self):
        """save into mongo db"""
        # insert the content into mongo db                                                                                                                                                                                    
        docID = self.xmldata.insert(self.content)
        return docID


#class Task(models.Model):
#    def foo(self):
#        return "bar"

