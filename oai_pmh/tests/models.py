################################################################################
#
# File Name: models.py
# Application: oai_pmh/tests
# Purpose:
#
# Author: Xavier SCHMITT
#         xavier.schmitt@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from testing.models import RegressionTest, OaiMyMetadataFormat, DUMP_OAI_PMH_TEST_PATH, join, OaiMySet, OaiSettings, ADMIN_AUTH, USER_AUTH

class OAI_PMH_Test(RegressionTest):

    def setUp(self):
        super(OAI_PMH_Test, self).setUp()
        self.clean_db()

    def dump_oai_my_metadata_format(self):
        self.assertEquals(len(OaiMyMetadataFormat.objects()), 0)
        self.restoreDump(join(DUMP_OAI_PMH_TEST_PATH, 'oai_my_metadata_format.bson'), 'oai_my_metadata_format')
        self.assertTrue(len(OaiMyMetadataFormat.objects()) > 0)

    def dump_oai_my_set(self):
        self.assertEquals(len(OaiMySet.objects()), 0)
        self.restoreDump(join(DUMP_OAI_PMH_TEST_PATH, 'oai_my_set.bson'), 'oai_my_set')
        self.assertTrue(len(OaiMySet.objects()) > 0)

    def dump_oai_settings(self):
        self.assertEquals(len(OaiSettings.objects()), 0)
        self.restoreDump(join(DUMP_OAI_PMH_TEST_PATH, 'oai_settings.bson'), 'oai_settings')
        self.assertTrue(len(OaiSettings.objects()) > 0)
