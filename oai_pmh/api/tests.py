################################################################################
#
# File Name: tests.py
# Application: oai_pmh/api
# Purpose:
#
# Author: Xavier SCHMITT
#         xavier.schmitt@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from oai_pmh.tests.models import OAI_PMH_Test

class tests_OAI_PMH_API(OAI_PMH_Test):

    def test_dumps(self):
        self.dump_result_xslt()
        self.dump_oai_settings()
        self.dump_oai_my_metadata_format()
        self.dump_xmldata()
        self.dump_oai_my_set()
