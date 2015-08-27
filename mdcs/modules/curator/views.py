from models import BlobHosterModule, RawXMLModule

def blob_hoster(request):
    return BlobHosterModule().render(request)

def raw_xml(request):
    return RawXMLModule().render(request)
