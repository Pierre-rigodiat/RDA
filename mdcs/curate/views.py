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
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.core.servers.basehttp import FileWrapper
from bson.objectid import ObjectId
import lxml.etree as etree
from xlrd import open_workbook

from mgi.models import Template, TemplateVersion, Htmlform, XML2Download


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
def curate_enter_data_downloadform(request):
    if request.user.is_authenticated():
        if 'currentTemplateID' not in request.session:
            return redirect('/curate/select-template')
        else:
            htmlFormId = request.GET.get('id','')
            htmlFormObject = Htmlform.objects.get(pk=htmlFormId)

            formStringEncoded = htmlFormObject.content.encode('utf-8')
            fileObj = StringIO(formStringEncoded)

            htmlFormObject.delete()

            response = HttpResponse(FileWrapper(fileObj), content_type='text/html')
            response['Content-Disposition'] = 'attachment; filename=' + "form.html"
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
