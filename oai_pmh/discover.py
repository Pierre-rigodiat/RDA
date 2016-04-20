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
from mgi.models import OaiSettings, OaiMyMetadataFormat
from lxml import etree
from lxml.etree import XMLSyntaxError
import os
from mgi.settings import SITE_ROOT

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


def load_metadata_prefixes():
    """
    Load default metadata prefixes for OAI-PMH
    """
    metadataPrefixes = OaiMyMetadataFormat.objects.all()
    if len(metadataPrefixes) == 0:
        #Add OAI_DC metadata prefix
        schemaURL = "http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
        file = open(os.path.join(SITE_ROOT, 'oai_pmh', 'resources', 'xsd', 'oai_dc.xsd'),'r')
        xsdContent = file.read()
        dom = etree.fromstring(xsdContent.encode('utf-8'))
        if 'targetNamespace' in dom.find(".").attrib:
            metadataNamespace = dom.find(".").attrib['targetNamespace'] or "namespace"
        else:
            metadataNamespace = "http://www.w3.org/2001/XMLSchema"
        OaiMyMetadataFormat(metadataPrefix='oai_dc',
                            schema=schemaURL,
                            metadataNamespace=metadataNamespace,
                            xmlSchema=xsdContent,
                            isDefault=True).save()

