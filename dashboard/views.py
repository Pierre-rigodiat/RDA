################################################################################
#
# File Name: views.py
# Application: dashboard
# Description:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Xavier SCHMITT
#         xavier.schmitt@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.contrib.auth.decorators import login_required
from django.conf import settings
from mgi.settings import BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI
from utils.BLOBHoster.BLOBHosterFactory import BLOBHosterFactory
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from mgi.models import Template, FormData, XMLdata, Type, Module
from admin_mdcs.forms import EditProfileForm, ChangePasswordForm, UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
import lxml.etree as etree
from io import BytesIO
from mgi import common
import os
import xmltodict

################################################################################
#
# Function Name: my_profile(request)
# Inputs:        request -
# Outputs:       My Profile Page
# Exceptions:    None
# Description:   Page that allows to look at user's profile information
#
################################################################################
@login_required(login_url='/login')
def my_profile(request):
    template = loader.get_template('dashboard/my_profile.html')
    context = RequestContext(request, {
        '': '',
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: my_profile_edit(request)
# Inputs:        request -
# Outputs:       Edit My Profile Page
# Exceptions:    None
# Description:   Page that allows to edit a profile
#
################################################################################
@login_required(login_url='/login')
def my_profile_edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            if request.POST['username'] != user.username:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    message = "A user with the same username already exists."
                    return render(request, 'my_profile_edit.html', {'form':form, 'action_result':message})
                except:
                    user.username = request.POST['username']

            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.email = request.POST['email']
            user.save()
            messages.add_message(request, messages.INFO, 'Profile information edited with success.')
            return redirect('/my-profile')
    else:
        user = User.objects.get(id=request.user.id)
        data = {'firstname':user.first_name,
                'lastname':user.last_name,
                'username':user.username,
                'email':user.email}
        form = EditProfileForm(data)

    return render(request, 'dashboard/my_profile_edit.html', {'form':form})


################################################################################
#
# Function Name: my_profile_change_password(request)
# Inputs:        request -
# Outputs:       Change Password Page
# Exceptions:    None
# Description:   Page that allows to change a password
#
################################################################################
@login_required(login_url='/login')
def my_profile_change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            auth_user = authenticate(username=user.username, password=request.POST['old'])
            if auth_user is None:
                message = "The old password is incorrect."
                return render(request, 'my_profile_change_password.html', {'form':form, 'action_result':message})
            else:
                user.set_password(request.POST['new1'])
                user.save()
                messages.add_message(request, messages.INFO, 'Password changed with success.')
                return redirect('/my-profile')
    else:
        form = ChangePasswordForm()

    return render(request, 'dashboard/my_profile_change_password.html', {'form':form})

################################################################################
#
# Function Name: dashboard_resources(request)
# Inputs:        request -
# Outputs:       Dashboard - Resources
# Exceptions:    None
# Description:   Dashboard - Resources
#
################################################################################
@login_required(login_url='/login')
def dashboard_resources(request):
    template = loader.get_template('dashboard/my_dashboard_my_resources.html')
    context = RequestContext(request, {
            'XMLdatas': XMLdata.find({'iduser': str(request.user.id)}),
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: dashboard_my_forms(request)
# Inputs:        request -
# Outputs:       Review forms page
# Exceptions:    None
# Description:   Page that allows to review user forms
#
################################################################################
@login_required(login_url='/login')
def dashboard_my_forms(request):
    forms = FormData.objects(user=str(request.user.id), xml_data_id__exists=False).order_by('template') # xml_data_id False if document not curated
    detailed_forms = []
    for form in forms:
        detailed_forms.append({'form': form, 'template_name': Template.objects().get(pk=form.template).title})
    user_form = UserForm(request.user)

    return render(request, 'dashboard/my_dashboard_my_forms.html', {'forms':detailed_forms, 'user_form': user_form})


################################################################################
#
# Function Name: dashboard_templates(request)
# Inputs:        request -
# Outputs:       Dashboard - Templates
# Exceptions:    None
# Description:   Dashboard - Templates
#
################################################################################
@login_required(login_url='/login')
def dashboard_templates(request):
    template = loader.get_template('dashboard/my_dashboard_my_templates_types.html')
    context = RequestContext(request, {
                'objects': Template.objects(user=str(request.user.id)),
                'objectType': "Template",
            })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: dashboard_types(request)
# Inputs:        request -
# Outputs:       Dashboard - Types
# Exceptions:    None
# Description:   Dashboard - Types
#
################################################################################
@login_required(login_url='/login')
def dashboard_types(request):
    template = loader.get_template('dashboard/my_dashboard_my_templates_types.html')
    context = RequestContext(request, {
                'objects': Type.objects(user=str(request.user.id)),
                'objectType': "Type",
            })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: dashboard_modules(request)
# Inputs:        request -
# Outputs:       User Request Page
# Exceptions:    None
# Description:   Page that allows to add modules to a template or a type
#
################################################################################
@login_required(login_url='/login')
def dashboard_modules(request):
    template = loader.get_template('dashboard/my_dashboard_modules.html')

    object_id = request.GET.get('id', None)
    object_type = request.GET.get('type', None)

    if object_id is not None:
        try:
            if object_type == 'Template':
                db_object = Template.objects.get(pk=object_id)
            elif object_type == 'Type':
                db_object = Type.objects.get(pk=object_id)
            else:
                raise AttributeError('Type parameter unrecognized')

            xslt_path = os.path.join(settings.SITE_ROOT, 'static', 'resources', 'xsl', 'xsd2html4modules.xsl')
            xslt = etree.parse(xslt_path)
            transform = etree.XSLT(xslt)

            dom = etree.parse(BytesIO(db_object.content.encode('utf-8')))
            annotations = dom.findall(".//{http://www.w3.org/2001/XMLSchema}annotation")
            for annotation in annotations:
                annotation.getparent().remove(annotation)
            newdom = transform(dom)
            xsd_tree = str(newdom)

            request.session['moduleTemplateID'] = object_id
            request.session['moduleTemplateContent'] = db_object.content

            request.session['moduleNamespaces'] = common.get_namespaces(BytesIO(str(db_object.content)))
            for prefix, url in request.session['moduleNamespaces'].items():
                if url == "{http://www.w3.org/2001/XMLSchema}":
                    request.session['moduleDefaultPrefix'] = prefix
                    break

            context = RequestContext(request, {
                'xsdTree': xsd_tree,
                'modules': Module.objects,
                'object_type': object_type
            })

            return HttpResponse(template.render(context))
        except:
            return redirect('/')
    else:
        return redirect('/')


################################################################################
#
# Function Name: dashboard_files(request)
# Inputs:        request -
# Outputs:       Dashboard - Files
# Exceptions:    None
# Description:   Dashboard - Files
#
################################################################################
@login_required(login_url='/login')
def dashboard_files(request):
    template = loader.get_template('dashboard/my_dashboard_my_files.html')

    bh_factory = BLOBHosterFactory(BLOB_HOSTER, BLOB_HOSTER_URI, BLOB_HOSTER_USER, BLOB_HOSTER_PSWD, MDCS_URI)
    blob_hoster = bh_factory.createBLOBHoster()

    files = []
    for grid in blob_hoster.find("metadata.iduser", str(request.user.id)):
        item={'name':grid.name,
              'id':str(grid._id),
              'uploadDate':grid.upload_date
        }
        files.append(item)
    context = RequestContext(request, {
                'files': files,
                'url': MDCS_URI,
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: dashboard_detail_resource
# Inputs:        request -
# Outputs:       Detail of a resource
# Exceptions:    None
# Description:   Page that allows to see detail resource from a selected resource
#
################################################################################
@login_required(login_url='/login')
def dashboard_detail_resource(request) :
    template = loader.get_template('dashboard/my_dashboard_detail_resource.html')
    result_id = request.GET['id']
    xmlString = XMLdata.get(result_id)
    title = xmlString['title']
    schemaId = xmlString['schema']

    xmlString = xmltodict.unparse(xmlString['content']).encode('utf-8')
    xsltPath = os.path.join(settings.SITE_ROOT, 'static', 'resources', 'xsl', 'xml2html.xsl')
    xslt = etree.parse(xsltPath)
    transform = etree.XSLT(xslt)

    #Check if a custom detailed result XSLT has to be used
    try:
        if (xmlString != ""):
            dom = etree.fromstring(str(xmlString))
            schema = Template.objects.get(pk=schemaId)
            if schema.ResultXsltDetailed:
                shortXslt = etree.parse(BytesIO(schema.ResultXsltDetailed.content.encode('utf-8')))
                shortTransform = etree.XSLT(shortXslt)
                newdom = shortTransform(dom)
            else:
                newdom = transform(dom)
    except Exception, e:
        #We use the default one
        newdom = transform(dom)

    result = str(newdom)
    context = RequestContext(request, {
        'XMLHolder': result,
        'title': title
    })

    return HttpResponse(template.render(context))
