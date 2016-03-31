################################################################################
#
# File Name: discover.py
# Purpose:
#
# Author: Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from django.conf import settings
from mgi.models import OaiSettings


def init_settings():
    """
    Init settings for the OAI-PMH feature.
    Set the name, identifier and the harvesting information
    """
    try:
        #Get OAI-PMH settings information about this server
        information = OaiSettings.objects.all()
        #If we don't have settings in database, we have to initialize them
        if not information:
            OaiSettings(repositoryName = settings.OAI_NAME, repositoryIdentifier = settings.OAI_REPO_IDENTIFIER,
                        enableHarvesting= False).save()

    except Exception, e:
        print('ERROR : Impossible to init the settings : ' + e.message)


