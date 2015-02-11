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
from mgi.models import SavedQuery, Jsondata, Template, TemplateVersion, Type, TypeVersion, Instance, MetaSchema
from django.contrib.auth.models import User
# Serializers
from api.serializers import savedQuerySerializer, jsonDataSerializer, querySerializer, sparqlQuerySerializer, sparqlResultsSerializer, schemaSerializer, templateSerializer, typeSerializer, resTypeSerializer, TemplateVersionSerializer, TypeVersionSerializer, instanceSerializer, resInstanceSerializer, UserSerializer, insertUserSerializer, resSavedQuerySerializer, updateUserSerializer
from explore import sparqlPublisher
from curate import rdfPublisher
from lxml import etree
from django.conf import settings
import os
from mongoengine import *
from pymongo import Connection
from bson.objectid import ObjectId
import re
import requests
from django.db.models import Q
import operator
import json
import xmltodict
from collections import OrderedDict
from StringIO import StringIO
from django.http.response import HttpResponse
from utils.XSDhash import XSDhash
from mgi import utils
from io import BytesIO
from utils.APIschemaLocator.APIschemaLocator import getSchemaLocation
from utils.XSDflattenerMDCS.XSDflattenerMDCS import XSDFlattenerMDCS


################################################################################
# 
# Function Name: select_all_savedqueries(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get all saved queries
# 
################################################################################
@api_view(['GET'])
def select_all_savedqueries(request):
    """
    GET http://localhost/rest/saved_queries/select/all
    """
    queries = SavedQuery.objects()
    serializer = savedQuerySerializer(queries)
    return Response(serializer.data, status=status.HTTP_200_OK)


