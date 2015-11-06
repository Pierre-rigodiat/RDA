from models import BlobHosterModule, RawXMLModule, HandleModule


def blob_hoster(request):
    return BlobHosterModule().render(request)


def raw_xml(request):
    return RawXMLModule().render(request)


def handle(request):
    return HandleModule().render(request)
