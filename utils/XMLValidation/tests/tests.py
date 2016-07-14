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

from mgi.models import create_type
from mgi.settings import BASE_DIR
from os.path import join
from django.utils.importlib import import_module
from lxml import etree
import platform
from utils.XMLValidation.xml_schema import _lxml_validate_xsd, _xerces_validate_xsd, validate_xml_schema

RESOURCES_PATH = join(BASE_DIR, 'utils', 'XMLValidation', 'tests', 'data')


class ComposerTestSuite(TestCase):
    """
    Test suite for the Compose application
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


    # def test_empty(self):
    #     # load template
    #     template_path = join(RESOURCES_PATH, 'empty.xsd')
    #     self.assertRaises(Exception, self.load_template(template_path))
    #
    #     # test LXML
    #     self.assertRaises(Exception, _lxml_validate_xsd(self.xsd_tree))
    #     # test global method
    #     self.assertRaises(Exception, validate_xml_schema(self.xsd_tree))
    #
    #     # test Xerces
    #     if platform.system() != "Windows":
    #         _xerces_validate_xsd("")

    def test_basic(self):
        # load template
        template_path = join(RESOURCES_PATH, 'basic.xsd')
        self.load_template(template_path)

        # test LXML
        _lxml_validate_xsd(self.xsd_tree)
        # test global method
        self.assertEquals(validate_xml_schema(self.xsd_tree), None)

        # test Xerces
        if platform.system() != "Windows":
            _xerces_validate_xsd(self.xsd_string)
