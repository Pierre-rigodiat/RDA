################################################################################
#
# File Name: rest_views.py
# Application: Informatics Core
# Description:
#
# Author: Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.views.generic import TemplateView
from mgi.models import Template, TemplateVersion, XMLdata, OaiSettings
import os
from oai_pmh.server.exceptions import *
import xmltodict
from bson.objectid import ObjectId
from StringIO import StringIO
import lxml.etree as etree
import re
from oai_pmh import datestamp
import datetime

RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'oai_pmh/server/resources/')

class OAIProvider(TemplateView):
    content_type = 'text/xml'

    def last_modified(self, obj):
        # datetime object was last modified
        pass

################################################################################
#
# Function Name: render_to_response(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Render the XML file
#
################################################################################
    def render_to_response(self, context, **response_kwargs):
        # all OAI responses should be xml
        if 'content_type' not in response_kwargs:
            response_kwargs['content_type'] = self.content_type

        # add common context data needed for all responses
        context.update({
            'now': datestamp.datetime_to_datestamp(datetime.datetime.now()),
            'verb': self.oai_verb,
            'identifier': self.identifier,
            'metadataPrefix': self.metadataPrefix,
            'url': self.request.build_absolute_uri(self.request.path),
            'from': self.From,
            'until': self.until,
        })

        return super(TemplateView, self) \
            .render_to_response(context, **response_kwargs)


    def getEarliestDate(self):
        try:
            data = XMLdata.getMinValue('publicationdate')
            if data != None:
                return datestamp.datetime_to_datestamp(data)
            else:
                return ''
        except Exception:
            return ''

################################################################################
#
# Function Name: identify(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Response to identify request
#
################################################################################
    def identify(self):
        self.template_name = 'oai_pmh/xml/identify.xml'
        information = OaiSettings.objects.get()
        if information:
            name = information.repositoryName
            repoIdentifier = information.repositoryIdentifier
        else:
            name = settings.OAI_NAME
            repoIdentifier = settings.OAI_REPO_IDENTIFIER

        identify_data = {
            'name': name,
            'protocole_version': settings.OAI_PROTOCOLE_VERSION,
            'admins': (email for name, email in settings.OAI_ADMINS),
            'earliest_date': self.getEarliestDate(),   # placeholder
            'deleted': settings.OAI_DELETED_RECORD,  # no, transient, persistent
            'granularity': settings.OAI_GRANULARITY,  # or YYYY-MM-DD
            'identifier_scheme': settings.OAI_SCHEME,
            'repository_identifier': repoIdentifier,
            'identifier_delimiter': settings.OAI_DELIMITER,
            'sample_identifier': settings.OAI_SAMPLE_IDENTIFIER
        }
        return self.render_to_response(identify_data)

################################################################################
#
# Function Name: list_sets(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Response to ListSets request
#
################################################################################
    def list_sets(self):
        # self.template_name = 'admin/oai_pmh/xml/list_sets.xml'
        # items = []
        try:
            raise noSetHierarchy
        except OAIExceptions, e:
            return self.errors(e.errors)
        except OAIException, e:
            return self.error(e)
        except Exception, e:
            return self.error(e.code, e.message)
        #TODO
        except badResumptionToken, e:
            return self.error(badResumptionToken.code, badResumptionToken.message)

################################################################################
#
# Function Name: list_metadata_formats(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Response to ListMetadataFormats request
#
################################################################################
    def list_metadata_formats(self):
        try:
            self.template_name = 'oai_pmh/xml/list_metadata_formats.xml'
            items = []
            # If an identifier is provided, with look for its metaformats
            if self.identifier != None:
                #Check if the identifier pattern is OK
                p = re.compile("%s:%s:id/(.*)" % (settings.OAI_SCHEME, settings.OAI_REPO_IDENTIFIER))
                idMatch = p.search(self.identifier)
                if idMatch:
                    #If yes, we retrieve the record ID
                    id = idMatch.group(1)
                else:
                    raise idDoesNotExist(self.identifier)
                #We retrieve all schema id for this record
                listId = []
                listId.append(id)
                listSchemaIds = XMLdata.getByIDsAndDistinctBy(listId, 'schema')
                #Remove templates which are not current or deleted
                templatesCurrent = TemplateVersion.objects(current__in=listSchemaIds, isDeleted=False)\
                                  .distinct(field="current")
                #Get templates
                templates = Template.objects(pk__in=templatesCurrent)
            else:
                templatesCurrent = TemplateVersion.objects(isDeleted=False).distinct(field="current")
                templates = Template.objects(pk__in=templatesCurrent)

            if len(templates) == 0:
                raise noMetadataFormat
            else:
                url = self.request.build_absolute_uri(self.request.path)
                for template in templates:
                    item_info = {
                        'metadataNamespace': url + template.title,
                        'metadataPrefix':  template.title,
                        'schema':  url + 'XSD/' + template.filename
                    }
                    items.append(item_info)

            return self.render_to_response({'items': items})
        except OAIExceptions, e:
            return self.errors(e.errors)
        except OAIException, e:
            return self.error(e)
        except Exception, e:
            return self.error(e.code, e.message)

