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

from mgi.models import SavedQuery, Jsondata, Template, TemplateVersion
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
import json
from rdflib.plugins.parsers.pyRdfa.extras.httpheader import content_type
from lxml import etree

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
        Test case for json data detail
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
     
# DO NOT USE on production environment because it adds triples that can't be removed for now
# class CurateTestCase(APITestCase):
#     """
#         Test case for curate
#     """
#      
#     def test_POST(self):
#         url = reverse('curate')
#         params = {"title":"title","schema":"schema","content":"<test>value</test>"}
#           
#         # Test post new data
#         nbData = len(Jsondata.objects())
#         response = self.client.post(url, data=params)
#         
#         # Test HTTP Response CREATED
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         
#         # Test that the document was well inserted
#         self.assertEqual(nbData + 1, len(Jsondata.objects()))
#         query = {"title":"title","schema":"schema"}
#         
#         # Delete the data
#         results = Jsondata.find(query)
#         Jsondata.delete(results[0]['_id'])
        
class ExploreTestCase(APITestCase):
    """
        Test case for explore
    """
    
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
    """
        Test case for query by example
    """
     
    def test_POST(self):
        url = reverse('query_by_example')
        data = Jsondata(schemaID="schema", xml="<el1><el2><el3>test</el3></el2></el1>", title="test")
        id = data.save()
        
        params = {"query": {"content.el1.el2.el3" : "test"}}        
        response = self.client.post(url, data=params, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual('"_id": "'+str(id)+'"' in response.content, True)
        Jsondata.delete(str(id))
        
class SparqlTestCase(APITestCase):
    """
        Test case for sparql endpoint
    """
     
    def test_POST(self):
        url = reverse('sparql_query')
        params = {"query": "SELECT * WHERE {?s ?p ?o}"}        
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        params = {"query": "SELECT * WHERE {?s ?p ?o}","format":"xml"}        
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        etree.fromstring(eval(response.content)['content'])
    
class AddSchemaTestCase(APITestCase):
    """
        Test case for schema addition
    """
     
    def test_POST(self):
        url = reverse('add_schema')
        
        # TEST HTTP 201 CREATED
        params = {"title": "title","filename":"filename","content":"content"}        
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        template = Template.objects(title = "title", filename = "filename", content = "content")[0]
        TemplateVersion.objects.get(pk=template.templateVersion).delete()
        template.delete()
          
        # TEST HTTP 201 CREATED (with version)
        template1 = Template(title = "title1", filename = "filename1", content = "content1").save()
        templateVersion = TemplateVersion(versions=[str(template1.id)], current=str(template1.id)).save()
        params = {"title": "title","filename":"filename","content":"content","templateVersion":str(templateVersion.id)}        
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Template.objects(title = "title", filename = "filename", content = "content")[0].delete()
        Template.objects.get(pk=template1.id).delete()
        TemplateVersion.objects.get(pk=templateVersion.id).delete()
        
        # TEST HTTP 400 BAD REQUEST (with wrong version id)        
        params = {"title": "title","filename":"filename","content":"content","templateVersion":"NOT_A_VALID_ID"}        
        response = self.client.post(url, data=params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)      
        
        
class SelectSchemaTestCase(APITestCase):
    """
        Test case for schema selection
    """
     
    def test_GET(self):
        # Test insert a template and get it
        template = Template(title = "title", filename = "filename", content = "content").save()
        id = template.id
          
        url = '/api/schema/select/' + str(id)
        response = self.client.get(url)
          
        self.assertEqual(response.status_code, HTTP_200_OK)
        template = response.data
        self.assertEqual(template['title'],"title")
        self.assertEqual(template['filename'],"filename")
        self.assertEqual(template['content'],"content")
        Template(id=str(id)).delete()
        
class DeleteSchemaTestCase(APITestCase):
    """
        Test case for schema deletion
    """
     
    def test_GET(self):
        # Test insert a template and get it
        template = Template(title = "title", filename = "filename", content = "content").save()
        id = template.id
          
        nbTemplates = len(Template.objects)
          
        url = '/api/schema/delete/' + str(id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
          
        currentNbTemplates = len(Template.objects)
        self.assertEqual(currentNbTemplates, nbTemplates - 1)
