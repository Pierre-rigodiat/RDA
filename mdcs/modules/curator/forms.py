from django import forms

CONTENTTYPE = (
            ('application/atom+xml', 'application/atom+xml'),
            ('application/vnd.dart', 'application/vnd.dart'),
            ('application/ecmascript', 'application/ecmascript'),
            ('application/EDI-X12', 'application/EDI-X12'),
            ('application/EDIFACT', 'application/EDIFACT'),
            ('application/json', 'application/json'),
            ('application/javascript', 'application/javascript'),
            ('application/octet-stream', 'application/octet-stream'),
            ('application/ogg', 'application/ogg'),
            ('application/dash+xml', 'application/dash+xml'),
            ('application/pdf', 'application/pdf'),
            ('application/postscript', 'application/postscript'),
            ('application/rdf+xml', 'application/rdf+xml'),
            ('application/rss+xml', 'application/rss+xml'),
            ('application/soap+xml', 'application/soap+xml'),
            ('application/font-woff', 'application/font-woff'),
            ('application/xhtml+xml', 'application/xhtml+xml'),
            ('application/xml', 'application/xml'),
            ('application/xml-dtd', 'application/xml-dtd'),
            ('application/xop+xml', 'application/xop+xml'),
            ('application/zip', 'application/zip'),
            ('application/gzip', 'application/gzip'),
            ('application/example', 'application/example'),
            ('application/x-nacl', 'application/x-nacl'),
            ('application/x-pnacl', 'application/x-pnacl'),
            ('application/smil+xml', 'application/smil+xml'),
            ('image/gif', 'image/gif'),
            ('image/jpeg', 'image/jpeg'),
            ('image/pjpeg', 'image/pjpeg'),
            ('image/png', 'image/png'),
            ('image/bmp', 'image/bmp'),
            ('image/svg+xml', 'image/svg+xml'),
            ('image/tiff', 'image/tiff'),
            ('image/vnd.djvu', 'image/vnd.djvu'),
            ('image/example', 'image/example'))

class BLOBHosterForm(forms.Form):
    contentType = forms.ChoiceField(label='Content Type', choices=CONTENTTYPE, required=True)
    file = forms.FileField()