################################################################################
#
# Function Name: list_identifiers(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Response to ListIdentifiers request
#
################################################################################
    def list_identifiers(self):
        try:
            self.template_name = 'oai_pmh/xml/list_identifiers.xml'
            query = dict()
            #FROM AND UNTIL
            date_errors = []
            if self.until:
                try:
                    endDate = datestamp.datestamp_to_datetime(self.until)
                    query['publicationdate'] = { "$lte" : endDate}
                except:
                    error = 'Illegal date/time for "until" (%s)' % self.until
                    date_errors.append(badArgument(error))
            if self.From:
                try:
                    startDate = datestamp.datestamp_to_datetime(self.From)
                    query['publicationdate'] = { "$gte" : startDate}
                except:
                    error = 'Illegal date/time for "from" (%s)' % self.From
                    date_errors.append(badArgument(error))
            if len(date_errors) > 0:
                raise OAIExceptions(date_errors)
            try:
                templatesVersionID = Template.objects(title=self.metadataPrefix).distinct(field="templateVersion")
                templateID = TemplateVersion.objects(pk__in=templatesVersionID, isDeleted=False).distinct(field="current")
                templates = Template.objects.get(pk__in=templateID)
            except:
                raise cannotDisseminateFormat(self.metadataPrefix)
            query['schema'] = str(templates.id)
            items = []
            data = XMLdata.executeQueryFullResult(query)
            if len(data) == 0:
                raise noRecordsMatch
            for i in data:
                identifier = '%s:%s:id/%s' % (settings.OAI_SCHEME, settings.OAI_REPO_IDENTIFIER, str(i['_id']))
                item_info = {
                    'identifier': identifier,
                    'last_modified': datestamp.datetime_to_datestamp(i['publicationdate']) if 'publicationdate' in i else datestamp.datetime_to_datestamp(datetime.datetime.min),
                    'sets': ''
                }
                items.append(item_info)

            return self.render_to_response({'items': items})
        except OAIExceptions, e:
            return self.errors(e.errors)
        except OAIException, e:
            return self.error(e)
        except Exception, e:
            return self.error(e.code, e.message)
        #TODO
        except badResumptionToken, e:
            return self.error(badResumptionToken.code, badResumptionToken.message)

################################################################################
#
# Function Name: get_record(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Response to GetRecord request
#
################################################################################
    def get_record(self):
        try:
            #Check if the identifier pattern is OK
            p = re.compile("%s:%s:id/(.*)" % (settings.OAI_SCHEME, settings.OAI_REPO_IDENTIFIER))
            idMatch = p.search(self.identifier)
            if idMatch:
                #If yes, we retrieve the record ID
                id = idMatch.group(1)
            else:
                raise idDoesNotExist(self.identifier)
            self.template_name = 'oai_pmh/xml/get_record.xml'
            try:
                templatesVersionID = Template.objects(title=self.metadataPrefix).distinct(field="templateVersion")
                templateID = TemplateVersion.objects(pk__in=templatesVersionID, isDeleted=False).distinct(field="current")
                templates = Template.objects.get(pk__in=templateID)
            except:
                raise cannotDisseminateFormat(self.metadataPrefix)
            query = dict()
            try:
                query['_id'] = ObjectId(id)
            except Exception:
                raise idDoesNotExist(self.identifier)
            data = XMLdata.executeQueryFullResult(query)
            #This id doesn't exist
            if len(data) == 0:
                raise idDoesNotExist(self.identifier)
            query['schema'] = str(templates.id)
            data = XMLdata.executeQueryFullResult(query)
            #The metadataForm at doesn't match with the id
            if len(data) == 0:
                raise cannotDisseminateFormat(self.metadataPrefix)
            else:
                data = data[0]
            xml = xmltodict.unparse(data['content'])
            clean_parser = etree.XMLParser(remove_blank_text=True,remove_comments=True,remove_pis=True)
            # set the parser
            etree.set_default_parser(parser=clean_parser)
            # load the XML tree from the text
            xmlEncoding = etree.XML(str(xml.encode('utf-8')))
            xmlStr = etree.tostring(xmlEncoding)
            record_info = {
                'identifier': self.identifier,
                'last_modified': datestamp.datetime_to_datestamp(data['publicationdate']) if 'publicationdate' in data else datestamp.datetime_to_datestamp(datetime.datetime.min),
                'sets': '',
                'XML': xmlStr
            }
            return self.render_to_response(record_info)
        except OAIExceptions, e:
            return self.errors(e.errors)
        except OAIException, e:
            return self.error(e)
        except Exception, e:
            return self.error(e.code, e.message)

