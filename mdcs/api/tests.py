################################################################################
#
# File Name: tests.py
# Application: api
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from mgi.models import SavedQuery, Jsondata
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
import json
from rdflib.plugins.parsers.pyRdfa.extras.httpheader import content_type

class SavedQueryListTestCase(APITestCase):
    def test_GET(self):
        url = reverse('savedQuery_list')
        response = self.client.get(url)
          
        # Test HTTP Response OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
          
        # Test get as many queries from the api than from mongo directly
        nbQueries = len(response.data)
        self.assertEqual(nbQueries, len(SavedQuery.objects))
          
        # Test get as many queries from the api than from mongo directly after adding 1
        query = SavedQuery(user="user",template="template",query="query", displayedQuery="displayedQuery")
        query.save()
        id = query.id 
        response = self.client.get(url)
        currentNbQueries = len(response.data)
        self.assertEqual(currentNbQueries, len(SavedQuery.objects))
        self.assertEqual(currentNbQueries, nbQueries + 1)
        SavedQuery(id=str(id)).delete()
          
    def test_POST(self):
        url = reverse('savedQuery_list')
        params = {"user":"user","template":"template","query":"query", "displayedQuery":"displayedQuery"}
          
        # Test post new saved query
        nbQueries = len(SavedQuery.objects)
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(nbQueries + 1, len(SavedQuery.objects))
        SavedQuery.objects(user="user",template="template",query="query", displayedQuery="displayedQuery")[0].delete()
          
class SavedQueryDetailsTestCase(APITestCase):
    """
        Test case for saved query detail
    """
    def test_GET(self):
        # Test insert a query and get it
        query = SavedQuery(user="user",template="template",query="query", displayedQuery="displayedQuery")
        query.save()
        id = query.id
          
        url = '/api/savedqueries/' + str(id)
        response = self.client.get(url)
          
        self.assertEqual(response.status_code, HTTP_200_OK)
        savedQuery = response.data
        self.assertEqual(savedQuery['user'],"user")
        self.assertEqual(savedQuery['template'],"template")
        self.assertEqual(savedQuery['query'],"query")
        self.assertEqual(savedQuery['displayedQuery'],"displayedQuery")
        SavedQuery(id=str(id)).delete()
           
       
    def test_PUT(self):
        # Test update a saved query
        # PUT is not PATCH (allows to update 1 field)
        query = SavedQuery(user="user",template="template",query="query", displayedQuery="displayedQuery")
        query.save()
        id = query.id
          
        url = '/api/savedqueries/' + str(id)
        response = self.client.put(url, {"user":"new user","template":"template","query":"query", "displayedQuery":"displayedQuery"})
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(SavedQuery.objects.get(id=str(id)).user, "new user")
        SavedQuery(id=str(id)).delete()
       
    def test_DELETE(self):
        # Test delete a saved query
        query = SavedQuery(user="user",template="template",query="query", displayedQuery="displayedQuery")
        query.save()
        id = query.id
          
        nbQueries = len(SavedQuery.objects)
          
        url = '/api/savedqueries/' + str(id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
          
        currentNbQueries = len(SavedQuery.objects)
        self.assertEqual(currentNbQueries, nbQueries - 1)
          
class JsonDataListTestCase(APITestCase):
    """
        Test case for json data list
    """
    def test_GET(self):
        url = reverse('jsonData_list')
        response = self.client.get(url)
          
        # Test HTTP Response OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
          
        # Test get as many data from the api than from mongo directly  
        nbData = len(response.data)
        self.assertEqual(nbData, len(Jsondata.objects()))
          
        # Test get as many data from the api than from mongo directly after adding 1
        data = Jsondata(schemaID="schema", xml="<test></test>", title="test")
        id = data.save() 
        response = self.client.get(url)
        currentNbData = len(response.data)
        self.assertEqual(currentNbData, len(Jsondata.objects()))
        self.assertEqual(currentNbData, nbData + 1)
        Jsondata.delete(str(id))
        
    def test_POST(self):
        url = reverse('jsonData_list')
        params = {"title":"title","schema":"schema","content":{"content":"content"}}
            
        # Test post new data
        nbData = len(Jsondata.objects())
        response = self.client.post(url, data=params, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(nbData + 1, len(Jsondata.objects()))
        query = {"title":"title","schema":"schema"}
        results = Jsondata.find(query)
        Jsondata.delete(results[0]['_id'])
  
class JsonDataDetailsTestCase(APITestCase):
    """
        Test case for saved query detail
    """
    def test_GET(self):
        # Test insert data and get it
        data = Jsondata(schemaID="schema", xml="<test>value</test>", title="test")
        id = data.save()
          
        url = '/api/data/' + str(id)
        response = self.client.get(url)
          
        self.assertEqual(response.status_code, HTTP_200_OK)
        jsondata = response.data
        self.assertEqual(jsondata['schema'],"schema")
        self.assertEqual(jsondata['content'],{"test":"value"})
        self.assertEqual(jsondata['title'],"test")
        Jsondata.delete(str(id))
           
       
    def test_PUT(self):
        # Test update data
        # PUT is not PATCH (allows to update 1 field)
        data = Jsondata(schemaID="schema", xml="<test>value</test>", title="test")
        id = data.save()
            
        url = '/api/data/' + str(id)
        response = self.client.put(url, json.dumps({"schema":"new schema","content":{"test":"value"},"title":"test"}), content_type='application/json')
          
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Jsondata.get(str(id))['schema'], "new schema")
        Jsondata.delete(str(id))
        
    def test_DELETE(self):
        # Test delete data
        data = Jsondata(schemaID="schema", xml="<test>value</test>", title="test")
        id = data.save()
           
        nbQueries = len(Jsondata.objects())
           
        url = '/api/data/' + str(id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
           
        currentNbQueries = len(Jsondata.objects())
        self.assertEqual(currentNbQueries, nbQueries - 1)
     
class CurateTestCase(APITestCase):
     
    def test_POST(self):
        url = reverse('curate')
        params = {"title":"title","schema":"schema","content":"<test>value</test>"}
          
        # Test post new data
        nbData = len(Jsondata.objects())
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(nbData + 1, len(Jsondata.objects()))
        query = {"title":"title","schema":"schema"}
        results = Jsondata.find(query)
        Jsondata.delete(results[0]['_id'])
        
class ExploreTestCase(APITestCase):
    
    def test_GET(self):
        url = reverse('explore')
        response = self.client.get(url)
          
        # Test HTTP Response OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
          
        # Test get as many data from the api than from mongo directly  
        nbData = len(response.data)
        self.assertEqual(nbData, len(Jsondata.objects()))
          
        # Test get as many data from the api than from mongo directly after adding 1
        data = Jsondata(schemaID="schema", xml="<test>value</test>", title="test")
        id = data.save() 
        response = self.client.get(url)
        currentNbData = len(response.data)
        self.assertEqual(currentNbData, len(Jsondata.objects()))
        self.assertEqual(currentNbData, nbData + 1)
        Jsondata.delete(str(id))
        
class QbeTestCase(APITestCase):
     
    def test_POST(self):
        url = reverse('query_by_example')
        params = {"query": {"content.Experiment.ExperimentType.TracerDiffusivity.Material.MaterialName" : "aluminum"}}        
        response = self.client.post(url, data=params, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class SparqlTestCase(APITestCase):
     
    def test_POST(self):
        url = reverse('sparql_query')
        params = {"query": "SELECT * WHERE {?s ?p ?o}"}        
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        params = {"query": "SELECT * WHERE {?s ?p ?o}","format":"xml"}        
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
