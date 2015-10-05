from models import XSLTExporter, BasicExporter
import unittest
import lxml.etree as etree
from io import BytesIO
from exporter import get_exporter
import inspect

class Test(unittest.TestCase):
    def setUp(self):
        print "In method", self._testMethodName


    def test_one_file(self):
        #The list of data
        dataXML = []
        #Open the XSLT File
        xslt = open('testData/xsl-music.xsl','r')
        contentXslt = xslt.read()
        #Instanciate the exporter
        exporter = XSLTExporter(contentXslt)
        #Open the XML File
        xml = open('testData/xml2transform-1.xml','r')
        contentXml = xml.read()
        #Add the xml content to the list of data to transform
        dataXML.append({'title':'Test ', 'content': str(contentXml)})
        #Transformation
        contentRes = exporter._transform(dataXML)
        #Open the expected res
        resExpected = open('testData/xmlExporter-result.html','r')
        contentResExpected = resExpected.read()

        #Comparison
        self.assertEquals(contentRes[0]['title'], 'Test ' )
        self.assertEquals(contentRes[0]['content'], contentResExpected)


    def test_two_file(self):
        #The list of data
        dataXML = []
        #Open the XSLT File
        xslt = open('testData/xsl-music.xsl','r')
        contentXslt = xslt.read()
        #Instanciate the exporter
        exporter = XSLTExporter(contentXslt)
        #Open the XML File
        xml = open('testData/xml2transform-1.xml','r')
        contentXml = xml.read()
        #Add the xml content to the list of data to transform
        dataXML.append({'title':'Test ', 'content': str(contentXml)})
        dataXML.append({'title':'Test2 ', 'content': str(contentXml)})
        #Transformation
        contentRes = exporter._transform(dataXML)
        #Open the expected res
        resExpected = open('testData/xmlExporter-result.html','r')
        contentResExpected = resExpected.read()

        #Comparison
        self.assertEquals(contentRes[0]['title'], 'Test ')
        self.assertEquals(contentRes[0]['content'], contentResExpected)
        self.assertEquals(contentRes[1]['title'], 'Test2 ')
        self.assertEquals(contentRes[1]['content'], contentResExpected)


    def test_basicExporter(self):
        #The list of data
        dataXML = []
        xml = open('testData/xml2transform-1.xml','r')
        contentXml = xml.read()
        #Instanciate the exporter
        exporter = BasicExporter()
        #Add the xml content to the list of data to transform
        dataXML.append({'title':'Test ', 'content': str(contentXml)})
        #Transformation
        contentRes = exporter._transform(dataXML)

        #Comparison
        self.assertEquals(contentRes[0]['title'], 'Test ')
        self.assertEquals(contentRes[0]['content'], contentXml)




if __name__ == '__main__':
    unittest.main()