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
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.conf import settings
from datetime import date
from mgi.models import Template, TemplateVersion, Instance, SavedQuery, QueryResults, XMLdata
from cStringIO import StringIO
from django.core.servers.basehttp import FileWrapper
import zipfile


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
def index(request):
    template = loader.get_template('explore.html')
    if request.user.is_authenticated():
    
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
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')


################################################################################
#
# Function Name: explore_select_template(request)
# Inputs:        request -
# Outputs:       Main Page of Explore Application
# Exceptions:    None
# Description:   Page that allows to select a template to start Exploring
#
################################################################################
def explore_select_template(request):
    if request.user.is_authenticated():
        template = loader.get_template('explore.html')
        context = RequestContext(request, {
            '': '',
        })
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/select-template'
        return redirect('/login')


################################################################################
#
# Function Name: explore_customize_template(request)
# Inputs:        request -
# Outputs:       Customize Template Page
# Exceptions:    None
# Description:   Page that allows to select fields being used during Exploration
#
################################################################################
def explore_customize_template(request):
    if request.user.is_authenticated():
        template = loader.get_template('explore_customize_template.html')
        context = RequestContext(request, {
        })    
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore/customize-template'
        return redirect('/login')


################################################################################
#
# Function Name: explore_perform_search(request)
# Inputs:        request -
# Outputs:       Perform Search Page
# Exceptions:    None
# Description:   Page that allows to submit queries
#
################################################################################
def explore_perform_search(request):
    try:
        if request.user.is_authenticated():
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
        else:
            if 'loggedOut' in request.session:
                del request.session['loggedOut']
            request.session['next'] = '/explore/perform-search'
            return redirect('/login')
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
def explore_results(request):
    if request.user.is_authenticated():
        template = loader.get_template('explore_results.html')
        context = RequestContext(request, {
            '': '',
        })
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore/results'
        return redirect('/login')


################################################################################
#
# Function Name: explore_all_results(request)
# Inputs:        request -
# Outputs:       Query results page
# Exceptions:    None
# Description:   Page that allows to see all results from a template
#
################################################################################
def explore_all_results(request):
    if request.user.is_authenticated():
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
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore/results'
        return redirect('/login')
    
################################################################################
#
# Function Name: explore_all_versions_results(request)
# Inputs:        request -
# Outputs:       Query results page
# Exceptions:    None
# Description:   Page that allows to see all results from all versions of a template
#
################################################################################
def explore_all_versions_results(request):
    if request.user.is_authenticated():
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
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore/results'
        return redirect('/login')


################################################################################
#
# Function Name: explore_download_results(request)
# Inputs:        request -
# Outputs:       results of a query as xml files
# Exceptions:    None
# Description:   Download XML results in a ZIP file
#
################################################################################
def explore_download_results(request):
    if request.user.is_authenticated():
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:
            savedResultsID = request.GET.get('id', None)
            
            if savedResultsID is not None:
                ResultsObject = QueryResults.objects.get(pk=savedResultsID)
    
                in_memory = StringIO()
                zip = zipfile.ZipFile(in_memory, "a")
    
                for result in ResultsObject.results:
                    zip.writestr(result['title'], result['content'])
    
                # fix for Linux zip files read in Windows
                for xmlFile in zip.filelist:
                    xmlFile.create_system = 0
    
                zip.close()
    
                ResultsObject.delete()
    
                response = HttpResponse(content_type="application/zip")
                response["Content-Disposition"] = "attachment; filename=results.zip"
    
                in_memory.seek(0)
                response.write(in_memory.read())
    
                return response
            else:
                return redirect('/')
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')
