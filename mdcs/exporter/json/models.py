from exporter.builtin.models import Exporter
import lxml.etree as etree
import os
import json
import xmltodict

def postprocessor(path, key, value):
        if(key == "#text"):
            return key, str(value)
        try:
            return key, int(value)
        except (ValueError, TypeError):
            try:
                return key, float(value)
            except (ValueError, TypeError):
                return key, value

class JSONExporter(Exporter):

    def __init__(self):
        self.name = "JSON"
        self.extension= ".json"

    def _transform(self, results):
        returnTransformation = []
        try:
            for result in results:
                xml = result['content']
                if xml != "":
                    #We remove the extension
                    result['title'] = os.path.splitext(result['title'])[0]
                    try:
                        contentEncoded = xmltodict.parse(xml,postprocessor=postprocessor)
                        transformation = json.dumps(contentEncoded, indent=4)
                        returnTransformation.append({'title':result['title'], 'content': transformation})
                    except etree.ParseError as e:
                        raise
                    except:
                        raise
        except etree.ParseError as e:
            raise
        except:
            raise

        return returnTransformation




