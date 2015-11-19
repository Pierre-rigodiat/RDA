################################################################################
#
# File Name: views.py
# Application: explore
# Description:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.shortcuts import redirect
from django.conf import settings
from mgi.models import TemplateVersion, Instance, SavedQuery, XMLdata, ExporterXslt
import mgi.rights as RIGHTS
from cStringIO import StringIO
from django.core.servers.basehttp import FileWrapper
import zipfile
import lxml.etree as etree
import os
import xmltodict
import json
from explore.forms import *
from exporter import get_exporter
from exporter.builtin.models import XSLTExporter
from admin_mdcs.models import login_or_anonymous_perm_required

################################################################################
#
# Function Name: index(request)
# Inputs:        request - 
# Outputs:       Data Exploration homepage
# Exceptions:    None
# Description:   renders the main data exploration home page from template 
#                (index.html)
#
################################################################################

@login_or_anonymous_perm_required(anonymous_permission=RIGHTS.explore_access, login_url='/login')
def index(request):
    template = loader.get_template('explore.html')
    currentTemplateVersions = []
    for tpl_version in TemplateVersion.objects():
        currentTemplateVersions.append(tpl_version.current)

    currentTemplates = dict()
    for tpl_version in currentTemplateVersions:
        tpl = Template.objects.get(pk=tpl_version)
        templateVersions = TemplateVersion.objects.get(pk=tpl.templateVersion)
        currentTemplates[tpl] = templateVersions.isDeleted

    context = RequestContext(request, {
        'templates':currentTemplates,
        'userTemplates': Template.objects(user=str(request.user.id)),
    })
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: explore_select_template(request)
# Inputs:        request -
# Outputs:       Main Page of Explore Application
# Exceptions:    None
# Description:   Page that allows to select a template to start Exploring
#
################################################################################
@login_or_anonymous_perm_required(anonymous_permission=RIGHTS.explore_access, login_url='/login')
def explore_select_template(request):
    template = loader.get_template('explore.html')
    context = RequestContext(request, {
        '': '',
    })
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: explore_customize_template(request)
# Inputs:        request -
# Outputs:       Customize Template Page
# Exceptions:    None
# Description:   Page that allows to select fields being used during Exploration
#
################################################################################
@login_or_anonymous_perm_required(anonymous_permission=RIGHTS.explore_access, login_url='/login')
def explore_customize_template(request):
    template = loader.get_template('explore_customize_template.html')
    context = RequestContext(request, {
    })
    if 'exploreCurrentTemplateID' not in request.session:
        return redirect('/explore/select-template')
    else:
        return HttpResponse(template.render(context))

################################################################################
#
# Function Name: explore_perform_search(request)
# Inputs:        request -
# Outputs:       Perform Search Page
# Exceptions:    None
# Description:   Page that allows to submit queries
#
################################################################################
@login_or_anonymous_perm_required(anonymous_permission=RIGHTS.explore_access, login_url='/login')
def explore_perform_search(request):
    try:
        template = loader.get_template('explore_perform_search.html')
        instances = Instance.objects()
        if 'HTTPS' in request.META['SERVER_PROTOCOL']:
            protocol = "https"
        else:
            protocol = "http"
        local = Instance(name="Local", protocol=protocol, address=request.META['REMOTE_ADDR'], port=request.META['SERVER_PORT'])
        listInstances = [local]
        for instance in instances:
            listInstances.append(instance)

        template_hash = Template.objects.get(pk=request.session['exploreCurrentTemplateID']).hash

        queries = SavedQuery.objects(user=str(request.user.id), template=str(request.session['exploreCurrentTemplateID']))
        context = RequestContext(request, {
            'instances': listInstances,
            'template_hash': template_hash,
            'queries':queries,
            'template_id': request.session['exploreCurrentTemplateID']
        })
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:
            return HttpResponse(template.render(context))
    except:
        return redirect("/explore")


################################################################################
#
# Function Name: explore_results(request)
# Inputs:        request -
# Outputs:       Query results page
# Exceptions:    None
# Description:   Page that allows to see results from a query
#
################################################################################
@login_or_anonymous_perm_required(anonymous_permission=RIGHTS.explore_access, login_url='/login')
def explore_results(request):
    template = loader.get_template('explore_results.html')
    context = RequestContext(request, {
        '': '',
    })
    if 'exploreCurrentTemplateID' not in request.session:
        return redirect('/explore/select-template')
    else:
        return HttpResponse(template.render(context))

################################################################################
#
# Function Name: explore_all_results(request)
# Inputs:        request -
# Outputs:       Query results page
# Exceptions:    None
# Description:   Page that allows to see all results from a template
#
################################################################################
@login_or_anonymous_perm_required(anonymous_permission=RIGHTS.explore_access, login_url='/login')
def explore_all_results(request):
    template_id = request.GET['id']

    if 'HTTPS' in request.META['SERVER_PROTOCOL']:
        protocol = "https"
    else:
        protocol = "http"

    request.session['queryExplore'] = {"schema": template_id}
    json_instances = [Instance(name="Local", protocol=protocol, address=request.META['REMOTE_ADDR'], port=request.META['SERVER_PORT'], access_token="token", refresh_token="token").to_json()]
    request.session['instancesExplore'] = json_instances

    template = loader.get_template('explore_results.html')

    context = RequestContext(request, {
        '': '',
    })
    if 'exploreCurrentTemplateID' not in request.session:
        return redirect('/explore/select-template')
    else:
        return HttpResponse(template.render(context))

