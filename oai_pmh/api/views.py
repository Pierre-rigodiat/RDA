################################################################################
#
# File Name: rest_views.py
# Application: Informatics Core
# Description:
#
# Author: Marcus Newrock
#         marcus.newrock@nist.gov
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
# Serializers
from oai_pmh.api.serializers import RegistrySerializer, ListRecordsSerializer, RegistryURLSerializer, RecordSerializer, \
    IdentifySerializer, SaveRecordSerializer, UpdateRecordSerializer, DeleteRecordSerializer, UpdateRegistrySerializer, DeleteRegistrySerializer
# Models
from mgi.models import Registry
# DB Connection
from pymongo import MongoClient
from mgi.settings import MONGODB_URI, MGI_DB
from mongoengine import NotUniqueError

################################################################################
#
# Function Name: add_record(request)
# Inputs:        request -
# Outputs:       200 Record added
# Exceptions:    400 Error connecting to database.
#                400 Error getting content.
#                400 An error occurred when trying to save document. [Document content]
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH Add Record
#
################################################################################
@api_view(['POST'])
def add_record(request):
    """
    POST http://localhost/oai_pmh/add/record
    """
    if request.user.is_authenticated():
        try:
            serializer = SaveRecordSerializer(data=request.DATA)
            if serializer.is_valid():
                try:
                    rec_collection = MongoClient(MONGODB_URI)[MGI_DB]['records']
                except Exception:
                    return Response({'message':'Error connecting to database.'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    content = request.DATA['content']
                except ValueError:
                    return Response({'message':'Error getting content.'}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    rec_collection.insert(content)
                except Exception as e:
                    return Response({'message':'An error occured when trying to save document. %s'%e.message}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message':'Record Added. %s'%serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
# Description:   OAI-PMH Add Registry
#
################################################################################
@api_view(['POST'])
def add_registry(request):
    """
    POST http://localhost/oai_pmh/add/registry
    """
    if request.user.is_authenticated():
        serializer = RegistrySerializer(data=request.DATA)
        if serializer.is_valid():
            errors = []
            try:
                name = request.DATA['name']
            except ValueError:
                errors.append("Invalid Name")
            try:
                url = request.DATA['url']
            except ValueError:
                errors.append("Invalid URL")
            if 'harvestrate' in request.DATA:
                harvestrate = request.DATA['harvestrate']
            else:
                harvestrate = ""
            if 'harvest' in request.DATA:
                harvest = request.DATA['harvest'] == 'True'
            else:
                harvest = False
            if 'metadataprefix' in request.DATA:
                metadataprefix = request.DATA['metadataprefix']
            else:
                metadataprefix = ""
            if 'identity' in request.DATA:
                identity = request.DATA['identity']
            else:
                identity = {}
            if 'sets' in request.DATA:
                sets = request.DATA['sets']
            else:
                sets = {}
            if 'description' in request.DATA:
                description = request.DATA['description']
            else:
                description = ""

            if len(errors) > 0:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                registry = Registry()
                registry.name = name
                registry.url = url
                registry.harvestrate = harvestrate
                registry.metadataprefix = metadataprefix
                registry.identity = identity
                registry.sets = sets
                registry.description = description
                registry.harvest = harvest
                registry.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except NotUniqueError as e:
                return Response({'message':'Unable to create the registry. The registry already exists.%s'%e.message}, status=status.HTTP_409_CONFLICT)
            except Exception as e:
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
    """
    if request.user.is_authenticated:
        errors = []
        try:
            name = request.QUERY_PARAMS.get('name', None)
        except ValueError:
            errors.append("Invalid Name")
        if len(errors) > 0:
            Response(errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            registry = Registry.objects.get(name=name)
        except Exception as e:
            registry = {}

        srl = {}

        for a in registry:
            if str(a) != 'id':

                srl.update({a:registry[a]})
            else:
                print "ID is %s"%registry[a]

        return Response(srl, status=status.HTTP_200_OK)
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
#                409 Duplicate name.
# Description:   OAI-PMH Update Registry
#
################################################################################
@api_view(['PUT'])
def update_registry(request):
    """
    PUT http://localhost/oai_pmh/update/registry
    """
    if request.user.is_authenticated():
        serializer = UpdateRegistrySerializer(data=request.DATA)

        if serializer.is_valid():
            try:
                if 'id' in request.DATA:
                    id = request.DATA['id']
                    registry = Registry.objects.get(pk=id)
                else:
                    rsp = {'message':'\'Id\' not found in request.'}
                    return Response(rsp, status=status.HTTP_400_BAD_REQUEST)
            except:
                content = {'message':'No registry found with the given id.'}
                return Response(content, status=status.HTTP_404_NOT_FOUND)

            if 'name' in request.DATA:
                name = request.DATA['name']
                if name:
                    registry.name = name
            if 'url' in request.DATA:
                url = request.DATA['url']
                if url:
                    registry.url = url
            if 'harvestrate' in request.DATA:
                harvestrate = request.DATA['harvestrate']
                if harvestrate:
                    registry.harvestrate = harvestrate
            if 'metadataprefix' in request.DATA:
                metadataprefix = request.DATA['metadataprefix']
                if metadataprefix:
                    registry.metadataprefix = metadataprefix
            if 'description' in request.DATA:
                description = request.DATA['description']
                if description:
                    registry.description = description
            if 'identity' in request.DATA:
                identity = request.DATA['identity']
                if identity:
                    registry.identity = identity
            if 'sets' in request.DATA:
                sets = request.DATA['sets']
                if sets:
                    registry.sets = sets
            if 'harvest' in request.DATA:
                harvest = request.DATA['harvest']
                if harvest:
                    registry.harvest =  harvest == 'True'

            try:
               registry.save()
            except NotUniqueError as e:
                return Response({'message':'Unable to update registry. The registry already exists.'}, status=status.HTTP_409_CONFLICT)
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
# Function Name: delete_registry(request)
# Inputs:        request -
# Outputs:       204 Record deleted.
# Exceptions:    400 Error connecting to database.
#                400 [Name] not found in request.
#                400 Unspecified.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                404 No record found with the given identity.
# Description:   OAI-PMH Delete Registry
#
################################################################################
@api_view(['POST'])
def delete_registry(request):
    """
    POST http://localhost/oai_pmh/delete/registry
    """
    if request.user.is_authenticated():
        try:
            serializer = DeleteRegistrySerializer(data=request.DATA)
        except Exception as e:
            return Response({"message":e.message}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            try:
                id = request.DATA['RegistryId']
            except:
                rsp = {'message':'\'ResgistryId\' not found in request.'}
                return Response(rsp, status=status.HTTP_400_BAD_REQUEST)

            try:
                registry = Registry.objects.get(pk=id)
                registry.delete()
                content = {'message':"Deleted registry with success."}
                return Response(content, status=status.HTTP_200_OK)
            except Exception as e:
                Response({"message":e.message}, status=status.HTTP_400_BAD_REQUEST)

            content = {'message':'Bad request.'}
        else:
            return Response({'message':'Serializer failed validation.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
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
    """
    if request.user.is_authenticated():
        try:
            serializer = IdentifySerializer(data=request.DATA)
            if serializer.is_valid():
                errors = []
                try:
                    url = request.DATA['url']
                except ValueError:
                    errors.append("Error in URL value.")
                try:
                    identifier = request.DATA['identifier']
                except ValueError:
                    errors.append("Error in Identifier value.")
                try:
                    metadataprefix = request.DATA['metadataprefix']
                except ValueError:
                    errors.append("Error in Metadata Prefix value.")
                if len(errors) > 0:
                    return Response({"message":errors}, status=status.HTTP_400_BAD_REQUEST)
                sickle = Sickle(url)
                grResponse = sickle.GetRecord(metadataPrefix=metadataprefix, identifier=identifier)
                rsp = dict(grResponse)
                return Response({'message':rsp}, status=status.HTTP_200_OK)
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

################################################################################
#
# Function Name: identify(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    400 Error getting URL.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH Identify
#
################################################################################
@api_view(['POST'])
def identify(request):
    """
    POST http://localhost/oai_pmh/identify
    """
    if request.user.is_authenticated():
        try:
            serializer = IdentifySerializer(data=request.DATA)
            if serializer.is_valid():
                try:
                    url = request.DATA['url']
                except ValueError:
                   return Response({'message':'Error getting URL.'}, status=status.HTTP_400_BAD_REQUEST)

                sickle = Sickle(url)
                idResponse = sickle.Identify()
                rsp = dict(idResponse)

                return Response({'message':rsp}, status=status.HTTP_200_OK)
        except Exception:
            content = {'message':'An error occurred when attempting to identify resource.'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

################################################################################
#
# Function Name: listMetadataFormats(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    400 Error in URL value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List Metadata Formats
#
################################################################################
@api_view(['POST'])
def listMetadataFormats(request):
    """
    POST http://localhost/oai_pmh/listmetadataformats
    """
    if request.user.is_authenticated():
        try:
            serializer = IdentifySerializer(data=request.DATA)

            if serializer.is_valid():
                errors = []
                try:
                    url = request.DATA['url']
                except ValueError:
                    errors.append("Error in URL value.")

                if len(errors) > 0:
                    return Response({"message":errors}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'message':'Serializer failed validation.'}, status=status.HTTP_400_BAD_REQUEST)
            sickle = Sickle(url)
            rsp = sickle.ListMetadataFormats()
            return Response(rsp, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
def listRecords(request):
    """
    POST http://localhost/oai_pmh/listrecords
    """

    if request.user.is_authenticated():
        try:
            serializer = ListRecordsSerializer(data=request.DATA)

            if serializer.is_valid():
                errors = []
                try:
                    url = request.DATA['url']
                except ValueError:
                    errors.append("Error in URL value.")
                try:
                    metadataprefix = request.DATA['metadataprefix']
                except ValueError:
                    errors.append("Error in Metadata Prefix value.")

                if 'resumptionToken' in request.DATA:
                    resumptionToken = request.DATA['resumptionToken']
                else:
                    resumptionToken = ""
                if 'set' in request.DATA:
                    set_h = request.DATA['set']
                else:
                    set_h = ""
                if 'fromDate' in request.DATA:
                    fromDate = request.DATA['fromDate']
                else:
                    fromDate = ""
                if 'until' in request.DATA:
                    untilDate = request.DATA['until']
                else:
                    untilDate = ""

                if len(errors) > 0:
                    return Response({"message":errors}, status=status.HTTP_400_BAD_REQUEST)

                sickle = Sickle(url)
                rsp = sickle.ListRecords(**{
                    'metadataPrefix':metadataprefix,
                    'set':set_h,
                    'resumptionToken':resumptionToken,
                    'from':fromDate, # from is reserved in python: Sickle instructions say to use a pointer: http://sickle.readthedocs.org/en/latest/tutorial.html
                    'until':untilDate
                })
                rtn = []
                try:
                    while True:
                        rtn.append( dict(rsp.next()) )
                except StopIteration:
                    pass

                return Response(rtn, status=status.HTTP_200_OK)
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
# Function Name: listSets(request)
# Inputs:        request -
# Outputs:       200 Response successful.
# Exceptions:    400 Error(s) in required values value.
#                400 Serializer failed validation.
#                401 Unauthorized.
#                500 An error occurred when attempting to identify resource.
# Description:   OAI-PMH List Sets
#
################################################################################
@api_view(['POST'])
def listSets(request):
    """
    POST http://localhost/oai_pmh/listsets
    """
    if request.user.is_authenticated():
        try:
            serializer = IdentifySerializer(data=request.DATA)
            if serializer.is_valid():
                errors = []
                try:
                    url = request.DATA['url']
                except ValueError:
                    errors.append("Error in URL value.")
                if len(errors) > 0:
                    return Response({"message":errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'serializer failed validation.'}, status=status.HTTP_400_BAD_REQUEST)
            sickle = Sickle(url)
            rsp = sickle.ListSets()
            rtn = []
            try:
                while True:
                    rtn.append( dict(rsp.next()) )
            except StopIteration:
                pass
            return Response(rtn, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

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
    """
    if request.user.is_authenticated():
        try:
            serializer = RegistryURLSerializer(data=request.DATA)
            if serializer.is_valid():
                errors = []
                try:
                    url = request.DATA['url']
                except ValueError:
                    errors.append("Error in URL value.")
                try:
                    metadataprefix = request.DATA['metadataprefix']
                except ValueError:
                    errors.append("Error in Metadata Prefix value.")
                if 'set' in request.DATA:
                    setH = request.DATA['set']
                else:
                    setH = ""

                if len(errors) > 0:
                    return Response({"message":errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'Serializer failed validation.'}, status=status.HTTP_400_BAD_REQUEST)
            sickle = Sickle(url)
            rsp = sickle.ListIdentifiers(metadataPrefix=metadataprefix, set=setH)
            rtn = []
            try:
                while True:
                    rtn.append( dict(rsp.next()) )
            except StopIteration:
                pass

            return Response({'message':rtn}, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'message':'An error occurred when attempting to identify resource: %s'%e.message}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        content = {'message':'Only an administrator can use this feature.'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)