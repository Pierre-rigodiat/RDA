from exporter.builtin.models import BasicExporter
from exporter.csv.models import CSVExporter
import unittest
from exporter import get_exporter

class Test(unittest.TestCase):
    def test_get_exporter(self):
        instance = get_exporter('exporter.builtin.models.BasicExporter')
        instanceBis = get_exporter('exporter.csv.models.CSVExporter')
        self.assertEquals(isinstance(instance, BasicExporter), True)
        self.assertEquals(isinstance(instanceBis, CSVExporter), True)
