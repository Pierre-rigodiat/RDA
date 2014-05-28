################################################################################
#
# File Name: models.py
# Application: explore
# Description:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from django.db import models
import lxml.etree as etree
# Create your models here.

class XMLSchema(models.Model):
    tree = etree.ElementTree