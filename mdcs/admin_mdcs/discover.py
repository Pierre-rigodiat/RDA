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
from mgi.rights import anonymous_group, explore_access


def init_rules():
    #We check if the anonymous group exists. If not, we create it
    try:
        # Get or Create the Group
        group, created = Group.objects.get_or_create(name=anonymous_group)
        if created:
            #We add the exploration_access by default
            explore_access_perm = Permission.objects.get(codename=explore_access)
            group.permissions.add(explore_access_perm)
    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)