################################################################################
# 
# Function Name: select_savedquery(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get saved queries that match the parameters
# 
################################################################################
@api_view(['GET'])
def select_savedquery(request):
    """
    GET http://localhost/rest/saved_queries/select
    id: string (ObjectId)
    user: string 
    template: string
    query: string
    displayedQuery: string
    """
    id = request.QUERY_PARAMS.get('id', None)
    user = request.QUERY_PARAMS.get('user', None)
    template = request.QUERY_PARAMS.get('template', None)
    dbquery = request.QUERY_PARAMS.get('query', None)
    displayedQuery = request.QUERY_PARAMS.get('displayedQuery', None)
    
    try:        
        # create a connection                                                                                                                                                                                                 
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        savedQueries = db['saved_query']
        query = dict()
        if id is not None:            
            query['_id'] = ObjectId(id)            
        if user is not None:
            if len(user) >= 2 and user[0] == '/' and user[-1] == '/':
                query['user'] = re.compile(user[1:-1])
            else:
                query['user'] = user            
        if template is not None:
            if len(template) >= 2 and template[0] == '/' and template[-1] == '/':
                query['template'] = re.compile(template[1:-1])
            else:
                query['template'] = template
        if dbquery is not None:
            if len(dbquery) >= 2 and dbquery[0] == '/' and dbquery[-1] == '/':
                query['query'] = re.compile(dbquery[1:-1])
            else:
                query['query'] = dbquery
        if displayedQuery is not None:
            if len(displayedQuery) >= 2 and displayedQuery[0] == '/' and displayedQuery[-1] == '/':
                query['displayedQuery'] = re.compile(displayedQuery[1:-1])
            else:
                query['displayedQuery'] = displayedQuery
        if len(query.keys()) == 0:
            content = {'message':'No parameters given.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            cursor = savedQueries.find(query)
            listSavedQueries = []
            for resultSavedQuery in cursor:
                resultSavedQuery['id'] = resultSavedQuery['_id']
                del resultSavedQuery['_id']
                listSavedQueries.append(resultSavedQuery)
            serializer = resSavedQuerySerializer(listSavedQueries)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        content = {'message':'No saved query found with the given parameters.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

################################################################################
# 
# Function Name: add_savedquery(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Add a saved query
# 
################################################################################
@api_view(['POST'])
def add_savedquery(request):
    """
    POST http://localhost/rest/saved_queries/add
    POST data user="user", template="template" query="query", displayedQuery="displayedQuery"
    """    
    serializer = resSavedQuerySerializer(data=request.DATA)
    if serializer.is_valid():
        errors = ""
        try:
            json_object = json.loads(request.DATA["query"])
        except ValueError:
            errors += "Invalid query."
        try:
            template = Template.objects.get(pk=request.DATA["template"])
        except Exception:
            errors += "Unknown template."
        try:
            user = User.objects.get(pk=request.DATA["user"])
        except Exception:
            errors += "Unknown user."
        
        if errors != "":
            content = {'message':errors}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            SavedQuery(user=request.DATA["user"],template=request.DATA["template"],query=request.DATA["query"],displayedQuery=request.DATA["displayedQuery"]).save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception, e:
            content = {'message':e.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: delete_savedquery(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Delete a saved query
# 
################################################################################
@api_view(['GET'])
def delete_savedquery(request):
    """
    GET http://localhost/rest/saved_queries/delete?id=id
    URL parameters: 
    id: string 
    """
    id = request.QUERY_PARAMS.get('id', None)
    if id is not None:
        try:
            query = SavedQuery.objects.get(pk=id)
            query.delete()
            content = {'message':"Query deleted with success."}
            return Response(content, status=status.HTTP_200_OK)
        except:
            content = {'message':"No query found with the given id."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':"No id provided."}
        return Response(content, status=status.HTTP_404_NOT_FOUND)


################################################################################
# 
# Function Name: explore(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get all XML data
# 
################################################################################
@api_view(['GET'])
def explore(request):
    """
    GET http://localhost/rest/explore/select/all
    dataformat: [xml,json]
    """
    dataformat = request.QUERY_PARAMS.get('dataformat', None)

    jsonData = Jsondata.objects()
    
    if dataformat== None or dataformat=="xml":
        for jsonDoc in jsonData:
            jsonDoc['content'] = xmltodict.unparse(jsonDoc['content'])  
        serializer = jsonDataSerializer(jsonData)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif dataformat == "json":
        serializer = jsonDataSerializer(jsonData)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message':'The specified format is not accepted.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: explore_detail(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get XML data that match the parameters
# 
################################################################################
@api_view(['GET'])
def explore_detail(request):
    """
    GET http://localhost/rest/explore/select
    id: string (ObjectId)
    schema: string (ObjectId)
    title: string
    dataformat: [xml,json]
    """        
    id = request.QUERY_PARAMS.get('id', None)
    schema = request.QUERY_PARAMS.get('schema', None)
    title = request.QUERY_PARAMS.get('title', None)
    dataformat = request.QUERY_PARAMS.get('dataformat', None)
    
    try:        
        query = dict()
        if id is not None:            
            query['_id'] = ObjectId(id)            
        if schema is not None:
            if len(schema) >= 2 and schema[0] == '/' and schema[-1] == '/':
                query['schema'] = re.compile(schema[1:-1])
            else:
                query['schema'] = schema
        if title is not None:
            if len(title) >= 2 and title[0] == '/' and title[-1] == '/':
                query['title'] = re.compile(title[1:-1])
            else:
                query['title'] = title
        if len(query.keys()) == 0:
            content = {'message':'No parameters given.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            jsonData = Jsondata.executeQueryFullResult(query)
        
            if dataformat== None or dataformat=="xml":
                for jsonDoc in jsonData:
                    jsonDoc['content'] = xmltodict.unparse(jsonDoc['content'])  
                serializer = jsonDataSerializer(jsonData)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif dataformat == "json":
                serializer = jsonDataSerializer(jsonData)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                content = {'message':'The specified format is not accepted.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except:
        content = {'message':'No data found with the given parameters.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

################################################################################
# 
# Function Name: explore_delete(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Delete the XML data with the provided id
# 
################################################################################
@api_view(['GET'])
def explore_delete(request):
    """
    GET http://localhost/rest/explore/delete
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

################################################################################
# 
# Function Name: manageRegexInAPI(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Compile the regex in a query
# 
################################################################################
def manageRegexInAPI(query):
    for key, value in query.iteritems():
        if key == "$and" or key == "$or":
            for subValue in value:
                manageRegexInAPI(subValue)
        elif isinstance(value, str) or isinstance(value, unicode):
            if (len(value) >= 2 and value[0] == "/" and value[-1] == "/"):
                query[key] = re.compile(value[1:-1])
        elif isinstance(value, dict):
            manageRegexInAPI(value)

################################################################################
# 
# Function Name: query_by_example(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Submit a query to MongoDB
# 
################################################################################
@api_view(['POST'])
def query_by_example(request):
    """
    POST http://localhost/rest/explore/query-by-example
    POST data query="{'element':'value'}" repositories="Local,Server1,Server2" dataformat: [xml,json]
    {"query":"{'content.root.property1.value':'xxx'}"}
    """
         
    dataformat = None
    if 'dataformat' in request.DATA:
        dataformat = request.DATA['dataformat']
    
    qSerializer = querySerializer(data=request.DATA)
    if qSerializer.is_valid():
        if 'repositories' in request.DATA:
            instanceResults = []
            repositories = request.DATA['repositories'].strip().split(",")
            if len(repositories) == 0:
                content = {'message':'Repositories keyword found but the list is empty.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                instances = []
                local = False
                for repository in repositories:
                    if repository == "Local":
                        local = True
                    else:
                        try:
                            instance = Instance.objects.get(name=repository)
                            instances.append(instance)
                        except:
                            content = {'message':'Unknown repository.'}
                            return Response(content, status=status.HTTP_400_BAD_REQUEST)
                if local:
                    try:
                        query = eval(request.DATA['query'])
                        manageRegexInAPI(query)
                        instanceResults = instanceResults + Jsondata.executeQueryFullResult(query)                        
                    except:
                        content = {'message':'Bad query: use the following format {\'element\':\'value\'}'}
                        return Response(content, status=status.HTTP_400_BAD_REQUEST)
                for instance in instances:
                    url = instance.protocol + "://" + instance.address + ":" + str(instance.port) + "/rest/explore/query-by-example"   
                    query = request.DATA['query']              
                    data = {"query":query}
                    r = requests.post(url, data, auth=(instance.user, instance.password))   
                    result = r.text
                    instanceResults = instanceResults + json.loads(result,object_pairs_hook=OrderedDict)
            
                if dataformat== None or dataformat=="xml":
                    for jsonDoc in instanceResults:
                        jsonDoc['content'] = xmltodict.unparse(jsonDoc['content'])  
                    serializer = jsonDataSerializer(instanceResults)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                elif dataformat == "json":
                    serializer = jsonDataSerializer(instanceResults)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    content = {'message':'The specified format is not accepted.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                query = eval(request.DATA['query'])
                manageRegexInAPI(query)
                results = Jsondata.executeQueryFullResult(query)
            
                if dataformat== None or dataformat=="xml":
                    for jsonDoc in results:
                        jsonDoc['content'] = xmltodict.unparse(jsonDoc['content'])  
                    serializer = jsonDataSerializer(results)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                elif dataformat == "json":
                    serializer = jsonDataSerializer(results)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    content = {'message':'The specified format is not accepted.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            except:
                content = {'message':'Bad query: use the following format {\'element\':\'value\'}'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(qSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: sparql_query(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Submit a SPARQL query to the Jena triplestore
# 
################################################################################
@api_view(['POST'])
def sparql_query(request):
    """
    POST http://localhost/rest/explore/sparql-query
    POST data query="SELECT * WHERE {?s ?p ?o}" dataformat="xml" repositories="Local,Server1,Server2"
    """
    sqSerializer = sparqlQuerySerializer(data=request.DATA)
    if sqSerializer.is_valid():
        if 'dataformat' in request.DATA:
            format = request.DATA['dataformat']
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
        
        if 'repositories' in request.DATA:
            instanceResults = []
            repositories = request.DATA['repositories'].strip().split(",")
            if len(repositories) == 0:
                content = {'message':'Repositories keyword found but the list is empty.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                instances = []
                local = False
                for repository in repositories:
                    if repository == "Local":
                        local = True
                    else:
                        try:
                            instance = Instance.objects.get(name=repository)
                            instances.append(instance)
                        except:
                            content = {'message':'Unknown repository.'}
                            return Response(content, status=status.HTTP_400_BAD_REQUEST)
                if local:
                    instanceResults.append(sparqlPublisher.sendSPARQL(query)) 
                for instance in instances:
                    url = instance.protocol + "://" + instance.address + ":" + str(instance.port) + "/rest/explore/sparql-query"
                    if 'dataformat' in request.DATA:
                        data = {"query": request.DATA['query'], "dataformat":request.DATA['dataformat']}
                    else:
                        data = {"query": request.DATA['query']}
                    r = requests.post(url, data, auth=(instance.user, instance.password))        
                    instanceResultsDict = eval(r.text)
                    instanceResults.append(instanceResultsDict['content'])
                    
                results = dict()
                results['content'] = instanceResults
                
                srSerializer = sparqlResultsSerializer(results)
                return Response(srSerializer.data, status=status.HTTP_200_OK)
        else:
            results = dict()  
            results['content'] = sparqlPublisher.sendSPARQL(query) 
            
            srSerializer = sparqlResultsSerializer(results)
            return Response(srSerializer.data, status=status.HTTP_200_OK)
    return Response(sqSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
  

################################################################################
# 
# Function Name: curate(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Curate an XML document: save the data in MongoDB and Jena
# 
################################################################################
@api_view(['POST'])
def curate(request):
    """
    POST http://localhost/rest/curate
    POST data title="title", schema="schemaID", content="<root>...</root>"
    """        
    serializer = jsonDataSerializer(data=request.DATA)
    if serializer.is_valid():
        try:
            schema = Template.objects.get(pk=ObjectId(request.DATA['schema']))
            templateVersion = TemplateVersion.objects.get(pk=ObjectId(schema.templateVersion))
            if str(schema.id) in templateVersion.deletedVersions:
                content = {'message: The provided template is currently deleted.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'message: No template found with the given id.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        xmlStr = request.DATA['content']
        try:
            try:
                utils.validateXMLDocument(schema.id, xmlStr)
            except Exception, e:
                content = {'message':e.message}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            jsondata = Jsondata(schemaID = request.DATA['schema'], xml = xmlStr, title = request.DATA['title'])
            docID = jsondata.save()            
            
            xsltPath = os.path.join(settings.SITE_ROOT, 'static/resources/xsl/xml2rdf3.xsl')
            xslt = etree.parse(xsltPath)
            root = xslt.getroot()
            namespace = root.nsmap['xsl']
            URIparam = root.find("{" + namespace +"}param[@name='BaseURI']") #find BaseURI tag to insert the project URI
            URIparam.text = settings.PROJECT_URI + str(docID)
        
            # SPARQL : transform the XML into RDF/XML
            transform = etree.XSLT(xslt)
            # add a namespace to the XML string, transformation didn't work well using XML DOM
            template = Template.objects.get(pk=schema.id)
            xmlStr = xmlStr.replace('>',' xmlns="' + settings.PROJECT_URI + template.hash + '">', 1) #TODO: OR schema name...                
            # domXML.attrib['xmlns'] = projectURI + schemaID #didn't work well
            domXML = etree.fromstring(xmlStr)
            domRDF = transform(domXML)
        
            # SPARQL : get the rdf string
            rdfStr = etree.tostring(domRDF)
        
            # SPARQL : send the rdf to the triplestore
            rdfPublisher.sendRDF(rdfStr)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            content = {'message: Unable to insert data.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: add_schema(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Add a template or a version of a template
# 
################################################################################
@api_view(['POST'])
def add_schema(request):
    """
    POST http://localhost/rest/templates/add
    POST data title="title", filename="filename", content="<xsd:schema>...</xsd:schema>" templateVersion="id", dependencies="id,id"
    """
    
    xsdContent = None
    xsdFlatContent = None
    xsdAPIContent = None
        
    sSerializer = schemaSerializer(data=request.DATA)
    if sSerializer.is_valid():
        xsdContent = request.DATA['content']
        
        # is this a valid XMl document?
        try:
            xmlTree = etree.parse(BytesIO(xsdContent.encode('utf-8')))
        except Exception, e:
            content = {'message':'This is not a valid XML document.' + e.message.replace("'","")}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        # check that the schema is valid for the MDCS
        errors = utils.getValidityErrorsForMDCS(xmlTree, "Template")
        if len(errors) > 0:
            content = {'message':'This template is not supported by the current version of the MDCS.', 'errors': errors}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        # manage the dependencies
        includes = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}include")        
        idxInclude = 0
        
        if 'dependencies' in request.DATA:  
            dependencies = request.DATA['dependencies'].strip().split(",")
            if len(dependencies) == len(includes):
                listTypesId = []
                for typeId in Type.objects.all().values_list('id'):     
                    listTypesId.append(str(typeId))

                # replace includes/imports by API calls
                for dependency in dependencies:
                    if dependency in listTypesId: 
                        includes[idxInclude].attrib['schemaLocation'] = getSchemaLocation(request, str(dependency))
                        idxInclude += 1
                    else:
                        content = {'message':'One or more dependencies can not be found in the database.'}
                        return Response(content, status=status.HTTP_400_BAD_REQUEST)
                flattener = XSDFlattenerMDCS(etree.tostring(xmlTree))
                flatStr = flattener.get_flat()
                flatTree = etree.fromstring(flatStr)
                # is this a valid XML schema?
                try:
                    xmlSchema = etree.XMLSchema(flatTree)
                    xsdFlatContent = flatStr
                    xsdAPIContent = etree.tostring(xmlTree)
                except Exception, e:
                    content = {'message':'This is not a valid XML schema.' + e.message.replace("'","")}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {'message':'The number of given dependencies (' + str(len(dependencies)) + ')  is different from the actual number of dependencies found in the uploaded template (' + str(len(includes)) + ').'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            if len(includes) > 0:
                content = {'message':'The template that you are trying to upload has some dependencies. Use the "dependencies" keyword to register a template with its dependencies.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                # is this a valid XML schema?
                try:
                    xmlSchema = etree.XMLSchema(xmlTree)
                except Exception, e:
                    content = {'message':'This is not a valid XML schema.' + e.message.replace("'","")}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        # a template version is provided: if it exists, add the schema as a new version and manage the version numbers
        if "templateVersion" in request.DATA:
            try:
                templateVersions = TemplateVersion.objects.get(pk=request.DATA['templateVersion'])
                if templateVersions.isDeleted == True:
                    content = {'message':'This template version belongs to a deleted template. You are not allowed to add a template to it.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                templateVersions.nbVersions = templateVersions.nbVersions + 1
                hash = XSDhash.get_hash(xsdContent)
                newTemplate = Template(title=request.DATA['title'], filename=request.DATA['filename'], content=xsdContent, templateVersion=request.DATA['templateVersion'], version=templateVersions.nbVersions, hash=hash).save()
                templateVersions.versions.append(str(newTemplate.id))                
                templateVersions.save()
                # Save Meta schema
                if xsdFlatContent is not None and xsdAPIContent is not None:
                    MetaSchema(schemaId=str(newTemplate.id), flat_content=xsdFlatContent, api_content=xsdAPIContent).save()
            except:
                content = {'message':'No template version found with the given id.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            templateVersion = TemplateVersion(nbVersions=1, isDeleted=False).save()
            hash = XSDhash.get_hash(xsdContent)
            newTemplate = Template(title=request.DATA['title'], filename=request.DATA['filename'], content=xsdContent, version=1, templateVersion=str(templateVersion.id), hash=hash).save()
            templateVersion.versions = [str(newTemplate.id)]
            templateVersion.current=str(newTemplate.id)
            templateVersion.save()
            newTemplate.save()
            # Save Meta schema
            if xsdFlatContent is not None and xsdAPIContent is not None:
                MetaSchema(schemaId=str(newTemplate.id), flat_content=xsdFlatContent, api_content=xsdAPIContent).save()
        
        return Response(eval(newTemplate.to_json()), status=status.HTTP_201_CREATED)
    return Response(sSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: select_schema(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get templates that match the parameters
# 
################################################################################
@api_view(['GET'])
def select_schema(request):
    """
    GET http://localhost/rest/templates/select?param1=value1&param2=value2
    URL parameters: 
    id: string (ObjectId)
    filename: string
    content: string
    title: string
    version: integer
    templateVersion: string (ObjectId)
    hash: string
    For string fields, you can use regular expressions: /exp/
    """
    id = request.QUERY_PARAMS.get('id', None)
    filename = request.QUERY_PARAMS.get('filename', None)
    content = request.QUERY_PARAMS.get('content', None)
    title = request.QUERY_PARAMS.get('title', None)
    version = request.QUERY_PARAMS.get('version', None)
    templateVersion = request.QUERY_PARAMS.get('templateVersion', None)
    hash = request.QUERY_PARAMS.get('hash', None)
    
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
            if len(filename) >= 2 and filename[0] == '/' and filename[-1] == '/':
                query['filename'] = re.compile(filename[1:-1])
            else:
                query['filename'] = filename            
        if content is not None:
            if len(content) >= 2 and content[0] == '/' and content[-1] == '/':
                query['content'] = re.compile(content[1:-1])
            else:
                query['content'] = content
        if title is not None:
            if len(title) >= 2 and title[0] == '/' and title[-1] == '/':
                query['title'] = re.compile(title[1:-1])
            else:
                query['title'] = title
        if version is not None:
            query['version'] = version
        if templateVersion is not None:
            if len(templateVersion) >= 2 and templateVersion[0] == '/' and templateVersion[-1] == '/':
                query['templateVersion'] = re.compile(templateVersion[1:-1])
            else:
                query['templateVersion'] = templateVersion
        if hash is not None:
            if len(hash) >= 2 and hash[0] == '/' and hash[-1] == '/':
                query['hash'] = re.compile(hash[1:-1])
            else:
                query['hash'] = hash
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

################################################################################
# 
# Function Name: select_all_schemas(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get all schemas
# 
################################################################################
@api_view(['GET'])
def select_all_schemas(request):
    """
    GET http://localhost/rest/templates/select/all
    """
    templates = Template.objects
    serializer = templateSerializer(templates)
    return Response(serializer.data, status=status.HTTP_200_OK)

################################################################################
# 
# Function Name: select_all_schemas_versions(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get all template version managers
# 
################################################################################
@api_view(['GET'])
def select_all_schemas_versions(request):
    """
    GET http://localhost/rest/schemas/versions/select/all
    """
    templateVersions = TemplateVersion.objects
    serializer = TemplateVersionSerializer(templateVersions)
    return Response(serializer.data, status=status.HTTP_200_OK)

################################################################################
# 
# Function Name: current_template_version(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Set the current version of a template
# 
################################################################################
@api_view(['GET'])
def current_template_version(request):
    """
    GET http://localhost/rest/templates/versions/current?id=IdToBeCurrent
    """
    id = request.QUERY_PARAMS.get('id', None)
    if id is not None:   
        try:
            template = Template.objects.get(pk=id)        
        except:
            content = {'message':'No template found with the given id.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No template id provided to be current.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    templateVersion = TemplateVersion.objects.get(pk=template.templateVersion)
    if templateVersion.isDeleted == True:
        content = {'message':'This template version belongs to a deleted template. You are not allowed to restore it. Please restore the template first (id:'+ str(templateVersion.id) +').'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if templateVersion.current == id:
        content = {'message':'The selected template is already the current template.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if id in templateVersion.deletedVersions:
        content = {'message':'The selected template is deleted. Please restore it first to make it current.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    templateVersion.current = id
    templateVersion.save()
    content = {'message':'Current template set with success.'}
    return Response(content, status=status.HTTP_200_OK)

################################################################################
# 
# Function Name: delete_schema(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Delete a template
# 
################################################################################
@api_view(['GET'])
def delete_schema(request):
    """
    GET http://localhost/rest/templates/delete?id=IDtodelete&next=IDnextCurrent
    GET http://localhost/rest/templates/delete?templateVersion=IDtodelete
    URL parameters: 
    id: string (ObjectId)
    next: string (ObjectId)
    templateVersion: string (ObjectId)
    """
    id = request.QUERY_PARAMS.get('id', None)
    next = request.QUERY_PARAMS.get('next', None)
    versionID = request.QUERY_PARAMS.get('templateVersion', None)  
    
    if versionID is not None:
        if id is not None or next is not None:
            content = {'message':'Wrong parameters combination.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                templateVersion = TemplateVersion.objects.get(pk=versionID)
                if templateVersion.isDeleted == False:
                    templateVersion.deletedVersions.append(templateVersion.current)
                    templateVersion.isDeleted = True
                    templateVersion.save()
                    content = {'message':'Template version deleted with success.'}
                    return Response(content, status=status.HTTP_200_OK)
                else:
                    content = {'message':'Template version already deleted.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            except:
                content = {'message':'No template version found with the given id.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    if id is not None:   
        try:
            template = Template.objects.get(pk=id)        
        except:
            content = {'message':'No template found with the given id.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No template id provided to delete.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    if next is not None:
        try:
            nextCurrent = Template.objects.get(pk=next)
            if nextCurrent.templateVersion != template.templateVersion:
                content = {'message':'The specified next current template is not a version of the current template.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'message':'No template found with the given id to be the next current.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
    templateVersion = TemplateVersion.objects.get(pk=template.templateVersion)
    if templateVersion.isDeleted == True:
        content = {'message':'This template version belongs to a deleted template. You are not allowed to restore it. Please restore the template first (id:'+ str(templateVersion.id) +').'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if templateVersion.current == str(template.id) and next is None:
        content = {'message':'The selected template is the current. It can\'t be deleted. If you still want to delete this template, please provide the id of the next current template using \'next\' parameter'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif templateVersion.current == str(template.id) and next is not None and str(template.id) == str(nextCurrent.id):
        content = {'message':'Template id to delete and next id are the same.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif templateVersion.current != str(template.id) and next is not None:
        content = {'message':'You should only provide the next parameter when you want to delete a current version of a template.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif templateVersion.current == str(template.id) and next is not None:
        if next in templateVersion.deletedVersions:
            content = {'message':'The template is deleted, it can\'t become current.'}
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
            content = {'message':'This template is already deleted.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        templateVersion.deletedVersions.append(str(template.id)) 
        templateVersion.save()
        content = {'message':'Template deleted with success.'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

################################################################################
# 
# Function Name: restore_schema(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Restore a template or a template version manager
# 
################################################################################
@api_view(['GET'])
def restore_schema(request):
    """
    GET http://localhost/rest/templates/restore?id=IDtorestore
    GET http://localhost/rest/templates/delete?templateVersion=IDtorestore
    URL parameters: 
    id: string (ObjectId)
    templateVersion: string (ObjectId)
    """
    id = request.QUERY_PARAMS.get('id', None)    
    versionID = request.QUERY_PARAMS.get('templateVersion', None)
    
    if versionID is not None:
        if id is not None:
            content = {'message':'Wrong parameters combination.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                templateVersion = TemplateVersion.objects.get(pk=versionID)
                if templateVersion.isDeleted == False:
                    content = {'message':'Template version not deleted. No need to be restored.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                else:
                    templateVersion.isDeleted = False
                    del templateVersion.deletedVersions[templateVersion.deletedVersions.index(templateVersion.current)]
                    templateVersion.save()
                    content = {'message':'Template restored with success.'}
                    return Response(content, status=status.HTTP_200_OK)
            except:
                content = {'message':'No template version found with the given id.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        
    if id is not None:   
        try:
            template = Template.objects.get(pk=id)        
        except:
            content = {'message':'No template found with the given id.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No template id provided to restore.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    templateVersion = TemplateVersion.objects.get(pk=template.templateVersion)
    if templateVersion.isDeleted == True:
        content = {'message':'This template version belongs to a deleted template. You are not allowed to restore it. Please restore the template first (id:'+ str(templateVersion.id) +').'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if id in templateVersion.deletedVersions:
        del templateVersion.deletedVersions[templateVersion.deletedVersions.index(id)]
        templateVersion.save()
        content = {'message':'Template version restored with success.'}
        return Response(content, status=status.HTTP_200_OK)
    else:
        content = {'message':'Template version not deleted. No need to be restored.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: add_type(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Add a type
# 
################################################################################
@api_view(['POST'])
def add_type(request):
    """
    POST http://localhost/rest/types/add
    POST data title="title", filename="filename", content="..." typeVersion="id" dependencies="id,id"
    """
    
    xsdContent = None
    xsdFlatContent = None
    xsdAPIContent = None
    
    oSerializer = typeSerializer(data=request.DATA)
    if oSerializer.is_valid():
        xsdContent = request.DATA['content']
        
        # is this a valid XMl document?
        try:
            xmlTree = etree.parse(BytesIO(xsdContent.encode('utf-8')))
        except Exception, e:
            content = {'message':'This is not a valid XML document.' + e.message.replace("'","")}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        # check that the schema is valid for the MDCS
        errors = utils.getValidityErrorsForMDCS(xmlTree, "Type")
        if len(errors) > 0:
            content = {'message':'This type is not supported by the current version of the MDCS.', 'errors': errors}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        # manage the dependencies
        includes = xmlTree.findall("{http://www.w3.org/2001/XMLSchema}include")        
        idxInclude = 0
        
        if 'dependencies' in request.DATA:  
            dependencies = request.DATA['dependencies'].strip().split(",")
            if len(dependencies) == len(includes):
                listTypesId = []
                for typeId in Type.objects.all().values_list('id'):     
                    listTypesId.append(str(typeId))
                
                # replace includes/imports by API calls
                for dependency in dependencies:
                    if dependency in listTypesId: 
                        includes[idxInclude].attrib['schemaLocation'] = getSchemaLocation(request, str(dependency))
                        idxInclude += 1
                    else:
                        content = {'message':'One or more dependencies can not be found in the database.'}
                        return Response(content, status=status.HTTP_400_BAD_REQUEST)
                flattener = XSDFlattenerMDCS(etree.tostring(xmlTree))
                flatStr = flattener.get_flat()
                flatTree = etree.fromstring(flatStr)
                # is this a valid XML schema?
                try:
                    xmlSchema = etree.XMLSchema(flatTree)
                    xsdFlatContent = flatStr
                    xsdAPIContent = etree.tostring(xmlTree)
                except Exception, e:
                    content = {'message':'This is not a valid XML schema.' + e.message.replace("'","")}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {'message':'The number of given dependencies (' + str(len(dependencies)) + ')  is different from the actual number of dependencies found in the uploaded template (' + str(len(includes)) + ').'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            if len(includes) > 0:
                content = {'message':'The template that you are trying to upload has some dependencies. Use the "dependencies" keyword to register a template with its dependencies.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                # is this a valid XML schema?
                try:
                    xmlSchema = etree.XMLSchema(xmlTree)
                except Exception, e:
                    content = {'message':'This is not a valid XML schema.' + e.message.replace("'","")}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)


        
        # an type version is provided: if it exists, add the type as a new version and manage the version numbers
        if "typeVersion" in request.DATA:
            try:
                typeVersions = TypeVersion.objects.get(pk=request.DATA['typeVersion'])
                if typeVersions.isDeleted == True:
                    content = {'message':'This type version belongs to a deleted type. You can not add a type to it.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                typeVersions.nbVersions = typeVersions.nbVersions + 1
                newType = Type(title=request.DATA['title'], filename=request.DATA['filename'], content=request.DATA['content'], typeVersion=request.DATA['typeVersion'], version=typeVersions.nbVersions).save()
                typeVersions.versions.append(str(newType.id))                
                typeVersions.save()
                # Save Meta schema
                if xsdFlatContent is not None and xsdAPIContent is not None:
                    MetaSchema(schemaId=str(newType.id), flat_content=xsdFlatContent, api_content=xsdAPIContent).save()
            except:
                content = {'message':'No type version found with the given id.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            typeVersion = TypeVersion(nbVersions=1, isDeleted=False).save()
            newType = Type(title=request.DATA['title'], filename=request.DATA['filename'], content=request.DATA['content'], version=1, typeVersion=str(typeVersion.id)).save()
            typeVersion.versions = [str(newType.id)]
            typeVersion.current=str(newType.id)
            typeVersion.save()
            newType.save()
            # Save Meta schema
            if xsdFlatContent is not None and xsdAPIContent is not None:
                MetaSchema(schemaId=str(newType.id), flat_content=xsdFlatContent, api_content=xsdAPIContent).save()
        return Response(eval(newType.to_json()), status=status.HTTP_201_CREATED)
    return Response(oSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: select_type(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Select types that match parameters
# 
################################################################################
@api_view(['GET'])
def select_type(request):
    """
    GET http://localhost/rest/types/select?param1=value1&param2=value2
    URL parameters: 
    id: string (ObjectId)
    filename: string
    content: string
    title: string
    version: integer
    typeVersion: string (ObjectId)
    For string fields, you can use regular expressions: /exp/
    """
    id = request.QUERY_PARAMS.get('id', None)
    filename = request.QUERY_PARAMS.get('filename', None)
    content = request.QUERY_PARAMS.get('content', None)
    title = request.QUERY_PARAMS.get('title', None)
    version = request.QUERY_PARAMS.get('version', None)
    typeVersion = request.QUERY_PARAMS.get('typeVersion', None)
    
    try:        
        # create a connection                                                                                                                                                                                                 
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        type = db['type']
        query = dict()
        if id is not None:            
            query['_id'] = ObjectId(id)            
        if filename is not None:
            if len(filename) >= 2 and filename[0] == '/' and filename[-1] == '/':
                query['filename'] = re.compile(filename[1:-1])
            else:
                query['filename'] = filename            
        if content is not None:
            if len(content) >= 2 and content[0] == '/' and content[-1] == '/':
                query['content'] = re.compile(content[1:-1])
            else:
                query['content'] = content
        if title is not None:
            if len(title) >= 2 and title[0] == '/' and title[-1] == '/':
                query['title'] = re.compile(title[1:-1])
            else:
                query['title'] = title
        if version is not None:
            query['version'] = version
        if typeVersion is not None:
            if len(typeVersion) >= 2 and typeVersion[0] == '/' and typeVersion[-1] == '/':
                query['typeVersion'] = re.compile(typeVersion[1:-1])
            else:
                query['typeVersion'] = typeVersion
        if len(query.keys()) == 0:
            content = {'message':'No parameters given.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            cursor = type.find(query)
            types = []
            for resultType in cursor:
                resultType['id'] = resultType['_id']
                del resultType['_id']
                types.append(resultType)
            serializer = resTypeSerializer(types)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        content = {'message':'No type found with the given parameters.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

################################################################################
# 
# Function Name: select_all_types(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get all types
# 
################################################################################
@api_view(['GET'])
def select_all_types(request):
    """
    GET http://localhost/rest/types/select/all
    """
    types = Type.objects
    serializer = resTypeSerializer(types)
    return Response(serializer.data, status=status.HTTP_200_OK)

################################################################################
# 
# Function Name: select_all_types_versions(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get all type versions managers
# 
################################################################################
@api_view(['GET'])
def select_all_types_versions(request):
    """
    GET http://localhost/rest/types/versions/select/all
    """
    typeVersions = TypeVersion.objects
    serializer = TypeVersionSerializer(typeVersions)
    return Response(serializer.data, status=status.HTTP_200_OK)

################################################################################
# 
# Function Name: current_type_version(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Set the current version of a type
# 
################################################################################
@api_view(['GET'])
def current_type_version(request):
    """
    GET http://localhost/rest/types/versions/current?id=IdToBeCurrent
    """
    id = request.QUERY_PARAMS.get('id', None)
    if id is not None:   
        try:
            type = Type.objects.get(pk=id)        
        except:
            content = {'message':'No type found with the given id.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No type id provided to be current.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    typeVersion = TypeVersion.objects.get(pk=type.typeVersion)
    if typeVersion.isDeleted == True:
        content = {'message':'This type version belongs to a deleted type. You are not allowed to restore it. Please restore the type first (id:'+ str(typeVersion.id) +').'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if typeVersion.current == id:
        content = {'message':'The selected type is already the current type.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if id in typeVersion.deletedVersions:
        content = {'message':'The selected type is deleted. Please restore it first to make it current.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    typeVersion.current = id
    typeVersion.save()
    content = {'message':'Current type set with success.'}
    return Response(content, status=status.HTTP_200_OK)

################################################################################
# 
# Function Name: delete_type(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Delete a type
# 
################################################################################
@api_view(['GET'])
def delete_type(request):
    """
    GET http://localhost/rest/types/delete?id=IDtodelete&next=IDnextCurrent
    GET http://localhost/rest/types/delete?typeVersion=IDtodelete
    URL parameters: 
    id: string (ObjectId)
    next: string (ObjectId)
    typeVersion: string (ObjectId)
    """
    id = request.QUERY_PARAMS.get('id', None)
    next = request.QUERY_PARAMS.get('next', None)  
    versionID = request.QUERY_PARAMS.get('typeVersion', None)  
    
    if versionID is not None:
        if id is not None or next is not None:
            content = {'message':'Wrong parameters combination.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                typeVersion = TypeVersion.objects.get(pk=versionID)
                if typeVersion.isDeleted == False:
                    typeVersion.deletedVersions.append(typeVersion.current)
                    typeVersion.isDeleted = True
                    typeVersion.save()
                    content = {'message':'Type version deleted with success.'}
                    return Response(content, status=status.HTTP_200_OK)
                else:
                    content = {'message':'Type version already deleted.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            except:
                content = {'message':'No type version found with the given id.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            
    if id is not None:   
        try:
            type = Type.objects.get(pk=id)        
        except:
            content = {'message':'No type found with the given id.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No type id provided to delete.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    if next is not None:
        try:
            nextCurrent = Type.objects.get(pk=next)
            if nextCurrent.typeVersion != type.typeVersion:
                content = {'message':'The specified next current type is not a version of the current type.'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except:
            content = {'message':'No type found with the given id to be the next current.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
    typeVersion = TypeVersion.objects.get(pk=type.typeVersion)
    if typeVersion.isDeleted == True:
        content = {'message':'This type version belongs to a deleted type. You are not allowed to delete it. please restore the type first (id='+ str(typeVersion.id) +')'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if typeVersion.current == str(type.id) and next is None:
        content = {'message':'The selected type is the current. It can\'t be deleted. If you still want to delete this type, please provide the id of the next current type using \'next\' parameter'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif typeVersion.current == str(type.id) and next is not None and str(type.id) == str(nextCurrent.id):
        content = {'message':'Type id to delete and next id are the same.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif typeVersion.current != str(type.id) and next is not None:
        content = {'message':'You should only provide the next parameter when you want to delete a current version of a type.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    elif typeVersion.current == str(type.id) and next is not None:
        if next in typeVersion.deletedVersions:
            content = {'message':'The type is deleted, it can\'t become current.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        typeVersion.deletedVersions.append(str(type.id)) 
        typeVersion.current = str(nextCurrent.id)
        typeVersion.save()
        content = {'message':'Current type deleted with success. A new version is current.'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
    else:
        if str(type.id) in typeVersion.deletedVersions:
            content = {'message':'This type is already deleted.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        typeVersion.deletedVersions.append(str(type.id)) 
        typeVersion.save()
        content = {'message':'Type deleted with success.'}
        return Response(content, status=status.HTTP_204_NO_CONTENT)

################################################################################
# 
# Function Name: restore_type(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Restore a type
# 
################################################################################
@api_view(['GET'])
def restore_type(request):
    """
    GET http://localhost/rest/types/restore?id=IDtorestore
    GET http://localhost/rest/types/delete?typeVersion=IDtorestore
    URL parameters: 
    id: string (ObjectId)
    typeVersion: string (ObjectId)
    """
    id = request.QUERY_PARAMS.get('id', None)    
    versionID = request.QUERY_PARAMS.get('typeVersion', None)
    
    if versionID is not None:
        if id is not None:
            content = {'message':'Wrong parameters combination.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                typeVersion = TypeVersion.objects.get(pk=versionID)
                if typeVersion.isDeleted == False:
                    content = {'message':'Type version not deleted. No need to be restored.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                else:
                    typeVersion.isDeleted = False
                    del typeVersion.deletedVersions[typeVersion.deletedVersions.index(typeVersion.current)]
                    typeVersion.save()
                    content = {'message':'Type restored with success.'}
                    return Response(content, status=status.HTTP_200_OK)
            except:
                content = {'message':'No type version found with the given id.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        
    if id is not None:   
        try:
            type = Type.objects.get(pk=id)        
        except:
            content = {'message':'No type found with the given id.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No type id provided to restore.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    typeVersion = TypeVersion.objects.get(pk=type.typeVersion)
    if typeVersion.isDeleted == True:
        content = {'message':'This type version belongs to a deleted type. You are not allowed to restore it. Please restore the type first (id:'+ str(typeVersion.id) +').'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if id in typeVersion.deletedVersions:
        del typeVersion.deletedVersions[typeVersion.deletedVersions.index(id)]
        typeVersion.save()
        content = {'message':'Type version restored with success.'}
        return Response(content, status=status.HTTP_200_OK)
    else:
        content = {'message':'Type version not deleted. No need to be restored.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: select_all_repositories(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get all repositories
# 
################################################################################
@api_view(['GET'])
def select_all_repositories(request):
    """
    GET http://localhost/rest/repositories/select/all
    """
    instances = Instance.objects
    serializer = instanceSerializer(instances)
    return Response(serializer.data, status=status.HTTP_200_OK)

################################################################################
# 
# Function Name: select_repository(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get repositories that match the parameters
# 
################################################################################
@api_view(['GET'])
def select_repository(request):
    """
    GET http://localhost/rest/repositories/select?param1=value1&param2=value2
    URL parameters: 
    id: string (ObjectId)
    name: string
    protocol: string
    address: string
    port: integer
    user: string
    status: string
    For string fields, you can use regular expressions: /exp/
    """
    id = request.QUERY_PARAMS.get('id', None)
    name = request.QUERY_PARAMS.get('filename', None)
    protocol = request.QUERY_PARAMS.get('protocol', None)
    address = request.QUERY_PARAMS.get('address', None)
    port = request.QUERY_PARAMS.get('port', None)
    user = request.QUERY_PARAMS.get('user', None)
    inst_status = request.QUERY_PARAMS.get('status', None)
    
    try:        
        # create a connection                                                                                                                                                                                                 
        connection = Connection()
        # connect to the db 'mgi'
        db = connection['mgi']
        # get the xmldata collection
        instance = db['instance']
        query = dict()
        if id is not None:            
            query['_id'] = ObjectId(id)            
        if name is not None:
            if len(name) >= 2 and name[0] == '/' and name[-1] == '/':
                query['name'] = re.compile(name[1:-1])
            else:
                query['name'] = name            
        if protocol is not None:
            if len(protocol) >= 2 and protocol[0] == '/' and protocol[-1] == '/':
                query['protocol'] = re.compile(protocol[1:-1])
            else:
                query['protocol'] = protocol
        if address is not None:
            if len(address) >= 2 and address[0] == '/' and address[-1] == '/':
                query['address'] = re.compile(address[1:-1])
            else:
                query['address'] = address
        if port is not None:
            query['port'] = port
        if user is not None:
            if len(user) >= 2 and user[0] == '/' and user[-1] == '/':
                query['user'] = re.compile(user[1:-1])
            else:
                query['user'] = user
        if inst_status is not None:
            if len(inst_status) >= 2 and inst_status[0] == '/' and inst_status[-1] == '/':
                query['status'] = re.compile(inst_status[1:-1])
            else:
                query['status'] = inst_status
        if len(query.keys()) == 0:
            content = {'message':'No parameters given.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            cursor = instance.find(query)
            instances = []
            for resultInstance in cursor:
                resultInstance['id'] = resultInstance['_id']
                del resultInstance['_id']
                instances.append(resultInstance)
            serializer = resInstanceSerializer(instances)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        content = {'message':'No template found with the given parameters.'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

################################################################################
# 
# Function Name: add_repository(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Add a repository
# 
################################################################################
@api_view(['POST'])
def add_repository(request):
    """
    POST http://localhost/rest/repositories/add
    POST data name="name", protocol="protocol", address="address", port=port, user="user", password="password"
    """
    iSerializer = instanceSerializer(data=request.DATA)
    if iSerializer.is_valid():
        errors = ""
        # test if the protocol is HTTP or HTTPS
        if request.DATA['protocol'].upper() not in ['HTTP','HTTPS']:
            errors += 'Allowed protocol are HTTP and HTTPS.'
        # test if the name is "Local"
        if (request.DATA['name'] == ""):
            errors += "The name cannot be empty."
        elif (request.DATA['name'] == "Local"):
            errors += 'By default, the instance named Local is the instance currently running.'
        else:
            # test if an instance with the same name exists
            instance = Instance.objects(name=request.DATA['name'])
            if len(instance) != 0:
                errors += "An instance with the same name already exists."
        regex = re.compile("^[0-9]{1,5}$")
        if not regex.match(str(request.DATA['port'])):
            errors += "The port number is not valid."
        regex = re.compile("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        if not regex.match(request.DATA['address']):
            errors += "The address is not valid."
        # test if new instance is not the same as the local instance
        if request.DATA['address'] == request.META['REMOTE_ADDR'] and str(request.DATA['port']) == request.META['SERVER_PORT']:
            errors += "The address and port you entered refer to the instance currently running."
        else:
            # test if an instance with the same address/port exists
            instance = Instance.objects(address=request.DATA['address'], port=request.DATA['port'])
            if len(instance) != 0:
                errors += "An instance with the address/port already exists."
        
        if errors != "":
            content = {'message': errors}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        inst_status = "Unreachable"
        try:
            url = request.DATA['protocol'] + "://" + request.DATA['address'] + ":" + request.DATA['port'] + "/rest/ping"
            r = requests.get(url, auth=(request.DATA['user'], request.DATA['password']))
            if r.status_code == 200:
                inst_status = "Reachable"
        except Exception, e:
            pass
        Instance(name=request.DATA['name'], protocol=request.DATA['protocol'], address=request.DATA['address'], port=request.DATA['port'], user=request.DATA['user'], password=request.DATA['password'], status=inst_status).save()
        return Response(iSerializer.data, status=status.HTTP_201_CREATED)
    return Response(iSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: delete_repository(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Delete a repository
# 
################################################################################
@api_view(['GET'])
def delete_repository(request):
    """
    GET http://localhost/rest/repositories/delete?id=IDtodelete
    """
    id = request.QUERY_PARAMS.get('id', None)
    
    if id is not None:   
        try:
            instance = Instance.objects.get(pk=id)        
        except:
            content = {'message':'No instance found with the given id.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No instance id provided to restore.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    instance.delete()
    content = {'message':'Instance deleted with success.'}
    return Response(content, status=status.HTTP_404_NOT_FOUND)

################################################################################
# 
# Function Name: update_repository(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Update a repository
# 
################################################################################
@api_view(['PUT'])
def update_repository(request):  
    """
    PUT http://localhost/rest/repositories/update?id=IDtoUpdate
    PUT data name="name", protocol="protocol", address="address", port=port, user="user", password="password"
    """    
    id = request.QUERY_PARAMS.get('id', None)        
    
    if id is not None:   
        try:
            instance = Instance.objects.get(pk=id)        
        except:
            content = {'message':'No instance found with the given id.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No instance id provided to restore.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    serializer = instanceSerializer(instance, data=request.DATA)
    if serializer.is_valid():
        errors = ""
        # test if the protocol is HTTP or HTTPS
        if request.DATA['protocol'].upper() not in ['HTTP','HTTPS']:
            errors += 'Allowed protocol are HTTP and HTTPS.'
        # test if the name is "Local"
        if (request.DATA['name'] == ""):
            errors += "The name cannot be empty."
        elif (request.DATA['name'] == "Local"):
            errors += 'By default, the instance named Local is the instance currently running.'
        else:
            # test if an instance with the same name exists
            instances = Instance.objects(name=request.DATA['name'])
            if len(instances) != 0:
                errors += "An instance with the same name already exists."
        regex = re.compile("^[0-9]{1,5}$")
        if not regex.match(str(request.DATA['port'])):
            errors += "The port number is not valid."
        regex = re.compile("^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$")
        if not regex.match(request.DATA['address']):
            errors += "The address is not valid."
        # test if new instance is not the same as the local instance
        if request.DATA['address'] == request.META['REMOTE_ADDR'] and str(request.DATA['port']) == request.META['SERVER_PORT']:
            errors += "The address and port you entered refer to the instance currently running."
        else:
            # test if an instance with the same address/port exists
            instances = Instance.objects(address=request.DATA['address'], port=request.DATA['port'])
            if len(instances) != 0:
                errors += "An instance with the address/port already exists."
        
        if errors != "":
            content = {'message': errors}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
        inst_status = "Unreachable"
        try:
            url = request.DATA['protocol'] + "://" + request.DATA['address'] + ":" + request.DATA['port'] + "/rest/ping"
            r = requests.get(url, auth=(request.DATA['user'], request.DATA['password']))
            if r.status_code == 200:
                inst_status = "Reachable"
        except Exception, e:
            pass
        instance.name=request.DATA['name']
        instance.protocol=request.DATA['protocol']
        instance.address=request.DATA['address']
        instance.port=request.DATA['port']
        instance.user=request.DATA['user']
        instance.password=request.DATA['password']
        instance.status=inst_status
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: select_all_users(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get all users
# 
################################################################################
@api_view(['GET'])
def select_all_users(request):
    """
    GET http://localhost/rest/users/select/all
    """
    users = User.objects.all()
    serializer = UserSerializer(users)
    return Response(serializer.data, status=status.HTTP_200_OK)

################################################################################
# 
# Function Name: select_user(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Select users that match parameters
# 
################################################################################
@api_view(['GET'])
def select_user(request):
    """
    GET http://localhost/rest/users/select?param1=value1&param2=value2
    URL parameters: 
    username: string
    first_name: string
    last_name: string
    email: string    
    For string fields, you can use regular expressions: /exp/
    """    
    username = request.QUERY_PARAMS.get('username', None)
    first_name = request.QUERY_PARAMS.get('first_name', None)
    last_name = request.QUERY_PARAMS.get('last_name', None)
    email = request.QUERY_PARAMS.get('email', None)
            
    predicates = []
    if username is not None:
        if len(username) >= 2 and username[0] == '/' and username[-1] == '/':
            predicates.append(['username__regex',username[1:-1]])
        else:
            predicates.append(['username',username])
    if first_name is not None:
        if len(first_name) >= 2 and first_name[0] == '/' and first_name[-1] == '/':
            predicates.append(['first_name__regex',first_name[1:-1]])
        else:
            predicates.append(['first_name',first_name])
    if last_name is not None:
        if len(last_name) >= 2 and last_name[0] == '/' and last_name[-1] == '/':
            predicates.append(['last_name__regex',last_name[1:-1]])
        else:
            predicates.append(['last_name',last_name])
    if email is not None:
        if len(email) >= 2 and email[0] == '/' and email[-1] == '/':
            predicates.append(['email__regex',email[1:-1]])
        else:
            predicates.append(['email',email])
    
    q_list = [Q(x) for x in predicates]
    if len(q_list) != 0:
        try:
            users = User.objects.get(reduce(operator.and_, q_list))
        except:
            users = []
    else:
        users = []
    serializer = UserSerializer(users)
    return Response(serializer.data, status=status.HTTP_200_OK)

################################################################################
# 
# Function Name: add_user(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Add an user to the system
# 
################################################################################
@api_view(['POST'])
def add_user(request):
    """
    POST http://localhost/rest/users/add
    POST data username="username", password="password" first_name="first_name", last_name="last_name", port=port, email="email"
    """    
    serializer = insertUserSerializer(data=request.DATA)
    if serializer.is_valid():
        username = request.DATA['username']
        password = request.DATA['password']
        if 'first_name' in request.DATA:
            first_name = request.DATA['first_name']
        else:
            first_name = ""
        if 'last_name' in request.DATA:
            last_name = request.DATA['last_name']
        else:
            last_name = ""
        if 'email' in request.DATA:
            email = request.DATA['email']
        else:
            email = ""
        try:
            user = User.objects.create_user(username=username,password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception, e:
            content = {'message':e.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: delete_user(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Delete an user
# 
################################################################################
@api_view(['GET'])
def delete_user(request):
    """
    GET http://localhost/rest/users/delete?username=username
    URL parameters: 
    username: string
    """
    username = request.QUERY_PARAMS.get('username', None)
    if username is not None:
        try:
            user = User.objects.get(username=username)
            user.delete()
            content = {'message':"User deleted with success."}
            return Response(content, status=status.HTTP_200_OK)
        except:
            content = {'message':"The given username does not exist."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':"No username provided."}
        return Response(content, status=status.HTTP_404_NOT_FOUND)

################################################################################
# 
# Function Name: update_user(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Update user's information
# 
################################################################################  
@api_view(['PUT'])
def update_user(request):
    """
    PUT http://localhost/rest/users/update?username=userToUpdate
    PUT data first_name="first_name", last_name="last_name", port=port, email="email"
    """    
    username = request.QUERY_PARAMS.get('username', None)        
        
    if id is not None:   
        try:
            user = User.objects.get(username=username)        
        except:
            content = {'message':'No user found with the given username.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
    else:
        content = {'message':'No username provided to restore.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    serializer = updateUserSerializer(data=request.DATA)
    if serializer.is_valid():    
        try:
            if 'first_name' in request.DATA:
                user.first_name = request.DATA['first_name']
            if 'last_name' in request.DATA:
                user.last_name = request.DATA['last_name']
            if 'email' in request.DATA:
                user.email = request.DATA['email']
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception, e:
            content = {'message':e.message}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: docs(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Gives the link to the API documentation
# 
################################################################################
@api_view(['GET'])
def docs(request):
    content={'message':'Invalid command','docs':'http://'+str(request.get_host())+'/docs/api'}
    return Response(content, status=status.HTTP_400_BAD_REQUEST)

################################################################################
# 
# Function Name: ping(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Ping the API
# 
################################################################################
@api_view(['GET'])
def ping(request):
    content={'message':'Endpoint reached'}
    return Response(content, status=status.HTTP_200_OK)


################################################################################
# 
# Function Name: get_dependency(request)
# Inputs:        request - 
# Outputs:        
# Exceptions:    None
# Description:   Get a template dependency using its mongodb id
# 
################################################################################   
@api_view(['GET'])
def get_dependency(request):
    """
    GET http://localhost/rest/types/get-dependency?id=id
    """  
    # TODO: can change to the hash
    id = request.QUERY_PARAMS.get('id', None)
    
    if id is None:
        content={'message':'No dependency id provided.'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            if id in MetaSchema.objects.all().values_list('schemaId'):
                meta = MetaSchema.objects.get(schemaId=id)
                content = meta.api_content
            else:
                type = Type.objects.get(pk=str(id))
                content = type.content
            
            xsdEncoded = content.encode('utf-8')
            fileObj = StringIO(xsdEncoded)
            response = HttpResponse(fileObj, content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=' + str(id)
            return response
        except: 
            content={'message':'No dependency could be found with the given id.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        