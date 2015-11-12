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

from cStringIO import StringIO
from django.http import HttpResponse
from django.template import RequestContext, loader, Context
from django.shortcuts import redirect
from django.core.servers.basehttp import FileWrapper
from bson.objectid import ObjectId
import lxml.etree as etree
from lxml.etree import XMLSyntaxError
import json 
import xmltodict
from django.contrib import messages
from mgi.models import Template, TemplateVersion, XML2Download, FormData,\
    XMLdata, FormElement, XMLElement
from curate.forms import NewForm, OpenForm, UploadForm, SaveDataForm
from django.http.response import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

################################################################################
#
# Function Name: index(request)
# Inputs:        request - 
# Outputs:       Main Page of Curate Application
# Exceptions:    None
# Description:   Page that allows to select a template to start curating         
#
################################################################################
@login_required(login_url='/login')
def index(request):
    template = loader.get_template('curate.html')
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
# Function Name: curate_select_template(request)
# Inputs:        request -
# Outputs:       Main Page of Curate Application
# Exceptions:    None
# Description:   Page that allows to select a template to start curating data
#
#
################################################################################
@login_required(login_url='/login')
def curate_select_template(request):
    template = loader.get_template('curate.html')
    context = RequestContext(request, {
        '': '',
    })
    return HttpResponse(template.render(context))

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
@login_required(login_url='/login')
def curate_enter_data(request):
    print "BEGIN curate_enter_data(request)"
    template = loader.get_template('curate_enter_data.html')
    context = RequestContext(request, {
        '': '',
    })

    if 'id' in request.GET:
        if request.user.is_superuser:
            try:
                xml_data_id = request.GET['id']
                xml_data = XMLdata.get(xml_data_id)
                json_content = xml_data['content']
                xml_content = xmltodict.unparse(json_content)
                request.session['curate_edit_data'] = xml_content
                request.session['curate_edit'] = True
                request.session['curate_min_tree'] = True
                request.session['currentTemplateID'] = xml_data['schema']
                # remove previously created forms when editing a new one
                previous_forms = FormData.objects(user=str(request.user.id), xml_data_id__exists=True)
                for previous_form in previous_forms:
                    # cascade delete references
                    for form_element_id in previous_form.elements.values():
                        try:
                            form_element = FormElement.objects().get(pk=form_element_id)
                            if form_element.xml_element is not None:
                                try:
                                    xml_element = XMLElement.objects().get(pk=str(form_element.xml_element.id))
                                    xml_element.delete()
                                except:
                                    # raise an exception when element not found
                                    pass
                            form_element.delete()
                        except:
                            # raise an exception when element not found
                            pass
                    previous_form.delete()
                form_data = FormData(user=str(request.user.id), template=xml_data['schema'], name=xml_data['title'], xml_data=xml_content, xml_data_id=xml_data_id).save()
                request.session['curateFormData'] = str(form_data.id)
                if 'formString' in request.session:
                    del request.session['formString']
                if 'xmlDocTree' in request.session:
                    del request.session['xmlDocTree']

                return HttpResponse(template.render(context))
            except:
                # can't find the data
                messages.add_message(request, messages.INFO, 'XML data not found.')
                return redirect('/')
        else:
            if 'currentTemplateID' not in request.session:
                return redirect('/curate/select-template')
        return HttpResponse(template.render(context))
    else:
        return HttpResponse(template.render(context))

