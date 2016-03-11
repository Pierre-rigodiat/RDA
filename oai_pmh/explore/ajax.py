################################################################################
#
# File Name: ajax.py
# Application: explore
# Purpose:   AJAX methods used for Explore purposes
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume Sousa Amaral
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

import re
from django.http import HttpResponse
from django.conf import settings
from io import BytesIO
import xmltodict
import os
import json
import lxml.etree as etree
from mgi.models import Template, Instance, TemplateVersion, OaiRecord, OaiMetadataFormat, OaiRegistry
from django.template import loader, Context, RequestContext


################################################################################
#
# Function Name: getResults(query)
# Inputs:        query -
# Outputs:       JSON data
# Exceptions:    None
# Description:   Transform the query to get rid of Regex object
#
################################################################################
def manageRegexBeforeExe(query):
    for key, value in query.iteritems():
        if key == "$and" or key == "$or":
            for subValue in value:
                manageRegexBeforeExe(subValue)
        elif isinstance(value, unicode):
            if (len(value) >= 2 and value[0] == "/" and value[-1] == "/"):
                query[key] = re.compile(value[1:-1])
        elif isinstance(value, dict):
            manageRegexBeforeExe(value)

################################################################################
#
# Function Name: get_results_by_instance_keyword(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Get results of a query for a specific keyword
#
################################################################################
def get_results_by_instance_keyword(request):
    print 'BEGIN def getResultsKeyword(request)'
    resultsByKeyword = []
    results = []
    resultString = ""

    #Instance
    json_instances = []
    if 'HTTPS' in request.META['SERVER_PROTOCOL']:
        protocol = "https"
    else:
        protocol = "http"
    instance = Instance(name="Local", protocol=protocol, address=request.META['REMOTE_ADDR'], port=request.META['SERVER_PORT'], access_token="token", refresh_token="token")
    json_instances.append(instance.to_json())
    request.session['instancesExplore'] = json_instances
    sessionName = "resultsExplore" + instance['name']


    try:
        keyword = request.GET['keyword']
        schemas = request.GET.getlist('schemas[]')
        onlySuggestions = json.loads(request.GET['onlySuggestions'])
    except:
        keyword = ''
        schemas = []
        onlySuggestions = True


    instanceResults = OaiRecord.executeFullTextQuery(keyword, schemas)
    if len(instanceResults) > 0:
        if not onlySuggestions:
            xsltPath = os.path.join(settings.SITE_ROOT, 'static/resources/xsl/xml2html.xsl')
            xslt = etree.parse(xsltPath)
            transform = etree.XSLT(xslt)
            template = loader.get_template('oai_pmh/explore/explore_result_keyword.html')

        #Retrieve schema and registries. Avoid to retrieve the information for each result
        registriesName = {}
        schemasName = {}
        listRegistriesID = set([x['registry'] for x in instanceResults])
        for registryId in listRegistriesID:
            obj = OaiRegistry.objects(pk=registryId).get()
            registriesName[str(registryId)] = obj.name
        listSchemaId = set([x['metadataformat'] for x in instanceResults])
        for schemaId in listSchemaId:
            obj = OaiMetadataFormat.objects(pk=schemaId).get()
            schemasName[str(schemaId)] = obj

        for instanceResult in instanceResults:
            if not onlySuggestions:
                custom_xslt = False
                results.append({'title':instanceResult['identifier'], 'content':xmltodict.unparse(instanceResult['metadata']),'id':str(instanceResult['_id'])})
                dom = etree.XML(str(xmltodict.unparse(instanceResult['metadata']).encode('utf-8')))
                #Check if a custom list result XSLT has to be used
                try:
                    schema = schemasName[str(instanceResult['metadataformat'])]
                    if schema.ResultXsltList:
                        listXslt = etree.parse(BytesIO(schema.ResultXsltList.content.encode('utf-8')))
                        listTransform = etree.XSLT(listXslt)
                        newdom = listTransform(dom)
                        custom_xslt = True
                    else:
                        newdom = transform(dom)
                except Exception, e:
                    #We use the default one
                    newdom = transform(dom)
                    custom_xslt = False

                context = RequestContext(request, {'id':str(instanceResult['_id']),
                                   'xml': str(newdom),
                                   'title': instanceResult['identifier'],
                                   'custom_xslt': custom_xslt,
                                   'schema_name': schema.metadataPrefix,
                                   'registry_name': registriesName[instanceResult['registry']]})

                resultString+= template.render(context)
            else:
                wordList = re.sub("[^\w]", " ",  keyword).split()
                wordList = [x + "|" + x +"\w+" for x in wordList]
                wordList = '|'.join(wordList)
                listWholeKeywords = re.findall("\\b("+ wordList +")\\b", xmltodict.unparse(instanceResult['metadata']).encode('utf-8'), flags=re.IGNORECASE)
                labels = list(set(listWholeKeywords))

                for label in labels:
                    label = label.lower()
                    result_json = {}
                    result_json['label'] = label
                    result_json['value'] = label
                    if not result_json in resultsByKeyword:
                        resultsByKeyword.append(result_json)

        result_json = {}
        result_json['resultString'] = resultString

    request.session[sessionName] = results
    print 'END def getResultsKeyword(request)'

    return HttpResponse(json.dumps({'resultsByKeyword' : resultsByKeyword, 'resultString' : resultString, 'count' : len(instanceResults)}), content_type='application/javascript')
