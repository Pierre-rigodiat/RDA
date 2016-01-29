################################################################################
#
# File Name: models.py
# Application: explore
# Purpose:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume Sousa Amaral
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from django.db import models
import mgi.rights as RIGHTS

class OAIPMH(models.Model):
    # model stuff here
    class Meta:
        default_permissions = ()
        permissions = (
            (RIGHTS.oai_pmh_access, RIGHTS.get_description(RIGHTS.oai_pmh_access)),
        )