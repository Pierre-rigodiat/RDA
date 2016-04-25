from django.test import TestCase
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import requests
from datetime import datetime, timedelta
from mgi.models import Instance, XMLdata

from django.utils.importlib import import_module
import os
settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
MONGODB_URI = settings.MONGODB_URI
MGI_DB = settings.MGI_DB

URL_TEST = "http://127.0.0.1:8000"
OPERATION_GET = "get"
OPERATION_POST = "post"
OPERATION_DELETE = "delete"

class RegressionTest(TestCase):

    def createXMLData(self):
        return XMLdata(schemaID='', xml='<test>test xmldata</test>', title='test', iduser=1).save()

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

    def get_token(self, username, password, client_id, client_secret):
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

                token = Instance(name='remote_mdcs', protocol='http', address='127.0.0.1', port='8000',
                                 access_token=eval(r.content)["access_token"],
                                 refresh_token=eval(r.content)["refresh_token"], expires=expires).save()
                return token
            else:
                return ''
        except Exception, e:
            return ''

    def get_token_admin(self):
        return self.get_token('admin', 'admin', 'client_id', 'client_secret')

    def get_token_user(self):
        return self.get_token('user', 'user', 'client_id_user', 'client_secret_user')

    def doRequest(self, token, url, data, params, operation):
        if token == '':
            self.assertTrue(False)
        headers = {'Authorization': 'Bearer ' + token.access_token}
        if operation == OPERATION_GET:
            return requests.get(URL_TEST + url, data=data, params=params, headers=headers)
        elif operation == OPERATION_DELETE:
            return requests.delete(URL_TEST + url, data=data, params=params, headers=headers)