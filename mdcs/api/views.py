################################################################################
#
# File Name: views.py
# Application: api
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

# REST Framework
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.status import HTTP_200_OK
# Models
from mgi.models import SavedQuery, Jsondata
# Serializers
from api.serializers import savedQuerySerializer, jsonDataSerializer, querySerializer, sparqlQuerySerializer, sparqlResultsSerializer

from explore import sparqlPublisher
from curate import rdfPublisher
from lxml import etree
from django.conf import settings
import os

projectURI = "http://www.example.com/"

@api_view(['GET','POST'])
def savedQuery_list(request):
    if request.method == 'GET':
        savedQueries = SavedQuery.objects
        serializer = savedQuerySerializer(savedQueries)
        return Response(serializer.data)

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
    except SavedQuery.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = savedQuerySerializer(savedQuery)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = savedQuerySerializer(savedQuery, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        savedQuery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class JsonDataList(generics.ListCreateAPIView):
#     serializer_class = jsonDataSerializer
#     
#     def get_queryset(self):
#         return Jsondata.objects()

@api_view(['GET','POST'])
def jsonData_list(request):
    if request.method == 'GET':
        jsonData = Jsondata.objects()
        serializer = jsonDataSerializer(jsonData)
        return Response(serializer.data)
 
    elif request.method == 'POST':        
        serializer = jsonDataSerializer(data=request.DATA)
        if serializer.is_valid():
            jsondata = Jsondata(schemaID = request.DATA['schema'], json = request.DATA['content'], title = request.DATA['title'])
            jsondata.save()
#             serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def jsonData_detail(request, pk):
    """
    Retrieve, update or delete a saved query instance.
    """              

    jsonData = Jsondata.get(pk)
    if jsonData is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = jsonDataSerializer(jsonData)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = jsonDataSerializer(jsonData, data=request.DATA)
        if serializer.is_valid():
            Jsondata.update(pk, request.DATA)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Jsondata.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def explore(request):
    """
    GET http://localhost/api/explore
    """
    jsonData = Jsondata.objects()
    serializer = jsonDataSerializer(jsonData)
    return Response(serializer.data, status=HTTP_200_OK)

@api_view(['POST'])
def query_by_example(request):
    """
    POST http://localhost/api/explore/query-by-example/
    POST data query="{'element':'value'}"
    """
    qSerializer = querySerializer(data=request.DATA)
    if qSerializer.is_valid():
        results = Jsondata.executeQueryFullResult(request.DATA['query'])
        jsonSerializer = jsonDataSerializer(results)
        return Response(jsonSerializer.data, status=HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

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
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            query = '0' + request.DATA['query']
         
        results = dict()  
        results['content'] = sparqlPublisher.sendSPARQL(query) 
        
        srSerializer = sparqlResultsSerializer(results)
        return Response(srSerializer.data, status=HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def curate(request):        
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

# Previous work
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

#from rest_framework.generics import (
#    ListCreateAPIView, RetrieveUpdateDestroyAPIView)

from curate.models import Task
from api.serializers import TaskSerializer
from api.permissions import IsOwnerOrReadOnly


#class TaskMixin(object):
#    queryset = Task.objects.all()
#    serializer_class = TaskSerializer
#    permission_classes = (IsOwnerOrReadOnly,)

#    def pre_save(self,obj):
#        obj.owner = self.request.user

#class TaskList(TaskMixin, ListCreateAPIView):
#    pass

#class TaskDetail(TaskMixin, RetrieveUpdateDestroyAPIView):
#    pass

@api_view(['GET', 'POST'])
def task_list(request):
    """
    List all tasks, or creat a new task.
    """

    if request.method == 'GET':
        print "task_list GET request"
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks)
        return Response(serializers.data)

    elif request.method == 'POST':
        print "task_list POST request"
        serializer = TaskSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response (
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def task_detail(request, pk):
    """
    Get, update, or delete a specific task
    """

    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


