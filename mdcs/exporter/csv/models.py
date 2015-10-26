from exporter.builtin.models import XSLTExporter
import lxml.etree as etree
from io import BytesIO
import os
import datetime
from django.utils.timezone import activate
from django.conf import settings
from django.utils import timezone
from dateutil import tz

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

    def _transform(self, results):
        transformation = ""
        try:
            #Invoke parent transformation
            transformation = super(CSVExporter, self)._transform(results)
        except etree.ParseError as e:
            raise
        except:
            raise

        return transformation




