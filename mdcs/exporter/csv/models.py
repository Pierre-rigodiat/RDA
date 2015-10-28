from exporter.builtin.models import XSLTExporter
import lxml.etree as etree
import os
import re
from django.conf import settings

RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'exporter/csv/resources/')

class CSVExporter(XSLTExporter):

    def __init__(self):
        #Invoke parent constructor
        dir = os.path.join(RESOURCES_PATH, 'xslt/xml2csv.xsl')
        xslt = open(dir,'r')
        contentXslt = xslt.read()
        xslt.close()
        super(CSVExporter, self).__init__(contentXslt)
        self.name = "CSV"
        self.extension= ".csv"

    def _transform(self, results):
        transformation = ""
        returnTransformation = []
        try:
            #Invoke parent transformation
            transformation = super(CSVExporter, self)._transform(results)
            #We generate one file per table
            for result in transformation:
                nb_table = 1;
                xml = result['content']
                if xml != "":
                    #We remove the extension
                    result['title'] = os.path.splitext(result['title'])[0]
                    try:
                        data = xml.split("---END TABLE---\n")
                        data = filter(None, data)
                        if len(data) == 1:
                            returnTransformation.append({'title':result['title'], 'content': str(data[0])})
                        else:
                            for res in data:
                                returnTransformation.append({'title':result['title']+"_Table"+str(nb_table), 'content': str(res)})
                                nb_table += 1
                    except etree.ParseError as e:
                        raise
                    except:
                        raise
        except etree.ParseError as e:
            raise
        except:
            raise

        return returnTransformation




