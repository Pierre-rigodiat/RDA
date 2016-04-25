################################################################################
#
# File Name: tests.py
# Application: api
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

from testing.models import TokenTest

class tests_token(TokenTest):
    def test_select_all_schema_admin(self):
        self.select_all_schema(self.get_token_admin(), False)

    def test_select_all_schema_user(self):
        self.select_all_schema(self.get_token_user(), True)

    def select_all_schema(self, token, result):
        r = self.doRequest(token, "/rest/templates/select/all", '', '')
        if r.status_code == 200:
            self.assertTrue(r.text != '')
        elif r.status_code == 401:
            self.assertTrue(result)
        else:
            self.assertFalse(False)

    def test_explore_error(self):
        r = self.doRequest(self.get_token_admin(), "/rest/explore/select/all", '', {'dataformat': 'error'})
        if r.status_code == 400:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_explore_admin(self):
        #TODO create XMLData when we will use the test database
        self.createXMLData()

        r = self.doRequest(self.get_token_admin(), "/rest/explore/select/all", '', '')
        if r.status_code == 200:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_explore_user(self):
        #TODO create XMLData when we will use the test database
        id = str(self.createXMLData())
        print('id: '+id)

        r = self.doRequest(self.get_token_user(), "/rest/explore/select/all", '', '')
        if r.status_code == 200:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


    def test_explore_delete_error_no_param(self):
        # TODO create XMLData when we will use the test database
        id = str(self.createXMLData())

        r = self.doRequest(self.get_token_admin(), "/rest/explore/delete", '', '')
        print('status code: ' + str(r.status_code))
        if r.status_code == 400:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_explore_delete_error_wrong_id(self):
        # TODO create XMLData when we will use the test database
        id = str(self.createXMLData())

        r = self.doRequest(self.get_token_admin(), "/rest/explore/delete", '', {'id': 'test'})
        print('status code: ' + str(r.status_code))
        if r.status_code == 404:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


    def test_explore_delete_error_user(self):
        r = self.doRequest(self.get_token_user(), "/rest/explore/delete", '', {'id': 'test'})
        if r.status_code == 401:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_explore_delete_admin(self):
        # TODO create XMLData when we will use the test database
        id = str(self.createXMLData())

        r = self.doRequest(self.get_token_admin(), "/rest/explore/delete", '', {'id': id})
        if r.status_code == 204:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
