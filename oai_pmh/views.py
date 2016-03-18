################################################################################
#
# File Name: views.py
# Application: Informatics Core
# Description:
#
# Author: Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

# Responses
from django.core.servers.basehttp import FileWrapper
from rest_framework import status
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect
# Requests
import requests
from oai_pmh.forms import RequestForm
import json
from mgi.settings import OAI_HOST_URI, OAI_USER, OAI_PASS
from django.template import RequestContext, loader
from mgi.models import XML2Download
import datetime
from mgi.models import OaiSet, OaiMetadataFormat
from django.contrib.auth.decorators import login_required
from django.conf import settings
import lxml.etree as etree
import os
from StringIO import StringIO

################################################################################
#
# Function Name: oai_pmh_downloadxml(request)
# Inputs:        request -
# Outputs:       XML representation of the current build request
# Exceptions:    None
# Description:   Returns an XML representation of the current build request.
#                Used when user wants to download the XML file.
#
################################################################################
@login_required(login_url='/login')
def download_xml_build_req(request):
    if request.method == 'POST':
        if 'xmlStringOAIPMH' in request.session:
            xmlDataObject = request.session['xmlStringOAIPMH']
            try:
                # Load a parser able to clean the XML from blanks, comments and processing instructions
                clean_parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, remove_pis=True)
                # set the parser
                etree.set_default_parser(parser=clean_parser)
                # load the XML tree from the text
                xmlDoc = etree.XML(str(xmlDataObject.encode('utf-8')))
                xmlStringEncoded = etree.tostring(xmlDoc, pretty_print=True)
            except:
                xmlStringEncoded = xmlDataObject

            i = datetime.datetime.now()
            title = "OAI_PMH_BUILD_REQ_%s_.xml" % i.isoformat()
            xml2download = XML2Download(title=title, xml=xmlStringEncoded).save()
            xml2downloadID = str(xml2download.id)

            response_dict = {"xml2downloadID": xml2downloadID}
            return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
        else:
            return HttpResponseBadRequest('An error occured. Please reload the page and try again.')
    else:
        xml2downloadID = request.GET.get('id', None)

        if xml2downloadID is not None:
            xmlDataObject = XML2Download.objects.get(pk=xml2downloadID)
            xmlStringEncoded = xmlDataObject.xml.encode('utf-8')
            fileObj = StringIO(xmlStringEncoded)
            xmlDataObject.delete()
            if not xmlDataObject.title.lower().endswith('.xml'):
                xmlDataObject.title += ".xml"

            response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=' + xmlDataObject.title
            request.session['xmlStringOAIPMH'] = xmlStringEncoded

            return response
        else:
            return redirect('/')


################################################################################
#
# Function Name: all_sets(request)
# Inputs:        request -
# Outputs:       List of set's name
# Exceptions:    None
# Description:   Returns all the sets of a registry.
#
################################################################################
@login_required(login_url='/login')
def all_sets(request, registry):
    sets = []
    registrySets = OaiSet.objects(registry=registry).order_by("setName")
    for set in registrySets:
        sets.append(set.setName)
    return HttpResponse(json.dumps(sets), content_type="application/javascript")

################################################################################
#
# Function Name: all_metadataprefix(request)
# Inputs:        request -
# Outputs:       List of metadataprefix's name
# Exceptions:    None
# Description:   Returns all the sets of a registry.
#
################################################################################
@login_required(login_url='/login')
def all_metadataprefix(request, registry):
    prefix = []
    metadataformats = OaiMetadataFormat.objects(registry=registry).order_by("metadataPrefix")
    for format in metadataformats:
        prefix.append(format.metadataPrefix)
    return HttpResponse(json.dumps(prefix), content_type="application/javascript")

################################################################################
#
# Function Name: getData(request)
# Inputs:        request -
# Outputs:       XML representation of the build request response
# Exceptions:    None
# Description:   Returns OAI PMH response
#
################################################################################
@login_required(login_url='/login')
def getData(request):
    url = request.POST['url']

    uri= OAI_HOST_URI + "/oai_pmh/api/getdata/"
    req = requests.post(uri, {"url":url}, auth=(OAI_USER, OAI_PASS))

    if (req.status_code == status.HTTP_200_OK):
        data = json.load(StringIO(req.content))

        xsltPath = os.path.join(settings.SITE_ROOT, 'static', 'resources', 'xsl', 'xml2html.xsl')
        xslt = etree.parse(xsltPath)
        transform = etree.XSLT(xslt)

        XMLParser = etree.XMLParser(remove_blank_text=True, recover=True)
        dom = etree.XML(str(data.encode("utf8")),  parser=XMLParser)
        request.session['xmlStringOAIPMH'] = str(data.encode("utf8"))
        newdom = transform(dom)
        xmlTree = str(newdom)

        content = {'message' : xmlTree}
        return HttpResponse(json.dumps(content), content_type="application/javascript")
    else:
        return HttpResponseBadRequest(req.content, content_type="application/javascript")


################################################################################
#
# Function Name: oai_pmh_build_request(request)
# Inputs:        request -
# Outputs:       OAI-PMH Page
# Exceptions:    None
# Description:   Page that allows to manage OAI-PMH
#
################################################################################
@login_required(login_url='/login')
def oai_pmh_build_request(request):
    template = loader.get_template('oai_pmh/oai_pmh_build_request.html')
    requestForm = RequestForm();
    context = RequestContext(request, {'request_form': requestForm})
    return HttpResponse(template.render(context))
