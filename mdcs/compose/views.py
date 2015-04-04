################################################################################
#
# File Name: views.py
# Application: compose
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


# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.core.servers.basehttp import FileWrapper
from datetime import date
from cStringIO import StringIO
from mgi.models import Template, TemplateVersion, XML2Download, Type, TypeVersion, Bucket


def currentYear():
    return date.today().year


################################################################################
#
# Function Name: index(request)
# Inputs:        request - 
# Outputs:       Main Page of Composer Application
# Exceptions:    None
# Description:   Page that allows to select a template to start composing         
#
################################################################################
def index(request):
    template = loader.get_template('compose.html')
    request.session['currentYear'] = currentYear()
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
        request.session['next'] = '/compose'
        return redirect('/login')


################################################################################
#
# Function Name: compose_build_template(request)
# Inputs:        request -
# Outputs:       Build Template Page
# Exceptions:    None
# Description:   Page that allows to Compose the Template
#
################################################################################
def compose_build_template(request):
    template = loader.get_template('compose_build_template.html')
    request.session['currentYear'] = currentYear()
    if request.user.is_authenticated():

        # 1) user types: list of ids
        userTypes = []
        for user_type in Type.objects(user=request.user.id):
            userTypes.append(user_type)

        # 2) buckets: label -> list of type that are not deleted
        # 3) nobuckets: list of types that are not assigned to a specific bucket
        bucketsTypes = dict()
        nobucketsTypes = []

        buckets = Bucket.objects

        for type_version in TypeVersion.objects():
            if type_version.isDeleted == False:
                hasBucket = False
                for bucket in buckets:
                    if str(type_version.id) in bucket.types:
                        if bucket not in bucketsTypes.keys():
                            bucketsTypes[bucket] = []
                        bucketsTypes[bucket].append(Type.objects.get(pk=type_version.current))
                        hasBucket = True
                if hasBucket == False:
                    nobucketsTypes.append(Type.objects.get(pk=type_version.current))

        context = RequestContext(request, {
           'bucketsTypes': bucketsTypes,
           'nobucketsTypes': nobucketsTypes,
           'userTypes': userTypes,
        })

        return HttpResponse(template.render(context))
    else:
        if 'loggedOut' in request.session:
            del request.session['loggedOut']
        request.session['next'] = '/compose/build-template'
        return redirect('/login')


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