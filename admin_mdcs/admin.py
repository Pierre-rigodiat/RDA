################################################################################
#
# File Name: admin.py
# Application: admin_mdcs
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth import models as auth_models
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import forms as auth_forms
from mgi.common import validate_password_strength
import os
from django.utils.importlib import import_module
settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
USE_PASSWORD_STRENGTH = settings.USE_PASSWORD_STRENGTH
PASSWORD_MIN_LENGTH = settings.PASSWORD_MIN_LENGTH
PASSWORD_MIN_DIGITS = settings.PASSWORD_MIN_DIGITS
PASSWORD_MIN_UPPERCASE = settings.PASSWORD_MIN_UPPERCASE

admin.site.register(Permission)

class AdminPasswordChangeForm(auth_forms.AdminPasswordChangeForm):
    def clean_password1(self):
        return validate_password_strength(self.cleaned_data['password1'])

    def __init__ (self, *args, **kwargs):
        super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)
        if USE_PASSWORD_STRENGTH:
            password_policy = '{0} character(s) minimum, {1} digit(s) minimum ' \
                          'and {2} uppercase minimum'.format(PASSWORD_MIN_LENGTH, PASSWORD_MIN_DIGITS,
                                                                PASSWORD_MIN_UPPERCASE)
            self.fields['password1'].help_text = password_policy

class UserCreationForm(auth_forms.UserCreationForm):
    def clean_password1(self):
        return validate_password_strength(self.cleaned_data['password1'])

    def __init__ (self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        if USE_PASSWORD_STRENGTH:
            password_policy = '{0} character(s) minimum, {1} digit(s) minimum ' \
                          'and {2} uppercase minimum'.format(PASSWORD_MIN_LENGTH, PASSWORD_MIN_DIGITS,
                                                                PASSWORD_MIN_UPPERCASE)
            self.fields['password1'].help_text = password_policy

class UserAdmin(auth_admin.UserAdmin):
    change_password_form = AdminPasswordChangeForm
    add_form = UserCreationForm


# Re-register UserAdmin
admin.site.unregister(auth_models.User)
admin.site.register(auth_models.User, UserAdmin)