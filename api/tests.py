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

from testing.models import TokenTest, OPERATION_GET, OPERATION_DELETE

class tests_token(TokenTest):
    def test_select_all_schema_admin(self):
        r = self.doRequest(self.get_token_admin(), "/rest/templates/select/all", '', '', OPERATION_GET)
        if r.status_code == 200:
            self.assertTrue(r.text != '')
        else:
            self.assertFalse(False)

    def test_select_all_schema_user(self):
        r = self.doRequest(self.get_token_user(), "/rest/templates/select/all", '', '', OPERATION_GET)
        self.isStatusUnauthorized(r)

    def test_select_schema_error_no_param(self):
        r = self.doRequest(self.get_token_admin(), "/rest/templates/select", '', '', OPERATION_GET)
        self.isStatusBadRequest(r)

    def test_select_schema_error_no_schema(self):
        param = {'id':'test'}
        r = self.doRequest(self.get_token_admin(), "/rest/templates/select", '', param, OPERATION_GET)
        self.isStatusNotFound(r)

    def test_select_schema_error_user(self):
        param = {'id':'test'}
        r = self.doRequest(self.get_token_user(), "/rest/templates/select", '', param, OPERATION_GET)
        self.isStatusUnauthorized(r)

    def test_select_schema_admin_id(self):
        templateID = self.createTemplate()
        param = {'id': templateID.id}
        r = self.doRequest(self.get_token_admin(), "/rest/templates/select", '', param, OPERATION_GET)
        self.isStatusOK(r)

    def test_explore_error(self):
        r = self.doRequest(self.get_token_admin(), "/rest/explore/select/all", '', {'dataformat': 'error'}, OPERATION_GET)
        self.isStatusBadRequest(r)

    def test_explore_admin(self):
        self.createXMLData()
        r = self.doRequest(self.get_token_admin(), "/rest/explore/select/all", '', '', OPERATION_GET)
        self.isStatusOK(r)

    def test_explore_user(self):
        r = self.doRequest(self.get_token_user(), "/rest/explore/select/all", '', '', OPERATION_GET)
        self.isStatusOK(r)

    def test_explore_delete_error_no_param(self):
        r = self.doRequest(self.get_token_admin(), "/rest/explore/delete", '', '', OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_explore_delete_error_wrong_id(self):
        r = self.doRequest(self.get_token_admin(), "/rest/explore/delete", '', {'id': 'test'}, OPERATION_DELETE)
        self.isStatusNotFound(r)

    def test_explore_delete_error_user(self):
        r = self.doRequest(self.get_token_user(), "/rest/explore/delete", '', {'id': 'test'}, OPERATION_DELETE)
        self.isStatusUnauthorized(r)

    def test_explore_delete_admin(self):
        id = str(self.createXMLData())
        r = self.doRequest(self.get_token_admin(), "/rest/explore/delete", '', {'id': id}, OPERATION_DELETE)
        self.isStatusNoContent(r)
