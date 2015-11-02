from abc import ABCMeta, abstractmethod
import os

class Exporter(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = "Results"
        self.extension= ".xml"


    def _transformAndZip(self, instance, results, zip):
        resultsTransform = self._transform(results)
        for result in resultsTransform:
            # We check if the extension is already ok
            if self.extension and not result['title'].endswith(self.extension):
                #We remove the extension
                result['title'] = os.path.splitext(result['title'])[0]
                result['title'] += self.extension

            if instance == None:
                path = "{!s}/{!s}".format(self.name,result['title'])
                zip.writestr(path, result['content'])
            else:
                path = "{!s}/{!s} {!s}/{!s}".format(self.name,self.name,instance,result['title'])
                zip.writestr(path, result['content'])

         # fix for Linux zip files read in Windows
        for xmlFile in zip.filelist:
            xmlFile.create_system = 0


    @abstractmethod
    def _transform(self, results):
        """
            Method:
                Get the convert data
            Outputs:
                return the data converted
        """
        raise NotImplementedError("This method is not implemented.")

