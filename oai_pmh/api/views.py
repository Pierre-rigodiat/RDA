################################################################################
#
# File Name: views.py
# Application: Informatics Core
# Description:
#
# Author: Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

# REST Framework
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
# OAI-PMH
from sickle import Sickle
from sickle.models import Set, MetadataFormat, Record
from sickle.oaiexceptions import NoSetHierarchy, NoMetadataFormat
# Serializers
from oai_pmh.api.serializers import IdentifyObjectSerializer, MetadataFormatSerializer, SetSerializer,\
    RegistrySerializer, ListRecordsSerializer, RegistryURLSerializer, RecordSerializer, \
    IdentifySerializer, UpdateRecordSerializer, DeleteRecordSerializer, UpdateRegistrySerializer, \
    UpdateMyRegistrySerializer, MyMetadataFormatSerializer, DeleteMyMetadataFormatSerializer,\
    UpdateMyMetadataFormatSerializer, GetRecordSerializer, UpdateMySetSerializer, DeleteMySetSerializer,\
    MySetSerializer, MyTemplateMetadataFormatSerializer
# Models
from mgi.models import OaiRegistry, OaiSet, OaiMetadataFormat, OaiIdentify, OaiSettings, Template, OaiRecord,\
OaiMyMetadataFormat, OaiMySet, OaiMetadataformatSet
# DB Connection
from pymongo import MongoClient
from mgi.settings import MONGODB_URI, MGI_DB
from mongoengine import NotUniqueError
import xmltodict
import requests
from utils.XSDhash import XSDhash
from lxml import etree
from lxml.etree import XMLSyntaxError
import datetime
from oai_pmh import datestamp


