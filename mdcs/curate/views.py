################################################################################
#
# File Name: views.py
# Application: curate
# Purpose:   
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


from datetime import date
from cStringIO import StringIO

from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.shortcuts import redirect, render
from django.core.servers.basehttp import FileWrapper
from bson.objectid import ObjectId
import lxml.etree as etree
from lxml.etree import XMLSyntaxError
from xlrd import open_workbook
from django.contrib import messages
import json 

from mgi.models import Template, TemplateVersion, XML2Download, FormData
from curate.forms import NewForm, OpenForm, UploadForm, AdvancedOptionsForm
from django.http.response import HttpResponseRedirect, HttpResponseBadRequest


################################################################################
#
# Function Name: index(request)
# Inputs:        request - 
# Outputs:       Main Page of Curate Application
# Exceptions:    None
# Description:   Page that allows to select a template to start curating         
#
################################################################################
def index(request):
    template = loader.get_template('curate.html')
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
        request.session['next'] = '/curate'
        return redirect('/login')


################################################################################
#
# Function Name: curate_select_template(request)
# Inputs:        request -
# Outputs:       Main Page of Curate Application
# Exceptions:    None
# Description:   Page that allows to select a template to start curating data
#
#
################################################################################
def curate_select_template(request):
    if request.user.is_authenticated():
        template = loader.get_template('curate.html')
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
# Function Name: curate_select_hdf5file(request)
# Inputs:        request -
# Outputs:       Select Spreadsheet page
# Exceptions:    None
# Description:   Page that allows to select an Excel Spreadsheet
#
#
################################################################################
def curate_select_hdf5file(request):
    if request.user.is_authenticated():
        template = loader.get_template('curate_select_hdf5file.html')
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
# Function Name: curate_upload_hdf5file(request)
# Inputs:        request -
# Outputs:       Result of the upload
# Exceptions:    None
# Description:   Transforms the spreadsheet into XML and displays a success or error message
#
################################################################################
def curate_upload_spreadsheet(request):
    if request.user.is_authenticated():
        template = loader.get_template('curate_upload_successful.html')

        context = RequestContext(request, {
            '': '',
        })
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            if request.method == 'POST':
                try:
                    print request.FILES
                    input_excel = request.FILES['excelSpreadsheet']
                    print input_excel
                    book = open_workbook(file_contents=input_excel.read())

                    root = etree.Element("table")
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

#                     xmlString = etree.tostring(root)
                    xmlString = etree.tostring(header)
                    xmlString += etree.tostring(values)

                    request.session['spreadsheetXML'] = xmlString
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
# Outputs:       Enter Data Page
# Exceptions:    None
# Description:   Page that allows to fill XML document data using an HTML form
#
#
################################################################################
def curate_enter_data(request):
    print "BEGIN curate_enter_data(request)"
    if request.user.is_authenticated():
        template = loader.get_template('curate_enter_data.html')
        context = RequestContext(request, {
            '': '',
        })
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
# Outputs:       View Data Page
# Exceptions:    None
# Description:   Page that allows to view XML data to be curated
#
################################################################################
def curate_view_data(request):
    if request.user.is_authenticated():
        template = loader.get_template('curate_view_data.html')
        context = RequestContext(request, {
            '': '',
        })
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
def curate_view_data_downloadxml(request):
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            xml2downloadID = request.GET.get('id', None)
            
            if xml2downloadID is not None:
                xmlDataObject = XML2Download.objects.get(pk=xml2downloadID)
    
    
                xmlStringEncoded = xmlDataObject.xml.encode('utf-8')
                fileObj = StringIO(xmlStringEncoded)
    
                xmlDataObject.delete()
    
                response = HttpResponse(FileWrapper(fileObj), content_type='application/xml')
                response['Content-Disposition'] = 'attachment; filename=' + xmlDataObject.title
                return response
            else:
                return redirect('/')
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')


def start_curate(request):
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            if request.method == 'POST':                                              
                # parameters to build FormData object in db
                user = request.user.id
                template_id = request.session['currentTemplateID']
                
                form_data = None
                
                selected_option = request.POST['curate_form']
                if selected_option == "new":
                    request.session['curate_edit'] = False
                    new_form = NewForm(request.POST)
                    form_data = FormData(user=str(user), template=template_id, name=new_form.data['document_name'], xml_data=None).save()
                elif selected_option == "open":
                    request.session['curate_edit'] = True
                    open_form = OpenForm(request.POST)
                    form_data = FormData.objects.get(pk=ObjectId(open_form.data['forms']))
                    request.session['curate_edit_data'] = form_data.xml_data
                elif selected_option == "upload":
                    request.session['curate_edit'] = True
                    upload_form = UploadForm(request.POST, request.FILES)
                    xml_file = request.FILES['file']
                    # put the cursor at the beginning of the file
                    xml_file.seek(0)
                    # read the content of the file
                    xml_data = xml_file.read()
                    # check XML data or not?
                    try:
                        etree.fromstring(xml_data)
                    except XMLSyntaxError:
                        return HttpResponseBadRequest('Uploaded File is not well formed XML.')
                    form_data = FormData(user=str(user), template=template_id, name=xml_file.name, xml_data=xml_data).save()
                        
                # parameters that will be used during curation
                request.session['curateFormData'] = str(form_data.id)                
                
                # TODO: remove default options to True 
                request.session['curate_min_tree'] = False                
                request.session['curate_siblings_mod'] = False
                
                options_form = AdvancedOptionsForm(request.POST)
                if 'options' in options_form.data:
                    if 'min_tree' in dict(options_form.data)['options']:
                        request.session['curate_min_tree'] = True
                    if 'siblings_mod' in dict(options_form.data)['options']:
                        request.session['curate_siblings_mod'] = True
                
                return HttpResponse('ok')
            else:
                new_form = NewForm()
                open_form = OpenForm(forms=FormData.objects(user=str(request.user.id), template=request.session['currentTemplateID']))
                upload_form = UploadForm()
                options_form = AdvancedOptionsForm()
                
                template = loader.get_template('curate_start.html')
                context = Context({'new_form':new_form, 'open_form': open_form, 'upload_form': upload_form, 'options_form': options_form})
                
                return HttpResponse(json.dumps({'template': template.render(context)}), content_type='application/javascript')           
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/curate'
        return redirect('/login')
