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
from mgi.models import OaiSettings, OaiMySet
from exceptions import BAD_VERB, NO_SET_HIERARCHY
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
