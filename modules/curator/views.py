from curate.models import SchemaElement
from models import BlobHosterModule, RawXMLModule, HandleModule,\
    RemoteBlobHosterModule, AdvancedBlobHosterModule, AutoKeyRefModule
from django.http.response import HttpResponse
import json


def blob_hoster(request):
    return BlobHosterModule().render(request)


def remote_blob_hoster(request):
    return RemoteBlobHosterModule().render(request)


def advanced_blob_hoster(request):
    return AdvancedBlobHosterModule().render(request)


def raw_xml(request):
    return RawXMLModule().render(request)


def handle(request):
    return HandleModule().render(request)


def auto_keyref(request):
    return AutoKeyRefModule().render(request)


def get_updated_keys(request):
    """
        updated_keys[key] = {'ids': [],
                            'tagIDs': []}
        key = key name
        ids = list of posssible values for a key
        tagIDs = HTML element that needs to be updated with the values (keyrefs)
    """

    updated_keyrefs = []
    for keyref, values in request.session['keyrefs'].iteritems():
        updated_keyrefs.extend(values['module_ids'])

    return HttpResponse(json.dumps(updated_keyrefs), content_type='application/javascript')