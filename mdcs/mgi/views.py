################################################################################
#
# File Name: views.py
# Application: mgi
# Description: Django views used to render pages for the system.
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

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout
from django.template import RequestContext, loader
from django.shortcuts import redirect
from mgi.models import Template, Request, Message, TermsOfUse, PrivacyPolicy, Help, FormData
from admin_mdcs.forms import RequestAccountForm, EditProfileForm, ChangePasswordForm, ContactForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


################################################################################
#
# Function Name: home(request)
# Inputs:        request - 
# Outputs:       Materials Data Curation System homepage
# Exceptions:    None
# Description:   renders the main home page from template (index.html)
#
################################################################################
def home(request):
    template = loader.get_template('index.html')

    context = RequestContext(request, {
        'templates': Template.objects(user=None).order_by('-id')[:7]
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: all_options(request)
# Inputs:        request - 
# Outputs:       All Options Page
# Exceptions:    None
# Description:   Page that allows to access every features of the System   
#
################################################################################
def all_options(request):
    template = loader.get_template('all-options.html')
    context = RequestContext(request, {
        '': '',
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: browse_all(request)
# Inputs:        request - 
# Outputs:       Browse All Page
# Exceptions:    None
# Description:   Page that allows to access the list of all existing templates
#
################################################################################
def browse_all(request):
    template = loader.get_template('browse-all.html')

    context = RequestContext(request, {
        'templates': Template.objects(user=None).order_by('title')
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: request_new_account(request)
# Inputs:        request - 
# Outputs:       Request New Account Page
# Exceptions:    None
# Description:   Page that allows to request a user account
#
################################################################################
def request_new_account(request):
    if request.method == 'POST':
        form = RequestAccountForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username=request.POST["username"])
                message = "This username already exists. Please choose another username."
                return render(request, 'request_new_account.html', {'form':form, 'action_result':message})
            except:
                Request(username=request.POST["username"], password=request.POST["password1"],first_name=request.POST["firstname"], last_name=request.POST["lastname"], email=request.POST["email"]).save()
                messages.add_message(request, messages.INFO, 'User Account Request sent to the administrator.')
                return redirect('/')
                
    else:
        form = RequestAccountForm()
    
    return render(request, 'request_new_account.html', {'form':form})


################################################################################
#
# Function Name: logout_view(request)
# Inputs:        request - 
# Outputs:       Login Page
# Exceptions:    None
# Description:   Page that redirects to login page
#                
#
################################################################################
def logout_view(request):
    logout(request)
    request.session['next'] = '/'
    return redirect('/login')


################################################################################
#
# Function Name: my_profile(request)
# Inputs:        request - 
# Outputs:       My Profile Page
# Exceptions:    None
# Description:   Page that allows to look at user's profile information
#
################################################################################
@login_required(login_url='/login')
def my_profile(request):
    template = loader.get_template('my_profile.html')
    context = RequestContext(request, {
        '': '',
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: my_profile_edit(request)
# Inputs:        request - 
# Outputs:       Edit My Profile Page
# Exceptions:    None
# Description:   Page that allows to edit a profile
#
################################################################################
@login_required(login_url='/login')
def my_profile_edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            if request.POST['username'] != user.username:
                try:
                    user = User.objects.get(username=request.POST['username'])
                    message = "A user with the same username already exists."
                    return render(request, 'my_profile_edit.html', {'form':form, 'action_result':message})
                except:
                    user.username = request.POST['username']

            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.email = request.POST['email']
            user.save()
            messages.add_message(request, messages.INFO, 'Profile information edited with success.')
            return redirect('/my-profile')
    else:
        user = User.objects.get(id=request.user.id)
        data = {'firstname':user.first_name,
                'lastname':user.last_name,
                'username':user.username,
                'email':user.email}
        form = EditProfileForm(data)

    return render(request, 'my_profile_edit.html', {'form':form})


################################################################################
#
# Function Name: my_profile_change_password(request)
# Inputs:        request - 
# Outputs:       Change Password Page
# Exceptions:    None
# Description:   Page that allows to change a password
#
################################################################################
@login_required(login_url='/login')
def my_profile_change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.user.id)
            auth_user = authenticate(username=user.username, password=request.POST['old'])
            if auth_user is None:
                message = "The old password is incorrect."
                return render(request, 'my_profile_change_password.html', {'form':form, 'action_result':message})
            else:
                user.set_password(request.POST['new1'])
                user.save()
                messages.add_message(request, messages.INFO, 'Password changed with success.')
                return redirect('/my-profile')
    else:
        form = ChangePasswordForm()

    return render(request, 'my_profile_change_password.html', {'form':form})

################################################################################
#
# Function Name: my_profile_my_forms(request)
# Inputs:        request - 
# Outputs:       Review forms page
# Exceptions:    None
# Description:   Page that allows to review user forms
#
################################################################################
@login_required(login_url='/login')
def my_profile_my_forms(request):
    forms = FormData.objects(user=str(request.user.id), xml_data_id__exists=False).order_by('template') # xml_data_id False if document not curated
    detailed_forms = []
    for form in forms:
        detailed_forms.append({'form': form, 'template_name': Template.objects().get(pk=form.template).title})
    return render(request, 'my_profile_my_forms.html', {'forms':detailed_forms})


################################################################################
#
# Function Name: contact(request)
# Inputs:        request - 
# Outputs:       
# Exceptions:    None
# Description:   
#                
#
################################################################################
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Message(name=request.POST['name'], email=request.POST['email'], content=request.POST['message']).save()
            messages.add_message(request, messages.INFO, 'Your message was sent to the administrator.')
            return redirect('/')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form':form})


################################################################################
#
# Function Name: privacy_policy(request)
# Inputs:        request - 
# Outputs:       Privacy Policy Page
# Exceptions:    None
# Description:   Page that provides privacy policy     
#
################################################################################
def privacy_policy(request):
    template = loader.get_template('privacy-policy.html')
    policy = None
    if len(PrivacyPolicy.objects) != 0:
        policy = PrivacyPolicy.objects[0] 

    context = RequestContext(request, { 
        'policy': policy
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: terms_of_use(request)
# Inputs:        request - 
# Outputs:       Terms of Use page
# Exceptions:    None
# Description:   Page that provides terms of use
#
################################################################################
def terms_of_use(request):
    template = loader.get_template('terms-of-use.html')
    terms = None
    if len(TermsOfUse.objects) != 0:
        terms = TermsOfUse.objects[0] 

    context = RequestContext(request, { 
        'terms': terms
    })
    return HttpResponse(template.render(context))


################################################################################
#
# Function Name: help(request)
# Inputs:        request - 
# Outputs:       Help Page
# Exceptions:    None
# Description:   Page that provides FAQ
#
################################################################################
def help(request):
    template = loader.get_template('help.html')
    help = None
    if len(Help.objects) != 0:
        help = Help.objects[0] 

    context = RequestContext(request, { 
        'help': help
    })
    return HttpResponse(template.render(context))
