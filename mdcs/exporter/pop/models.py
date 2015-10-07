from exporter.models import Exporter
from django.conf import settings
import lxml.etree as etree
from io import BytesIO
from exporter.builtin.models import XSLTExporter
import os

RESOURCES_PATH = os.path.join(os.path.dirname(__file__), 'resources')

class POPExporter(Exporter):

    def __init__(self):
        #Invoke parent constructor
        self.name = "POP"

    def _transform(self, results):
        transformation = ""
        try:
            contentXml = '<root>'
            for result in results:
                xml = result['content'].replace('<?xml version="1.0" encoding="utf-8"?>',"")
                if xml != "":
                    contentXml += xml
            contentXml += '</root>'

            dataXML = []
            dataXML.append({'title':'Results.pop', 'content': str(contentXml)})

            #Transform many xml results files into one file
            dir = os.path.join(RESOURCES_PATH, 'xslt/many2one.xsl')
            xslt = open(dir,'r')
            contentXslt = xslt.read()
            xslt.close()
            many_to_one = XSLTExporter(contentXslt)
            res = many_to_one._transform(dataXML)

            #Take the previous file and generate one POP file
            dir = os.path.join(RESOURCES_PATH, 'xslt/xml2pop.xsl')
            xslt = open(dir,'r')
            contentXslt = xslt.read()
            xslt.close()
            xml_to_pop = XSLTExporter(contentXslt)
            transformation = xml_to_pop._transform(res)

        except etree.ParseError as e:
            raise
        except:
            raise

        return transformation

