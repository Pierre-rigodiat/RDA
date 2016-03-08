################################################################################
#
# File Name: discover.py
# Purpose:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#         Pierre Francois RIGODIAT
#		  pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from django.conf import settings
from mgi.models import OaiPmhSettings


def init_settings():
    """
    Init settings for the OAI-PMH feature.
    Set the name, identifier and the harvesting information
    """
    try:
        information = OaiPmhSettings.objects.all()
        if not information:
            OaiPmhSettings(repositoryName = settings.OAI_NAME, repositoryIdentifier = settings.OAI_REPO_IDENTIFIER,
                        enableHarvesting= False).save()

    except Exception, e:
        print('ERROR : Impossible to init the settings : ' + e.message)


