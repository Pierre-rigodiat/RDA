from models import XSLTExporter, POPExporter
import unittest
import lxml.etree as etree
from io import BytesIO
from exporter import get_exporter
import inspect
import os
from django.conf import settings

class Test(unittest.TestCase):
    def setUp(self):
        print "In method", self._testMethodName


    def test_one_file(self):
        #The list of data
        dataXML = []
        #Instanciate the exporter
        exporter = POPExporter()
        #Open the XML File
        xml = open('testData/result1.xml','r')
        contentXml = xml.read()
        #Add the xml content to the list of data to transform
        dataXML.append({'title':'Results.pop', 'content': str(contentXml)})

        #Transformation
        contentRes = exporter._transform(dataXML)

        #Open the expected res
        resExpected = open('testData/pop_result_one.txt','r')
        contentResExpected = resExpected.read()

        #Comparison
        self.assertEquals(contentRes[0]['title'], 'Results.pop')
        self.assertEquals(contentRes[0]['content'], "\n".join(contentResExpected.splitlines()))


    def test_many_files(self):
        #The list of data
        dataXML = []
        #Instanciate the exporter
        exporter = POPExporter()
        #Open the XML File
        contentXml = open('testData/result1.xml','r').read()
        contentXml2 = open('testData/result2.xml','r').read()
        contentXml3 = open('testData/result3.xml','r').read()
        #Add the xml content to the list of data to transform
        dataXML.append({'title':'Results ', 'content': str(contentXml)})
        dataXML.append({'title':'Results ', 'content': str(contentXml2)})
        dataXML.append({'title':'Results ', 'content': str(contentXml3)})

        #Transformation
        contentRes = exporter._transform(dataXML)

        #Open the expected res
        resExpected = open('testData/pop_result_many.txt','r')
        contentResExpected = resExpected.read()

        #Comparison
        self.assertEquals(contentRes[0]['title'], 'Results.pop')
        self.assertEquals(contentRes[0]['content'], "\n".join(contentResExpected.splitlines()))



if __name__ == '__main__':
    unittest.main()