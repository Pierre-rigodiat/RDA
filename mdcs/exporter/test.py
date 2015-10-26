import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from django.contrib.auth.models import User
import time
import datetime
from dateutil import tz
import os
from mgi.models import ExporterXslt

class TestSelenium(LiveServerTestCase):

    file_name = ""
    server = "http://127.0.0.1:8000"

    def setUp(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("http.response.timeout", 50)
        fp.set_preference("dom.max_script_run_time", 50)
        self.selenium = webdriver.Firefox(firefox_profile=fp)
        #We create a test admin user
        self.user = User.objects.create_user('testAdmin', '', 'admin')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        super(TestSelenium, self).setUp()


    def tearDown(self):
        self.selenium.quit()
        super(TestSelenium, self).tearDown()
        #We delete the test admin user
        self.user.delete()

    def init(self):
        selenium = self.selenium
        #Opening the link we want to test
        selenium.get(TestSelenium.server+'/admin/xml-schemas/manage-xslt')
        #find the form element
        username = selenium.find_element_by_id('id_username')
        password = selenium.find_element_by_id('id_password')
        submit = selenium.find_element_by_xpath('//button[@type="submit" and @value="login"]')
        # #Fill the form with data
        username.send_keys('testAdmin')
        password.send_keys('admin')
        # #submitting the form
        submit.send_keys(Keys.RETURN)
        time.sleep(2)
        return selenium

    def test0_manage_xslt_not_login(self):
        selenium = self.selenium
        #Opening the link we want to test
        selenium.get(TestSelenium.server+'/admin/xml-schemas/manage-xslt')
        #check the returned result
        assert TestSelenium.server+'/login' in selenium.current_url


    def test1_manage_xslt_login(self):
        selenium = self.init()
        #check the returned result
        assert TestSelenium.server in selenium.current_url


    def test03_xslt_HTML(self):
        selenium = self.init()
        administration = selenium.find_element_by_link_text('Administration')
        administration.click()
        # Move to the new page
        selenium.switch_to.window(selenium.window_handles[-1])
        assert TestSelenium.server+'/admin' in selenium.current_url
        templates_types = selenium.find_element_by_link_text('Templates & Types')
        templates_types.click()
        assert TestSelenium.server+'/admin/xml-schemas' in selenium.current_url
        manage_xslt = selenium.find_element_by_link_text('Manage XSLT')
        manage_xslt.click()
        assert TestSelenium.server+'/admin/xml-schemas/manage-xslt' in selenium.current_url

        #Check title
        title = selenium.find_element_by_xpath('//div[@id="featured"]/h1').text
        assert 'XSLT Manager' in title
        #Check current tab
        tab = selenium.find_element_by_xpath('//li[@class=" current_page_item "]/a').text
        assert 'Templates & Types' in tab
        subtab = selenium.find_element_by_xpath('descendant::li[@class=" current_page_item "][2]/a').text
        assert 'Manage XSLT' in subtab
        return selenium


    def test04_add_xslt(self):
        #Retrieve existing XSLT
        exportersXSLT = list(ExporterXslt.objects.all())
        selenium = self.test03_xslt_HTML()
        popup = selenium.find_element_by_xpath('descendant::div[@onclick="displayImport();"]')
        assert 'Upload XSLT' in popup.text
        popup.click()
        #Name
        selenium.find_element_by_xpath('//span[text()="Upload"]').click()
        assert 'Please enter a name.' in selenium.find_element_by_id('form_start_errors').text
        xslt_name = selenium.find_element_by_id('id_name')
        #We create a name with the current date to have the chance to have a unique name
        from_zone = tz.tzutc()
        datetimeUTC = datetime.datetime.now().replace(tzinfo=from_zone).strftime("%m-%d-%Y %I:%M:%S %p")
        TestSelenium.file_name = 'test_'+datetimeUTC
        xslt_name.send_keys(TestSelenium.file_name)
        #File
        selenium.find_element_by_xpath('//span[text()="Upload"]').click()
        assert 'Please select an XSLT file.' in selenium.find_element_by_id('form_start_errors').text
        #We upload a file
        elm = selenium.find_element_by_xpath("//input[@type='file']")
        path = os.path.abspath("./builtin/testData/xsl-music.xsl")
        elm.send_keys(path)
        #We check available for all
        selenium.find_element_by_xpath('descendant::input[@id="id_available_for_all"]').click()
        #We upload
        selenium.find_element_by_xpath('//span[text()="Upload"]').click()
        #Click on ok
        selenium.find_element_by_xpath('//span[text()="Ok"]').click()
        #Retrieve XSLT
        exportersXSLTRes = list(ExporterXslt.objects.all())
        #Get the new XSLT added
        newXSLT = list(set(exportersXSLTRes) - set(exportersXSLT))
        newXSLT = newXSLT[0]
        assert TestSelenium.file_name in newXSLT.name
        assert "xsl-music.xsl" in newXSLT.filename
        self.assertTrue(newXSLT.available_for_all)



    def test05_edit_xslt(self):
        selenium = self.init()
        selenium.get(TestSelenium.server+'/admin/xml-schemas/manage-xslt')
        assert TestSelenium.server+'/admin/xml-schemas/manage-xslt' in selenium.current_url
        edit = selenium.find_element_by_xpath('descendant::td[text()="'+TestSelenium.file_name+'"]/ancestor::tr//div[text()="Edit"]')
        edit.click()
        #We edit
        xslt_name = selenium.find_element_by_id('edit-name')
        xslt_name.clear()
        selenium.find_element_by_xpath('//span[text()="Ok"]').click()
        assert 'Please enter a name.' in selenium.find_element_by_id('form_edit_errors').text
        TestSelenium.file_name = TestSelenium.file_name +"_Edit"
        xslt_name.send_keys(TestSelenium.file_name)
        selenium.find_element_by_xpath('//span[text()="Ok"]').click()
        #Click on ok
        selenium.find_element_by_xpath('//span[text()="Ok"]').click()


    def test06_delete_xslt(self):
        #Retrieve existing XSLT
        exportersXSLT = list(ExporterXslt.objects.all())
        nb_elt = len(exportersXSLT)
        selenium = self.init()
        selenium.get(TestSelenium.server+'/admin/xml-schemas/manage-xslt')
        assert TestSelenium.server+'/admin/xml-schemas/manage-xslt' in selenium.current_url
        delete = selenium.find_element_by_xpath('descendant::td[text()="'+TestSelenium.file_name+'"]/ancestor::tr//div[text()="Delete"]')
        delete.click()
        #We delete
        selenium.find_element_by_xpath('//span[text()="Delete"]').click()
        #Click on ok
        selenium.find_element_by_xpath('//span[text()="Ok"]').click()
        #Retrieve XSLT
        exportersXSLTRes = list(ExporterXslt.objects.all())
        nb_elt_res = len(exportersXSLTRes)
        self.assertEquals(nb_elt_res, nb_elt-1)
        #Get the new XSLT added
        deleteXSLT = list(set(exportersXSLT) - set(exportersXSLTRes))
        deleteXSLT = deleteXSLT[0]
        assert TestSelenium.file_name in deleteXSLT.name
        assert "xsl-music.xsl" in deleteXSLT.filename
        self.assertTrue(deleteXSLT.available_for_all)


    def test07_manage_exporter_HTML(self):
        selenium = self.init()
        administration = selenium.find_element_by_link_text('Administration')
        administration.click()
        # Move to the new page
        selenium.switch_to.window(selenium.window_handles[-1])
        assert TestSelenium.server+'/admin' in selenium.current_url
        templates_types = selenium.find_element_by_link_text('Templates & Types')
        templates_types.click()
        assert TestSelenium.server+'/admin/xml-schemas' in selenium.current_url
        manage_xslt = selenium.find_element_by_link_text('Manage Templates')
        manage_xslt.click()
        assert TestSelenium.server+'/admin/xml-schemas/manage-schemas' in selenium.current_url

        #Check title
        title = selenium.find_element_by_xpath('//div[@id="featured"]/h1').text
        assert 'Template Manager' in title
        #Check current tab
        tab = selenium.find_element_by_xpath('//li[@class=" current_page_item "]/a').text
        assert 'Templates & Types' in tab
        subtab = selenium.find_element_by_xpath('descendant::li[@class=" current_page_item "][2]/a').text
        assert 'Manage XSLT' in subtab
        return selenium



if __name__ == '__main__':
    unittest.main()