################################################################################
#
# File Name: tests.py
# Application: oai_pmh/api
# Purpose:
#
# Author: Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from oai_pmh.tests.models import OAI_PMH_Test
from oai_pmh.api.views import createRegistry, createOaiIdentify, setDataToRegistry, createMetadataformatsForRegistry,\
    sickleListObjectMetadataFormats, sickleListObjectSets, setMetadataFormatXMLSchema, createSetsForRegistry, \
    sickleObjectIdentify
from mgi.models import OaiRegistry, OaiIdentify, OaiMetadataFormat, OaiMyMetadataFormat, OaiSettings, Template, OaiSet,\
    OaiMySet, OaiRecord
import xmltodict
import lxml.etree as etree
from testing.models import URL_TEST, ADMIN_AUTH, ADMIN_AUTH_GET, USER_AUTH
from django.core.urlresolvers import reverse
from rest_framework import status
import mongoengine.errors as MONGO_ERRORS
from testing.models import FAKE_ID
URL_TEST_SERVER = URL_TEST + "/oai_pmh/server/"
import requests
from django.conf import settings

class tests_OAI_PMH_API(OAI_PMH_Test):

    def test_dumps(self):
        self.dump_result_xslt()
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        self.dump_xmldata()
        self.dump_oai_my_set()