################################################################################
#
# Function Name: list_records(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Response to ListRecords request
#
################################################################################
    def list_records(self):
        try:
            items = []
            self.template_name = 'oai_pmh/xml/list_records.xml'
            query = dict()
            #FROM AND UNTIL
            date_errors = []
            if self.until:
                try:
                    endDate = datestamp.datestamp_to_datetime(self.until)
                    query['publicationdate'] = { "$lte" : endDate}
                except:
                    error = 'Illegal date/time for "until" (%s)' % self.until
                    date_errors.append(badArgument(error))
            if self.From:
                try:
                    startDate = datestamp.datestamp_to_datetime(self.From)
                    query['publicationdate'] = { "$gte" : startDate}
                except:
                    error = 'Illegal date/time for "from" (%s)' % self.From
                    date_errors.append(badArgument(error))
            if len(date_errors) > 0:
                raise OAIExceptions(date_errors)
            try:
                templatesVersionID = Template.objects(title=self.metadataPrefix).distinct(field="templateVersion")
                templateID = TemplateVersion.objects(pk__in=templatesVersionID, isDeleted=False).distinct(field="current")
                templates = Template.objects.get(pk__in=templateID)
            except:
                raise cannotDisseminateFormat(self.metadataPrefix)
            query['schema'] = str(templates.id)
            data = XMLdata.executeQueryFullResult(query)
            if len(data) == 0:
                raise noRecordsMatch
            for elt in data:
                xml = xmltodict.unparse(elt['content'])
                identifier = '%s:%s:id/%s' % (settings.OAI_SCHEME, settings.OAI_REPO_IDENTIFIER,
                      elt['_id'])
                clean_parser = etree.XMLParser(remove_blank_text=True,remove_comments=True,remove_pis=True)
                # set the parser
                etree.set_default_parser(parser=clean_parser)
                # load the XML tree from the text
                xmlEncoding = etree.XML(str(xml.encode('utf-8')))
                xmlStr = etree.tostring(xmlEncoding)
                record_info = {
                    'identifier': identifier,
                    'last_modified': datestamp.datetime_to_datestamp(elt['publicationdate']) if 'publicationdate' in elt else datestamp.datetime_to_datestamp(datetime.datetime.min),
                    'sets': '',
                    'XML': xmlStr
                }
                items.append(record_info)
            return self.render_to_response({'items': items})
        except OAIExceptions, e:
            return self.errors(e.errors)
        except OAIException, e:
            return self.error(e)
        except Exception, e:
            return self.error(e.code, e.message)
        #TODO
        #Illegal date/time for "until" (55)
        except badResumptionToken, e:
            return self.error(badResumptionToken.code, badResumptionToken.message)

################################################################################
#
# Function Name: error(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Error response
#
################################################################################
    def error(self, error):
        return self.errors([error])

################################################################################
#
# Function Name: errors(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Errors response
#
################################################################################
    def errors(self, errors):
        self.template_name = 'oai_pmh/xml/error.xml'
        return self.render_to_response({
            'errors': errors,
        })


################################################################################
#
# Function Name: checkIllegalAndRequired(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Check OAI Error and Exception - Illegal and required arguments
#
################################################################################
    def checkIllegalAndRequired(self, legal, required, data):
        errors = []
        illegal = [arg for arg in data if arg not in legal]
        if len(illegal) > 0:
            for arg in illegal:
                error = 'Arguments ("%s") was passed that was not valid for ' \
                            'this verb' % arg
                errors.append(badArgument(error))

        missing = [arg for arg in required if arg not in data]
        if len(missing) > 0:
            for arg in missing:
                error = 'Missing required argument - %s' % arg
                errors.append(badArgument(error))

        if len(errors) > 0:
            raise OAIExceptions(errors)


