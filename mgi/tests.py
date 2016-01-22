# Application: mgi
# Purpose: tests
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
from os.path import join
from time import sleep

from pymongo import MongoClient
from mgi.settings import MONGODB_TEST_URI
from pymongo.errors import OperationFailure
from mgi.settings import BASE_DIR
# from mgi.models import Template, TemplateVersion, XMLdata
import os
# import unittest
# from utils.XSDhash import XSDhash
# import xmltodict
from unittest import TestCase
from selenium import webdriver
from modules.discover import discover_modules


TESTS_RESOURCES_PATH = os.path.join(BASE_DIR, 'static', 'resources', 'tests')
XSD_TEST_PATH = os.path.join(BASE_DIR, 'static', 'xsd', 'tests')


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
        client = MongoClient(MONGODB_TEST_URI)
        # connect to the db 'mgi.test'
        db = client['mgi.test']
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

#
#
# def check_uploaded(driver, name):
#     driver.get("http://localhost:8000/admin/xml-schemas/manage-schemas")
#
#     elements = driver.find_elements_by_xpath("//div[@id='model_selection']/table/tbody/tr/td[1]")
#     elements = [el.text for el in elements]
#
#     if name not in elements:
#         raise IndexError("Template "+name+" has not been uploaded")
#
#
# def select_template(driver, page, tpl_name):
#     driver.get(page)
#
#     templates = driver.find_elements_by_xpath("//div[@id='template_selection']/table/tbody/tr/td[1]")
#     tpl_names = [tpl.text for tpl in templates]
#
#     if tpl_name not in tpl_names:
#         raise IndexError("Template does not seem to be present in the database")
#
#     tpl_index = tpl_names.index(tpl_name)
#     templates[tpl_index].find_element_by_xpath("./../td[3]/button").click()
#
#
# def create_new_document(driver, doc_name):
#     driver.find_element_by_name("curate_form").click()
#     driver.find_element_by_id("id_document_name").clear()
#     driver.find_element_by_id("id_document_name").send_keys(doc_name)
#     driver.find_element_by_xpath("(//button[@type='button'])[2]").click()


# class Test_Model_XMLdata(unittest.TestCase):
#     def setUp(self):
#         # clean all collections in db
#         clean_db()
#         # remove all result files if there are some
#         for filename in os.listdir(os.path.join(TESTS_RESOURCES_PATH, "results")):
#             os.remove(os.path.join(TESTS_RESOURCES_PATH, "results", filename))
#         # add demo.diffusion Template
#         template_path = os.path.join(TESTS_RESOURCES_PATH, "templates", "demo.diffusion.xsd")
#         with open(template_path, 'r') as template_file:
#             template_content = template_file.read()
#         hash = XSDhash.get_hash(template_content)
#         # save the object
#         template_versions = TemplateVersion(nbVersions=1, isDeleted=False).save()
#         self.template = Template(title='Demo Diffusion', filename='demo.diffusion.xsd', content=template_content,
#                                  version=1, templateVersion=str(template_versions.id), hash=hash).save()
#         template_versions.versions = [str(self.template.id)]
#         template_versions.current = str(self.template.id)
#         template_versions.save()
#         self.template.save()
#
#
#     # xmltodict:
#     # - removes blanks/spaces... in attributes texts
#     # - float conversion removes exponential notation (1.0e-4 -> 0.0001)
#
#     # 1) store all data as string and use JS:
#     # use mgi
#     # db.auth("mgi_user", "mgi_password")
#     db.xmldata
# .find("this.content.experiment.experimentType.tracerDiffusivity.material.Composition.constituents.constituent.error
# <= 1e-4" )
#     def test_xml_to_json(self):
#         for filename in os.listdir(os.path.join(TESTS_RESOURCES_PATH, "data", "diffusion")):
#             with open(os.path.join(TESTS_RESOURCES_PATH, "data", "diffusion", filename)) as file:
#                 file_content = file.read()
#                 xml_data = XMLdata(schemaID=str(self.template.id), xml=file_content, title=filename)
#                 xml_data_id = xml_data.save()
#                 json_data = XMLdata.get(xml_data_id)
#                 json_to_xml = str(xmltodict.unparse(json_data['content'])
# .replace('<?xml version="1.0" encoding="utf-8"?>\n',""))
#                 with open(os.path.join(TESTS_RESOURCES_PATH, "results", filename), 'w') as result_file:
#                     result_file.write(json_to_xml)
#                 self.assertTrue(file_content == json_to_xml)
#
#     def tearDown(self):
#         # clean all collections in db
#         clean_db()


# if __name__ == "__main__":
    # run one
    # unittest.main(Test_Model_XMLdata.test_xml_to_json)
