import unittest

from modules.diffusion.models import PeriodicTableModule
from django.http.request import HttpRequest
import json


class TestPeriodicTable(unittest.TestCase):
    def setUp(self):
        pass 
            
    def test(self):     
        module = PeriodicTableModule()
        request = HttpRequest()
        
        request.method = 'GET'
        
        response = module.view(request)
        data = json.loads(response.content)
        self.assertNotEqual(len(data['module']), 0)
        self.assertEqual(data['moduleDisplay'], "No element selected")
        self.assertEqual(data['moduleResult'], "")
        
        request.method = 'POST'
        request.POST['selectedElement'] = 'Al'
        
        
        response = module.view(request)  
        data = json.loads(response.content)      
        self.assertEqual(data['moduleDisplay'], "Chosen element: Al")
        self.assertEqual(data['moduleResult'], "Al")
        
if __name__ == '__main__':
    unittest.main()