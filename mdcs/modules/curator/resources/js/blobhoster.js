var blobHosterPopupOptions = {
    title: "Upload File",
}

saveBlobHosterData = function() {
    return new FormData(openPopUp.find('.blobhoster-form')[0]);
}

configurePopUp(blobHosterPopupOptions, saveBlobHosterData);