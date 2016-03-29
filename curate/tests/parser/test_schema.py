from django.http.request import HttpRequest
from django.test import TestCase
from django.utils.importlib import import_module
from os import walk
from os.path import splitext
from curate.parser import *
from mgi.models import FormData
from mgi.settings import SITE_ROOT
from mgi.tests import DataHandler
from lxml import etree


class ParserGenerateFormTestSuite(TestCase):
    """
    """

    def setUp(self):
        schema_data = join('curate', 'tests', 'data', 'parser')
        self.schema_data_handler = DataHandler(schema_data)

        self.request = HttpRequest()
        engine = import_module('django.contrib.sessions.backends.db')
        session_key = None
        self.request.session = engine.SessionStore(session_key)

        self.request.session['curate_edit'] = False  # Data edition

        form_data = FormData()
        form_data.name = ''
        form_data.user = ''
        form_data.template = ''

        form_data.save()

        self.request.session['curateFormData'] = form_data.pk

    def test_schema_generation(self):
        main_directory = self.schema_data_handler.dirname
        main_dir_len = len(main_directory) + 1

        filepath_list = []

        for root, dirs, files in walk(main_directory):
            for filename in files:
                file_ext = splitext(filename)

                if file_ext[1] == '.xsd':
                    full_path = join(root, file_ext[0])
                    filepath_list.append(full_path[main_dir_len:])

        report_content = []

        for filepath in filepath_list:
            report_line = filepath

            try:
                xsd_data = self.schema_data_handler.get_xsd2(filepath)
                self.request.session['xmlDocTree'] = etree.tostring(xsd_data)

                root_pk = generate_form(self.request)

                if root_pk != -1:
                    report_line += ',OK\n'
                else:
                    report_line += ',NOK\n'
            except Exception as e:
                print e
                report_line += ',EXC,' + e.message + '\n'

            report_content.append(report_line)

        with open(join(SITE_ROOT, 'full_tests_report.csv'), 'w') as report_file:
            report_file.writelines(report_content)

    # def test_sample_file(self):
    #     filepath = 'schema/namespace/include/5'
    #
    #     try:
    #         xsd_data = self.schema_data_handler.get_xsd2(filepath)
    #         self.request.session['xmlDocTree'] = etree.tostring(xsd_data)
    #
    #         root_pk = generate_form(self.request)
    #
    #         if root_pk != -1:
    #             print "Passed!"
    #         else:
    #             print "NOK"
    #     except Exception as e:
    #         print "Exception: "+e
