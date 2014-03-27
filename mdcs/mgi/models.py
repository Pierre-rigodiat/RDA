################################################################################
#
# File Name: models.py
# Application: mgi
# Description: 
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institue of Standards and Technology
#
################################################################################

from django.db import models

# Create your models here.

class Task(models.Model):
    def foo(self):
        return "bar"

class MyForm(forms.Form):
    usernamefield = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass'}))