################################################################################
#
# Function Name: checkBadArgument(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Check OAI Error and Exception - Bad Argument in request
#
################################################################################
    def checkBadArgument(self, data):
        #Check if we have duplicate arguments
        duplicates = [arg for arg in data if len(data.getlist(arg)) > 1]
        if len(duplicates) > 0:
            error_msg = 'An argument ("multiple occurances of %s") was passed that was not valid for ' \
                        'this verb' % ', '.join(duplicates)
            raise badArgument(error_msg)

        #Check illegal and required arguments
        if self.oai_verb != None:
            if self.oai_verb == 'Identify':
                legal = ['verb']
                required = ['verb']
            elif self.oai_verb== 'ListIdentifiers':
                legal = ['verb', 'metadataPrefix', 'from', 'until', 'set', 'resumptionToken']
                required = ['verb', 'metadataPrefix']
            elif self.oai_verb == 'ListSets':
                legal = ['verb', 'resumptionToken']
                required = ['verb']
            elif self.oai_verb == 'ListMetadataFormats':
                legal = ['verb', 'identifier']
                required = ['verb']
            elif self.oai_verb == 'GetRecord':
                legal = ['verb', 'identifier', 'metadataPrefix']
                required = ['verb', 'identifier', 'metadataPrefix']
            elif self.oai_verb == 'ListRecords':
                legal = ['verb', 'metadataPrefix', 'from', 'until', 'set', 'resumptionToken']
                required = ['verb', 'metadataPrefix']
            else:
                error_msg = 'The verb "%s" is illegal' % self.oai_verb
                raise badVerb(error_msg)
        else:
            error_msg = 'The request did not provide any verb.'
            raise badVerb(error_msg)

        self.checkIllegalAndRequired(legal, required, data)


################################################################################
#
# Function Name: get(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Determine OAI verb and hand off to appropriate
#
################################################################################
    def get(self, request, *args, **kwargs):
        try:
            information = OaiSettings.objects.get()
            if information and not information.enableHarvesting:
                return HttpResponseNotFound('<h1>OAI-PMH not available for harvesting</h1>')
            self.oai_verb = request.GET.get('verb', None)
            if self.oai_verb is None:
                error_msg = 'The request did not provide any verb.'
                raise badVerb(error_msg)
            #Init
            self.request = request
            self.identifier = None
            self.metadataPrefix = None
            self.From = None
            self.until = None
            self.sets = None
            self.resumptionToken = None
            #Check entry
            self.checkBadArgument(request.GET)

            #Verb treatment
            if self.oai_verb == 'Identify':
                return self.identify()
            elif self.oai_verb == 'ListIdentifiers':
                if 'sets' in request.GET: raise noSetHierarchy
                else:
                    self.From = request.GET.get('from', None)
                    self.until = request.GET.get('until', None)
                    self.sets = request.GET.get('sets', None)
                    self.resumptionToken = request.GET.get('resumptionToken', None)
                    self.metadataPrefix = request.GET.get('metadataPrefix', None)
                    return self.list_identifiers()
            elif self.oai_verb == 'ListSets':
                return self.list_sets()
            elif self.oai_verb == 'ListMetadataFormats':
                self.identifier = request.GET.get('identifier', None)
                return self.list_metadata_formats()
            elif self.oai_verb == 'GetRecord':
                self.identifier = request.GET.get('identifier', None)
                self.metadataPrefix = request.GET.get('metadataPrefix', None)
                return self.get_record()
            elif self.oai_verb == 'ListRecords':
                if 'sets' in request.GET: raise noSetHierarchy
                else:
                    self.From = request.GET.get('from', None)
                    self.until = request.GET.get('until', None)
                    self.sets = request.GET.get('sets', None)
                    self.resumptionToken = request.GET.get('resumptionToken', None)
                    self.metadataPrefix = request.GET.get('metadataPrefix', None)
                    return self.list_records()

        except OAIExceptions, e:
            return self.errors(e.errors)
        except OAIException, e:
            return self.error(e)
        except Exception, e:
            return self.error(e.code, e.message)


################################################################################
#
# Function Name: get_xsd(request)
# Inputs:        request -
# Outputs:       An XML Schema
# Exceptions:    None
# Description:   Page that allows to retrieve an XML Schema by its name
#
################################################################################
def get_xsd(request, schema):
    #TODO Available if publication ok and no user template
    #We retrieve the schema filename in the schema attribute
    #Get the templateVersion ID
    templatesVersionID = Template.objects(filename=schema).distinct(field="templateVersion")
    templateID = TemplateVersion.objects(pk__in=templatesVersionID, isDeleted=False).distinct(field="current")

    templates = Template.objects.get(pk__in=templateID)
    #Get the XML schema
    contentEncoded = templates.content.encode('utf-8')
    fileObj = StringIO(contentEncoded)
    #Return the XML
    response = HttpResponse(fileObj)
    response['Content-Type'] = 'text/xml'

    return response