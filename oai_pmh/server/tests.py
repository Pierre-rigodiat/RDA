################################################################################
#
# File Name: tests.py
# Application: oai_pmh/server
# Purpose:
#
# Author: Xavier SCHMITT
#         xavier.schmitt@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from oai_pmh.tests.models import OAI_PMH_Test
from mgi.models import OaiSettings, OaiMySet, OaiMyMetadataFormat
from exceptions import BAD_VERB, NO_SET_HIERARCHY, BAD_ARGUMENT, DISSEMINATE_FORMAT, NO_RECORDS_MATCH, NO_METADATA_FORMAT
from lxml import etree

URL = '/oai_pmh/server'

XMLParser = etree.XMLParser(remove_blank_text=True, recover=True)

class tests_OAI_PMH_server(OAI_PMH_Test):

    def setUp(self):
        super(tests_OAI_PMH_server, self).setUp()
        self.dump_oai_settings()
        self.doHarvest(True)

    def doHarvest(self, harvest):
        information = OaiSettings.objects.get()
        information.enableHarvesting = harvest
        information.save()

    def checkTagErrorCode(self, text, error):
        for tag in etree.XML(text.encode("utf8"), parser=XMLParser).iterfind('.//' + '{http://www.openarchives.org/OAI/2.0/}' + 'error'):
            self.assertEqual(tag.attrib['code'], error)

    def checkTagExist(self, text, checkTag):
        for tag in etree.XML(text.encode("utf8"), parser=XMLParser).iterfind('.//' + '{http://www.openarchives.org/OAI/2.0/}' + checkTag):
            self.assertTrue(tag)

    def checkTagCount(self, text, checkTag, number):
        count = 0
        for tag in etree.XML(text.encode("utf8"), parser=XMLParser).iterfind('.//' + '{http://www.openarchives.org/OAI/2.0/}' + checkTag):
            count+=1
        self.assertEquals(number, count)

    def doRequestServer(self, data=None):
        return self.doRequestGet(URL, params=data)

    def test_no_setting(self):
        self.clean_db()
        r = self.doRequestServer()
        self.isStatusInternalError(r)

    def test_no_harvesting(self):
        self.doHarvest(False)
        r = self.doRequestServer()
        self.isStatusNotFound(r)

    def test_no_verb(self):
        r = self.doRequestServer()
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, BAD_VERB)

    def test_duplicate(self):
        data = {'verb': ['test2', 'test2']}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, BAD_ARGUMENT)

    def test_identify(self):
        data = {'verb': 'Identify'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagExist(r.text, 'Identify')

    def test_listSets_no_sets(self):
        data = {'verb': 'ListSets'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, NO_SET_HIERARCHY)

    def test_listSets(self):
        self.dump_oai_my_set()
        data = {'verb': 'ListSets'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagExist(r.text, 'ListSets')
        self.checkTagCount(r.text, 'set', len(OaiMySet.objects().all()))

    def test_list_identifiers_error_argument_metadataprefix_missing(self):
        data = {'verb': 'ListIdentifiers', 'from':'test'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, BAD_ARGUMENT)

    def test_list_identifiers_error_date_from(self):
        data = {'verb': 'ListIdentifiers', 'metadataPrefix': 'test', 'from': 'test'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, BAD_ARGUMENT)

    def test_list_identifiers_error_date_until(self):
        data = {'verb': 'ListIdentifiers', 'metadataPrefix': 'test', 'until': 'test'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, BAD_ARGUMENT)

    def test_list_identifiers_error_no_metadataformat(self):
        data = {'verb': 'ListIdentifiers', 'metadataPrefix': 'oai_dc', 'from': '2015-01-01T12:12:12Z', 'until': '2016-01-01T12:12:12Z'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, DISSEMINATE_FORMAT)

    def test_list_identifiers_error_with_no_set(self):
        self.dump_oai_my_metadata_format()
        data = {'verb': 'ListIdentifiers', 'metadataPrefix': 'oai_dc', 'from': '2015-01-01T12:12:12Z', 'until': '2016-01-01T12:12:12Z', 'set': 'test'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, NO_RECORDS_MATCH)

    def test_list_identifiers_error_with_bad_set(self):
        self.dump_oai_my_metadata_format()
        self.dump_oai_my_set()
        data = {'verb': 'ListIdentifiers', 'metadataPrefix': 'oai_dc', 'from': '2015-01-01T12:12:12Z', 'until': '2016-01-01T12:12:12Z', 'set': 'test'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, NO_RECORDS_MATCH)

    # def test_list_identifiers_TODO(self):
        # self.dump_oai_templ_mf_xslt()
        # self.dump_template()
    #     self.dump_oai_my_metadata_format()
    #     self.dump_oai_my_set()
    #     data = {'verb': 'ListIdentifiers', 'metadataPrefix': 'TODO replace here', 'from': '2015-01-01T12:12:12Z', 'until': '2016-01-01T12:12:12Z', 'set': 'TODO replace here'}
    #     r = self.doRequestServer(data=data)
    #     self.isStatusOK(r)

    def test_list_metadataformat_no_data(self):
        data = {'verb': 'ListMetadataFormats'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagErrorCode(r.text, NO_METADATA_FORMAT)

    def test_list_metadataformat_no_identifier(self):
        self.dump_oai_my_metadata_format()
        data = {'verb': 'ListMetadataFormats'}
        r = self.doRequestServer(data=data)
        self.isStatusOK(r)
        self.checkTagExist(r.text, 'ListMetadataFormats')
        self.checkTagCount(r.text, 'metadataFormat', len(OaiMyMetadataFormat.objects().all()))

    # def test_list_metadataformat_with_identifier(self):
    #     self.dump_xmldata()
    #     self.dump_oai_templ_mf_xslt()
    #     self.dump_oai_my_metadata_format()
    #     data = {'verb': 'ListMetadataFormats'}
    #     r = self.doRequestServer(data=data)
    #     self.isStatusOK(r)
    #     self.checkTagExist(r.text, 'ListMetadataFormats')
    #     self.checkTagExist(r.text, 'metadataFormat')
    #     #self.checkTagCount(r.text, 'metadataFormat', len(OaiMyMetadataFormat.objects().all()))