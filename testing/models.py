from django.test import TestCase
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import requests
from datetime import datetime, timedelta
from mgi.models import Instance, XMLdata, Template, TemplateVersion
from utils.XSDhash import XSDhash
from django.contrib.auth.models import User
from oauth2_provider.models import Application

import os
from django.utils.importlib import import_module

settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
MONGODB_URI = settings.MONGODB_URI
MGI_DB = settings.MGI_DB

#from mgi.settings_test import MGI_DB, MONGODB_URI

URL_TEST = "http://127.0.0.1:8000"
OPERATION_GET = "get"
OPERATION_POST = "post"
OPERATION_DELETE = "delete"
OPERATION_POST = "post"

TEMPLATE_VALID_CONTENT = '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"> <xsd:element name="root" type="test"/> <xsd:complexType name="test"> <xsd:sequence> </xsd:sequence> </xsd:complexType> </xsd:schema>'
XMLDATA_VALID_CONTENT  = '<?xml version="1.0" encoding="utf-8"?> <root xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"></root>'
FAKE_ID = 'abcdefghijklmn'

# Constante for application token
CLIENT_ID_ADMIN = 'client_id'
CLIENT_SECRET_ADMIN = 'client_secret'
CLIENT_ID_USER = 'client_id_user'
CLIENT_SECRET_USER = 'client_secret_user'
USER_APPLICATION = 'remote_mdcs'
ADMIN_APPLICATION = 'remote_mdcs'

class RegressionTest(TestCase):

    def createXMLData(self):
        return XMLdata(schemaID='', xml='<test>test xmldata</test>', title='test', iduser=1).save()

    def createTemplate(self):
        hash = XSDhash.get_hash('<test>test xmldata</test>')
        objectVersions = self.createTemplateVersion()
        return Template(title='test', filename='test', content='<test>test xmldata</test>', version=1, templateVersion=str(objectVersions.id), hash=hash).save()

    def createTemplateWithTemplateVersion(self, templateVersionId):
        hash = XSDhash.get_hash('<test>test xmldata</test>')
        return Template(title='test', filename='test', content='<test>test xmldata</test>', version=1, templateVersion=templateVersionId, hash=hash).save()

    def createTemplateWithTemplateVersionValidContent(self, templateVersionId):
        hash = XSDhash.get_hash(TEMPLATE_VALID_CONTENT)
        return Template(title='test', filename='test', content=TEMPLATE_VALID_CONTENT, version=1, templateVersion=templateVersionId, hash=hash).save()

    def createTemplateVersion(self):
        return TemplateVersion(nbVersions=1, isDeleted=False, current=FAKE_ID).save()

    def createTemplateVersionDeleted(self):
        return TemplateVersion(nbVersions=1, isDeleted=True).save()

    def tearDown(self):
        self.clean_db()

    def clean_db(self):
        # create a connection
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi.test'
        db = client[MGI_DB]
        # clear all collections
        for collection in db.collection_names():
            try:
                if collection != 'system.indexes':
                    db.drop_collection(collection)
            except OperationFailure:
                pass


class TokenTest(RegressionTest):

    # @classmethod
    # def setUpClass(cls):
    #     user, created = User.objects.get_or_create(username = 'user')
    #     if created:
    #         user.set_password('user')
    #         user.save()
    #
    #     user_application = Application()
    #     user_application.user = user
    #     user_application.client_type = 'confidential'
    #     user_application.authorization_grant_type = 'password'
    #     user_application.name = USER_APPLICATION
    #     user_application.client_id = CLIENT_ID_USER
    #     user_application.client_secret = CLIENT_SECRET_USER
    #     user_application.save()
    #
    #     admin = User.objects.get_by_natural_key('admin')
    #
    #     admin_application = Application()
    #     admin_application.user = admin
    #     admin_application.client_type = 'confidential'
    #     admin_application.authorization_grant_type = 'password'
    #     admin_application.name = ADMIN_APPLICATION
    #     admin_application.client_id = CLIENT_ID_ADMIN
    #     admin_application.client_secret = CLIENT_SECRET_ADMIN
    #     admin_application.save()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     user = User.objects.get_by_natural_key('user')
    #     user.delete()

    def get_token(self, username, password, client_id, client_secret, application):
        try:
            url = URL_TEST + "/o/token/"
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            data = {
                'grant_type': 'password',
                'username': username,
                'password': password,
                'client_id': client_id,
                'client_secret': client_secret
            }
            r = requests.post(url=url, data=data, headers=headers, timeout=int(310000))
            if r.status_code == 200:
                now = datetime.now()
                delta = timedelta(seconds=int(eval(r.content)["expires_in"]))
                expires = now + delta

                token = Instance(name=application, protocol='http', address='127.0.0.1', port='8000',
                                 access_token=eval(r.content)["access_token"],
                                 refresh_token=eval(r.content)["refresh_token"], expires=expires).save()
                return token
            else:
                return ''
        except Exception, e:
            return ''

    def get_token_admin(self):
        return self.get_token('admin', 'admin', CLIENT_ID_ADMIN, CLIENT_SECRET_ADMIN, ADMIN_APPLICATION)

    def get_token_user(self):
        return self.get_token('user', 'user', CLIENT_ID_USER, CLIENT_SECRET_USER, USER_APPLICATION)

    def doRequest(self, token, url, data, params, operation):
        if token == '':
            self.assertTrue(False)
        headers = {'Authorization': 'Bearer ' + token.access_token}
        if operation == OPERATION_GET:
            return requests.get(URL_TEST + url, data=data, params=params, headers=headers)
        elif operation == OPERATION_DELETE:
            return requests.delete(URL_TEST + url, data=data, params=params, headers=headers)
        elif operation == OPERATION_POST:
            return requests.post(URL_TEST + url, data=data, params=params, headers=headers)

    def isStatusOK(self, r):
        if r.status_code == 200:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def isStatusNotFound(self, r):
        if r.status_code == 404:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def isStatusBadRequest(self, r):
        if r.status_code == 400:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def isStatusUnauthorized(self, r):
        if r.status_code == 401:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def isStatusNoContent(self, r):
        if r.status_code == 204:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def isStatusCreated(self, r):
        if r.status_code == 201:
            self.assertTrue(True)
        else:
            self.assertTrue(False)
