from models import BlobHosterModule, RawXMLModule, HandleModule,\
    RemoteBlobHosterModule, AdvancedBlobHosterModule
from modules.curator.models import EnumAutoCompleteModule


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


def enum_autocomplete(request):
    return EnumAutoCompleteModule().render(request)
