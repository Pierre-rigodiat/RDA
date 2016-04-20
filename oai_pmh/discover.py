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
from mgi.models import OaiSettings, OaiMyMetadataFormat, Template
from lxml import etree
from lxml.etree import XMLSyntaxError
import os
from mgi.settings import SITE_ROOT, OAI_HOST_URI
from django.core.urlresolvers import reverse

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
        #Add NMRR templates as metadata prefixes
        templates = {
            'all': {'path': 'AllResources.xsd', 'metadataPrefix': 'oai_all'},
            'organization': {'path': 'Organization.xsd', 'metadataPrefix': 'oai_org'},
            'datacollection': {'path': 'DataCollection.xsd', 'metadataPrefix': 'oai_datacol'},
            'repository': {'path': 'Repository.xsd', 'metadataPrefix': 'oai_repo'},
            'projectarchive': {'path': 'ProjectArchive.xsd', 'metadataPrefix': 'oai_proj'},
            'database': {'path': 'Database.xsd', 'metadataPrefix': 'oai_database'},
            'dataset': {'path': 'Dataset.xsd', 'metadataPrefix': 'oai_dataset'},
            'service': {'path': 'Service.xsd', 'metadataPrefix': 'oai_serv'},
            'informational': {'path': 'Informational.xsd', 'metadataPrefix': 'oai_info'},
            'software': {'path': 'Software.xsd', 'metadataPrefix': 'oai_soft'},
        }

        for template_name, info in templates.iteritems():
            try:
                template = Template.objects.get(title=template_name, filename=info['path'])
                #Check if the XML is well formed
                try:
                    xml_schema = template.content
                    dom = etree.fromstring(xml_schema.encode('utf-8'))
                    if 'targetNamespace' in dom.find(".").attrib:
                        metadataNamespace = dom.find(".").attrib['targetNamespace'] or "namespace"
                    else:
                        metadataNamespace = "http://www.w3.org/2001/XMLSchema"
                except XMLSyntaxError:
                    print('ERROR : Impossible to set the template "%s" as a metadata prefix. The template XML is not well formed.'% template_name)
                #Create a schema URL
                schemaURL = OAI_HOST_URI + reverse('getXSD', args=[template.filename])
                #Add in database
                OaiMyMetadataFormat(metadataPrefix=info['metadataPrefix'],
                                   schema=schemaURL,
                                   metadataNamespace=metadataNamespace, xmlSchema='', isDefault=False,
                                   isTemplate=True, template=template).save()
            except Exception, e:
                print('ERROR : Impossible to set the template "{!s}" as a metadata prefix. {!s}'.format(template_name, e.message))
