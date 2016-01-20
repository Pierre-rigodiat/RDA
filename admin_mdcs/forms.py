################################################################################
#
# File Name: forms.py
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

from django import forms

# list of possible protocols available in the form
PROTOCOLS = (('http', 'HTTP'),
            ('https', 'HTTPS'))

class RepositoryForm(forms.Form):
    """
    Form to register a new repository
    """
    name = forms.CharField(label='Instance Name', max_length=100, required=True)
    protocol = forms.ChoiceField(label='Protocol', choices=PROTOCOLS, required=True)
    ip_address = forms.CharField(label='IP Address', required=True)
    port = forms.IntegerField(label='Port', required=True, min_value=0, initial=8000)
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password',widget=forms.PasswordInput, required=True)
    client_id = forms.CharField(label='Client ID', max_length=100, required=True)
    client_secret = forms.CharField(label='Client Secret', max_length=100, required=True)
    timeout = forms.IntegerField(label="Timeout (s)", min_value=1, max_value=60, initial=1)
    
class RefreshRepositoryForm(forms.Form):
    """
    Form to refresh the token of a repository
    """
    client_id = forms.CharField(label='Client ID', max_length=100, required=True)
    client_secret = forms.CharField(label='Client Secret', max_length=100, required=True)
    timeout = forms.IntegerField(label="Timeout (s)", min_value=1, max_value=60, initial=1)

class RequestAccountForm(forms.Form):
    """
    Form to request an account
    """
    username = forms.CharField(label='Username', max_length=100, required=True)
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput, required=True)
    firstname = forms.CharField(label='First Name', max_length=100, required=True)
    lastname = forms.CharField(label='Last Name', max_length=100, required=True)
    email = forms.EmailField(label='Email Address', max_length=100, required=True)
    
class EditProfileForm(forms.Form):
    """
    Form to edit the profile information
    """
    firstname = forms.CharField(label='First Name', max_length=100, required=True)
    lastname = forms.CharField(label='Last Name', max_length=100, required=True)
    username = forms.CharField(label='Username', max_length=100, required=True, widget=forms.HiddenInput())
    email = forms.EmailField(label='Email Address', max_length=100, required=True)
    
class ChangePasswordForm(forms.Form):
    """
    Form to change the password
    """
    old = forms.CharField(label='Old Password',widget=forms.PasswordInput, required=True)
    new1 = forms.CharField(label='New Password',widget=forms.PasswordInput, required=True)
    new2 = forms.CharField(label='Confirm New Password',widget=forms.PasswordInput, required=True)
    
class ContactForm(forms.Form):
    """
    Form to contact the administrator
    """
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label='Email Address', max_length=100, required=True)
    message = forms.CharField(label='Message', widget=forms.Textarea, required=True)

class PrivacyPolicyForm(forms.Form):
    """
    Form to update the privacy policy
    """
    content = forms.CharField(label="Privacy Policy", widget=forms.Textarea, required=False)

class TermsOfUseForm(forms.Form):
    """
    Form to update the terms of use
    """
    content = forms.CharField(label="Terms of Use", widget=forms.Textarea, required=False)
    
class HelpForm(forms.Form):
    """
    Form to update the help
    """
    content = forms.CharField(label="Help", widget=forms.Textarea, required=False)

class UploadXSLTForm(forms.Form):
    """
    Form to upload a new XSLT
    """
    name = forms.CharField(label='Enter XSLT name', max_length=100, required=True)
    xslt_file = forms.FileField(label='Select a file',required=True)
    available_for_all = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'cmn-toggle cmn-toggle-round'}))

class UploadResultXSLTForm(forms.Form):
    """
    Form to upload a new XSLT to display results
    """
    result_name = forms.CharField(label='Enter XSLT name', max_length=100, required=True)
    result_xslt_file = forms.FileField(label='Select a file',required=True)

    