################################################################################
#
# File Name: views.py
# Application: api
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

# REST Framework
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
# Models
from mgi.models import SavedQuery, Jsondata, Template, TemplateVersion
# Serializers
from api.serializers import savedQuerySerializer, jsonDataSerializer, querySerializer, sparqlQuerySerializer, sparqlResultsSerializer, schemaSerializer, templateSerializer

from explore import sparqlPublisher
from curate import rdfPublisher
from lxml import etree
from django.conf import settings
import os
from mongoengine import *
from pymongo import Connection
from bson.objectid import ObjectId
import re

projectURI = "http://www.example.com/"

@api_view(['GET','POST'])
def savedQuery_list(request): 
    if request.method == 'GET':
        savedQueries = SavedQuery.objects
        serializer = savedQuerySerializer(savedQueries)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':        
        serializer = savedQuerySerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def savedQuery_detail(request, pk):
    """
    Retrieve, update or delete a saved query instance.
    """              
    try:
        savedQuery = SavedQuery.objects.get(pk=pk)
    except:
        content = {'message':'No saved query with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = savedQuerySerializer(savedQuery)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = savedQuerySerializer(savedQuery, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        savedQuery.delete()
        content = {'message':'The query was deleted with success.'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
def jsonData_list(request):
    if request.method == 'GET':
        jsonData = Jsondata.objects()
        serializer = jsonDataSerializer(jsonData)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    elif request.method == 'POST':        
        serializer = jsonDataSerializer(data=request.DATA)
        if serializer.is_valid():
            jsondata = Jsondata(schemaID = request.DATA['schema'], json = request.DATA['content'], title = request.DATA['title'])
            jsondata.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def jsonData_detail(request, pk):
    """
    Retrieve, update or delete a saved query instance.
    """              
    jsonData = Jsondata.get(pk)
    if jsonData is None:
        content = {'message':'No data with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = jsonDataSerializer(jsonData)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = jsonDataSerializer(jsonData, data=request.DATA)
        if serializer.is_valid():
            Jsondata.update(pk, request.DATA)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Jsondata.delete(pk)
        content = {'message':'Data deleted with success.'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def explore(request):
    """
    GET http://localhost/api/explore/select/all
    """
    jsonData = Jsondata.objects()
    serializer = jsonDataSerializer(jsonData)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def explore_detail(request):
    """
    GET http://localhost/api/explore/select
    id: string (ObjectId)
    schema: string (ObjectId)
    title: string
    """        
    id = request.QUERY_PARAMS.get('id', None)
    schema = request.QUERY_PARAMS.get('schema', None)
    title = request.QUERY_PARAMS.get('title', None)
    
    try:        
        query = dict()
        if id is not None:            
            query['_id'] = ObjectId(id)            
        if schema is not None:
            if schema[0] == '/' and schema[-1] == '/':
                query['schema'] = re.compile(schema[1:-1])
            else:
                query['schema'] = schema
        if title is not None:
            if title[0] == '/' and title[-1] == '/':
                query['title'] = re.compile(title[1:-1])
            else:
                query['title'] = title
        if len(query.keys()) == 0:
            content = {'message':'No parameters given.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            jsonData = Jsondata.executeQueryFullResult(query)
            serializer = jsonDataSerializer(jsonData)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        content = {'message':'No data found with the given parameters.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def explore_delete(request):
    """
    GET http://localhost/api/explore/delete
    id: string (ObjectId)
    """        
    id = request.QUERY_PARAMS.get('id', None)
    
    try:        
        query = dict()
        if id is not None:            
            query['_id'] = ObjectId(id)            
        if len(query.keys()) == 0:
            content = {'message':'No id given.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            Jsondata.delete(id)
            content = {'message':'Data deleted with success.'}
            return Response(content, status=status.HTTP_204_NO_CONTENT)
    except:
        content = {'message':'No data found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def query_by_example(request):
    """
    POST http://localhost/api/explore/query-by-example/
    POST data query="{'element':'value'}"
    """
    qSerializer = querySerializer(data=request.DATA)
    if qSerializer.is_valid():
        try:
            results = Jsondata.executeQueryFullResult(request.DATA['query'])
            jsonSerializer = jsonDataSerializer(results)        
            return Response(jsonSerializer.data, status=status.HTTP_200_OK)
        except:
            content = {'message':'Bad query: use the following format {\'element\':\'value\'}'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    return Response(qSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def sparql_query(request):
    """
    POST http://localhost/api/explore/sparql-query/
    POST data query="SELECT * WHERE {?s ?p ?o}" format="xml"
    """
    sqSerializer = sparqlQuerySerializer(data=request.DATA)
    if sqSerializer.is_valid():
        if 'format' in request.DATA:
            format = request.DATA['format']
            if (format.upper() == "TEXT"):
                query = '0' + request.DATA['query']
            elif (format.upper() == "XML"):
                query = '1' + request.DATA['query']
            elif (format.upper() == "CSV"):
                query = '2' + request.DATA['query']
            elif (format.upper() == "TSV"):
                query = '3' + request.DATA['query']
            elif (format.upper() == "JSON"):
                query = '4' + request.DATA['query']
            else:
                content = {'message':'Accepted formats: text, xml, csv, tsv, json'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            query = '0' + request.DATA['query']
         
        results = dict()  
        results['content'] = sparqlPublisher.sendSPARQL(query) 
        
        srSerializer = sparqlResultsSerializer(results)
        return Response(srSerializer.data, status=status.HTTP_200_OK)
    return Response(sqSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def curate(request):
    """
    POST http://localhost/api/curate/
    POST data title="title", schema="schemaID", content="<root>...</root>"
    """        
    serializer = jsonDataSerializer(data=request.DATA)
    if serializer.is_valid():
        try:
            schema = Template.objects.get(pk=ObjectId(request.DATA['schema']))
            templateVersion = TemplateVersion.objects.get(pk=ObjectId(schema.templateVersion))
            if str(schema.id) in templateVersion.deletedVersions:
                content = {'message: The provided schema is currently deleted.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'message: No schema found with the given id.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        xmlStr = request.DATA['content']
        try:
            try:
                xmlTree = etree.fromstring(xmlStr)
            except Exception, e:
                content = {'message: Unable to read the XML data: '+ e.message}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            #TODO: XML validation
#             xmlSchemaTree = etree.fromstring(schema.content)
#             xmlSchema = etree.XMLSchema(xmlSchemaTree)
#             try:
#                 xmlSchema.assertValid(xmlTree)
#             except Exception, e:
#                 content = {'message':e.message}
#                 return Response(content, status=status.HTTP_400_BAD_REQUEST)
#             jsondata = Jsondata(schemaID = request.DATA['schema'], xml = xmlStr, title = request.DATA['title'])
#             docID = jsondata.save()            

            #xsltPath = './xml2rdf3.xsl' #path to xslt on my machine
            #xsltFile = open(os.path.join(PROJECT_ROOT,'xml2rdf3.xsl'))
            xsltPath = os.path.join(settings.SITE_ROOT, 'static/resources/xsl/xml2rdf3.xsl')
            xslt = etree.parse(xsltPath)
            root = xslt.getroot()
            namespace = root.nsmap['xsl']
            URIparam = root.find("{" + namespace +"}param[@name='BaseURI']") #find BaseURI tag to insert the project URI
            URIparam.text = projectURI + str(docID)
        
            # SPARQL : transform the XML into RDF/XML
            transform = etree.XSLT(xslt)
            # add a namespace to the XML string, transformation didn't work well using XML DOM
            xmlStr = xmlStr.replace('>',' xmlns="' + projectURI + request.DATA['schema'] + '">', 1) #TODO: OR schema name...
            # domXML.attrib['xmlns'] = projectURI + schemaID #didn't work well
            domXML = etree.fromstring(xmlStr)
            domRDF = transform(domXML)
        
            # SPARQL : get the rdf string
            rdfStr = etree.tostring(domRDF)
        
            print "rdf string: " + rdfStr
        
            # SPARQL : send the rdf to the triplestore
            rdfPublisher.sendRDF(rdfStr)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            content = {'message: Unable to insert data.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_schema(request):
    """
    POST http://localhost/api/schema/add/
    POST data title="title", filename="filename", content="<xsd:schema>...</xsd:schema>" templateVersion="id"
    """
    sSerializer = schemaSerializer(data=request.DATA)
    if sSerializer.is_valid():
        # a template version is provided: if it exists, add the schema as a new version and manage the version numbers
        if "templateVersion" in request.DATA:
            try:
                templateVersions = TemplateVersion.objects.get(pk=request.DATA['templateVersion'])
                templateVersions.nbVersions = templateVersions.nbVersions + 1
                newTemplate = Template(title=request.DATA['title'], filename=request.DATA['filename'], content=request.DATA['content'], templateVersion=request.DATA['templateVersion'], version=templateVersions.nbVersions).save()
                templateVersions.versions.append(str(newTemplate.id))                
                templateVersions.save()
            except:
                content = {'message':'No template version found with the given id.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            templateVersion = TemplateVersion(nbVersions=1, isDeleted=False).save()
            newTemplate = Template(title=request.DATA['title'], filename=request.DATA['filename'], content=request.DATA['content'], version=1, templateVersion=str(templateVersion.id)).save()
            templateVersion.versions = [str(newTemplate.id)]
            templateVersion.current=str(newTemplate.id)
            templateVersion.save()
            newTemplate.save()
        return Response(sSerializer.data, status=status.HTTP_201_CREATED)
    return Response(sSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def select_schema(request):
    """
    GET http://localhost/api/schema/select?param1=value1&param2=value2
    URL parameters: 
    id: string (ObjectId)
    filename: string
    content: string
    title: string
    version: integer
    templateVersion: string (ObjectId)
    For string fields, you can use regular expressions: /exp/
    """
    id = request.QUERY_PARAMS.get('id', None)
    filename = request.QUERY_PARAMS.get('filename', None)
    content = request.QUERY_PARAMS.get('content', None)
    title = request.QUERY_PARAMS.get('title', None)
    version = request.QUERY_PARAMS.get('version', None)
    templateVersion = request.QUERY_PARAMS.get('templateVersion', None)
    
    try:        
        # create a connection                                                                                                                                                                                                 
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        template = db['template']
        query = dict()
        if id is not None:            
            query['_id'] = ObjectId(id)            
        if filename is not None:
            if filename[0] == '/' and filename[-1] == '/':
                query['filename'] = re.compile(filename[1:-1])
            else:
                query['filename'] = filename            
        if content is not None:
            if content[0] == '/' and content[-1] == '/':
                query['content'] = re.compile(content[1:-1])
            else:
                query['content'] = content
        if title is not None:
            if title[0] == '/' and title[-1] == '/':
                query['title'] = re.compile(title[1:-1])
            else:
                query['title'] = title
        if version is not None:
            query['version'] = version
        if templateVersion is not None:
            if templateVersion[0] == '/' and templateVersion[-1] == '/':
                query['templateVersion'] = re.compile(templateVersion[1:-1])
            else:
                query['templateVersion'] = templateVersion
        if len(query.keys()) == 0:
            content = {'message':'No parameters given.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            cursor = template.find(query)
            templates = []
            for resultTemplate in cursor:
                resultTemplate['id'] = resultTemplate['_id']
                del resultTemplate['_id']
                templates.append(resultTemplate)
            serializer = templateSerializer(templates)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        content = {'message':'No template found with the given parameters.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def select_all_schemas(request):
    """
    GET http://localhost/api/schema/select/all
    """
    templates = Template.objects
    serializer = templateSerializer(templates)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def delete_schema(request):
    """
    GET http://localhost/api/schema/delete?id=IDtodelete&next=IDnextCurrent
    URL parameters: 
    id: string (ObjectId)
    next: string (ObjectId)
    """
    id = request.QUERY_PARAMS.get('id', None)
    next = request.QUERY_PARAMS.get('next', None)  
    
    if id is not None:   
        try:
            template = Template.objects.get(pk=id)        
        except:
            content = {'message':'No template found with the given id.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No schema id provided to delete.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    if next is not None:
        try:
            nextCurrent = Template.objects.get(pk=next)
            if nextCurrent.templateVersion != template.templateVersion:
                content = {'message':'The specified next current schema is not a version of the current schema.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'message':'No template found with the given id to be the next current.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
    templateVersion = TemplateVersion.objects.get(pk=template.templateVersion)
    if templateVersion.current == str(template.id) and next is None:
        content = {'message':'The selected template is the current. It can\'t be deleted. If you still want to delete this template, please provide the id of the next current schema using \'next\' parameter'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif templateVersion.current == str(template.id) and next is not None and str(template.id) == str(nextCurrent.id):
        content = {'message':'Schema id to delete and next id are the same.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif templateVersion.current != str(template.id) and next is not None:
        content = {'message':'You should only provide the next parameter when you want to delete a current version of a schema.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif templateVersion.current == str(template.id) and next is not None:
        if next in templateVersion.deletedVersions:
            content = {'message':'The schema is deleted, it can\'t become current.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        templateVersion.deletedVersions.append(str(template.id)) 
        templateVersion.current = str(nextCurrent.id)
        templateVersion.save()
        content = {'message':'Current template deleted with success. A new version is current.'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
    else:
#             del templateVersion.versions[templateVersion.versions.index(str(template.id))]
#             template.delete()
        if str(template.id) in templateVersion.deletedVersions:
            content = {'message':'This schema is already deleted.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        templateVersion.deletedVersions.append(str(template.id)) 
        templateVersion.save()
        content = {'message':'Template deleted with success.'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

    
@api_view(['GET'])
def docs(request):
    content={'message':'Invalid command','docs':'http://'+str(request.get_host())+'/docs/api'}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)
