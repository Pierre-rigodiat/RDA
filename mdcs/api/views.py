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
from django.shortcuts import redirect
# Models
from mgi.models import SavedQuery, Jsondata, Template, TemplateVersion
# Serializers
from api.serializers import savedQuerySerializer, jsonDataSerializer, querySerializer, sparqlQuerySerializer, sparqlResultsSerializer, schemaSerializer

from explore import sparqlPublisher
from curate import rdfPublisher
from lxml import etree
from django.conf import settings
import os
from mongoengine import *

projectURI = "http://www.example.com/"

@api_view(['GET','POST'])
def savedQuery_list(request):
    connect('mgi') 
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
    connect('mgi')          
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
    connect('mgi') 
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
    connect('mgi') 
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
    GET http://localhost/api/explore
    """
    connect('mgi') 
    jsonData = Jsondata.objects()
    serializer = jsonDataSerializer(jsonData)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def query_by_example(request):
    """
    POST http://localhost/api/explore/query-by-example/
    POST data query="{'element':'value'}"
    """
    connect('mgi') 
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
    connect('mgi') 
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
    POST data title="title", schema="schemaID", content="<xml>...</xml>"
    """        
    connect('mgi') 
    serializer = jsonDataSerializer(data=request.DATA)
    if serializer.is_valid():
        xmlStr = request.DATA['content']
        try:
            xmlTree = etree.fromstring(xmlStr)            
            jsondata = Jsondata(schemaID = request.DATA['schema'], xml = xmlStr, title = request.DATA['title'])
            docID = jsondata.save()            

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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_schema(request):
    """
    POST http://localhost/api/schema/add/
    POST data title="title", filename="filename", content="<xsd:schema>...</xsd:schema>" templateVersion="id"
    """
    connect('mgi') 
    sSerializer = schemaSerializer(data=request.DATA)
    if sSerializer.is_valid():
        if "templateVersion" in request.DATA:
            try:
                templateVersions = TemplateVersion.objects.get(pk=request.DATA['templateVersion'])
                newTemplate = Template(title=request.DATA['title'], filename=request.DATA['filename'], content=request.DATA['content'], templateVersion=request.DATA['templateVersion']).save()
                templateVersions.versions.append(str(newTemplate.id))
                templateVersions.save()
            except:
                content = {'message':'No template version found with the given id.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            newTemplate = Template(title=request.DATA['title'], filename=request.DATA['filename'], content=request.DATA['content']).save()
            templateVersion = TemplateVersion(versions=[str(newTemplate.id)], current=str(newTemplate.id)).save()
            newTemplate.templateVersion = str(templateVersion.id)
            newTemplate.save()
        return Response(sSerializer.data, status=status.HTTP_201_CREATED)
    return Response(sSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def select_schema(request, pk):
    """
    GET http://localhost/api/schema/select/<id>
    """
    connect('mgi') 
    try:
        template = Template.objects.get(pk=pk)
    except:
        content = {'message':'No template found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    serializer = schemaSerializer(template)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def delete_schema(request, pk):
    """
    GET http://localhost/api/schema/delete/<id>
    Can't delete template if it is the current version
    """
    connect('mgi') 
    try:
        template = Template.objects.get(pk=pk)
    except:
        content = {'message':'No template found with the given id.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    if hasattr(template,'version'):
        templateVersion = TemplateVersion.objects.get(pk=template.templateVersion)
        if templateVersion.current == template.id:
            content = {'message':'The selected template is the current. It can\'t be deleted.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            del templateVersion.versions[templateVersion.versions.index(str(template.id))]
            templateVersion.save()
            template.delete()
            content = {'message':'Template deleted with success.'}
            return Response(content, status=status.HTTP_204_NO_CONTENT)
    else:
        template.delete()
        content = {'message':'Template deleted with success.'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
    

def docs(request):
    return redirect ('/docs')
