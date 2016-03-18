################################################################################
#
# File Name: apps.py
# Application: Informatics Core
# Description:
#
# Author: Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.apps import AppConfig
from oai_pmh import discover, tasks
from mgi.models import OaiRecord



# TODO: loaded two times (not a problem and may not happen in production) 
# see http://stackoverflow.com/a/16111968 
class OAIPMHConfig(AppConfig):
    name = 'oai_pmh'
    verbose_name = "oai_pmh"

    def ready(self):
        discover.init_settings()
        OaiRecord.initIndexes()
        tasks.init_harvest()