################################################################################
#
# Function Name: curate_view_data(request)
# Inputs:        request -
# Outputs:       View Data Page
# Exceptions:    None
# Description:   Page that allows to view XML data to be curated
#
################################################################################
@login_required(login_url='/login')
def curate_view_data(request):
    template = loader.get_template('curate_view_data.html')

    # get form data from the database
    form_data_id = request.session['curateFormData']
    form_data = FormData.objects.get(pk=ObjectId(form_data_id))
    if not form_data.name.lower().endswith('.xml'):
        form_data.name += ".xml"
    form_name = form_data.name

    context = RequestContext(request, {
        'form_save': SaveDataForm({"title": form_name}),
    })
    if 'currentTemplateID' not in request.session:
        return redirect('/curate/select-template')
    else:
        return HttpResponse(template.render(context))

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
@login_required(login_url='/login')
def curate_enter_data_downloadxsd(request):
    if 'currentTemplateID' not in request.session:
        return redirect('/curate/select-template')
    else:
        templateID = request.session['currentTemplateID']

        templateObject = Template.objects.get(pk=ObjectId(templateID))
        template_filename = templateObject.filename

        xsdDocData = templateObject.content

        xsdEncoded = xsdDocData.encode('utf-8')
        fileObj = StringIO(xsdEncoded)

        response = HttpResponse(FileWrapper(fileObj), content_type='application/xsd')
        response['Content-Disposition'] = 'attachment; filename=' + template_filename
        return response

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
@login_required(login_url='/login')
def curate_view_data_downloadxml(request):
    if 'currentTemplateID' not in request.session:
        return redirect('/curate/select-template')
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
            return response
        else:
            return redirect('/')

################################################################################
#
# Function Name: start_curate(request)
# Inputs:        request -
# Exceptions:    None
# Description:   Load forms to start curation
#
################################################################################
@login_required(login_url='/login')
def start_curate(request):
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
            request.session['curate_min_tree'] = True
#                 request.session['curate_siblings_mod'] = False

#                 options_form = AdvancedOptionsForm(request.POST)
#                 if 'options' in options_form.data:
#                     if 'min_tree' in dict(options_form.data)['options']:
#                         request.session['curate_min_tree'] = True
#                     if 'siblings_mod' in dict(options_form.data)['options']:
#                         request.session['curate_siblings_mod'] = True

            return HttpResponse('ok')
        else:
            new_form = NewForm()
            open_form = OpenForm(forms=FormData.objects(user=str(request.user.id), template=request.session['currentTemplateID'], xml_data_id__exists=False))
            upload_form = UploadForm()
#                 options_form = AdvancedOptionsForm()

            template = loader.get_template('curate_start.html')
            context = Context({'new_form':new_form, 'open_form': open_form, 'upload_form': upload_form})#, 'options_form': options_form})

            return HttpResponse(json.dumps({'template': template.render(context)}), content_type='application/javascript')

################################################################################
#
# Function Name: save_xml_data_to_db(request)
# Inputs:        request -
# Outputs:       
# Exceptions:    None
# Description:   Save the current XML document in MongoDB. The document is also
#                converted to RDF format and sent to a Jena triplestore.
#                
#
################################################################################
@login_required(login_url='/login')
def save_xml_data_to_db(request):
    xmlString = request.session['xmlString']
    templateID = request.session['currentTemplateID']

    form = SaveDataForm(request.POST)

    if form.is_valid():
        if xmlString != "":
            try:
                # get form data from the database
                form_data_id = request.session['curateFormData']
                form_data = FormData.objects.get(pk=ObjectId(form_data_id))
                if not form.data['title'].lower().endswith('.xml'):
                    form.data['title'] += ".xml"
                # update data if id is present
                if form_data.xml_data_id is not None:
                    XMLdata.update_content(form_data.xml_data_id, xmlString, title=form.data['title'])
                else:
                    #create new data otherwise
                    newJSONData = XMLdata(schemaID=templateID, xml=xmlString, title=form.data['title'])
                    newJSONData.save()
                # delete form data
                try:
                    form_data = FormData.objects().get(pk=form_data_id)
                    # cascade delete references
                    for form_element_id in form_data.elements.values():
                        try:
                            form_element = FormElement.objects().get(pk=form_element_id)
                            if form_element.xml_element is not None:
                                try:
                                    xml_element = XMLElement.objects().get(pk=str(form_element.xml_element.id))
                                    xml_element.delete()
                                except:
                                    # raise an exception when element not found
                                    pass
                            form_element.delete()
                        except:
                            # raise an exception when element not found
                            pass
                    form_data.delete()
                except Exception, e:
                    return HttpResponseBadRequest('Unable to save data.')
                return HttpResponse('ok')
            except Exception, e:
                message = e.message.replace('"', '\'')
                return HttpResponseBadRequest(message)
        else:
            return HttpResponseBadRequest('No data to save.')
    else:
        return HttpResponseBadRequest('Invalid title.')

    