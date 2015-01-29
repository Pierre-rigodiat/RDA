################################################################################
#
# File Name: XSDflattener.py
# 
# Purpose: Flatten an XSD file - gather all dependencies in one file
# 
# V1: 
#    - works with include statement only (not import)
#    - works with API URL in include schemaLocation attribute
#	 - works with local URI
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#		  Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from utils.XSDflattener.XSDflattener import XSDFlattener
from mgi.models import Type
from urlparse import urlparse

class XSDFlattenerMDCS(XSDFlattener):
			
	def get_dependency_content(self, uri):
		url = urlparse(uri)
		id = url.query.split("=")[1]
		type = Type.objects.get(pk=id)
		return type.content
	
	