############################### add_registry tests #############################
    def test_add_registry(self):
        self.dump_oai_settings()
        self.dump_oai_my_set()
        self.dump_oai_my_metadata_format()
        self.setHarvest(True)
        data = {"url": URL_TEST_SERVER, "harvestrate": 5000, "harvest": True}
        req = self.doRequestPost(url=reverse("api_add_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_201_CREATED)


    def test_add_registry_unavailable(self):
        self.dump_oai_settings()
        self.setHarvest(False)
        data = {"url": URL_TEST_SERVER, "harvestrate": 5000, "harvest": True}
        req = self.doRequestPost(url=reverse("api_add_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


    def test_add_registry_unauthorized(self):
        self.dump_oai_settings()
        data = {"url": URL_TEST_SERVER, "harvestrate": 5000, "harvest": True}
        #No authentification
        req = self.doRequestPost(url=reverse("api_add_registry"), data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_registry_serializer_invalid(self):
        self.dump_oai_settings()
        data = {"urlBad": URL_TEST_SERVER, "harvestrate": 5000, "harvest": True}
        req = self.doRequestPost(url=reverse("api_add_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_registry_already_exists(self):
        self.dump_oai_settings()
        self.dump_oai_my_set()
        self.dump_oai_my_metadata_format()
        self.setHarvest(True)
        data = {"url": URL_TEST_SERVER, "harvestrate": 5000, "harvest": True}
        req = self.doRequestPost(url=reverse("api_add_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_201_CREATED)
        data = {"url": URL_TEST_SERVER, "harvestrate": 5000, "harvest": True}
        req = self.doRequestPost(url=reverse("api_add_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_409_CONFLICT)

    def test_add_registry_bad_identify(self):
        self.dump_oai_settings()
        data = {"url": URL_TEST_SERVER, "harvestrate": 5000, "harvest": True}
        #No harvest TRUE Identify will fail
        req = self.doRequestPost(url=reverse("api_add_registry"), data=data, auth=ADMIN_AUTH)
        self.assertNotEquals(req.status_code, status.HTTP_200_OK)

    def test_add_registry_bad_metadata_format(self):
        self.dump_oai_settings()
        self.setHarvest(True)
        self.dump_oai_my_metadata_format()
        #Change an xml schema to make fail the treatment
        metadataFormat = OaiMyMetadataFormat.objects.all()[0]
        metadataFormat.schema = "http://noserver.com"
        metadataFormat.save()
        data = {"url": URL_TEST_SERVER, "harvestrate": 5000, "harvest": True}
        #No harvest TRUE Identify will fail
        req = self.doRequestPost(url=reverse("api_add_registry"), data=data, auth=ADMIN_AUTH)
        self.assertNotEquals(req.status_code, status.HTTP_200_OK)

################################################################################

########################## createRegistry tests ################################

    def test_createRegistry_function(self):
        #Call the function to create the registry
        identify, registry = self.call_createRegistry()
        self.assert_OaiIdentify(identify)
        #Check with the OaiRegistry returned by the function
        self.assert_OaiRegistry(registry=registry, objIdentify=identify)
        #Check with the OaiRegistry saved in database
        objInDatabase = OaiRegistry.objects.get(pk=registry.id)
        self.assert_OaiRegistry(registry=objInDatabase, objIdentify=identify)

    def test_createRegistry_function_bad_raw(self):
        #Call the function to create the registry
        strUrl, harvest, harvestrate = self.getRegistryData()
        identifyData = self.getIdentifyData()
        identifyData['raw'] = "<test>badXMLtest/>"
        identify, registry = createRegistry(harvest=harvest, harvestrate=harvestrate, identifyData=identifyData,
                                            url=strUrl)
        self.assertEqual(identify['raw'], {})


    def test_setDataToRegistry_function(self):
        #Get registry data
        strUrl, harvest, harvestrate = self.getRegistryData()
        registry = OaiRegistry()
        #Create the identity
        objIdentify = self.call_createOaiIdentify()
        #Test the method
        setDataToRegistry(harvest=harvest, harvestrate=harvestrate, identify=objIdentify, registry=registry,
                          url=strUrl)
        self.assert_OaiRegistry(registry=registry, objIdentify=objIdentify)

    def test_createOaiIdentify_function(self):
        #Call the function to create the identify
        objIdentify = self.call_createOaiIdentify()
        #Check with the OaiIdentify saved in database
        objInDatabase = OaiIdentify.objects.get(pk=objIdentify.id)
        self.assert_OaiIdentify(objInDatabase)

################################################################################


############################## objectIdentify tests ############################

    def test_objectIdentify(self):
        self.dump_oai_settings()
        self.setHarvest(True)
        data = {"url": URL_TEST_SERVER}
        req = self.doRequestPost(url=reverse("api_objectIdentify"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        retrievedSetsData = req.data
        self.assert_OaiIdentify_Settings(retrievedSetsData)

    def test_objectIdentify_unavailable(self):
        self.dump_oai_settings()
        self.setHarvest(False)
        data = {"url": URL_TEST_SERVER}
        req = self.doRequestPost(url=reverse("api_objectIdentify"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_objectIdentify_unauthorized(self):
        self.dump_oai_settings()
        data = {"url": URL_TEST_SERVER}
        #No authentification
        req = self.doRequestPost(url=reverse("api_objectIdentify"), data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_objectIdentify_serializer_invalid(self):
        self.dump_oai_settings()
        #Bad URL name
        data = {"urlBad": URL_TEST_SERVER}
        req = self.doRequestPost(url=reverse("api_objectIdentify"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sickleObjectIdentify(self):
        self.dump_oai_settings()
        self.setHarvest(True)
        url = URL_TEST_SERVER
        req = sickleObjectIdentify(url)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        retrievedIdentify = req.data
        self.assert_OaiIdentify_Settings(retrievedIdentify)

    def test_sickleObjectIdentify_unavailable(self):
        self.dump_oai_settings()
        self.setHarvest(False)
        url = URL_TEST_SERVER
        req = sickleObjectIdentify(url)
        self.assertEquals(req.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

################################################################################

############################## listObjectSets tests ############################

    def test_listObjectSets(self):
        self.dump_oai_settings()
        self.dump_oai_my_set()
        self.setHarvest(True)
        data = {"url": URL_TEST_SERVER}
        req = self.doRequestPost(url=reverse("api_listObjectSets"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        retrievedSetsData = req.data
        self.assert_OaiSet(retrievedSetsData)

    def test_listObjectSets_unavailable(self):
        self.dump_oai_settings()
        self.setHarvest(False)
        data = {"url": URL_TEST_SERVER}
        req = self.doRequestPost(url=reverse("api_listObjectSets"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_listObjectSets_unauthorized(self):
        self.dump_oai_settings()
        self.dump_oai_my_set()
        data = {"url": URL_TEST_SERVER}
        #No authentification
        req = self.doRequestPost(url=reverse("api_listObjectSets"), data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listObjectSets_serializer_invalid(self):
        self.dump_oai_settings()
        self.dump_oai_my_set()
        #Bad URL name
        data = {"urlBad": URL_TEST_SERVER}
        req = self.doRequestPost(url=reverse("api_listObjectSets"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sickleListObjectSets(self):
        self.dump_oai_settings()
        self.dump_oai_my_set()
        self.setHarvest(True)
        url = URL_TEST_SERVER
        req = sickleListObjectSets(url)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        retrievedSetsData = req.data
        self.assert_OaiSet(retrievedSetsData)

    def test_sickleListObjectSets_unavailable(self):
        self.dump_oai_settings()
        self.setHarvest(False)
        url = URL_TEST_SERVER
        req = sickleListObjectSets(url)
        self.assertEquals(req.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_sickleListObjectSets_no_content(self):
        self.dump_oai_settings()
        #DO NOT LOAD SETS
        self.setHarvest(True)
        url = URL_TEST_SERVER
        req = sickleListObjectSets(url)
        self.assertEquals(req.status_code, status.HTTP_204_NO_CONTENT)

################################################################################


######################## listObjectMetadataFormats tests #######################

    def test_listObjectMetadataFormats(self):
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        self.setHarvest(True)
        data = {"url": URL_TEST_SERVER}
        req = self.doRequestPost(url=reverse("api_listObjectMetadataFormats"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        retrievedMetadataformatsData = req.data
        self.assert_OaiMetadataFormat(retrievedMetadataformatsData)

    def test_listObjectMetadataFormats_unavailable(self):
        self.dump_oai_settings()
        self.setHarvest(False)
        data = {"url": URL_TEST_SERVER}
        req = self.doRequestPost(url=reverse("api_listObjectMetadataFormats"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_listObjectMetadataFormats_unauthorized(self):
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        data = {"url": URL_TEST_SERVER}
        #No authentification
        req = self.doRequestPost(url=reverse("api_listObjectMetadataFormats"), data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listObjectMetadataFormats_serializer_invalid(self):
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        #Bad URL name
        data = {"urlBad": URL_TEST_SERVER}
        req = self.doRequestPost(url=reverse("api_listObjectMetadataFormats"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sickleListObjectMetadataFormats(self):
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        self.setHarvest(True)
        url = URL_TEST_SERVER
        req = sickleListObjectMetadataFormats(url)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        retrievedMetadataformatsData = req.data
        self.assert_OaiMetadataFormat(retrievedMetadataformatsData)


    def test_sickleListObjectMetadataFormats_no_content(self):
        self.dump_oai_settings()
        #DO NOT LOAD METADATA FORMATS
        self.setHarvest(True)
        url = URL_TEST_SERVER
        req = sickleListObjectMetadataFormats(url)
        self.assertEquals(req.status_code, status.HTTP_204_NO_CONTENT)

    def test_sickleListObjectMetadataFormats_unavailable(self):
        self.dump_oai_settings()
        self.setHarvest(False)
        url = URL_TEST_SERVER
        req = sickleListObjectMetadataFormats(url)
        self.assertEquals(req.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_sickleListObjectMetadataFormats_no_identify(self):
        self.dump_oai_settings()
        #SERVER not available, harvest False
        self.setHarvest(False)
        url = URL_TEST_SERVER
        req = sickleListObjectMetadataFormats(url)
        self.assertEquals(req.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

################################################################################


########################## createSetsForRegistry tests #########################
    def test_createSetsForRegistry_function(self):
        registry = self.createFakeRegistry()
        setData = self.getSetData()
        createSetsForRegistry(registry, setData)
        for set in setData:
            objInDatabase = OaiSet.objects.get(setSpec=set['setSpec'],
                                                          registry=str(registry.id))
            self.assertEquals(set['setSpec'], objInDatabase.setSpec)
            self.assertEquals(set['setName'], objInDatabase.setName)
            self.assertEquals(str(registry.id), objInDatabase.registry)
            self.assertEquals(True, objInDatabase.harvest)
            # self.assertEquals(set['raw'], objInDatabase.raw)

    def test_createSetsForRegistry_function_bad_raw(self):
        registry = self.createFakeRegistry()
        setData = self.getSetDataBadRaw()
        createSetsForRegistry(registry, setData)
        with self.assertRaises(MONGO_ERRORS.DoesNotExist):
            OaiSet.objects.get(setSpec=setData[0]['setSpec'],
                                                          registry=str(registry.id))

################################################################################

################### createMetadataformatsForRegistry tests #####################

    def test_createMetadataformatsForRegistry_function(self):
        self.dump_template()
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        self.setHarvest(True)
        identify, registry = self.call_createRegistry()
        metadataformatsData = self.getMetadataFormatData()
        createMetadataformatsForRegistry(metadataformatsData, registry)

        for metadataformat in metadataformatsData:
            objInDatabase = OaiMetadataFormat.objects.get(metadataPrefix=metadataformat['metadataPrefix'],
                                                          registry=str(registry.id))
            self.assertEquals(metadataformat['metadataPrefix'], objInDatabase.metadataPrefix)
            self.assertEquals(metadataformat['metadataNamespace'], objInDatabase.metadataNamespace)
            self.assertEquals(metadataformat['schema'], objInDatabase.schema)
            self.assertEquals(str(registry.id), objInDatabase.registry)
            self.assertEquals(True, objInDatabase.harvest)
            # self.assertEquals(metadataformat['raw'], objInDatabase.raw)

    def test_createMetadataformatsForRegistry_function_bad_raw(self):
        self.dump_oai_settings()
        self.setHarvest(True)
        identify, registry = self.call_createRegistry()
        metadataformatsData = self.getMetadataFormatDataBadRaw()
        createMetadataformatsForRegistry(metadataformatsData, registry)
        with self.assertRaises(MONGO_ERRORS.DoesNotExist):
            OaiMetadataFormat.objects.get(metadataPrefix=metadataformatsData[0]['metadataPrefix'],
                                                          registry=str(registry.id))

    ###
    ### Add other data provider metadata format already existing in the server's metadata format
    ###
    def test_setMetadataFormatXMLSchema_existent_metadata(self):
        self.dump_template()
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        self.setHarvest(True)
        self.process_setMetadataFormatXMLSchema()

    def test_setMetadataFormatXMLSchema_metadataPrefix_exists_but_not_same_schema(self):
        self.dump_template()
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        self.setHarvest(True)
        #Get the template
        template = Template.objects.get(filename='AllResources.xsd')
        #Get AllResources.xsd metadata format
        metadataformat = self.getMetadataFormatDataAllResources()
        raw = xmltodict.parse(metadataformat['raw'])
        #Create an object
        obj = OaiMetadataFormat(metadataPrefix=metadataformat['metadataPrefix'],
                                metadataNamespace=metadataformat['metadataNamespace'],
                                schema=metadataformat['schema'], raw=raw, registry=FAKE_ID, harvest=True)
        #Get the schema
        xmlSchema = '<test>Not the same hash</test>'
        setMetadataFormatXMLSchema(obj, metadataformat['metadataPrefix'], xmlSchema)
        self.assertNotEquals(template.content, obj.xmlSchema)
        self.assertNotEquals(template.hash, obj.hash)
        self.assertEquals(None, obj.template)


    def test_setMetadataFormatXMLSchema_inexistent_metadata(self):
        self.dump_template()
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        self.setHarvest(True)
        #Delete the metadata format from the server's configuration
        OaiMyMetadataFormat.objects.get(metadataPrefix='oai_all').delete()
        self.process_setMetadataFormatXMLSchema()

    def process_setMetadataFormatXMLSchema(self):
        #Get the template
        template = Template.objects.get(filename='AllResources.xsd')
        #Get AllResources.xsd metadata format
        metadataformat = self.getMetadataFormatDataAllResources()
        raw = xmltodict.parse(metadataformat['raw'])
        #Create an object
        obj = OaiMetadataFormat(metadataPrefix=metadataformat['metadataPrefix'],
                                metadataNamespace=metadataformat['metadataNamespace'],
                                schema=metadataformat['schema'], raw=raw, registry=FAKE_ID, harvest=True)
        #Get the schema
        http_response = requests.get(obj.schema)
        if http_response.status_code == status.HTTP_200_OK:
            setMetadataFormatXMLSchema(obj, metadataformat['metadataPrefix'], http_response.text)
            self.assertEquals(template.content, obj.xmlSchema)
            self.assertEquals(template.hash, obj.hash)
            self.assertEquals(template, obj.template)

################################################################################


############################## Select registry tests ###########################

    def test_select_all_registries_zero(self):
        self.assertEquals(len(OaiRegistry.objects()), 0)
        req = self.doRequestGet(url="/oai_pmh/api/select/all/registries", auth=ADMIN_AUTH_GET)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        registriesData = req.content
        self.assertEquals(registriesData, '[]')


    def test_select_all_registries_one(self):
        self.createFakeRegistry()
        self.assertEquals(len(OaiRegistry.objects()), 1)
        req = self.doRequestGet(url="/oai_pmh/api/select/all/registries", auth=ADMIN_AUTH_GET)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        registriesData = req.content
        self.assertNotEquals(registriesData, '[]')

    def test_select_all_registries_unauthorized(self):
        req = self.doRequestGet(url="/oai_pmh/api/select/all/registries", auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    #
    # #TODO Find smthg to stop the database
    # def test_select_all_registries_error_database(self):
    #     self.assertEquals(len(OaiRegistry.objects()), 0)
    #     req = self.doRequestGet(url="/oai_pmh/api/select/all/registries", auth=ADMIN_AUTH_GET)
    #     self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)


    def test_select_all_registries_one(self):
        self.createFakeRegistry()
        self.assertEquals(len(OaiRegistry.objects()), 1)
        params = {"name": "Fake registry"}
        req = self.doRequestGet(url="/oai_pmh/api/select/registry", params=params, auth=ADMIN_AUTH_GET)
        self.assertEquals(req.status_code, status.HTTP_200_OK)

    def test_select_registry_zero(self):
        self.assertEquals(len(OaiRegistry.objects()), 0)
        params = {"name": "Fake registry"}
        req = self.doRequestGet(url="/oai_pmh/api/select/registry", params=params, auth=ADMIN_AUTH_GET)
        self.assertEquals(req.status_code, status.HTTP_404_NOT_FOUND)

    def test_select_all_registries_unauthorized(self):
        params = {"name": "Fake registry"}
        req = self.doRequestGet(url="/oai_pmh/api/select/registry", params=params, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_select_all_registries_serializer_invalid(self):
        params = {"nameBad": "Fake registry"}
        req = self.doRequestGet(url="/oai_pmh/api/select/registry", params=params, auth=ADMIN_AUTH_GET)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

################################################################################


############################## Update registry tests ###########################
    def test_update_registry(self):
        registry = self.createFakeRegistry()
        self.assertEquals(registry.harvestrate, None)
        self.assertEquals(registry.harvest, None)
        data = {"id": str(registry.id), "harvestrate": 1000, "harvest": "True"}
        req = self.doRequestPut(url="/oai_pmh/api/update/registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        objInDatabase = OaiRegistry.objects.get(pk=registry.id)
        self.assertEquals(objInDatabase.harvestrate, 1000)
        self.assertEquals(objInDatabase.harvest, True)

    def test_select_registry_bad_id(self):
        registry = self.createFakeRegistry()
        self.assertNotEquals(registry.id, FAKE_ID)
        data = {"id": FAKE_ID, 'harvestrate': 1000, 'harvest': 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_404_NOT_FOUND)

    def test_select_all_registries_unauthorized(self):
        data = {"id": FAKE_ID, 'harvestrate': 1000, 'harvest': 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/registry", data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_select_all_registries_unauthorized_user(self):
        data = {"id": FAKE_ID, 'harvestrate': 1000, 'harvest': 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/registry", data=data, auth=USER_AUTH)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_select_all_registries_serializer_invalid(self):
        data = {"idd": FAKE_ID, 'harvestrate': 1000, 'harvest': 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"id": FAKE_ID, 'harvestrate': 1000}#, 'harvest': 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"id": FAKE_ID, 'harvest': 'True'}#, 'harvestrate': 1000}
        req = self.doRequestPut(url="/oai_pmh/api/update/registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_select_all_registries_bad_entries(self):
        data = {"id": "badIdEntry", 'harvestrate': 'abcdde', 'harvest': 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"id": FAKE_ID, 'harvestrate': 'badHarvestrateEntry', 'harvest': 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

################################################################################

############################# Update my registry tests #########################
    def test_update_my_registry(self):
        self.dump_oai_settings()
        self.setHarvest(False)
        information = OaiSettings.objects.get()
        modifiedRepositoryName = "modifiedRepositoryName"
        self.assertNotEquals(information.repositoryName, modifiedRepositoryName)
        self.assertEquals(information.enableHarvesting, False)
        data = {"repositoryName": modifiedRepositoryName, "enableHarvesting": 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/my-registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        objInDatabase = OaiSettings.objects.get()
        self.assertEquals(objInDatabase.repositoryName, modifiedRepositoryName)
        self.assertEquals(objInDatabase.enableHarvesting, True)


    def test_update_my_registry_unauthorized(self):
        self.dump_oai_settings()
        modifiedRepositoryName = "modifiedRepositoryName"
        data = {"repositoryName": modifiedRepositoryName, "enableHarvesting": 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/my-registry", data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_my_registry_unauthorized_user(self):
        self.dump_oai_settings()
        modifiedRepositoryName = "modifiedRepositoryName"
        data = {"repositoryName": modifiedRepositoryName, "enableHarvesting": 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/my-registry", data=data, auth=USER_AUTH)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_my_registry_serializer_invalid(self):
        self.dump_oai_settings()
        modifiedRepositoryName = "modifiedRepositoryName"
        data = {"repositoryNName": modifiedRepositoryName, "enableHarvesting": 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/my-registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"repositoryName": modifiedRepositoryName, "enableHHarvesting": 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/my-registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"repositoryName": modifiedRepositoryName}
        req = self.doRequestPut(url="/oai_pmh/api/update/my-registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"enableHarvesting": 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/my-registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_my_registry_bad_entries(self):
        self.dump_oai_settings()
        data = {"repositoryName": 1000, "enableHarvesting": 'True'}
        req = self.doRequestPut(url="/oai_pmh/api/update/my-registry", data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

################################################################################

############################## Delete registry tests ###########################

    def test_delete_registry(self):
        self.dump_oai_settings()
        self.dump_oai_registry()
        registry = OaiRegistry.objects.get()
        data = {"RegistryId": str(registry.id)}
        req = self.doRequestPost(url=reverse("api_delete_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        self.assertEquals(len(OaiRegistry.objects()), 0)
        self.assertEquals(len(OaiIdentify.objects()), 0)
        self.assertEquals(len(OaiMetadataFormat.objects()), 0)
        self.assertEquals(len(OaiSet.objects()), 0)
        self.assertEquals(len(OaiRecord.objects()), 0)

    def test_delete_registry_unauthorized(self):
        data = {"RegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_delete_registry"), data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_registry_unauthorized_user(self):
        data = {"RegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_delete_registry"), data=data, auth=USER_AUTH)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_registry_not_found(self):
        data = {"RegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_delete_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_registry_serializer_invalid(self):
        data = {"RRegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_delete_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_registry_bad_entries(self):
        data = {"RegistryId": 1000}
        req = self.doRequestPost(url=reverse("api_delete_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)


################################################################################

###################### Deactivate / Activate registry tests ####################

    def test_deactivate_registry(self):
        self.dump_oai_settings()
        self.dump_oai_registry()
        registry = OaiRegistry.objects.get()
        self.assertEquals(registry.isDeactivated, False)
        data = {"RegistryId": str(registry.id)}
        req = self.doRequestPost(url=reverse("api_deactivate_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        objInDatabase = OaiRegistry.objects.get(pk=registry.id)
        self.assertEquals(objInDatabase.isDeactivated, True)

    def test_deactivate_registry_unauthorized(self):
        data = {"RegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_deactivate_registry"), data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deactivate_registry_unauthorized_user(self):
        data = {"RegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_deactivate_registry"), data=data, auth=USER_AUTH)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deactivate_registry_not_found(self):
        data = {"RegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_deactivate_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_404_NOT_FOUND)

    def test_deactivate_registry_serializer_invalid(self):
        data = {"RRegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_deactivate_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deactivate_registry_bad_entries(self):
        data = {"RegistryId": 1000}
        req = self.doRequestPost(url=reverse("api_deactivate_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reactivate_registry(self):
        self.dump_oai_settings()
        self.dump_oai_registry()
        registry = OaiRegistry.objects.get()
        registry.isDeactivated = True
        registry.save()
        objInDatabase = OaiRegistry.objects.get(pk=registry.id)
        self.assertEquals(objInDatabase.isDeactivated, True)
        data = {"RegistryId": str(registry.id)}
        req = self.doRequestPost(url=reverse("api_reactivate_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        objInDatabase = OaiRegistry.objects.get(pk=registry.id)
        self.assertEquals(objInDatabase.isDeactivated, False)

    def test_reactivate_registry_unauthorized(self):
        data = {"RegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_reactivate_registry"), data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reactivate_registry_unauthorized_user(self):
        data = {"RegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_reactivate_registry"), data=data, auth=USER_AUTH)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reactivate_registry_not_found(self):
        data = {"RegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_reactivate_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_404_NOT_FOUND)

    def test_reactivate_registry_serializer_invalid(self):
        data = {"RRegistryId": FAKE_ID}
        req = self.doRequestPost(url=reverse("api_reactivate_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reactivate_registry_bad_entries(self):
        data = {"RegistryId": 1000}
        req = self.doRequestPost(url=reverse("api_reactivate_registry"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)


################################################################################

######################### Update registry harvest tests ########################
    def test_update_registry_harvest(self):
        self.dump_oai_settings()
        self.dump_oai_registry()
        registry = OaiRegistry.objects.get()
        OaiMetadataFormat.objects(registry=str(registry.id)).update(set__harvest=False)
        OaiSet.objects(registry=str(registry.id)).update(set__harvest=False)
        twoFirstMF = [str(x.id) for x in OaiMetadataFormat.objects(registry=str(registry.id)).limit(2)]
        twoFirstSet = [str(x.id) for x in OaiSet.objects(registry=str(registry.id)).limit(2)]
        data = {"id": str(registry.id), 'metadataFormats': twoFirstMF, 'sets': twoFirstSet}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_200_OK)
        metadataFormatsInDatabaseModified = OaiMetadataFormat.objects(registry=str(registry.id), pk__in=twoFirstMF).all()
        setsInDatabaseModified = OaiSet.objects(registry=str(registry.id), pk__in=twoFirstSet).all()
        metadataFormatsInDatabase = OaiMetadataFormat.objects(registry=str(registry.id), pk__nin=twoFirstMF).all()
        setsInDatabase = OaiSet.objects(registry=str(registry.id), pk__nin=twoFirstSet).all()
        for metadataF in metadataFormatsInDatabaseModified:
            self.assertEquals(metadataF.harvest, True)
        for set in setsInDatabaseModified:
            self.assertEquals(set.harvest, True)
        for metadataF in metadataFormatsInDatabase:
            self.assertEquals(metadataF.harvest, False)
        for set in setsInDatabase:
            self.assertEquals(set.harvest, False)

    def test_update_registry_harvest_unauthorized(self):
        data = {"id": FAKE_ID, 'metadataFormats': [], 'sets': []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=None)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_registry_harvest_unauthorized_user(self):
        data = {"id": FAKE_ID, 'metadataFormats': [], 'sets': []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=USER_AUTH)
        self.assertEquals(req.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_registry_harvest_serializer_invalid(self):
        data = {"idd": FAKE_ID, 'metadataFormats': [], 'sets': []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"id": FAKE_ID, 'mmetadataFormats': [], 'sets': []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"id": FAKE_ID, 'metadataFormats': [], 'ssets': []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"id": FAKE_ID}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"metadataFormats": []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"sets": []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"id": FAKE_ID, 'metadataFormats': []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"id": FAKE_ID, 'sets': []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)
        data = {"metadataFormats": [], 'sets': []}
        req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_update_registry_harvest_bad_entries(self):
        #TODO Control charfield
        # data = {"id": 1000, 'metadataFormats': 1000, 'sets': 200}
        # req = self.doRequestPut(url=reverse("api_update_registry_harvest"), data=data, auth=ADMIN_AUTH)
        # self.assertEquals(req.status_code, status.HTTP_400_BAD_REQUEST)



################################################################################

################################################################################
########################## Common assert controls ##############################
################################################################################

    def assert_OaiIdentify_Settings(self, retrievedIdentifyData):
        information = OaiSettings.objects.get()
        # self.assertEquals(retrievedIdentifyData['adminEmail'], (email for name, email in settings.OAI_ADMINS))
        self.assertEquals(retrievedIdentifyData['baseURL'], URL_TEST_SERVER)
        self.assertEquals(retrievedIdentifyData['repositoryName'], information.repositoryName)
        self.assertEquals(retrievedIdentifyData['deletedRecord'], settings.OAI_DELETED_RECORD)
        self.assertEquals(retrievedIdentifyData['granularity'], settings.OAI_GRANULARITY)
        self.assertEquals(retrievedIdentifyData['protocolVersion'], settings.OAI_PROTOCOLE_VERSION)
        self.assertEquals(retrievedIdentifyData['repositoryIdentifier'], information.repositoryIdentifier)
        self.assertEquals(retrievedIdentifyData['sampleIdentifier'], settings.OAI_SAMPLE_IDENTIFIER)
        self.assertEquals(retrievedIdentifyData['scheme'], settings.OAI_SCHEME)


    def assert_OaiIdentify(self, objIdentify):
        identifyData = self.getIdentifyData()
        objInDatabaseXmlTree = etree.XML(xmltodict.unparse(objIdentify.raw).encode('utf-8'))
        objInDatabaseXmlString = etree.tostring(objInDatabaseXmlTree, xml_declaration=False)
        self.assertEquals(identifyData['adminEmail'], objIdentify.adminEmail)
        self.assertEquals(identifyData['baseURL'], objIdentify.baseURL)
        self.assertEquals(identifyData['repositoryName'], objIdentify.repositoryName)
        self.assertEquals(identifyData['deletedRecord'], objIdentify.deletedRecord)
        self.assertEquals(identifyData['description'], objIdentify.description)
        self.assertEquals(identifyData['earliestDatestamp'], objIdentify.earliestDatestamp)
        self.assertEquals(identifyData['granularity'], objIdentify.granularity)
        self.assertEquals(identifyData['oai_identifier'], objIdentify.oai_identifier)
        self.assertEquals(identifyData['protocolVersion'], objIdentify.protocolVersion)
        self.assertEquals(identifyData['repositoryIdentifier'], objIdentify.repositoryIdentifier)
        self.assertEquals(identifyData['sampleIdentifier'], objIdentify.sampleIdentifier)
        self.assertEquals(identifyData['scheme'], objIdentify.scheme)
        #TODO Keep the oriaginal XML order: OrderedDict
        # self.assertEquals(identifyData['raw'], objInDatabaseXmlString)

    def assert_OaiRegistry(self, registry, objIdentify):
        strUrl, harvest, harvestrate = self.getRegistryData()
        self.assertEquals(registry.identify, objIdentify)
        self.assertEquals(registry.name, objIdentify.repositoryName)
        self.assertEquals(registry.url, strUrl)
        self.assertEquals(registry.description, objIdentify.description)
        self.assertEquals(registry.harvest, harvest)
        self.assertEquals(registry.harvestrate, harvestrate)
        self.assertEquals(registry.isDeactivated, False)


    def assert_OaiMetadataFormat(self, retrievedMetadataformatsData):
        #Get metadata format in database
        metadataFormatsInDatabase = OaiMyMetadataFormat.objects.all()
        #Check with what we just retrieve
        for metadataFormat in metadataFormatsInDatabase:
            el = [x for x in retrievedMetadataformatsData if x['metadataPrefix'] == metadataFormat.metadataPrefix][0]
            self.assertNotEquals(el, None)
            self.assertEquals(el['metadataNamespace'], metadataFormat.metadataNamespace)
            self.assertEquals(el['schema'], metadataFormat.schema)
            # self.assertEquals(el['raw'], metadataFormat.raw)

    def assert_OaiSet(self, retrievedSetsData):
        #Get metadata format in database
        setsInDatabase = OaiMySet.objects.all()
        #Check with what we just retrieve
        for set in setsInDatabase:
            el = [x for x in retrievedSetsData if x['setSpec'] == set.setSpec][0]
            self.assertNotEquals(el, None)
            self.assertEquals(el['setName'], set.setName)
            # self.assertEquals(el['raw'], set.raw)

################################################################################
################################################################################
################################################################################

################################################################################
############################# Common methods ###################################
################################################################################

    def setHarvest(self, value):
        information = OaiSettings.objects.get()
        information.enableHarvesting = value
        information.save()

    def getIdentifyData(self):
        identifyData = {"adminEmail": "test@oai-pmh.us",
              "baseURL": "http://127.0.0.1:8000/oai_pmh/server/",
              "repositoryName": "X Repository",
              "deletedRecord": "no",
              "delimiter": ":",
              "description": "One OAI-PMH server",
              "earliestDatestamp": '1989-12-31T15:23:00Z',
              "granularity": 'YYYY-MM-DDThh:mm:ssZ',
              "oai_identifier": 'oai-identifier',
              "protocolVersion": '2.0',
              "repositoryIdentifier": 'server-127.0.0.1',
              "sampleIdentifier": "oai:server-127.0.0.1:id/12345678a123aff6ff5f2d9e",
              "scheme": 'oai',
              "raw": '<Identify xmlns="http://www.openarchives.org/OAI/2.0/" '
                     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                     '<repositoryName>X Repository</repositoryName>'
                     '<baseURL>http://127.0.0.1:8000/oai_pmh/server/</baseURL>'
                     '<protocolVersion>2.0</protocolVersion>'
                     '<adminEmail>test@oai-pmh.us</adminEmail>'
                     '<earliestDatestamp>1989-12-31T15:23:00Z</earliestDatestamp>'
                     '<deletedRecord>no</deletedRecord>'
                     '<granularity>YYYY-MM-DDThh:mm:ssZ</granularity>'
                     '<description><oai-identifier xmlns="http://www.openarchives.org/OAI/2.0/oai-identifier" '
                     'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                     'xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai-identifier '
                     'http://www.openarchives.org/OAI/2.0/oai-identifier.xsd"><scheme>oai</scheme>'
                     '<repositoryIdentifier>server-127.0.0.1</repositoryIdentifier><delimiter>:</delimiter>'
                     '<sampleIdentifier>oai:server-127.0.0.1:id/12345678a123aff6ff5f2d9e</sampleIdentifier>'
                     '</oai-identifier></description>'
                     '</Identify>'
        }
        return identifyData


    def getMetadataFormatData(self):
        metadataFormatData = [{'metadataPrefix': 'oai_dc',
                               'metadataNamespace': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
                               'schema': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
                               'raw': '<metadataFormat xmlns="http://www.openarchives.org/OAI/2.0/" '
                                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                                      '<metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>'
                                      '<metadataPrefix>oai_dc</metadataPrefix>'
                                      '<schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd</schema></metadataFormat>'},
                              {'metadataPrefix': 'oai_all',
                               'metadataNamespace': 'http://www.w3.org/2001/XMLSchema',
                               'schema': 'http://127.0.0.1:8082/oai_pmh/server/XSD/AllResources.xsd',
                               'raw': '<metadataFormat xmlns="http://www.openarchives.org/OAI/2.0/" '
                                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                                      '<metadataNamespace>http://www.w3.org/2001/XMLSchema</metadataNamespace>'
                                      '<metadataPrefix>oai_all</metadataPrefix>'
                                      '<schema>http://127.0.0.1:8082/oai_pmh/server/XSD/AllResources.xsd</schema></metadataFormat>'},
                              {'metadataPrefix': 'oai_soft',
                               'metadataNamespace': 'http://www.w3.org/2001/XMLSchema',
                               'schema': 'http://127.0.0.1:8082/oai_pmh/server/XSD/Software.xsd',
                               'raw': '<metadataFormat xmlns="http://www.openarchives.org/OAI/2.0/" '
                                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                                      '<metadataNamespace>http://www.w3.org/2001/XMLSchema</metadataNamespace>'
                                      '<metadataPrefix>oai_soft</metadataPrefix>'
                                      '<schema>http://127.0.0.1:8082/oai_pmh/server/XSD/Software.xsd</schema></metadataFormat>'}
                            ]
        return metadataFormatData


    def getSetData(self):
        setData = [{'setName': 'all', 'setSpec': 'all',
                    'raw': '<set xmlns="http://www.openarchives.org/OAI/2.0/" '
                           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                           '<setSpec>all</setSpec>'
                           '<setName>all</setName>'
                           '<setDescription><oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
                           'xmlns:dc="http://purl.org/dc/elements/1.1/"'
                           ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                           'xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/            '
                           ' http://www.openarchives.org/OAI/2.0/oai_dc.xsd">'
                           '<dc:description xml:lang="en">'
                           '\n                    Get all records\n                </dc:description>'
                           '</oai_dc:dc></setDescription></set>'},
                   {'setName': 'software', 'setSpec': 'soft',
                    'raw': '<set xmlns="http://www.openarchives.org/OAI/2.0/" '
                           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                           '<setSpec>soft</setSpec>'
                           '<setName>software</setName>'
                           '<setDescription><oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
                           'xmlns:dc="http://purl.org/dc/elements/1.1/" '
                           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                           'xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/             '
                           'http://www.openarchives.org/OAI/2.0/oai_dc.xsd">'
                           '<dc:description xml:lang="en">\n                    Get software records\n                '
                           '</dc:description></oai_dc:dc></setDescription></set>'}
                   ]
        return setData

    def getSetDataBadRaw(self):
        setData = [{'setName': 'software', 'setSpec': 'soft',
                    'raw': '<set xmlns="http://www.openarchives.org/OAI/2.0/" '
                           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                           '<setSpec>soft</setSpec>'
                           '<setName>software</setName>'
                           '<setDescription><oai_dc:dc xmlns:oai_dc="http://www.openarchives.org/OAI/2.0/oai_dc/" '
                           'xmlns:dc="http://purl.org/dc/elements/1.1/" '
                           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                           'xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/             '
                           'http://www.openarchives.org/OAI/2.0/oai_dc.xsd">'
                           '<dc:description xml:lang="en">\n                    Get software records\n                '
                           '</dc:description></oai_dc:dc></setDescription>/set>'}
                   ]
        return setData


    def getMetadataFormatDataAllResources(self):
        metadataFormatData = {'metadataPrefix': 'oai_all',
                               'metadataNamespace': 'http://www.w3.org/2001/XMLSchema',
                               'schema': 'http://127.0.0.1:8082/oai_pmh/server/XSD/AllResources.xsd',
                               'raw': '<metadataFormat xmlns="http://www.openarchives.org/OAI/2.0/" '
                                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                                      '<metadataNamespace>http://www.w3.org/2001/XMLSchema</metadataNamespace>'
                                      '<metadataPrefix>oai_all</metadataPrefix>'
                                      '<schema>http://127.0.0.1:8082/oai_pmh/server/XSD/AllResources.xsd</schema></metadataFormat>'}

        return metadataFormatData

    def getMetadataFormatDataBadRaw(self):
        metadataFormatData = [{'metadataPrefix': 'oai_dc',
                               'metadataNamespace': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
                               'schema': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
                               'raw': '<metadataFormat xmlns="http://www.openarchives.org/OAI/2.0/" '
                                      'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                                      '<metadataNamespace>http://www.openarchives.org/OAI/2.0/oai_dc/</metadataNamespace>'
                                      '<metadataPrefix>oai_dc</metadataPrefix>'
                                      '<schema>http://www.openarchives.org/OAI/2.0/oai_dc.xsd</schema>/metadataFormat>'}
                            ]
        return metadataFormatData


    def getRegistryData(self):
        strUrl = "http://127.0.0.1:8000/oai_pmh/server/"
        harvest = True
        harvestrate = 200
        return strUrl, harvest, harvestrate

    def call_createOaiIdentify(self):
        identifyData = self.getIdentifyData()
        identifyRaw = xmltodict.parse(identifyData['raw'])
        objIdentify = createOaiIdentify(identifyData, identifyRaw)
        return objIdentify

    def call_createRegistry(self):
        strUrl, harvest, harvestrate = self.getRegistryData()
        identifyData = self.getIdentifyData()
        identify, registry = createRegistry(harvest=harvest, harvestrate=harvestrate, identifyData=identifyData,
                                            url=strUrl)
        return identify, registry


    def createFakeRegistry(self):
        registry = OaiRegistry()
        registry.name = "Fake registry"
        registry.isDeactivated = False
        registry.url = "http://fakeserver.com"
        registry.save()
        return registry

################################################################################
################################################################################
################################################################################