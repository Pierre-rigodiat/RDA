from django import forms


class BLOBHosterForm(forms.Form):
    file = forms.FileField()


class URLForm(forms.Form):
    url = forms.URLField()