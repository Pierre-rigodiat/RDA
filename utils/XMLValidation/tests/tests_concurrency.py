################################################################################
#
# File Name: tests.py
# Application: compose
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
from django.http.request import HttpRequest
from django.test import TestCase
from mgi.common import update_dependencies
from mgi.models import create_type
from mgi.settings import BASE_DIR
from os.path import join
from django.utils.importlib import import_module
from lxml import etree
from utils.XMLValidation.xml_schema import validate_xml_schema

import thread

RESOURCES_PATH = join(BASE_DIR, 'utils', 'XMLValidation', 'tests', 'data')


class ValidateXSDConcurrencyTestSuite(TestCase):
    """
    Test suite for the XSD Validation
    """
    def setUp(self):
        # create the request
        self.request = HttpRequest()
        # create the session
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

    def load_template(self, template_path):
        """
        Load the template to use in validation
        :param template_path:
        :return:
        """
        # Open the the file
        with open(template_path, 'r') as template_file:
            # read the file content
            self.xsd_string = template_file.read()
            self.xsd_tree = etree.fromstring(self.xsd_string)

    def load_type(self, type_path):
        """
        Load the type to use in validation
        :param type_path:
        :return:
        """
        # Open the the file
        with open(type_path, 'r') as type_file:
            # read the file content
            type_content = type_file.read()
            # add the type in database
            type_object = create_type(type_content, 'type_name', type_path)
            return type_object

    def validate_schema_func(self):
        validate_xml_schema(self.xsd_tree)

    def test_concurrency(self):
        # load type
        type_path = join(RESOURCES_PATH, 'to-include.xsd')
        type_object = self.load_type(type_path)

        # load template
        template_path = join(RESOURCES_PATH, 'include.xsd')
        self.load_template(template_path)

        update_dependencies(self.xsd_tree, {'to-include.xsd': str(type_object.id)})

        for i in range(0, 10):
            thread.start_new_thread(self.validate_schema_func, ())
