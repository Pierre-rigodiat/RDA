from django.apps import AppConfig
from oai_pmh import discover


# TODO: loaded two times (not a problem and may not happen in production) 
# see http://stackoverflow.com/a/16111968 
class OAIPMHConfig(AppConfig):
    name = 'oai_pmh'
    verbose_name = "oai_pmh"

    def ready(self):
        discover.init_settings()