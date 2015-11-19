################################################################################
#
# File Name: models.py
# Application: mgi
# Description:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#         Pierre Francois RIGODIAT
#         pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

### Anonymous group ###
anonymous_group = "anonymous"
#######################

### Compose Rights ###
compose_access = "compose_access"
compose_save_template = "compose_save_template"
compose_save_type = "compose_save_type"
### End Compose Rights ###


### Curate Rights ###
curate_access = "curate_access"
curate_view_data_save_repo = "curate_view_data_save_repo"
### End Curate Rights ###


### Explore Rights ###
explore_access = "explore_access"
explore_save_query="explore_save_query"
explore_delete_query="explore_delete_query"
explore_edit_document="explore_edit_document"
explore_delete_document="explore_delete_document"
### End Explore Rights ###


def get_description(right):
    return "Can " + right.replace("_", " ")