################################################################################
#
# Function Name: explore_all_versions_results(request)
# Inputs:        request -
# Outputs:       Query results page
# Exceptions:    None
# Description:   Page that allows to see all results from all versions of a template
#
################################################################################
@login_or_anonymous_perm_required(anonymous_permission=RIGHTS.explore_access, login_url='/login')
def explore_all_versions_results(request):
    template_id = request.GET['id']
    template = Template.objects().get(pk=template_id)
    version_id = template.templateVersion
    template_version = TemplateVersion.objects().get(pk=version_id)

    if len(template_version.versions) == 1:
            query = {"schema": template_id}
    else:
        list_query = []
        for version in template_version.versions:
            list_query.append({'schema': version})
        query = {"$or": list_query}

    request.session['queryExplore'] = query

    if 'HTTPS' in request.META['SERVER_PROTOCOL']:
        protocol = "https"
    else:
        protocol = "http"
    json_instances = [Instance(name="Local", protocol=protocol, address=request.META['REMOTE_ADDR'], port=request.META['SERVER_PORT'], access_token="token", refresh_token="token").to_json()]
    request.session['instancesExplore'] = json_instances

    template = loader.get_template('explore_results.html')

    context = RequestContext(request, {
        '': '',
    })
    if 'exploreCurrentTemplateID' not in request.session:
        return redirect('/explore/select-template')
    else:
        return HttpResponse(template.render(context))

################################################################################
#
# Function Name: explore_detail_result
# Inputs:        request -
# Outputs:       Detail of result
# Exceptions:    None
# Description:   Page that allows to see all selected detail result from a template
#
################################################################################
@login_or_anonymous_perm_required(anonymous_permission=RIGHTS.explore_access, login_url='/login')
def explore_detail_result(request) :
    result_id = request.GET['id']

    template = loader.get_template('explore_detail_results.html')

    xmlString = XMLdata.get(result_id)
    xmlString = xmltodict.unparse(xmlString['content'])

    xsltPath = os.path.join(settings.SITE_ROOT, 'static', 'resources', 'xsl', 'xml2html.xsl')
    xslt = etree.parse(xsltPath)
    transform = etree.XSLT(xslt)
    xmlTree = ""
    if (xmlString != ""):
   	dom = etree.fromstring(str(xmlString))
        newdom = transform(dom)
        xmlTree = str(newdom)

    response_dict = {"XMLHolder": xmlTree}

    context = RequestContext(request, {
        'XMLHolder': xmlTree
    })

    if 'exploreCurrentTemplateID' not in request.session:
        return redirect('/explore/select-template')
    else:
        return HttpResponse(template.render(context))

################################################################################
#
# Function Name: start_export
# Inputs:        request - All ids
# Outputs:       Detail of results
# Exceptions:    None
# Description:   Page that allows to see all selected detail results from a template
#
################################################################################
@login_or_anonymous_perm_required(anonymous_permission=RIGHTS.explore_access, login_url='/login')
def start_export(request):
    if request.method == 'POST':
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:
            #We retrieve all selected exporters
            listExporter = request.POST.getlist('my_exporters')
            instances = request.session['instancesExplore']
            listId = request.session['listIdToExport']
            xmlResults = []
            #Creation of ZIP file
            in_memory = StringIO()
            zip = zipfile.ZipFile(in_memory, "a")
            is_many_inst = len(instances) > 1
            for instance in instances:
                #Retrieve data
                sessionName = "resultsExplore" + eval(instance)['name']
                results = request.session[sessionName]
                if (len(results) > 0):
                    for result in results:
                        if result['id'] in listId:
                            xmlResults.append(result)

                #For each data, we convert
                if len(xmlResults) > 0:
                    #Init the folder name
                    folder_name = None
                    if is_many_inst:
                        folder_name = eval(instance)['name']
                    #Check if the XSLT converter is asked. If yes, we start with this one because there is a specific treatment
                    listXslt = request.POST.getlist('my_xslts')
                    #Get the content of the file
                    if len(listXslt) > 0:
                        exporter = XSLTExporter()
                        for xslt in listXslt:
                            xslt = ExporterXslt.objects.get(pk=xslt)
                            exporter._setXslt(xslt.content)
                            if folder_name == None:
                                exporter._transformAndZip(xslt.name, xmlResults, zip)
                            else:
                                exporter._transformAndZip(folder_name+"/"+xslt.name, xmlResults, zip)

                    #We export for others exporters
                    for exporter in listExporter:
                        exporter = get_exporter(exporter)
                        exporter._transformAndZip(folder_name, xmlResults, zip)

            zip.close()

            #ZIP file to be downloaded
            in_memory.seek(0)
            response = HttpResponse(in_memory.read())
            response["Content-Disposition"] = "attachment; filename=Results.zip"
            response['Content-Type'] = 'application/x-zip'
            request.session['listIdToExport'] = ''

            return response
    else:
        # We retrieve the result_id for each file the user wants to export
        listId = request.GET.getlist('listId[]')
        request.session['listIdToExport'] = listId
        export_form = ExportForm(request.session['exploreCurrentTemplateID'])
        upload_xslt_Form = UploadXSLTForm(request.session['exploreCurrentTemplateID'])
        template = loader.get_template('export_start.html')
        context = Context({'export_form':export_form, 'upload_xslt_Form':upload_xslt_Form, 'nb_elts_exp': len(export_form.EXPORT_OPTIONS), 'nb_elts_xslt' : len(upload_xslt_Form.EXPORT_OPTIONS)})

        return HttpResponse(json.dumps({'template': template.render(context)}), content_type='application/javascript')
