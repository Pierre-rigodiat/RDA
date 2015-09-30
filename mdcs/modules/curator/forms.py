from django import forms


class BLOBHosterForm(forms.Form):
    file = forms.FileField()
