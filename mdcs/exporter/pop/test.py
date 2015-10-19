from models import POPExporter
import unittest

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
        #We don't take into account the first 2 lines cause of the current date
        self.assertEquals("\n".join(contentRes[0]['content'].splitlines()[2:]), "\n".join(contentResExpected.splitlines()[2:]))


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
        dataXML.append({'title':'Results.pop', 'content': str(contentXml)})
        dataXML.append({'title':'Results.pop', 'content': str(contentXml2)})
        dataXML.append({'title':'Results.pop', 'content': str(contentXml3)})

        #Transformation
        contentRes = exporter._transform(dataXML)

        #Open the expected res
        resExpected = open('testData/pop_result_many.txt','r')
        contentResExpected = resExpected.read()

        #Comparison
        self.assertEquals(contentRes[0]['title'], 'Results.pop')
        #We don't take into account the first 2 lines cause of the current date
        self.assertEquals("\n".join(contentRes[0]['content'].splitlines()[2:]), "\n".join(contentResExpected.splitlines()[2:]))



if __name__ == '__main__':
    unittest.main()