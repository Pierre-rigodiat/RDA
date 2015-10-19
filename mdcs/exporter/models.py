from abc import ABCMeta, abstractmethod

class Exporter(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.name = "Results"


    def _transformAndZip(self, instance, results, zip):
        resultsTransform = self._transform(results)
        for result in resultsTransform:
            if instance == None:
                zip.writestr(self.name+"/"+result['title'], result['content'])
            else:
                zip.writestr(self.name+"/"+self.name+instance+"/"+result['title'], result['content'])

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

