################################################################################
#
# File Name: views.py
# Application: mgi
# Description: Django views used to render pages for the system.
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

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from datetime import date
from mongoengine import *
from operator import itemgetter
from cStringIO import StringIO
import sys
from xlrd import open_workbook
from argparse import ArgumentError
from cgi import FieldStorage
import zipfile
from mgi.models import Template, Database, Htmlform, Xmldata, Hdf5file, QueryResults, SparqlQueryResults, ContactForm, XML2Download, TemplateVersion, Instance, XMLSchema, Request, Module, Type, TypeVersion, SavedQuery
from bson.objectid import ObjectId
import lxml.etree as etree
import os

# Create your views here.

################################################################################
#
# Function Name: currentYear(request)
# Inputs:        request - 
# Outputs:       Current Year
# Exceptions:    None
# Description:   Helper function - returns the current year
#
################################################################################
def currentYear():
    return date.today().year

################################################################################
#
# Function Name: home(request)
# Inputs:        request - 
# Outputs:       Materials Data Curation System homepage
# Exceptions:    None
# Description:   renders the main home page from template (index.html)
#
################################################################################
def home(request):
    template = loader.get_template('index.html')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: admin(request)
# Inputs:        request - 
# Outputs:       Administrative Dashboard page
# Exceptions:    None
# Description:   renders the admin page from template (admin/index.html)
#
################################################################################
def admin(request):
    template = loader.get_template('admin/index.html')

    context = RequestContext(request, {
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def user_requests(request):
    template = loader.get_template('admin/user_requests.html')

    context = RequestContext(request, {
        'requests': Request.objects
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def backup_database(request):
    template = loader.get_template('admin/backup-database.html')
    backupsDir = settings.SITE_ROOT + '/data/backups/'
        
    context = RequestContext(request, {
        'backups' : os.listdir(backupsDir)
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def restore_database(request):
    template = loader.get_template('admin/restore-database.html')

    backupsDir = settings.SITE_ROOT + '/data/backups/'
        
    context = RequestContext(request, {
        'backups' : os.listdir(backupsDir)
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: xml_schemas(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def xml_schemas(request):
    template = loader.get_template('admin/xml_schemas.html')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: manage_schemas(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def manage_schemas(request):
#     template = loader.get_template('admin/manage_schemas.html')
    template = loader.get_template('admin/manage_uploads.html')
    
    currentTemplateVersions = []
    for tpl_version in TemplateVersion.objects():
        currentTemplateVersions.append(tpl_version.current)
    
    currentTemplates = dict()
    for tpl_version in currentTemplateVersions:
        tpl = Template.objects.get(pk=tpl_version)
        templateVersions = TemplateVersion.objects.get(pk=tpl.templateVersion)
        currentTemplates[tpl] = templateVersions.isDeleted

    context = RequestContext(request, {
        'objects':currentTemplates,
        'objectType': "Template"
#        'templates': Template.objects.all()
#         'templates': Template.objects.order_by('-id')
        
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: manage_modules(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def module_management(request):
    template = loader.get_template('admin/manage_modules.html')

    context = RequestContext(request, {
        'modules': Module.objects
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

def module_add(request):
    template = loader.get_template('admin/add_module.html')

    context = RequestContext(request, {
        
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: manage_queries(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def manage_queries(request):
    template = loader.get_template('admin/manage_queries.html')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('-id')[:7]
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: manage_types(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def manage_types(request):
    template = loader.get_template('admin/manage_uploads.html')
    
    currentTypeVersions = []
    for type_version in TypeVersion.objects():
        currentTypeVersions.append(type_version.current)
    
    currentTypes = dict()
    for type_version in currentTypeVersions:
        type = Type.objects.get(pk=type_version)
        typeVersions = TypeVersion.objects.get(pk=type.typeVersion)
        currentTypes[type] = typeVersions.isDeleted

    context = RequestContext(request, {
        'objects':currentTypes,
        'objectType': "Type"
        
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: user_management(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def user_management(request):
    template = loader.get_template('admin/user_management.html')

    context = RequestContext(request, {
        
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: database_management(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def database_management(request):
    template = loader.get_template('admin/database_management.html')

    context = RequestContext(request, {
        'databases': Database.objects.order_by('-id')[:7]
    })

    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: federation_of_queries(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def federation_of_queries(request):
    template = loader.get_template('admin/federation_of_queries.html')

    context = RequestContext(request, {
        'instances': Instance.objects.order_by('-id')
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: curate(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate(request):
#    logout(request)
    template = loader.get_template('curate.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: curate_select_template(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate_select_template(request):
#    logout(request)
    template = loader.get_template('curate.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/select-template'
        return redirect('/login')


################################################################################
#
# Function Name: curate_select_hdf5file(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate_select_hdf5file(request):
#    logout(request)
    template = loader.get_template('curate_select_hdf5file.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/select-template'
        return redirect('/login')

from xlrd import open_workbook
################################################################################
#
# Function Name: curate_upload_hdf5file(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate_upload_spreadsheet(request):
    template = loader.get_template('curate_upload_successful.html')
    
    context = RequestContext(request, {
        '': '',
    })
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            if request.method == 'POST':
                try:
                    print request.FILES
                    input_excel = request.FILES['excelSpreadsheet']
                    print input_excel
                    book = open_workbook(file_contents=input_excel.read())
                    
                    root = etree.Element("excel")
                    root.set("name", str(input_excel))
                    header = etree.SubElement(root, "headers")
                    values = etree.SubElement(root, "rows")
                    
                    for sheet in book.sheets():
                        for rowIndex in range(sheet.nrows):
                    
                            if rowIndex != 0:
                                row = etree.SubElement(values, "row")
                                row.set("id", str(rowIndex))
                    
                            for colIndex in range(sheet.ncols):
                                if rowIndex == 0:
                                    col = etree.SubElement(header, "column")
                                else:
                                    col = etree.SubElement(row, "column")
                    
                                col.set("id", str(colIndex))
                                col.text = str(sheet.cell(rowIndex, colIndex).value)
                    
    
                    xmlString = etree.tostring(root)                    
                    
                    request.session['spreadsheetXML'] = xmlString                    
                    
#                     templateID = request.session['currentTemplateID']
#                     existingHDF5files = Hdf5file.objects(schema=templateID)
#                     if existingHDF5files is not None:
#                         for hdf5file in existingHDF5files:
#                             hdf5file.delete()
#                         newHDF5File = Hdf5file(title="hdf5file", schema=templateID, content=hdf5String).save()
#                     else:
#                         newHDF5File = Hdf5file(title="hdf5file", schema=templateID, content=hdf5String).save()
                except:
                    templateError = loader.get_template('curate_upload_failed.html')
                    return HttpResponse(templateError.render(context))

            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/enter-data'
        return redirect('/login')


################################################################################
#
# Function Name: curate_enter_data(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate_enter_data(request):
    print "BEGIN curate_enter_data(request)"
#    logout(request)
    template = loader.get_template('curate_enter_data.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
#    return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/enter-data'
        return redirect('/login')

################################################################################
#
# Function Name: curate_view_data(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def curate_view_data(request):
#    logout(request)
    template = loader.get_template('curate_view_data.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/view-data'
        return redirect('/login')

################################################################################
#
# Function Name: curate_view_data_downloadxsd(request)
# Inputs:        request - 
# Outputs:       XSD representation of the current form instance
# Exceptions:    None
# Description:   Returns an XSD representation of the current form instance.
#                Used when user wants to download the form / xml schema.
#
################################################################################
def curate_enter_data_downloadxsd(request):
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            templateFilename = request.session['currentTemplate']
            templateID = request.session['currentTemplateID']

            
            templateObject = Template.objects.get(pk=ObjectId(templateID))
                
            print templateObject
            xsdDocData = templateObject.content

            xsdEncoded = xsdDocData.encode('utf-8')
            fileObj = StringIO(xsdEncoded)

            response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=' + templateFilename
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: curate_view_data_downloadxml(request)
# Inputs:        request - 
# Outputs:       XML representation of the current data instance
# Exceptions:    None
# Description:   Returns an XML representation of the current data instance.
#                Used when user wants to download the XML file.
#
################################################################################
def curate_enter_data_downloadform(request):
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            global formString
            
            htmlFormObject = Htmlform.objects.get(title="form2download")

            formStringEncoded = htmlFormObject.content.encode('utf-8') #"abac" #formString.encode('utf-8')
            fileObj = StringIO(formStringEncoded)

            htmlFormObject.delete()

            response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=' + "form.xml" #templateFilename
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: curate_view_data_downloadxml(request)
# Inputs:        request - 
# Outputs:       XML representation of the current data instance
# Exceptions:    None
# Description:   Returns an XML representation of the current data instance.
#                Used when user wants to download the XML file.
#
################################################################################
def curate_view_data_downloadxml(request):
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            xml2downloadID = request.GET.get('id','')
            xmlDataObject = XML2Download.objects.get(pk=xml2downloadID)
            

            xmlStringEncoded = xmlDataObject.xml.encode('utf-8') 
            fileObj = StringIO(xmlStringEncoded)

            xmlDataObject.delete()

            response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
            response['Content-Disposition'] = 'attachment; filename=' + "data.xml" #templateFilename
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: view_schema(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def view_schema(request):
#    logout(request)
    template = loader.get_template('view_schema.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate/view-data'
        return redirect('/login')

################################################################################
#
# Function Name: explore(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore(request):
#    logout(request)
    template = loader.get_template('explore.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')
#        user = authenticate(username='materials', password='data123')
#        if user is not None:
            # the password verified for the user
#            if user.is_active:
#                return HttpResponse(template.render(context))
#                return HttpResponse("HomePage: User is valid, active and authenticated")
#            else:
#                return HttpResponse("HomePage: The password is valid, but the account has been disabled!")
#        else:
            # the authentication system was unable to verify the username and password
#            return HttpResponse("HomePage: The username and password were incorrect.")

################################################################################
#
# Function Name: explore_select_template(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore_select_template(request):
#    logout(request)
    template = loader.get_template('explore.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
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
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore_customize_template(request):
#    logout(request)
    template = loader.get_template('explore_customize_template.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
#     return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
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
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore_perform_search(request):
#    logout(request)
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
        })
        request.session['currentYear'] = currentYear()
        #return HttpResponse(template.render(context))  # remove after testing
        if request.user.is_authenticated():
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
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore_results(request):
#    logout(request)
    template = loader.get_template('explore_results.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
#     return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
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
# Function Name: explore_sparqlresults(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def explore_sparqlresults(request):
#    logout(request)
    template = loader.get_template('explore_sparqlresults.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
#     return HttpResponse(template.render(context))  # remove after testing
    if request.user.is_authenticated():
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:
            return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore/sparqlresults'
        return redirect('/login')

################################################################################
#
# Function Name: explore_download_results(request)
# Inputs:        request - 
# Outputs:       results of a query as xml files
# Exceptions:    None
# Description:   
#
################################################################################
def explore_download_results(request):
    if request.user.is_authenticated():
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:          
            savedResultsID = request.GET.get('id','')
            ResultsObject = QueryResults.objects.get(pk=savedResultsID)

#             fileObj = StringIO(formStringEncoded)
            in_memory = StringIO()
            zip = zipfile.ZipFile(in_memory, "a")
            
            resultNumber = 1
            for result in ResultsObject.results:
                zip.writestr("result"+str(resultNumber)+".xml", result)
                resultNumber += 1
                
            # fix for Linux zip files read in Windows  
            for xmlFile in zip.filelist:  
                xmlFile.create_system = 0 
            
            zip.close()
            
            ResultsObject.delete()

            response = HttpResponse(mimetype="application/zip")  
            response["Content-Disposition"] = "attachment; filename=results.zip"  
              
            in_memory.seek(0)      
            response.write(in_memory.read())  
              
            return response

#             response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
#             response['Content-Disposition'] = 'attachment; filename=results.zip' #templateFilename
#             return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')


################################################################################
#
# Function Name: explore_download_sparqlresults(request)
# Inputs:        request - 
# Outputs:       results of a sparql query
# Exceptions:    None
# Description:   
#
################################################################################
def explore_download_sparqlresults(request):
    if request.user.is_authenticated():
        if 'exploreCurrentTemplateID' not in request.session:
            return redirect('/explore/select-template')
        else:          
            savedResultsID = request.GET.get('id','')
            sparqlResults = SparqlQueryResults.objects.get(pk=savedResultsID)

            sparqlResultsEncoded = sparqlResults.results.encode('utf-8')
            fileObj = StringIO(sparqlResultsEncoded)

            response = HttpResponse(FileWrapper(fileObj), content_type='application/text')
            response['Content-Disposition'] = 'attachment; filename=sparql_results.txt'
            return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/explore'
        return redirect('/login')

################################################################################
#
# Function Name: compose(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def compose(request):
#    logout(request)
    template = loader.get_template('compose.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose'
        return redirect('/login')

################################################################################
#
# Function Name: compose_select_template(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def compose_select_template(request):
#    logout(request)
    template = loader.get_template('compose.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose/select-template'
        return redirect('/login')

################################################################################
#
# Function Name: compose_build_template(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def compose_build_template(request):
#    logout(request)
    template = loader.get_template('compose_build_template.html')
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        
        currentTypeVersions = []
        for type_version in TypeVersion.objects():
            currentTypeVersions.append(type_version.current)
        
        currentTypes = dict()
        for type_version in currentTypeVersions:
            type = Type.objects.get(pk=type_version)
            typeVersions = TypeVersion.objects.get(pk=type.typeVersion)
            currentTypes[type] = typeVersions.isDeleted
        
        for user_type in Type.objects(user=request.user.id):
            currentTypes[user_type] = False
    
        context = RequestContext(request, {
           'types':currentTypes
        })
        
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose/build-template'
        return redirect('/login')

################################################################################
#
# Function Name: compose_view_template(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def compose_view_template(request):
#    logout(request)
    template = loader.get_template('compose_view_template.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose/view-template'
        return redirect('/login')

################################################################################
#
# Function Name: contribute(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def contribute(request):
    template = loader.get_template('contribute.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')

################################################################################
#
# Function Name: all_options(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def all_options(request):
    template = loader.get_template('all-options.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: browse_all(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def browse_all(request):
    template = loader.get_template('browse-all.html')

    context = RequestContext(request, {
        'templates': Template.objects.order_by('title')
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: login_view(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def login_view(request):
#    del request.session['loggedOut']

    template = loader.get_template('login.html')
    context = RequestContext(request, {
        'next': 'http://www.google.com',
    })
    request.session['currentYear'] = currentYear()
    request.session['next'] = 'http://www.google.com'
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: request_new_account(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def request_new_account(request):
#    logout(request)
    template = loader.get_template('request_new_account.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: logout_view(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def logout_view(request):
    logout(request)
    if 'loggedOut' in request.session:
        request.session['loggedOut'] = 'true'
    request.session['next'] = '/'
    request.session['currentYear'] = currentYear()
    return redirect('/login')
#    template = loader.get_template('login.html')
#    context = RequestContext(request, {
#        '': '',
#    })
#    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: my_profile(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def my_profile(request):
    template = loader.get_template('my_profile.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/my-profile'
        return redirect('/login')

################################################################################
#
# Function Name: my_profile_edit(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def my_profile_edit(request):
    template = loader.get_template('my_profile_edit.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/my-profile'
        return redirect('/login')

################################################################################
#
# Function Name: my_profile_change_password(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def my_profile_change_password(request):
    template = loader.get_template('my_profile_change_password.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():
        return HttpResponse(template.render(context))
#        return HttpResponse("HomePage: User is authenticated")
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/my-profile'
        return redirect('/login')

################################################################################
#
# Function Name: contact(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def contact(request):
    if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = ContactForm() # An unbound form

    return render(request, 'contact.html', {
        'form': form,
    })
#    template = loader.get_template('contact.html')
#    context = RequestContext(request, {
#        '': '',
#    })
#    request.session['currentYear'] = currentYear()
#    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: about(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def about(request):
    template = loader.get_template('about.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: privacy_policy(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def privacy_policy(request):
    template = loader.get_template('privacy-policy.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: terms_of_use(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def terms_of_use(request):
    template = loader.get_template('terms-of-use.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

################################################################################
#
# Function Name: help(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def help(request):
    template = loader.get_template('help.html')
    context = RequestContext(request, {
        '': '',
    })
    request.session['currentYear'] = currentYear()
    return HttpResponse(template.render(context))

#    if request.user.is_authenticated():
#        return HttpResponse("HomePage: User is authenticated")
#    else:
#        user = authenticate(username='materials', password='data123')
#        if user is not None:
#            # the password verified for the user
#            if user.is_active:
#                return HttpResponse("HomePage: User is valid, active and authenticated")
#            else:
#                return HttpResponse("HomePage: The password is valid, but the account has been disabled!")
#        else:
#            # the authentication system was unable to verify the username and password
#            return HttpResponse("HomePage: The username and password were incorrect.")

################################################################################
#
# Function Name: compose_downloadxsd(request)
# Inputs:        request - 
# Outputs:       XSD representation of the current data instance
# Exceptions:    None
# Description:   Returns an XSD representation of the current data instance.
#                Used when user wants to download the XML file.
#
################################################################################
def compose_downloadxsd(request):
    if request.user.is_authenticated():                  
        xml2downloadID = request.GET.get('id','')
        xmlDataObject = XML2Download.objects.get(pk=xml2downloadID)
        

        xmlStringEncoded = xmlDataObject.xml.encode('utf-8') 
        fileObj = StringIO(xmlStringEncoded)

        xmlDataObject.delete()

        response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
        response['Content-Disposition'] = 'attachment; filename=' + "new_template.xsd"
        return response
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose'
        return redirect('/login')

