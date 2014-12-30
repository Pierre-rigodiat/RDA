################################################################################
#
# File Name: models.py
# Application: mgi
# Description: 
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
from django.db import models
from mongoengine import *

# Specific to MongoDB ordered inserts
from collections import OrderedDict
from pymongo import Connection
from bson.objectid import ObjectId
import xmltodict
import lxml.etree as etree
from email import email

# Create your models here.

# Class definitions
class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    
class Request(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)    

class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))

class Message(Document):
    name = StringField(max_length=100)
    email = EmailField()
    content = StringField()
    
class XMLSchema(models.Model):
    tree = etree.ElementTree
    
class Template(Document):
    title = StringField(required=True)
    filename = StringField(required=True)
    content = StringField(required=True)
    templateVersion = StringField(required=False)
    version = IntField(required=False)
    hash = StringField(required=True)
    user = IntField(required=False)
    
class TemplateVersion(Document):
    versions = ListField(StringField())
    deletedVersions = ListField(StringField())
    current = StringField()
    nbVersions = IntField(required=True)
    isDeleted = BooleanField(required=True)
    
class Type(Document):
    title = StringField(required=True)
    filename = StringField(required=True, unique=True)
    content = StringField(required=True)
    typeVersion = StringField(required=False)
    version = IntField(required=False)
    user = IntField(required=False)
    
class TypeVersion(Document):
    versions = ListField(StringField())
    deletedVersions = ListField(StringField())
    current = StringField()
    nbVersions = IntField(required=True)
    isDeleted = BooleanField(required=True)

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

class Instance(Document):
    name = StringField(required=True, unique=True)
    protocol = StringField(required=True) 
    address = StringField(required=True) 
    port = IntField(required=True)
    user = StringField(required=True)
    password = StringField(required=True)
    status = StringField()

class QueryResults(Document):
    results = ListField(required=True) 
    
class SparqlQueryResults(Document):
    results = StringField(required=True)
    
class SavedQuery(Document):
    user = StringField(required=True)
    template = StringField(required=True)    
    query = StringField(required=True)
    displayedQuery = StringField(required=True)

class ModuleResource(EmbeddedDocument):
    name = StringField(required=True)
    content = StringField(required=True)
    type = StringField(required=True)

class Module(Document):
    name = StringField(required=True)
    templates = ListField(StringField())
    tag = StringField(required=True)
    htmlTag = StringField(required=True)
    resources = ListField(EmbeddedDocumentField(ModuleResource))  
    
class XML2Download(Document):
    xml = StringField(required=True)
    
class PrivacyPolicy(Document):
    content = StringField()
    
class TermsOfUse(Document):
    content = StringField()

def postprocessor(path, key, value):
    if(key == "#text"):
        return key, str(value)
    try:
        return key, int(value)
    except (ValueError, TypeError):
        try:
            return key, float(value)
        except (ValueError, TypeError):
            return key, value
                                                                                                                                               
class Jsondata():
    """                                                                                                                                                                                                                       
        Wrapper to manage JSON Documents, like mongoengine would have manage them (but with ordered data)                                                                                                                     
    """

    def __init__(self, schemaID=None, xml=None, json=None, title=""):
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
        if (json is not None):
            # insert the json content after                                                                                                                                                                                       
            self.content['content'] = json
        else:
            # insert the json content after                                                                                                                                                                                       
            self.content['content'] = xmltodict.parse(xml, postprocessor=postprocessor)

    def save(self):
        """save into mongo db"""
        # insert the content into mongo db                                                                                                                                                                                    
        docID = self.xmldata.insert(self.content)
        return docID
    
    @staticmethod
    def objects():        
        """
            returns all objects as a list of dicts
             /!\ Doesn't return the same kind of objects as mongoengine.Document.objects()
        """
        # create a connection
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        # find all objects of the collection
        cursor = xmldata.find(as_class = OrderedDict)
        # build a list with the objects        
        results = []
        for result in cursor:
            results.append(result)
        return results
    
    @staticmethod
    def find(params):        
        """
            returns all objects that match params as a list of dicts 
             /!\ Doesn't return the same kind of objects as mongoengine.Document.objects()
        """
        # create a connection
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        # find all objects of the collection
        cursor = xmldata.find(params, as_class = OrderedDict)
        # build a list with the objects        
        results = []
        for result in cursor:
            results.append(result)
        return results
    
    @staticmethod
    def executeQuery(query):
        """queries mongo db and returns results data"""
        # create a connection
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        # query mongo db
        cursor = xmldata.find(query,as_class = OrderedDict)  
        # build a list with the xml representation of objects that match the query      
        queryResults = []
        for result in cursor:
            queryResults.append(result['content'])
        return queryResults
    
    @staticmethod
    def executeQueryFullResult(query):
        """queries mongo db and returns results data"""
        # create a connection
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        # query mongo db
        cursor = xmldata.find(query,as_class = OrderedDict)  
        # build a list with the xml representation of objects that match the query              
        results = []
        for result in cursor:
            results.append(result)
        return results

    @staticmethod
    def get(postID):
        """
            Returns the object with the given id
        """
        # create a connection
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        return xmldata.find_one({'_id': ObjectId(postID)})
    
    @staticmethod
    def delete(postID):
        """
            Delete the object with the given id
        """
        # create a connection
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        xmldata.remove({'_id': ObjectId(postID)})
    
    @staticmethod
    def update(postID, json):
        """
            Update the object with the given id
        """
        # create a connection
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        if '_id' in json:
            del json['_id']
        xmldata.update({'_id': ObjectId(postID)}, {"$set":json}, upsert=False)
    
        