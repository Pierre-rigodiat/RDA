################################################################################
#
# File Name: html_views.py
# Application: Informatics Core
# Description:
#
# Author: Marcus Newrock
#         marcus.newrock@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

# Responses
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from oai_pmh.explore.forms import KeywordForm, MetadataFormatsForm
import json

################################################################################
#
# Function Name: index(request)
# Inputs:        request -
# Outputs:       Data Exploration by keyword homepage
# Exceptions:    None
# Description:   renders the data exploration by keyword home page from template
#                (index.html)
#
################################################################################
@login_required(login_url='/login')
def index_keyword(request):
    template = loader.get_template('oai_pmh/explore/explore_keyword.html')
    search_form = KeywordForm(request.user.id)
    context = RequestContext(request, {
        'search_Form':search_form,
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: index(request)
# Inputs:        request -
# Outputs:       Data Exploration by keyword homepage
# Exceptions:    None
# Description:   renders the data exploration by keyword home page from template
#                (index.html)
#
################################################################################
@login_required(login_url='/login')
def get_metadata_formats(request):
    template = loader.get_template('oai_pmh/explore/explore_metadata_formats.html')
    listRegistriesId = request.GET.getlist('registries[]')
    metadata_formats_Form = MetadataFormatsForm(listRegistriesId)
    context = RequestContext(request, {
        'metadata_formats_Form':metadata_formats_Form,
    })

    return HttpResponse(json.dumps({'form': template.render(context)}), content_type='application/javascript')