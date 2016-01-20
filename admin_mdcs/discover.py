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
from mgi.rights import *


def init_rules():
    """
    Init of group and permissions for the application.
    If the anonymous group does not exist, creation of the group with associate permissions
    If the default group does not exist, creation of the group with associate permissions
    """
    try:
        ###########################################
        #### Get or Create the Group anonymous ####
        ###########################################
        anonymousGroup, created = Group.objects.get_or_create(name=anonymous_group)
        if not created:
            anonymousGroup.permissions.clear()

        ###########################################
        #### END Get or Create the Group anonymous#
        ###########################################

        ###########################################
        ##### Get or Create the default group #####
        ###########################################
        defaultGroup, created = Group.objects.get_or_create(name=default_group)
        if not created:
            defaultGroup.permissions.clear()

        #### EXPLORE ####
        explore_access_perm = Permission.objects.get(codename=explore_access)
        explore_save_query_perm = Permission.objects.get(codename=explore_save_query)
        explore_delete_query_perm = Permission.objects.get(codename=explore_delete_query)
        defaultGroup.permissions.add(explore_access_perm)
        defaultGroup.permissions.add(explore_save_query_perm)
        defaultGroup.permissions.add(explore_delete_query_perm)
        #### END EXPLORE ####

        #### CURATE ####
        curate_access_perm = Permission.objects.get(codename=curate_access)
        curate_view_data_save_repo_perm = Permission.objects.get(codename=curate_view_data_save_repo)
#         curate_edit_document_perm = Permission.objects.get(codename=curate_edit_document)
#         curate_delete_document_perm = Permission.objects.get(codename=curate_delete_document)
        defaultGroup.permissions.add(curate_access_perm)
        defaultGroup.permissions.add(curate_view_data_save_repo_perm)
#         defaultGroup.permissions.add(curate_edit_document_perm)
#         defaultGroup.permissions.add(curate_delete_document_perm)
        #### END CURATE ####

        #### COMPOSE ####
        compose_access_perm = Permission.objects.get(codename=compose_access)
        compose_save_template_perm = Permission.objects.get(codename=compose_save_template)
        compose_save_type_perm = Permission.objects.get(codename=compose_save_type)
        defaultGroup.permissions.add(compose_access_perm)
        defaultGroup.permissions.add(compose_save_template_perm)
        defaultGroup.permissions.add(compose_save_type_perm)
        #### END COMPOSE ####

        #### API ####
        api_access_perm = Permission.objects.get(codename=api_access)
        defaultGroup.permissions.add(api_access_perm)
        #### END API ####
        ###########################################
        ##### END Get or Create the default group #
        ###########################################

    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)


