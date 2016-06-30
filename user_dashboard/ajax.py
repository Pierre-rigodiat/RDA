################################################################################
#
# File Name: ajax.py
# Application: user_dashboard
# Purpose:   AJAX methods used for user dashboard purposes
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

from django.http import HttpResponse
import json
from mgi.models import XMLdata
from django.template import RequestContext
from mgi.common import send_mail_to_managers
import os
from django.utils.importlib import import_module
settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
MDCS_URI = settings.MDCS_URI


################################################################################
#
# Function Name: delete_result(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Delete an XML document from the database
#
################################################################################
def delete_result(request):
    result_id = request.GET['result_id']

    try:
        XMLdata.delete(result_id)
    except:
        # XML can't be found
        pass

    return HttpResponse(json.dumps({}), content_type='application/javascript')

################################################################################
#
# Function Name: update_publish(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Publish and update the publish date of an XMLdata
#
################################################################################
def update_publish(request):
    XMLdata.update_publish(request.GET['result_id'])
    resource = XMLdata.get(request.GET['result_id'])

    # Send mail to the user and the admin
    context = {'URI': MDCS_URI,
               'title': resource['title'],
               'publicationdate': resource['publicationdate'],
               'user': request.user.username}

    send_mail_to_managers(subject='Resource Published',
                                pathToTemplate='dashboard/email/resource_published.html',
                                context=context)
    return HttpResponse(json.dumps({}), content_type='application/javascript')

################################################################################
#
# Function Name: update_unpublish(request)
# Inputs:        request -
# Outputs:
# Exceptions:    None
# Description:   Unpublish an XMLdata
#
################################################################################
def update_unpublish(request):
    XMLdata.update_unpublish(request.GET['result_id'])
    return HttpResponse(json.dumps({}), content_type='application/javascript')
