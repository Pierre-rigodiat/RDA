
import os
from os.path import join
from time import sleep
from pymongo import MongoClient
from mgi.settings import MONGODB_URI
from mgi.settings import BASE_DIR
from pymongo.errors import OperationFailure
from django.test.testcases import TestCase
from lxml import etree
from mgi.settings import SITE_ROOT
from selenium import webdriver
from modules.discover import discover_modules


TESTS_RESOURCES_PATH = os.path.join(BASE_DIR, 'static', 'resources', 'tests')
XSD_TEST_PATH = os.path.join(BASE_DIR, 'static', 'xsd', 'tests')


class VariableTypesGenerator(object):

    def __init__(self):
        # List extracted from https://docs.python.org/2/library/types.html
        self.possible_types = {
            'int': 50,
            'float': 4.5,
            'str': "string",
            'unicode': u"string",
            'none': None,
            'bool': False,
            'long': 1L,
            'complex': 1.0j,
            'tuples': (1, 2),
            'list': [],
            'dict': {},
            'func': lambda x: x,
            # Generator type
            'code': compile('print "compile"', 'test', 'exec'),
            # Class
            # Instance
            # Method
            # UnboundMethod
            # BuiltinFunction
            # Module
            # File
            # Xrange
            # Slice
            # Ellipsis
            # Traceback
            # Frame
            # Buffer
            # DictProxy
            # NotImplemented
            # GetSetDescriptor
            # MemberDescriptor
        }

    def generate_types_excluding(self, excluded_types_list):
        if type(excluded_types_list) != list:
            raise TypeError('generate_types_excluding only accept lists')

        return [
            val for key, val in self.possible_types.items() if key not in excluded_types_list
        ]

    def generate_type_including(self, include_types_list):
        if type(include_types_list) != list:
            raise TypeError('generate_type_including only accept lists')

        return [
            val for key, val in self.possible_types.items() if key in include_types_list
        ]


# FIXME Correct this object before commiting
class DataHandler(object):

    def __init__(self, filename):
        # FIXME only use dirname
        self.dirname = join(SITE_ROOT, filename)
        self.filename = join(SITE_ROOT, filename)

    @staticmethod
    def _get_file_content_as_xml(filename):
        file_string = ''
        is_in_tag = False

        with open(filename, 'r') as file_content:
            file_lines = [line.strip('\r\n\t ') for line in file_content.readlines()]

            for line in file_lines:
                if is_in_tag:  # Add space if we are in the tag
                    file_string += ' '

                file_string += line

                # Leave the tag if we have one more closing that opening
                if is_in_tag and line.count('>') == line.count('<') + 1:
                    is_in_tag = False
                elif line.count('<') != line.count('>'):  # In tag if opening and closing count are different
                    is_in_tag = True

                # In any other cases the tag flag doesn't change

        return etree.fromstring(file_string)

    def get_xsd(self):
        xsd_name = self.filename + '.xsd'
        return self._get_file_content_as_xml(xsd_name)

    def get_xsd2(self, filename):
        self.filename = join(self.dirname, filename)
        return self.get_xsd()

    def get_xml(self, filename):
        self.filename = join(self.dirname, filename)
        xml_name = self.filename + '.xml'
        return self._get_file_content_as_xml(xml_name)

    def get_html(self):
        html_name = self.filename + '.html'
        return self._get_file_content_as_xml(html_name)

    def get_html2(self, filename):
        self.filename = join(self.dirname, filename)
        return self.get_html()


def are_equals(xml_tree_a, xml_tree_b):
    tag_a = xml_tree_a.tag
    tag_b = xml_tree_b.tag

    attrib_a = xml_tree_a.attrib
    attrib_b = xml_tree_b.attrib

    text_a = xml_tree_a.text
    text_b = xml_tree_b.text

    children_a = xml_tree_a.getchildren()
    children_b = xml_tree_b.getchildren()

    if len(children_a) != len(children_b):
        return False

    for i in xrange(len(children_a)):
        child_a = children_a[i]
        child_b = children_b[i]

        if not are_equals(child_a, child_b):
            return False

    if len(attrib_a) != len(attrib_b):
        return False

    for attr_key in attrib_a.keys():
        if attr_key not in attrib_b.keys():
            return False

        if attrib_a[attr_key] != attrib_b[attr_key]:
            return False

    return tag_a == tag_b and attrib_a == attrib_b and text_a == text_b


class SeleniumTestCase(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000/"

        self.pages = {
            "select": "curate/select-template",
        }

        self.template = "countries"

        self.verificationErrors = []
        self.accept_next_alert = True

        # Clean the database
        self.clean_db()
        discover_modules()

        # Login to MDCS
        self.login(self.base_url, "admin", "admin")

        # Upload the correct schema
        countries_enum_xsd_path = join('modules', 'curator', 'EnumAutoCompleteModule', 'countries-enum.xsd')
        self.upload_xsd(self.template, countries_enum_xsd_path)
        sleep(1)

        self.check_uploaded(self.template)

    def upload_xsd(self, name, file_path):
        self.driver.get("http://localhost:8000/admin/xml-schemas/manage-schemas")

        self.driver.find_element_by_xpath("//div[@id='model_selection']/div/span/div").click()

        self.driver.find_element_by_id("object_name").clear()
        self.driver.find_element_by_id("object_name").send_keys(name)

        self.driver.find_element_by_id("files").clear()
        self.driver.find_element_by_id("files").send_keys(os.path.join(XSD_TEST_PATH, file_path))

        self.driver.find_element_by_id("uploadFile").click()
        self.driver.find_element_by_xpath("//div[@id='objectUploadErrorMessage']/span[@class='btn']").click()

    def check_uploaded(self, name):
        self.driver.get("http://localhost:8000/admin/xml-schemas/manage-schemas")

        elements = self.driver.find_elements_by_xpath("//div[@id='model_selection']/table/tbody/tr/td[1]")
        elements = [el.text for el in elements]

        if name not in elements:
            raise IndexError("Template "+name+" has not been uploaded")

    def login(self, base_url, user, password):
        self.driver.get(base_url)
        self.driver.find_element_by_link_text("Login").click()
        self.driver.find_element_by_id("id_username").clear()
        self.driver.find_element_by_id("id_username").send_keys(user)
        self.driver.find_element_by_id("id_password").clear()
        self.driver.find_element_by_id("id_password").send_keys(password)
        self.driver.find_element_by_css_selector("button.btn").click()

    def clean_db(self):
        # create a connection
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi.test'
        db = client['mgi_test']
        # clear all collections
        for collection in db.collection_names():
            try:
                if collection != 'system.indexes':
                    db.drop_collection(collection)
            except OperationFailure:
                pass

    def tearDown(self):
        self.driver.quit()
        self.clean_db()
