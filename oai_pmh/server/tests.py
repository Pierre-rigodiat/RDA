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

URL = '/oai_pmh/server'

class tests_OAI_PMH_server(OAI_PMH_Test):

    def setUp(self):
        super(tests_OAI_PMH_server, self).setUp()
        self.dump_oai_settings()

    def doRequestServer(self, data=None, auth=None):
        return self.doRequestGet(URL, data=data, auth=auth)

    def test_no_setting(self):
        self.clean_db()
        r = self.doRequestServer()
        self.isStatusInternalError(r)
