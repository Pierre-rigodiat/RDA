from exporter.models import Exporter
import lxml.etree as etree
from io import BytesIO

class XSLTExporter(Exporter):

    def __init__(self, xslt=""):
        self.name = "XSLT"
        if xslt != "":
            self._setXslt(xslt)
        self.extension= "xml"

    def _setXslt(self, xslt):
        self.xslt = xslt

        xsltParsed = etree.parse(BytesIO(xslt.encode('utf-8')))
        #We define the extension
        try:
            method = xsltParsed.find("//xsl:output",namespaces={'xsl': 'http://www.w3.org/1999/XSL/Transform'}).attrib['method']
            self.extension = ".{!s}".format(method)
        except:
            pass

        self.transform = etree.XSLT(xsltParsed)

    def _transform(self, results):
        resultsTransform = []

        if self.xslt != "":
            for result in results:
                xml = result['content']
                if xml != "":
                    try:
                        dom = etree.XML(xml.encode('utf-8'))
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
        self.extension = ".xml"

    def _transform(self, results):
        return results



