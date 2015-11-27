from django import forms


class NamePIDForm(forms.Form):
    name = forms.CharField(label='Name')
    pid = forms.CharField(label='PID')