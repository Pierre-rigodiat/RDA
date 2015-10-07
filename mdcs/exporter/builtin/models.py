from exporter.models import Exporter
import lxml.etree as etree
from io import BytesIO
import xmltodict

class XSLTExporter(Exporter):

    def __init__(self, xslt=""):
        self.name = "XSLT"
        if xslt != "":
            self._setXslt(xslt)

    def _setXslt(self, xslt):
        self.xslt = xslt
        xsltParsed = etree.parse(BytesIO(xslt.encode('utf-8')))
        self.transform = etree.XSLT(xsltParsed)

    def _transform(self, results):
        resultsTransform = []

        if self.xslt != "":
            for result in results:
                xml = result['content']
                if xml != "":
                    try:
                        dom = etree.fromstring(str(xml.replace('<?xml version="1.0" encoding="utf-8"?>\n',"")))
                        newdom = self.transform(dom)
                        resultsTransform.append({'title':result['title'], 'content': str(newdom)})
                    except etree.ParseError as e:
                        raise
                    except:
                        raise

        return resultsTransform


class BasicExporter(Exporter):
    def __init__(self):
        self.name = "XML"

    def _transform(self, results):
        return results



