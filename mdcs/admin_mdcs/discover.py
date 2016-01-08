################################################################################
#
# File Name: discover.py
# Purpose:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#         Pierre Francois RIGODIAT
#		  pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from django.contrib.auth.models import Permission, Group
from mgi.rights import anonymous_group, default_group, explore_access, curate_access, \
    curate_edit_document, curate_delete_document, api_access


def init_rules():
    """
    Init of group and permissions for the application.
    If the anonymous group does not exist, creation of the group with associate permissions
    If the default group does not exist, creation of the group with associate permissions
    """
    try:
        # Get or Create the Group anonymous
        anonymousGroup, created = Group.objects.get_or_create(name=anonymous_group)
        if not created:
            anonymousGroup.permissions.clear()

        #We add the exploration_access by default
        explore_access_perm = Permission.objects.get(codename=explore_access)
        anonymousGroup.permissions.add(explore_access_perm)

        # Get or Create the default basic
        defaultGroup, created = Group.objects.get_or_create(name=default_group)
        if not created:
            defaultGroup.permissions.clear()

        #We add the exploration_access and curate_acces by default
        explore_access_perm = Permission.objects.get(codename=explore_access)
        curate_access_perm = Permission.objects.get(codename=curate_access)
        curate_edit_perm = Permission.objects.get(codename=curate_edit_document)
        curate_delete_perm = Permission.objects.get(codename=curate_delete_document)
        defaultGroup.permissions.add(explore_access_perm)
        defaultGroup.permissions.add(curate_access_perm)
        defaultGroup.permissions.add(curate_edit_perm)
        defaultGroup.permissions.add(curate_delete_perm)
    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)


