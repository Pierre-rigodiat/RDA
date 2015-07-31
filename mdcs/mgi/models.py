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

from mongoengine import *

# Specific to MongoDB ordered inserts
from collections import OrderedDict
from bson.objectid import ObjectId
import xmltodict
from pymongo import MongoClient
from mgi.settings import MONGODB_URI

 
class Request(Document):
    """Represents a request sent by an user to get an account"""
    username = StringField(required=True)
    password = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    email = StringField(required=True)    

class Message(Document):
    """Represents a message sent via the Contact form"""
    name = StringField(max_length=100)
    email = EmailField()
    content = StringField()
    
class Template(Document):
    """Represents an XML schema template that defines the structure of data for curation"""
    title = StringField(required=True)
    filename = StringField(required=True)
    content = StringField(required=True)
    templateVersion = StringField(required=False)
    version = IntField(required=False)
    hash = StringField(required=True)
    user = StringField(required=False)
    dependencies = ListField(StringField())
    
class TemplateVersion(Document):
    """Manages versions of templates"""
    versions = ListField(StringField())
    deletedVersions = ListField(StringField())
    current = StringField()
    nbVersions = IntField(required=True)
    isDeleted = BooleanField(required=True)
    
class Type(Document):    
    """Represents an XML schema type to use to compose XML Schemas"""
    title = StringField(required=True)
    filename = StringField(required=True)
    content = StringField(required=True)
    typeVersion = StringField(required=False)
    version = IntField(required=False)
    hash = StringField(required=True)
    user = StringField(required=False)
    dependencies = ListField(StringField())
    
class TypeVersion(Document):
    """Manages versions of types"""
    versions = ListField(StringField())
    deletedVersions = ListField(StringField())
    current = StringField()
    nbVersions = IntField(required=True)
    isDeleted = BooleanField(required=True)
    
class MetaSchema(Document):
    """Stores more information about templates/types"""
    schemaId = StringField(required=True, unique=True)
    flat_content = StringField(required=True)
    api_content = StringField(required=True)

class Htmlform(Document):
    """Represents an HTML form saved during curation"""
    title = StringField(required=True)
    schema = StringField(required=True)
    content = StringField(required=True)
    occurrences = StringField(required=True)

class Instance(Document):
    """Represents an instance of a remote MDCS"""
    name = StringField(required=True, unique=True)
    protocol = StringField(required=True) 
    address = StringField(required=True) 
    port = IntField(required=True)
    access_token = StringField(required=True)
    refresh_token = StringField(required=True)
    expires = DateTimeField(required=True)

class QueryResults(Document):
    """Stores results from a query (Query By Example)"""
    results = ListField(required=True) 
    
class SparqlQueryResults(Document):
    """Stores results from a query (SPARQL endpoint)"""
    results = StringField(required=True)
    
class SavedQuery(Document):
    """Represents a query saved by the user (Query by Example)"""
    user = StringField(required=True)
    template = StringField(required=True)    
    query = StringField(required=True)
    displayedQuery = StringField(required=True)

class Module(Document):
    """Represents a module, that will replace an existing input during curation"""
    name = StringField(required=True)
    url = StringField(required=True)  
    
class XML2Download(Document):
    """Temporarily stores the content of an XML document to download"""
    xml = StringField(required=True)
    
class PrivacyPolicy(Document):
    """Privacy Policy of the MDCS"""
    content = StringField()
    
class TermsOfUse(Document):
    """Terms of Use of the MDCS"""
    content = StringField()
    
class Bucket(Document):
    """Represents a bucket to store types by domain"""
    label = StringField(required=True, unique=True)
    color = StringField(required=True, unique=True)
    types = ListField()

def postprocessor(path, key, value):
    """Called after XML to JSON transformation"""
    if(key == "#text"):
        return key, str(value)
    try:
        return key, int(value)
    except (ValueError, TypeError):
        try:
            return key, float(value)
        except (ValueError, TypeError):
            return key, value


# Admin
class XSDElement(Document):
    xsd_xpath = StringField()
    minOccurs = FloatField()
    maxOccurs = FloatField()

class XSDStructure(Document):
    template = ReferenceField(Template)
    xsd_elements = ListField(ReferenceField(XSDElement))

# Curate
# good one
class XMLElement(Document):
    xsd_xpath = StringField() #xsd_element = ReferenceField(XSDElement)
    nbOccurs = IntField()
    minOccurs = FloatField()
    maxOccurs = FloatField()

# good one
class FormElement(Document):
    html_id = StringField()
    xml_xpath = StringField() # pour siblings module
    xml_element = ReferenceField(XMLElement)

# good one
class FormData(Document):
    """
        Stores data being entered and not yet curated
    """
    user = StringField(required=True)
    template = StringField(required=True)
    elements = DictField() # when loading form, just needed to work on the form, has to be regenerated when loading new document, can auto save that
    xml_data = StringField() # on save data (get active with no parent, then active children, take the name + value...)

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
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client['mgi']
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
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client['mgi']
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
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client['mgi']
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
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client['mgi']
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
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client['mgi']
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
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        return xmldata.find_one({'_id': ObjectId(postID)})
    
    @staticmethod
    def delete(postID):
        """
            Delete the object with the given id
        """
        # create a connection
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        xmldata.remove({'_id': ObjectId(postID)})
    
    @staticmethod
    def update(postID, json):
        """
            Update the object with the given id
        """
        # create a connection
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client['mgi']
        # get the xmldata collection
        xmldata = db['xmldata']
        if '_id' in json:
            del json['_id']
        xmldata.update({'_id': ObjectId(postID)}, {"$set":json}, upsert=False)
    
        