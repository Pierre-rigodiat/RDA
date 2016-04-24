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

import requests
from django.test import TestCase
from datetime import datetime, timedelta
from mgi.models import Instance
from pymongo import MongoClient
from mgi.settings import MONGODB_URI
from pymongo.errors import OperationFailure
from mgi.models import XMLdata

URL_TEST = "http://127.0.0.1:8000"


class tests_token(TestCase):

    def tearDown(self):
        #todo delete when we will use only the test database
        Instance.drop_collection()

        self.clean_db()

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

    def get_token(self, username, password, client_id, client_secret):
        try:
            url = "http://127.0.0.1:8000" + "/o/token/"
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

                token = Instance(name='remote_mdcs', protocol='http', address='127.0.0.1', port='8000', access_token=eval(r.content)["access_token"], refresh_token=eval(r.content)["refresh_token"], expires=expires).save()
                return token
            else:
                return ''
        except Exception, e:
            return ''

    def get_token_admin(self):
        return self.get_token('admin', 'admin', 'client_id', 'client_secret')

    def get_token_user(self):
        return self.get_token('user', 'user', 'client_id_user', 'client_secret_user')

    def test_select_all_schema_admin(self):
        self.select_all_schema(self.get_token_admin(), False)

    def test_select_all_schema_user(self):
        self.select_all_schema(self.get_token_user(), True)

    def select_all_schema(self, token, result):
        if token == '':
            self.assertTrue(False)
        url = URL_TEST + "/rest/templates/select/all"
        headers = {'Authorization': 'Bearer ' + token.access_token}
        r = requests.get(url, data='', headers=headers)
        if r.status_code == 200:
            self.assertTrue(r.text != '')
        elif r.status_code == 401:
            self.assertTrue(result)
        else:
            self.assertFalse(False)

    def test_explore_error(self):
        token = self.get_token_admin()
        if token == '':
            self.assertTrue(False)
        url = URL_TEST + "/rest/explore/select/all"
        data = {'dataformat': 'error'}
        headers = {'Authorization': 'Bearer ' + token.access_token}
        r = requests.get(url, params=data, headers=headers)
        if r.status_code == 400:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def createXMLData(self):
        return XMLdata(schemaID='', xml='<test>test xmldata</test>', title='test', iduser=1).save()

    def test_explore_admin(self):
        #TODO create XMLData when we will use the test database
        self.createXMLData()

        token = self.get_token_admin()
        if token == '':
            self.assertTrue(False)
        url = URL_TEST + "/rest/explore/select/all"
        headers = {'Authorization': 'Bearer ' + token.access_token}
        r = requests.get(url, params='', headers=headers)
        if r.status_code == 200:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_explore_user(self):
        #TODO create XMLData when we will use the test database
        id = str(self.createXMLData())
        print('id: '+id)

        token = self.get_token_user()
        if token == '':
            self.assertTrue(False)
        url = URL_TEST + "/rest/explore/select/all"
        headers = {'Authorization': 'Bearer ' + token.access_token}
        r = requests.get(url, params='', headers=headers)
        if r.status_code == 200:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


    def test_explore_delete_error_no_param(self):
        # TODO create XMLData when we will use the test database
        id = str(self.createXMLData())

        token = self.get_token_admin()
        if token == '':
            self.assertTrue(False)
        url = URL_TEST + "/rest/explore/delete"
        headers = {'Authorization': 'Bearer ' + token.access_token}
        r = requests.get(url, params='', headers=headers)
        print('status code: ' + str(r.status_code))
        if r.status_code == 400:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_explore_delete_error_wrong_id(self):
        # TODO create XMLData when we will use the test database
        id = str(self.createXMLData())

        token = self.get_token_admin()
        if token == '':
            self.assertTrue(False)
        url = URL_TEST + "/rest/explore/delete"
        headers = {'Authorization': 'Bearer ' + token.access_token}
        params = {'id': 'test'}
        r = requests.get(url, params=params, headers=headers)
        print('status code: ' + str(r.status_code))
        if r.status_code == 404:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


    def test_explore_delete_error_user(self):
        token = self.get_token_user()
        if token == '':
            self.assertTrue(False)
        url = URL_TEST + "/rest/explore/delete"
        headers = {'Authorization': 'Bearer ' + token.access_token}
        params = {'id': 'test'}
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 401:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_explore_delete_admin(self):
        # TODO create XMLData when we will use the test database
        id = str(self.createXMLData())

        token = self.get_token_admin()
        if token == '':
            self.assertTrue(False)
        url = URL_TEST + "/rest/explore/delete"
        headers = {'Authorization': 'Bearer ' + token.access_token}
        params = {'id': id}
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 204:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


