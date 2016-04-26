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

from testing.models import TokenTest, OPERATION_GET, OPERATION_DELETE, OPERATION_POST, TemplateVersion, XMLDATA_VALID_CONTENT, FAKE_ID, XMLdata

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

    def test_delete_schema_error_version_id_admin(self):
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'templateVersion': 'ver', 'id':'test'}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_error_version_next_admin(self):
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'templateVersion': 'ver', 'next':'test'}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_error_version_id_next_admin(self):
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'templateVersion': 'ver', 'id':'test', 'next':'test'}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_error_version_not_exist_admin(self):
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'templateVersion': 'ver'}, OPERATION_DELETE)
        self.isStatusNotFound(r)

    def test_delete_schema_error_user(self):
        r = self.doRequest(self.get_token_user(), "/rest/templates/delete", '', {'templateVersion': 'ver', 'id':'test', 'next':'test'}, OPERATION_DELETE)
        self.isStatusUnauthorized(r)

    def test_delete_schema_error_version_already_deleted_admin(self):
        templateVersion = self.createTemplateVersionDeleted()
        r = self.doRequest(self.get_token_user(), "/rest/templates/delete", '', {'templateVersion': str(templateVersion.id)}, OPERATION_DELETE)
        self.isStatusUnauthorized(r)

    def test_delete_schema_version_admin(self):
        templateVersion = self.createTemplateVersion()
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'templateVersion': str(templateVersion.id)}, OPERATION_DELETE)
        self.isStatusOK(r)

    def test_delete_schema_no_id_admin(self):
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', '', OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_bad_id_delete_schema(self):
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':'abcdefghijklmn'}, OPERATION_DELETE)
        self.isStatusNotFound(r)

    def test_delete_schema_next_not_found_admin(self):
        template1 = self.createTemplate()
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id), 'next':'abcdefghijklmn'}, OPERATION_DELETE)
        self.isStatusNotFound(r)

    def test_delete_schema_2_templates_different_version_admin(self):
        templateVersion1 = self.createTemplateVersion()
        templateVersion2 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        template2 = self.createTemplateWithTemplateVersion(str(templateVersion2.id))
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id), 'next':str(template2.id)}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_templateversion_deleted_admin(self):
        templateVersion1 = self.createTemplateVersionDeleted()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id)}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_templateversion_current_no_next_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        templateVersion1.current = str(template1.id)
        templateVersion1.save()
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id)}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_next_same_as_current_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        templateVersion1.current = str(template1.id)
        templateVersion1.save()
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id), 'next':str(template1.id)}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_template_not_current_and_next_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        template2 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id), 'next':str(template2.id)}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_template_and_next_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        template2 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        templateVersion1.current = str(template1.id)
        templateVersion1.save()
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id), 'next':str(template2.id)}, OPERATION_DELETE)
        self.isStatusNoContent(r)
        templateVersion = TemplateVersion.objects.get(pk=template1.templateVersion)
        self.assertTrue(templateVersion.current == str(template2.id))

    def test_delete_schema_template_and_deleted_next_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        template2 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        templateVersion1.current = str(template1.id)
        templateVersion1.deletedVersions.append(str(template2.id))
        templateVersion1.save()
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id), 'next':str(template2.id)}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_delete_schema_template_not_current_no_next_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id)}, OPERATION_DELETE)
        self.isStatusNoContent(r)
        templateVersion = TemplateVersion.objects.get(pk=template1.templateVersion)
        self.assertTrue(str(template1.id) in templateVersion.deletedVersions)

    def test_delete_schema_deleted_template_not_current_no_next_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        templateVersion1.deletedVersions.append(str(template1.id))
        templateVersion1.save()
        r = self.doRequest(self.get_token_admin(), "/rest/templates/delete", '', {'id':str(template1.id)}, OPERATION_DELETE)
        self.isStatusBadRequest(r)

    def test_curate_error_serializer_admin(self):
        data = {'content': '<test> test xml </test>'}
        r = self.doRequest(self.get_token_admin(), "/rest/curate", data, '', OPERATION_POST)
        self.isStatusBadRequest(r)

    def test_curate_error_schema_admin(self):
        data = {'title': 'test', 'schema': FAKE_ID, 'content': '<test> test xml </test>'}
        r = self.doRequest(self.get_token_admin(), "/rest/curate", data, '', OPERATION_POST)
        self.isStatusBadRequest(r)

    def test_curate_error_schema_deleted_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersion(str(templateVersion1.id))
        templateVersion1.deletedVersions.append(str(template1.id))
        templateVersion1.save()
        data = {'title': 'test', 'schema':str(template1.id), 'content': '<test> test xml </test>'}
        r = self.doRequest(self.get_token_admin(), "/rest/curate", data, '', OPERATION_POST)
        self.isStatusBadRequest(r)

    def test_curate_schema_error_xml_syntax_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersionValidContent(str(templateVersion1.id))
        data = {'title': 'test', 'schema': str(template1.id), 'content': '<test> test xml </test>'}
        r = self.doRequest(self.get_token_admin(), "/rest/curate", data, '', OPERATION_POST)
        self.isStatusBadRequest(r)

    def test_curate_schema_error_xml_validation_admin(self):
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersionValidContent(str(templateVersion1.id))
        data = {'title': 'test', 'schema': str(template1.id), 'content': XMLDATA_VALID_CONTENT + '<'}
        r = self.doRequest(self.get_token_admin(), "/rest/curate", data, '', OPERATION_POST)
        self.isStatusBadRequest(r)

    def test_curate_schema_admin(self):
        self.assertTrue(len(XMLdata.objects()) == 0)
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersionValidContent(str(templateVersion1.id))
        data = {'title': 'test', 'schema': str(template1.id), 'content': XMLDATA_VALID_CONTENT}
        r = self.doRequest(self.get_token_admin(), "/rest/curate", data, '', OPERATION_POST)
        self.isStatusCreated(r)
        self.assertTrue(len(XMLdata.objects()) == 1)

    def test_curate_schema_user(self):
        self.assertTrue(len(XMLdata.objects()) == 0)
        templateVersion1 = self.createTemplateVersion()
        template1 = self.createTemplateWithTemplateVersionValidContent(str(templateVersion1.id))
        data = {'title': 'test', 'schema': str(template1.id), 'content': XMLDATA_VALID_CONTENT}
        r = self.doRequest(self.get_token_user(), "/rest/curate", data, '', OPERATION_POST)
        self.isStatusCreated(r)
        self.assertTrue(len(XMLdata.objects()) == 1)