################################################################################
#
# Function Name: add_registry(request)
# Inputs:        request -
# Outputs:       201 Registry created.
# Exceptions:    400 Error connecting to database.
#                400 [List of missing required fields].
#                400 An error occured when trying to save document.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                409 Registry already exists
# Description:   OAI-PMH Add Registry
#
################################################################################
@api_view(['POST'])
def add_registry(request):
    """
    POST http://localhost/oai_pmh/add/registry
    POST data query="{'url':'value','harvestrate':'number', 'harvest':'True or False'}"
    """
    if request.user.is_authenticated():
        #Serialization of the input data
        serializer = RegistrySerializer(data=request.DATA)
        #If all fields are okay
        if serializer.is_valid():
            #Check the URL
            try:
                url = request.DATA['url']
                #We check first if this repository already exists in database. If yes, we return a response 409
                if OaiRegistry.objects(url__exact=url).count() > 0:
                    return Response({'message':'Unable to create the data provider. The data provider already exists.'}, status=status.HTTP_409_CONFLICT)
            except ValueError:
                return Response("Invalid URL", status=status.HTTP_400_BAD_REQUEST)

            #Chech the harvest rate. If not provided, set to none
            if 'harvestrate' in request.DATA:
                harvestrate = request.DATA['harvestrate']
            else:
                harvestrate = ""

            #Chech the harvest action. If not provided, set to false
            if 'harvest' in request.DATA:
                harvest = request.DATA['harvest'] == 'True'
            else:
                harvest = False

            #Get the identify information for the given URL
            identify = objectIdentify(request)
            #If status OK, we try to serialize data and check if it's valid
            if identify.status_code == status.HTTP_200_OK:
                identifyData = identify.data
                serializerIdentify = IdentifyObjectSerializer(data=identifyData)
                #If it's not valid, return with a bad request
                if not serializerIdentify.is_valid():
                    return Response(serializerIdentify.errors, status=status.HTTP_400_BAD_REQUEST)
            #Return a response with the status_code and the message provided by the called function
            else:
                return Response({'message': identify.data['message']}, status=identify.status_code)

            #Get the sets information for the given URL
            sets = listObjectSets(request)
            setsData = []
            #If status OK, we try to serialize data and check if it's valid
            if sets.status_code == status.HTTP_200_OK:
                setsData = sets.data
                serializerSet = SetSerializer(data=setsData)
                #If it's not valid, return with a bad request
                if not serializerSet.is_valid():
                    return Response(serializerSet.errors, status=status.HTTP_400_BAD_REQUEST)
             #Return a response with the status_code and the message provided by the called function
            elif sets.status_code != status.HTTP_204_NO_CONTENT:
                return Response({'message': sets.data['message']}, status=sets.status_code)

            #Get the metadata formats information for the given URL
            metadataformats = listObjectMetadataFormats(request)
            metadataformatsData = []
            #If status OK, we try to serialize data and check if it's valid
            if metadataformats.status_code == status.HTTP_200_OK:
                metadataformatsData = metadataformats.data
                serializerMetadataFormat = MetadataFormatSerializer(data=metadataformatsData)
                #If it's not valid, return with a bad request
                if not serializerMetadataFormat.is_valid():
                    return Response(serializerMetadataFormat.errors, status=status.HTTP_400_BAD_REQUEST)
             #Return a response with the status_code and the message provided by the called function
            elif metadataformats.status_code != status.HTTP_204_NO_CONTENT:
                return Response({'message': metadataformats.data['message']}, status=metadataformats.status_code)

            try:
                #Creation of the registry
                registry = OaiRegistry()
                #Get the raw XML from a dictionary
                try:
                    identifyRaw = xmltodict.parse(identifyData['raw'])
                except:
                    identifyRaw = {}
                #Constructor if Identity
                identify = OaiIdentify(adminEmail=identifyData['adminEmail'],
                                          baseURL=identifyData['baseURL'],
                                          repositoryName=identifyData['repositoryName'],
                                          deletedRecord=identifyData['deletedRecord'],
                                          delimiter=identifyData['delimiter'],
                                          description=identifyData['description'],
                                          earliestDatestamp=identifyData['earliestDatestamp'],
                                          granularity=identifyData['granularity'],
                                          oai_identifier=identifyData['oai_identifier'],
                                          protocolVersion=identifyData['protocolVersion'],
                                          repositoryIdentifier=identifyData['repositoryIdentifier'],
                                          sampleIdentifier=identifyData['sampleIdentifier'],
                                          scheme=identifyData['scheme'],
                                          raw=identifyRaw).save()
                #Add identity
                registry.identify = identify
                registry.name = identify.repositoryName
                registry.url = url
                registry.harvestrate = harvestrate
                registry.description = identify.description
                registry.harvest = harvest
                #Save the registry
                registry.save()
                #Creation of each set
                for set in setsData:
                    try:
                        raw = xmltodict.parse(set['raw'])
                        obj = OaiSet(setName=set['setName'], setSpec=set['setSpec'], raw= raw,
                                     registry=str(registry.id))
                        obj.save()
                    except:
                        pass
                #Creation of each metadata format
                for metadataformat in metadataformatsData:
                    try:
                        raw = xmltodict.parse(metadataformat['raw'])
                        obj = OaiMetadataFormat(metadataPrefix=metadataformat['metadataPrefix'],
                                                metadataNamespace=metadataformat['metadataNamespace'],
                                                schema=metadataformat['schema'], raw= raw, registry=str(registry.id))
                        http_response = requests.get(obj.schema)
                        if str(http_response.status_code) == "200":
                            xmlSchema = xmltodict.parse(http_response.text)
                            obj.xmlSchema = xmlSchema
                            hash = XSDhash.get_hash(http_response.text)
                            obj.hash = hash
                            template = Template.objects(hash=hash).first()
                            if template:
                                obj.template = template
                        obj.save()
                    except:
                        pass
                #Save the registry
                registry.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except NotUniqueError as e:
                #Manual Rollback
                if identify:
                    identify.delete()
                OaiSet.objects(registry=registry.id).delete()
                OaiMetadataFormat.objects(registry=registry.id).delete()
                return Response({'message':'Unable to create the registry. The registry already exists.%s'%e.message}, status=status.HTTP_409_CONFLICT)
            except Exception as e:
                #Manual Rollback
                if identify:
                    identify.delete()
                OaiSet.objects(registry=registry.id).delete()
                OaiMetadataFormat.objects(registry=registry.id).delete()
                return Response({'message':'An error occured when trying to save document. %s'%e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: select_all_registries(request)
# Inputs:        request -
# Outputs:       200 Found registries.
# Exceptions:    400 Error connecting to database.
#                401 Unauthorized.
# Description:   OAI-PMH Select All Registries
#
################################################################################
@api_view(['GET'])
def select_all_registries(request):
    """
    GET http://localhost/oai_pmh/select/all/registries
    """
    if request.user.is_authenticated():
        try:
            rec_collection = MongoClient(MONGODB_URI)[MGI_DB]['registry']
        except Exception:
            return Response({'message':'Error connecting to database.'}, status=status.HTTP_400_BAD_REQUEST)

        registry = rec_collection.find({}, {"_id":False}) # Exclude ObjectID from result

        rsp = []
        for r in registry:
            rsp.append(r)
        return Response(rsp, status=status.HTTP_200_OK)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: select_registry(request)
# Inputs:        request -
# Outputs:       200 Found registry.
# Exceptions:    400 Error connecting to database.
#                400 No record found matching the identifier: [identifier]
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH Select Registry
#
################################################################################
@api_view(['GET'])
def select_registry(request):
    """
    GET http://localhost/oai_pmh/select/registry
    name: string
    """
    if request.user.is_authenticated:
        errors = []
        try:
            name = request.GET['name']
        except:
            content = {'name':['This field is required.']}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        try:
            registry = OaiRegistry.objects.get(name=name)
        except Exception as e:
            content = {'message':'No registry found with the given parameters.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        serializer = RegistrySerializer(registry)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: update_registry(request)
# Inputs:        request -
# Outputs:       201 Registry updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No registry found with the given identity.
# Description:   OAI-PMH Update Registry
#
################################################################################
@api_view(['PUT'])
def update_registry(request):
    """
    PUT http://localhost/oai_pmh/update/registry
    PUT data query="{'id':'value'}"
    id: string
    """
    if request.user.is_authenticated():
        #Serialization of the input data
        serializer = UpdateRegistrySerializer(data=request.DATA)
        #If it's valid
        if serializer.is_valid():
            #We retrieve all information
            try:
                if 'id' in request.DATA:
                    id = request.DATA['id']
                    registry = OaiRegistry.objects.get(pk=id)
                else:
                    rsp = {'id':['This field is required.']}
                    return Response(rsp, status=status.HTTP_400_BAD_REQUEST)
            except:
                content = {'message':'No registry found with the given id.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            if 'harvestrate' in request.DATA:
                harvestrate = request.DATA['harvestrate']
                if harvestrate:
                    registry.harvestrate = harvestrate
            if 'harvest' in request.DATA:
                harvest = request.DATA['harvest']
                if harvest:
                    registry.harvest =  harvest == 'True'
            try:
                #Save the modifications
               registry.save()
            except Exception as e:
                return Response({'message':'Unable to update registry. \n%s'%e.message}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'Serializer failed validation. '}, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


################################################################################
#
# Function Name: update_my_registry(request)
# Inputs:        request -
# Outputs:       201 Registry updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No registry found with the given identity.
# Description:   OAI-PMH Update Registry
#
################################################################################
@api_view(['PUT'])
def update_my_registry(request):
    """
    PUT http://localhost/oai_pmh/update/my-registry
    PUT data query="{'repositoryName':'value', 'enableHarvesting':'True or False'}"
    """
    if request.user.is_authenticated():
        #Serialization of the input data
        serializer = UpdateMyRegistrySerializer(data=request.DATA)
        #If it's valid
        if serializer.is_valid():
            #We retrieve all information
            try:
                if 'repositoryName' in request.DATA:
                    repositoryName = request.DATA['repositoryName']
                if 'enableHarvesting' in request.DATA:
                    enableHarvesting = request.DATA['enableHarvesting']
                    if enableHarvesting:
                        enableHarvesting =  enableHarvesting == 'True'
            except:
                content = {'message':'Error while retrieving information.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            try:
                #Save the modifications
                information = OaiSettings.objects.get()
                information.repositoryName = repositoryName
                information.enableHarvesting = enableHarvesting
                information.save()
            except Exception as e:
                return Response({'message':'Unable to update registry. \n%s'%e.message}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: delete_registry(request)
# Inputs:        request -
# Outputs:       200 Record deleted.
# Exceptions:    400 Error connecting to database.
#                400 [Name] not found in request.
#                400 Unspecified.
#                401 Unauthorized.
#                404 No record found with the given identity.
# Description:   OAI-PMH Delete Registry
#
################################################################################
@api_view(['POST'])
def delete_registry(request):
    """
    POST http://localhost/oai_pmh/delete/registry
    POST data query="{'RegistryId':'value'}"
    """
    if request.user.is_authenticated():
        #Get the ID
        try:
            id = request.DATA['RegistryId']
        except:
            rsp = {'RegistryId':['This field is required.']}
            return Response(rsp, status=status.HTTP_400_BAD_REQUEST)
        try:
            try:
                registry = OaiRegistry.objects.get(pk=id)
            except:
                content = {'message':'No registry found with the given id.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            #Delete all ReferenceFields
            #Identify
            registry.identify.delete()
            #Records
            OaiRecord.objects(registry=id).delete()
            #Sets
            OaiSet.objects(registry=id).delete()
            #Metadata formats
            OaiMetadataFormat.objects(registry=id).delete()
            #We can now delete the registry
            registry.delete()
            content = {'message':"Registry deleted with success."}
            return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            Response({"message":e.message}, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: getRecord(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    400 Error in Metadata Prefix value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to retrieve record.
# Description:   OAI-PMH Get Record
#
################################################################################
@api_view(['POST'])
def getRecord(request):
    """
    POST http://localhost/oai_pmh/rest/getrecord
    POST data query="{'url':'value', 'identifier':'value', 'metadataprefix':'value'}"
    """
    if request.user.is_authenticated():
        try:
            serializer = GetRecordSerializer(data=request.DATA)
            if serializer.is_valid():
                url = request.DATA['url']
                identifier = request.DATA['identifier']
                metadataprefix = request.DATA['metadataprefix']
                sickle = Sickle(url)
                grResponse = sickle.GetRecord(metadataPrefix=metadataprefix, identifier=identifier)
                record = Record(grResponse.xml)
                rtn=[]
                rtn.append({"identifier": record.header.identifier,
                          "datestamp": record.header.datestamp,
                          "deleted": record.deleted,
                          "sets": record.header.setSpecs,
                          "metadataPrefix": metadataprefix,
                          "metadata": etree.tostring(record.xml.find('.//' + '{http://www.openarchives.org/OAI/2.0/}' + 'metadata/')),
                          "raw": record.raw})

                serializer = RecordSerializer(rtn)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            content = {'message':'An error occurred when attempting to retrieve record. %s'%e}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: getMetadata(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH Get Metadata
#
################################################################################
def getMetadata(request):
    """
    POST http://localhost/oai_pmh/identify
    """
    if request.user.is_authenticated():
        try:

            return Response("", status=status.HTTP_200_OK)
        except:
            content = {'message':'An error occurred when attempting to identify resource.'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

import json
################################################################################
#
# Function Name: objectIdentify(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    400 Error getting URL.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH Identify
#
################################################################################
@api_view(['POST'])
def objectIdentify(request):
    """
    POST http://localhost/oai_pmh/objectidentify
    POST data query="{'url':'value'}"
    """
    if request.user.is_authenticated():
        try:
            serializer = IdentifySerializer(data=request.DATA)
            if serializer.is_valid():
                url = request.DATA['url']
                req = sickleObjectIdentify(url)
                if req.status_code == status.HTTP_200_OK:
                    return Response(req.data, status=status.HTTP_200_OK)
                else:
                    return Response({'message':req.data['message']}, status=req.status_code)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            content = {'message':'An error occurred when attempting to identify resource.'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


################################################################################
#
# Function Name: sickleObjectIdentify(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH Identify
#
################################################################################
def sickleObjectIdentify(url):
    try:
        sickle = Sickle(url)
        identify = sickle.Identify()
        rtn= {"adminEmail": identify.adminEmail,
              "baseURL": identify.baseURL,
              "repositoryName": identify.repositoryName,
              "deletedRecord": identify.deletedRecord,
              "delimiter": identify.delimiter,
              "description": identify.description,
              "earliestDatestamp": identify.earliestDatestamp,
              "granularity": identify.granularity,
              "oai_identifier": identify.oai_identifier,
              "protocolVersion": identify.protocolVersion,
              "repositoryIdentifier": identify.repositoryIdentifier,
              "sampleIdentifier": identify.sampleIdentifier,
              "scheme": identify.scheme,
              "raw": identify.raw}
        serializer = IdentifyObjectSerializer(rtn)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        content = {'message':'An error occurred when attempting to identify resource.'}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

################################################################################
#
# Function Name: listObjectMetadataFormats(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    204 No metadata formats
#                400 Error in URL value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List Object Metadata Formats
#
################################################################################
@api_view(['POST'])
def listObjectMetadataFormats(request):
    """
    POST http://localhost/oai_pmh/listobjectmetadataformats
    POST data query="{'url':'value'}"
    """
    if request.user.is_authenticated():
        try:
            serializer = IdentifySerializer(data=request.DATA)
            if serializer.is_valid():
                url = request.DATA['url']
                req = sickleListObjectMetadataFormats(url)
                if req.status_code == status.HTTP_200_OK:
                    return Response(req.data, status=status.HTTP_200_OK)
                else:
                   return Response({'message':req.data['message']}, status=req.status_code)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


################################################################################
#
# Function Name: sickleListObjectMetadataFormats(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    204 No metadata formats
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List Object Metadata Formats
#
################################################################################
def sickleListObjectMetadataFormats(url):
    try:
        sickle = Sickle(url)
        rsp = sickle.ListMetadataFormats()
        rtn = []
        try:
            while True:
                obj = rsp.next()
                metadata = MetadataFormat(obj.xml)
                rtn.append({"metadataPrefix": metadata.metadataPrefix,
                          "metadataNamespace": metadata.metadataNamespace,
                          "schema": metadata.schema,
                          "raw": metadata.raw})
        except StopIteration:
            pass
        serializer = MetadataFormatSerializer(rtn)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except NoMetadataFormat as e:
        #This repository does not support sets
        content = {'message':'%s'%e.message}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

################################################################################
#
# Function Name: listObjectSets(request)
# Inputs:        request -
# Outputs:       200 Response successful.
#                204 No Sets
# Exceptions:    400 Error(s) in required values value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List object Sets
#
################################################################################
@api_view(['POST'])
def listObjectSets(request):
    """
    POST http://localhost/oai_pmh/listObjectSets
    POST data query="{'url':'value'}"
    """
    if request.user.is_authenticated():
        try:
            serializer = IdentifySerializer(data=request.DATA)
            if serializer.is_valid():
                url = request.DATA['url']
                req = sickleListObjectSets(url)
                if req.status_code == status.HTTP_200_OK:
                    return Response(req.data, status=status.HTTP_200_OK)
                else:
                   return Response({'message':req.data['message']}, status=req.status_code)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


################################################################################
#
# Function Name: sickleListObjectSets(request)
# Inputs:        request -
# Outputs:       200 Response successful.
#                204 No Sets
# Exceptions:    400 Error(s) in required values value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List object Sets
#
################################################################################
def sickleListObjectSets(url):
    try:
        sickle = Sickle(url)
        rsp = sickle.ListSets()
        rtn = []
        try:
            while True:
                obj = rsp.next()
                set = Set(obj.xml)
                rtn.append({  "setName":set.setName,
                              "setSpec":set.setSpec,
                              "raw":set.raw})
        except StopIteration:
            pass
        serializer = SetSerializer(rtn)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except NoSetHierarchy as e:
        #This repository does not support sets
        content = {'message':'%s'%e.message}
        return Response(content, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

################################################################################
#
# Function Name: listIdentifiers(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    400 Error(s) in required values value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List Identifiers
#
################################################################################
@api_view(['POST'])
def listIdentifiers(request):
    """
    POST http://localhost/oai_pmh/listidentifiers
    POST data query="{'url':'value', 'metadataprefix':'value'}" optional {'set':'value'}
    """
    if request.user.is_authenticated():
        try:
            serializer = RegistryURLSerializer(data=request.DATA)
            if serializer.is_valid():
                url = request.DATA['url']
                metadataprefix = request.DATA['metadataprefix']
                if 'set' in request.DATA:
                    setH = request.DATA['set']
                else:
                    setH = ""
                sickle = Sickle(url)
                rsp = sickle.ListIdentifiers(metadataPrefix=metadataprefix, set=setH)
                rtn = []
                try:
                    while True:
                        rtn.append( dict(rsp.next()) )
                except StopIteration:
                    pass
                return Response({'message':rtn}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: getData(request)
# Inputs:        request -
# Outputs:       OAI_PMH response.
#                400 Error(s) in required values value.
#                401 Unauthorized.
#                404 Server not found.
#                500 Malformed URL.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI_PMH response.
#
################################################################################
@api_view(['POST'])
def getData(request):
    """
    GET http://localhost/oai_pmh/api/getdata/
    url: string
    """
    if request.user.is_authenticated():
        try:
            url = request.POST['url']
        except Exception as e:
            content = {'url':['This field is required.']}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if str(url).__contains__('?'):
            registryURl = str(url).split('?')[0]
            #Check if the OAI Registry is available
            try:
                sickle = Sickle(registryURl)
                sickle.Identify()
            except Exception:
                return Response('An error occurred when attempting to identify resource.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            http_response = requests.get(url)
            if http_response.status_code == status.HTTP_200_OK:
                return Response(http_response.text, status=status.HTTP_200_OK)
            elif http_response.status_code == status.HTTP_404_NOT_FOUND:
                return Response('Server not found.', status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('An error occurred.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response('An error occurred, url malformed.', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response('Only an administrator can use this feature.', status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: harvest(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    400 Error(s) in required values value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List Records
#
################################################################################
@api_view(['POST'])
def harvest(request):
    """
    POST http://localhost/oai_pmh/api/harvest
    POST data query="{'registry_id':'value'}"
    """
    if request.user.is_authenticated():
        #List of errors
        allErrors = []
        try:
            try:
                registry_id = request.DATA['registry_id']
            except Exception:
                content = {'registry_id':['This field is required.']}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            #We retrieve the registry (data provider)
            try:
                registry = OaiRegistry.objects(pk=registry_id).get()
                url = registry.url
            except:
                content = {'message':'No registry found with the given parameters.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            #Set the last update date
            registry.lastUpdate = datetime.datetime.now()
            #We are harvesting
            registry.isHarvesting = True
            registry.save()
            records = []
            #Get all available metadata formats
            metadataformats = OaiMetadataFormat.objects(registry=registry_id, harvest=True)
            #Get all sets
            registryAllSets = OaiSet.objects(registry=registry_id).order_by("setName")
            #Get all available  sets
            registrySetsToHarvest = OaiSet.objects(registry=registry_id, harvest=True).order_by("setName")
            #Check if we have to retrieve all sets or not. If all sets, no need to provide the set parameter in the
            #harvest request. Avoid to retrieve same records for nothing (If records are in many sets).
            searchBySets = len(registryAllSets) != len(registrySetsToHarvest)
            #Search by sets
            if searchBySets or len(registryAllSets) != 0:
                for set in registrySetsToHarvest:
                    for metadataFormat in metadataformats:
                        currentDate = datetime.datetime.now()
                        try:
                            #Retrieve the last update for this metadata format and this set
                            objOaiMFSets = OaiMetadataformatSet.objects(metadataformat=metadataFormat, set=set).get()
                            lastUpdate = datestamp.datetime_to_datestamp(objOaiMFSets.lastUpdate)
                            #Set the new date
                            objOaiMFSets.lastUpdate = currentDate
                        except:
                            lastUpdate = None
                            #Set the new date
                            objOaiMFSets = OaiMetadataformatSet(metadataformat=metadataFormat, set=set, lastUpdate=currentDate)
                        errors = harvestRecords(url, registry_id, metadataFormat, lastUpdate, registryAllSets, set)
                        #If no exceptions was thrown and no errors occured, we can update the lastUpdate date
                        if len(errors) == 0:
                            #Set the last update date
                            metadataFormat.lastUpdate = datetime.datetime.now()
                            metadataFormat.save()
                            objOaiMFSets.save()
                        else:
                            allErrors.append(errors)
            #If we don't have to search by set or the OAI Registry doesn't support sets
            else:
                for metadataFormat in metadataformats:
                    try:
                        #Retrieve the last update for this metadata format
                        lastUpdate = datestamp.datetime_to_datestamp(metadataFormat.lastUpdate)
                    except:
                        lastUpdate = None
                    #Update the new date for the metadataFormat
                    currentDate = datetime.datetime.now()
                    errors = harvestRecords(url, registry_id, metadataFormat, lastUpdate, registryAllSets)
                    #If no exceptions was thrown and no errors occured, we can update the lastUpdate date
                    if errors and len(errors) == 0:
                        #Update the update date for all sets
                        if len(registrySetsToHarvest) != 0:
                            for set in registrySetsToHarvest:
                                set.lastUpdate = currentDate
                                set.save()
                        #Update the update date
                        metadataFormat.lastUpdate = currentDate
                        metadataFormat.save()
                    else:
                        allErrors.append(errors)
            #Stop harvesting
            registry.isHarvesting = False
            registry.save()
            #Return the harvest status
            if len(allErrors) == 0:
                content = {'message':'Harvest data succeeded without errors.'}
            else:
                content = {'message': errors}

            return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            registry.isHarvesting = False
            registry.save()
            content = {'message':'An error occurred during the harvest process: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: harvestRecords(request)
# Inputs:        url, registry_id, metadataFormat, lastUpdate, registryAllSets, set=None -
# Outputs:       List of errors.
# Description:   Save OAI-PMH ListRecords (retrieved via OAI-PMH request) in Database
#
################################################################################
def harvestRecords(url, registry_id, metadataFormat, lastUpdate, registryAllSets, set=None):
    errors = []
    dataLeft = True
    resumptionToken = None
    #Get all records. Use of the resumption token
    while dataLeft:
        #Get the list of records
        if set != None:
            http_response, resumptionToken = getListRecords(url=url, metadataPrefix=metadataFormat.metadataPrefix, set_h=set.setSpec, fromDate=lastUpdate, resumptionToken=resumptionToken)
        else:
            http_response, resumptionToken = getListRecords(url=url, metadataPrefix=metadataFormat.metadataPrefix, fromDate=lastUpdate, resumptionToken=resumptionToken)
        if http_response.status_code == status.HTTP_200_OK:
            rtn = http_response.data
            for info in rtn:
                #Get corresponding sets
                sets = [x for x in registryAllSets if x.setSpec in info['sets']]
                raw = xmltodict.parse(info['raw'])
                metadata = xmltodict.parse(info['metadata'])
                try:
                    obj = OaiRecord.objects.filter(identifier=info['identifier'], metadataformat=metadataFormat).get()
                except:
                    obj = OaiRecord()
                obj.identifier=info['identifier']
                obj.datestamp=info['datestamp']
                obj.deleted=info['deleted']
                obj.metadataformat=metadataFormat
                obj.sets=sets
                obj.raw=raw
                obj.registry=registry_id
                #Custom Save to keep the order of metadata's XML
                obj.save(metadata=metadata)
        #Else, we get the status code with the error message provided by the http_response
        else:
            error = {'status_code': http_response.status_code, 'error': http_response.data['error']}
            errors.append(error)
        #There is more records if we have a resumption token.
        dataLeft = resumptionToken != None and resumptionToken != ''

    return errors

################################################################################
#
# Function Name: update_registry_harvest(request)
# Inputs:        request -
# Outputs:       201 Registry updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No registry found with the given identity.
# Description:   OAI-PMH Update Registry Harvest configuration.
#                Harvest records for the metadata formats and sets provided
#
################################################################################
@api_view(['PUT'])
def update_registry_harvest(request):
    """
    PUT http://localhost/oai_pmh/update/registry-harvest
    PUT data query="{'id':'value', metadataFormats:['id1', 'id2'..], sets:['id1', 'id2'..]}"
    id: string
    """
    if request.user.is_authenticated():
        #Serialization of the input data
        serializer = UpdateRegistrySerializer(data=request.DATA)
        #If it's valid
        if serializer.is_valid():
            #We retrieve all information
            try:
                if 'id' in request.DATA:
                    id = request.DATA['id']
                else:
                    rsp = {'id':['This field is required.']}
                    return Response(rsp, status=status.HTTP_400_BAD_REQUEST)
            except:
                content = {'message':'No registry found with the given id.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            try:
                #Set harvest=False for all
                OaiMetadataFormat.objects(registry=id).update(set__harvest=False)
                #For each metadataFormats selected, set harvest=True
                if 'metadataFormats' in request.DATA:
                    metadataFormats = request.DATA.getlist('metadataFormats')
                    if len(metadataFormats):
                        OaiMetadataFormat.objects(pk__in=metadataFormats).update(set__harvest=True)

                #Set harvest=False for all
                OaiSet.objects(registry=id).update(set__harvest=False)
                #For each sets selected, set harvest=True
                if 'sets' in request.DATA:
                    sets = request.DATA.getlist('sets')
                    if len(sets):
                        OaiSet.objects(pk__in=sets).update(set__harvest=True)

            except Exception as e:
                return Response({'message':'Unable to update the harvest configuration for the registry.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'Serializer failed validation. '}, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


################################################################################
#
# Function Name: update_registry_info(request)
# Inputs:        request -
# Outputs:       201 Registry updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No registry found with the given identity.
# Description:   OAI-PMH update Data Provider information
#
################################################################################
@api_view(['PUT'])
def update_registry_info(request):
    """
    PUT http://localhost/oai_pmh/update/registry-info
    PUT data query="{'registry_id':'value'}"
    id: string
    """
    if request.user.is_authenticated():
        try:
            registry_id = request.DATA['registry_id']
        except Exception:
            content = {'registry_id':['This field is required.']}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        #We retrieve the registry (data provider)
        try:
            registry = OaiRegistry.objects(pk=registry_id).get()
            url = registry.url
            registry.isUpdating = True
            registry.save()
        except:
            content = {'message':'No registry found with the given parameters.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        #Get the identify information for the given URL
        identify = sickleObjectIdentify(url)
        #If status OK, we try to serialize data and check if it's valid
        if identify.status_code == status.HTTP_200_OK:
            identifyData = identify.data
            serializerIdentify = IdentifyObjectSerializer(data=identifyData)
            #If it's not valid, return with a bad request
            if not serializerIdentify.is_valid():
                return Response(serializerIdentify.errors, status=status.HTTP_400_BAD_REQUEST)
        #Return a response with the status_code and the message provided by the called function
        else:
            return Response({'message': identify.data['message']}, status=identify.status_code)

        #Get the sets information for the given URL
        sets = sickleListObjectSets(url)
        setsData = []
        #If status OK, we try to serialize data and check if it's valid
        if sets.status_code == status.HTTP_200_OK:
            setsData = sets.data
            serializerSet = SetSerializer(data=setsData)
            #If it's not valid, return with a bad request
            if not serializerSet.is_valid():
                return Response(serializerSet.errors, status=status.HTTP_400_BAD_REQUEST)
         #Return a response with the status_code and the message provided by the called function
        elif sets.status_code != status.HTTP_204_NO_CONTENT:
            return Response({'message': sets.data['message']}, status=sets.status_code)

        #Get the metadata formats information for the given URL
        metadataformats = sickleListObjectMetadataFormats(url)
        metadataformatsData = []
        #If status OK, we try to serialize data and check if it's valid
        if metadataformats.status_code == status.HTTP_200_OK:
            metadataformatsData = metadataformats.data
            serializerMetadataFormat = MetadataFormatSerializer(data=metadataformatsData)
            #If it's not valid, return with a bad request
            if not serializerMetadataFormat.is_valid():
                return Response(serializerMetadataFormat.errors, status=status.HTTP_400_BAD_REQUEST)
         #Return a response with the status_code and the message provided by the called function
        elif metadataformats.status_code != status.HTTP_204_NO_CONTENT:
            return Response({'message': metadataformats.data['message']}, status=metadataformats.status_code)

        try:
            #Get the raw XML from a dictionary
            try:
                identifyRaw = xmltodict.parse(identifyData['raw'])
            except:
                identifyRaw = {}
            #Constructor if Identity
            identify = OaiIdentify(id=registry.identify.id,
                                  adminEmail=identifyData['adminEmail'],
                                  baseURL=identifyData['baseURL'],
                                  repositoryName=identifyData['repositoryName'],
                                  deletedRecord=identifyData['deletedRecord'],
                                  delimiter=identifyData['delimiter'],
                                  description=identifyData['description'],
                                  earliestDatestamp=identifyData['earliestDatestamp'],
                                  granularity=identifyData['granularity'],
                                  oai_identifier=identifyData['oai_identifier'],
                                  protocolVersion=identifyData['protocolVersion'],
                                  repositoryIdentifier=identifyData['repositoryIdentifier'],
                                  sampleIdentifier=identifyData['sampleIdentifier'],
                                  scheme=identifyData['scheme'],
                                  raw=identifyRaw).save()
            #Add identity
            registry.identify = identify
            registry.name = identify.repositoryName
            registry.description = identify.description
            #Save the registry
            registry.save()
            #Creation of each set
            for set in setsData:
                try:
                    raw = xmltodict.parse(set['raw'])
                    #Try to retrieve the existing set for this registry
                    try:
                        #Update
                        obj = OaiSet.objects(setSpec=set['setSpec'], registry=str(registry.id)).get()
                        obj.setName = set['setName']
                        obj.raw = raw
                    except:
                        #New set. Creation
                        obj = OaiSet(setName=set['setName'], setSpec=set['setSpec'], raw= raw,
                                     registry=str(registry.id))
                    obj.save()
                except:
                    pass
            #Creation of each metadata format
            for metadataformat in metadataformatsData:
                try:
                    #Try to retrieve this existing metadata format for this registry
                    raw = xmltodict.parse(metadataformat['raw'])
                    try:
                        #Update
                        obj = OaiMetadataFormat.objects(metadataPrefix=metadataformat['metadataPrefix'], registry=str(registry.id)).get()
                        obj.metadataNamespace = metadataformat['metadataNamespace']
                        obj.schema = metadataformat['schema']
                        obj.raw = raw
                    except:
                        #New metadata format Creation
                        obj = OaiMetadataFormat(metadataPrefix=metadataformat['metadataPrefix'],
                                                metadataNamespace=metadataformat['metadataNamespace'],
                                                schema=metadataformat['schema'], raw= raw, registry=str(registry.id))
                    http_response = requests.get(obj.schema)
                    if str(http_response.status_code) == "200":
                        xmlSchema = xmltodict.parse(http_response.text)
                        obj.xmlSchema = xmlSchema
                        hash = XSDhash.get_hash(http_response.text)
                        obj.hash = hash
                        template = Template.objects(hash=hash).first()
                        if template:
                            obj.template = template
                    obj.save()
                except:
                    pass
            #Save the registry
            registry.isUpdating = False
            registry.save()
            return Response({'message':'Data provider updated with success.'}, status=status.HTTP_201_CREATED)
        except NotUniqueError as e:
            registry.isUpdating = False
            return Response({'message':'Unable to update the registry. The registry already exists.%s'%e.message}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            registry.isUpdating = False
            return Response({'message':'An error occurred during the Data Provider update. Please contact your administrator. %s'%e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: listRecords(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    400 Error(s) in required values value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List Records
#
################################################################################
@api_view(['POST'])
def listObjectAllRecords(request):
    """
    POST http://localhost/oai_pmh/listobjectrecords
    POST data query="{'url':'value', 'metadataprefix':'value'}" optional: {'set':'value', 'fromDate':'date', 'until':'date'}
    """
    if request.user.is_authenticated():
        try:
            serializer = ListRecordsSerializer(data=request.DATA)

            if serializer.is_valid():
                url = request.DATA['url']
                metadataPrefix = request.DATA['metadataprefix']
                set_h = None
                if 'set' in request.DATA:
                    set_h = request.DATA['set']

                fromDate = None
                if 'fromDate' in request.DATA:
                    fromDate = request.DATA['fromDate']

                untilDate = None
                if 'until' in request.DATA:
                    untilDate = request.DATA['until']

                http_response, token = getListRecords(url, metadataPrefix, set_h, fromDate, untilDate)
                if http_response.status_code == status.HTTP_200_OK:
                    rtn = http_response.data
                #Else, we return a bad request response with the message provided by the API
                else:
                    content = http_response.data['error']
                    return Response(content, status=http_response.status_code)
                serializer = RecordSerializer(rtn)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: getListRecords(url, metadataPrefix, resumptionToken, set_h, fromDate, untilDate)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    400 Error(s) in required values value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List Records
#
################################################################################
def getListRecords(url, metadataPrefix=None, resumptionToken=None, set_h=None, fromDate=None, untilDate=None):
    """
    POST http://localhost/oai_pmh/listrecords
    """
    XMLParser = etree.XMLParser(remove_blank_text=True, recover=True)
    try:
        # needed = True
        metadataPrefixQuery = ''
        if metadataPrefix != None:
            metadataPrefixQuery = '&metadataPrefix=%s' % metadataPrefix

        resumptionTokenQuery = ""
        if resumptionToken != None:
            resumptionTokenQuery = '&resumptionToken=%s' % resumptionToken

        setQuery = ""
        if set_h != None:
            setQuery = '&set=%s' % set_h

        fromDateQuery = ""
        if fromDate != None:
            fromDateQuery = '&from=%s' % fromDate

        untilDateQuery = ""
        if untilDate != None:
            untilDateQuery = '&until=%s' % untilDate
        rtn = []

        #Check if the resumptionToken is None
        if resumptionToken == None:
            callUrl = url + '?verb=ListRecords' + metadataPrefixQuery + setQuery  + fromDateQuery + untilDateQuery
        #If not None, call the ListRecords verb with only the resumption tokem
        else:
            callUrl = url + '?verb=ListRecords' + resumptionTokenQuery

        # while needed:
        http_response = requests.get(callUrl)
        resumptionToken = None
        if http_response.status_code == status.HTTP_200_OK:
            xml = http_response.text
            elements = etree.XML(xml.encode("utf8"), parser=XMLParser).iterfind('.//' + '{http://www.openarchives.org/OAI/2.0/}' + 'record')
            for elt in elements:
                record = Record(elt)
                rtn.append({"identifier": record.header.identifier,
                          "datestamp": record.header.datestamp,
                          "deleted": record.deleted,
                          "sets": record.header.setSpecs,
                          "metadataPrefix": metadataPrefix,
                          "metadata": etree.tostring(record.xml.find('.//' + '{http://www.openarchives.org/OAI/2.0/}' + 'metadata/')),
                          "raw": record.raw})

            resumptionTokenElt = etree.XML(xml.encode("utf8"), parser=XMLParser).iterfind('.//' + '{http://www.openarchives.org/OAI/2.0/}' + 'resumptionToken')
            for res in resumptionTokenElt:
                resumptionToken = res.text

            # if resumptionToken != None and resumptionToken != '':
            #     #Only the URL and the resumptionToken
            #     callUrl = url + '?verb=ListRecords' + '&resumptionToken=%s' % resumptionToken
                # needed = False
            # else:
            #     needed = False

        elif http_response.status_code == status.HTTP_404_NOT_FOUND:
            content = {'error':'Server not found.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            content = {'error': 'An error occurred.'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(rtn, status=status.HTTP_200_OK), resumptionToken

    except Exception as e:
        content = {'error':'An error occurred when attempting to identify resource: %s'%e.message}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

################################################################################
#
# Function Name: add_my_metadataFormat(request)
# Inputs:        request -
# Outputs:       201 Registry updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No registry found with the given identity.
# Description:   OAI-PMH Add a new my_metadataFormat
#
################################################################################
@api_view(['POST'])
def add_my_metadataFormat(request):
    """
    POST http://localhost/oai_pmh/add/my-metadataformat
    POST data query="{'metadataPrefix':'value', 'schema':'schemaURL'}"
    """
    if request.user.is_authenticated():
        try:
        #Serialization of the input data
            serializer = MyMetadataFormatSerializer(data=request.DATA)
            #If it's valid
            if serializer.is_valid():
                #We retrieve all information
                if 'metadataPrefix' in request.POST:
                    metadataprefix = request.DATA['metadataPrefix']
                if 'schema' in request.POST:
                    schema = request.DATA['schema']

                #Try to get the schema
                http_response = requests.get(schema)
                if http_response.status_code == status.HTTP_200_OK:
                    #Check if the XML is well formed
                    try:
                        xml_schema = http_response.text
                        dom = etree.fromstring(xml_schema.encode('utf-8'))
                        if 'targetNamespace' in dom.find(".").attrib:
                            metadataNamespace = dom.find(".").attrib['targetNamespace'] or "namespace"
                        else:
                            metadataNamespace = "http://www.w3.org/2001/XMLSchema"

                    except XMLSyntaxError:
                        return Response({'message':'Unable to add the new metadata format.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message':'Unable to add the new metadata format. Impossible to retrieve the schema at the given URL'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    #Add in database
                   OaiMyMetadataFormat(metadataPrefix=metadataprefix, schema=schema, metadataNamespace=metadataNamespace, xmlSchema=xml_schema, isDefault=False).save()
                except Exception as e:
                    return Response({'message':'Unable to add the new metadata format. \n%s'%e.message}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            return Response({'message':'Unable to add the new metadata format. \n%s'%e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


################################################################################
#
# Function Name: add_my_template_metadataFormat(request)
# Inputs:        request -
# Outputs:       201 Registry updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No registry found with the given identity.
# Description:   OAI-PMH Add a new template_my_metadataFormat
#
################################################################################
@api_view(['POST'])
def add_my_template_metadataFormat(request):
    """
    POST http://localhost/oai_pmh/add/my-template-metadataformat
    POST data query="{'metadataPrefix':'value', 'template':'templateID'}"
    """
    if request.user.is_authenticated():
        try:
        #Serialization of the input data
            serializer = MyTemplateMetadataFormatSerializer(data=request.DATA)
            #If it's valid
            if serializer.is_valid():
                #We retrieve all information
                if 'metadataPrefix' in request.POST:
                    metadataprefix = request.DATA['metadataPrefix']
                if 'template' in request.POST:
                    template = request.DATA['template']

                #Try to get the template
                try:
                    template = Template.objects.get(pk=template)
                    #Check if the XML is well formed
                    try:
                        xml_schema = template.content
                        dom = etree.fromstring(xml_schema.encode('utf-8'))
                        if 'targetNamespace' in dom.find(".").attrib:
                            metadataNamespace = dom.find(".").attrib['targetNamespace'] or "namespace"
                        else:
                            metadataNamespace = "http://www.w3.org/2001/XMLSchema"
                    except XMLSyntaxError:
                        return Response({'message':'Unable to add the new metadata format. XML Synthax error.'}, status=status.HTTP_400_BAD_REQUEST)
                except Exception, e:
                    return Response({'message':'Unable to add the new metadata format. Impossible to retrieve the template with the given template'}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    #Add in database
                   OaiMyMetadataFormat(metadataPrefix=metadataprefix,
                                       schema='http://127.0.0.1:8000/oai_pmh/server/XSD/'+template.filename,
                                       metadataNamespace=metadataNamespace, xmlSchema='', isDefault=False,
                                       isTemplate=True, template=template).save()
                except Exception as e:
                    return Response({'message':'Unable to add the new metadata format. \n%s'%e.message}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception, e:
            return Response({'message':'Unable to add the new metadata format. \n%s'%e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: delete_my_metadataFormat(request)
# Inputs:        request -
# Outputs:       204 Record deleted.
# Exceptions:    400 Error connecting to database.
#                400 [Name] not found in request.
#                400 Unspecified.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No record found with the given identity.
# Description:   OAI-PMH Delete my_metadataFormat
#
################################################################################
@api_view(['POST'])
def delete_my_metadataFormat(request):
    """
    POST http://localhost/oai_pmh/delete/my-metadataFormat
    POST data query="{'MetadataFormatId':'value'}"
    """
    if request.user.is_authenticated():
        try:
            serializer = DeleteMyMetadataFormatSerializer(data=request.DATA)
            if serializer.is_valid():
                #Get the ID
                id = request.DATA['MetadataFormatId']
                try:
                    metadataFormat = OaiMyMetadataFormat.objects.get(pk=id)
                except Exception as e:
                    content = {'message':'No metadata format found with the given id.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                #We can now delete the metadataFormat for my server
                metadataFormat.delete()
                content = {'message':"Deleted metadata format with success."}
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":e.message}, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: update_my_metadataFormat(request)
# Inputs:        request -
# Outputs:       201 Registry updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No registry found with the given identity.
# Description:   OAI-PMH Update my_metadataFormat
#
################################################################################
@api_view(['PUT'])
def update_my_metadataFormat(request):
    """
    PUT http://localhost/oai_pmh/update/my-metadataFormat
    PUT data query="{'id':'value', 'metadataPrefix':'value'}"
    """
    if request.user.is_authenticated():
        #Serialization of the input data
        serializer = UpdateMyMetadataFormatSerializer(data=request.DATA)
        #If it's valid
        if serializer.is_valid():
            #We retrieve all information
            try:
                try:
                    if 'id' in request.DATA:
                        id = request.DATA['id']
                        metadataFormat = OaiMyMetadataFormat.objects.get(pk=id)
                    else:
                        rsp = {'id':'\'Id\' not found in request.'}
                        return Response(rsp, status=status.HTTP_400_BAD_REQUEST)
                except:
                    content = {'message':'No metadata format found with the given id.'}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

                if 'metadataPrefix' in request.DATA:
                    metadataprefix = request.DATA['metadataPrefix']
                    if metadataprefix:
                        metadataFormat.metadataPrefix = metadataprefix
            except:
                content = {'message':'Error while retrieving information.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            try:
                #Save the modifications
                 metadataFormat.save()
            except Exception as e:
                return Response({'message':'Unable to update the metadata format. \n%s'%e.message}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


################################################################################
#
# Function Name: add_my_set(request)
# Inputs:        request -
# Outputs:       201 Registry updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No registry found with the given identity.
# Description:   OAI-PMH Update my_metadataFormat
#
################################################################################
@api_view(['POST'])
def add_my_set(request):
    """
    PUT http://localhost/oai_pmh/add/my-set
    PUT data query="{'setSpec':'value', 'setName':'value'}"
    """
    if request.user.is_authenticated():
        #Serialization of the input data
        serializer = MySetSerializer(data=request.DATA)
        #If it's valid
        if serializer.is_valid():
            #We retrieve all information
            if 'setSpec' in request.POST:
                setSpec = request.DATA['setSpec']
            if 'setName' in request.POST:
                setName = request.DATA['setName']
            try:
                #Add in databases
               OaiMySet(setSpec=setSpec, setName=setName).save()
            except Exception as e:
                return Response({'message':'Unable to add the new set. \n%s'%e.message}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


################################################################################
#
# Function Name: delete_my_set(request)
# Inputs:        request -
# Outputs:       204 Record deleted.
# Exceptions:    400 Error connecting to database.
#                400 [Name] not found in request.
#                400 Unspecified.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No record found with the given identity.
# Description:   OAI-PMH Delete my_set
#
################################################################################
@api_view(['POST'])
def delete_my_set(request):
    """
    POST http://localhost/oai_pmh/delete/my-set
    POST data query="{'set_id':'value'}"
    """
    if request.user.is_authenticated():
        try:
            serializer = DeleteMySetSerializer(data=request.DATA)
            if serializer.is_valid():
                #Get the ID
                id = request.DATA['set_id']
                try:
                    set = OaiMySet.objects.get(pk=id)
                except Exception as e:
                    content = {'message':'No set found with the given id.'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
                #We can now delete the set for my server
                set.delete()
                content = {'message':"Deleted set with success."}
                return Response(content, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":e.message}, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)


################################################################################
#
# Function Name: update_my_set(request)
# Inputs:        request -
# Outputs:       201 Registry updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No registry found with the given identity.
# Description:   OAI-PMH Update my_metadataFormat
#
################################################################################
@api_view(['PUT'])
def update_my_set(request):
    """
    PUT http://localhost/oai_pmh/update/my-set
    PUT data query="{'id':'value', 'setSpec':'value','setName':'value'}"
    """
    if request.user.is_authenticated():
        #Serialization of the input data
        serializer = UpdateMySetSerializer(data=request.DATA)
        #If it's valid
        if serializer.is_valid():
            #We retrieve all information
            try:
                try:
                    if 'id' in request.DATA:
                        id = request.DATA['id']
                        set = OaiMySet.objects.get(pk=id)
                    else:
                        rsp = {'id':'\'Id\' not found in request.'}
                        return Response(rsp, status=status.HTTP_400_BAD_REQUEST)
                except:
                    content = {'message':'No set found with the given id.'}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)

                if 'setSpec' in request.DATA:
                    setSpec = request.DATA['setSpec']
                    if setSpec:
                        set.setSpec = setSpec

                if 'setName' in request.DATA:
                    setName = request.DATA['setName']
                    if setName:
                        set.setName = setName
            except:
                content = {'message':'Error while retrieving information.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
            try:
                #Save the modifications
                 set.save()
            except Exception as e:
                return Response({'message':'Unable to update the set. \n%s'%e.message}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: select_record(request)
# Inputs:        request -
# Outputs:       200 Found record.
# Exceptions:    400 Error connecting to database.
#                400 Error getting content.
#                400 No record found matching the identifier: [identifier]
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   Select OAI-PMH Record
#
################################################################################
@api_view(['POST'])
def select_record(request):
    """
    POST http://localhost/oai_pmh/select/record
    """
    if request.user.is_authenticated():
        try:
            serializer = RecordSerializer(data=request.DATA)
            if serializer.is_valid():
                try:
                    rec_collection = MongoClient(MONGODB_URI)[MGI_DB]['records']
                except Exception:
                    return Response({'message':'Error connecting to database.'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    identifier = request.DATA['identifier']
                except ValueError:
                    return Response({'message':'Error getting content.'}, status=status.HTTP_400_BAD_REQUEST)

                record = rec_collection.find_one({"identifier":identifier}, {"_id":False}) # Exclude ObjectID from result

                if record is 'null':
                    return Response({'message':'No record found matching the identifier: %s'%identifier}, status=status.HTTP_400_BAD_REQUEST)
                return Response(record, status=status.HTTP_200_OK)
            else:
                return Response({'message':'Serializer failed validation.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: select_all_records(request)
# Inputs:        request -
# Outputs:       200 Found records.
# Exceptions:    400 Error connecting to database.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   Select All OAI-PMH Records
#
################################################################################
@api_view(['GET'])
def select_all_records(request):
    """
    POST http://localhost/oai_pmh/select/all/records
    """
    if request.user.is_authenticated():
        try:
            try:
                rec_collection = MongoClient(MONGODB_URI)[MGI_DB]['records']
            except Exception:
                return Response({'message':'Error connecting to database.'}, status=status.HTTP_400_BAD_REQUEST)

            records = rec_collection.find({}, {"_id":False}) # Exclude ObjectID from result
            rsp = {}
            for r in records:
                rsp.update(r)
            return Response(rsp, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: update_record(request)
# Inputs:        request -
# Outputs:       201 Record updated.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 [Content] not found in request.
#                400 Unable to update record.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No record found with the given identity.
# Description:   Update OAI-PMH Record
#
################################################################################
@api_view(['PUT'])
def update_record(request):
    """
    PUT http://localhost/oai_pmh/update/record
    """
    if request.user.is_authenticated():
        serializer = UpdateRecordSerializer(data=request.DATA)
        if serializer.is_valid():
            try:
                rec_collection = MongoClient(MONGODB_URI)[MGI_DB]['records']
            except Exception:
                return Response({'message':'Error connecting to database.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                identifier = request.DATA['identifier']
            except:
                rsp = {'message':'\'Identifier\' not found in request.'}
                return Response(rsp, status=status.HTTP_400_BAD_REQUEST)

            try:
                content = request.DATA['content']
            except:
                rsp = {'message':'\'Content\' not found in request.'}
                return Response(rsp, status=status.HTTP_400_BAD_REQUEST)

            try:
                record = rec_collection.find_one({"identifier":identifier})
                if record is "null":
                    pass
            except:
                rsp = {'message':'No record found with the given identity.'}
                return Response(rsp, status=status.HTTP_404_NOT_FOUND)

            try:

                rec_collection.update({"identifier":identifier}, { "$set": {"content":content} })
            except:
                return Response({'message':'Unable to update record.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'Serializer failed validation.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message':'Only an administrator can use this feature.'}, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: delete_record(request)
# Inputs:        request -
# Outputs:       204 Record deleted.
# Exceptions:    400 Error connecting to database.
#                400 [Identifier] not found in request.
#                400 [Content] not found in request.
#                400 Unspecified.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No record found with the given identity.
# Description:   Delete OAI-PMH Registry
#
################################################################################
@api_view(['POST'])
def delete_record(request):
    """
    POST http://localhost/oai_pmh/delete/record
    """
    if request.user.is_authenticated():
        try:
            serializer = DeleteRecordSerializer(data=request.DATA)
        except Exception as e:
            return Response({"message":e.message}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            try:
                rec_collection = MongoClient(MONGODB_URI)[MGI_DB]['records']
            except:
                return Response({'message':'Unable to connect to database.'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                identifier = request.DATA['identifier']
            except:
                rsp = {'message':'\'Identifier\' not found in request.'}
                return Response(rsp, status=status.HTTP_400_BAD_REQUEST)
            try:
                record = rec_collection.find_one({"identifier":identifier})
                if record is not 'null':
                    rec_collection.remove({"identifier":identifier})
                    content = {'message':"Deleted record %s with success."%identifier}
                    return Response(content, status=status.HTTP_204_NO_CONTENT)
            except ValueError as e:
                Response({"message":e.message}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message':'Serializer failed validation.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)