################################################################################
#
# File Name: models.py
# Application: curate
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
from django.db import models
import mgi.rights as RIGHTS

class Curate(models.Model):
    # model stuff here
    class Meta:
        permissions = (
            (RIGHTS.curate_access, RIGHTS.curate_access),
            (RIGHTS.curate_view_data_save_repo, RIGHTS.curate_view_data_save_repo),
        )
