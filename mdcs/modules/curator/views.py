from models import BlobHosterModule

def blob_hoster(request):
    return BlobHosterModule().render(request)
