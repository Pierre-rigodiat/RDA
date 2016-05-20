from io import BytesIO

from mgi.common import LXML_SCHEMA_NAMESPACE
from modules.builtin.models import CheckboxesModule, OptionsModule, InputModule, \
    TextAreaModule
from modules.models import Module
import os
from forms import NamePIDForm, DateForm
import lxml.etree as etree
from django.template import Context, Template
from pymongo import MongoClient
from django.utils.importlib import import_module
settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
MONGODB_URI = settings.MONGODB_URI
MGI_DB = settings.MGI_DB
from mgi import models as mgi_models, common
import random
import string

RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules', 'registry', 'resources')
TEMPLATES_PATH = os.path.join(RESOURCES_PATH, 'html')
SCRIPTS_PATH = os.path.join(RESOURCES_PATH, 'js')
STYLES_PATH = os.path.join(RESOURCES_PATH, 'css')


class RegistryCheckboxesModule(CheckboxesModule):
    """
    Module to transform an enumeration in checkboxes
    """
    def __init__(self, xml_tag):
        self.xml_tag = xml_tag
        self.selected = []
        CheckboxesModule.__init__(self, options={}, label='', name='')

        # This modules automatically manages occurences
        self.is_managing_occurences = True

    def _get_module(self, request):
        self.selected = []
        # get the values of the enumeration
        xml_doc_tree_str = request.session['xmlDocTree']
        xml_doc_tree = etree.fromstring(xml_doc_tree_str)

        namespaces = common.get_namespaces(BytesIO(str(xml_doc_tree_str)))

        # get the element where the module is attached
        xsd_element = xml_doc_tree.xpath(request.GET['xsd_xpath'], namespaces=namespaces)[0]
        xsd_element_type = xsd_element.attrib['type']
        # remove ns prefix if present
        if ':' in xsd_element_type:
            xsd_element_type = xsd_element_type.split(':')[1]
        xpath_type = "./{0}simpleType[@name='{1}']".format(LXML_SCHEMA_NAMESPACE, xsd_element_type)
        elementType = xml_doc_tree.find(xpath_type)
        enumeration_list = elementType.findall('./{0}restriction/{0}enumeration'.format(LXML_SCHEMA_NAMESPACE))
        
        for enumeration in enumeration_list:
            self.options[enumeration.attrib['value']] = enumeration.attrib['value']
        if 'data' in request.GET:
            data = request.GET['data']
            # get XML to reload
            reload_data = etree.fromstring("<root>" + data + "</root>")
            for child in reload_data:
                self.selected.append(child.text.strip())
        
        return CheckboxesModule.get_module(self, request)

    def _get_display(self, request):
        self.wrong_values = []
        for value in self.selected:
            if value not in self.options.values():
                self.wrong_values.append(value)
        if len(self.wrong_values) > 0:
            return '<span style="color:red;">Incorrect values found: ' + ', '.join(self.wrong_values) + "</span>"

        return ''

    def _get_result(self, request):
        xml_result = ''
        for value in self.selected:
            if value not in self.wrong_values:
                xml_result += '<' + self.xml_tag + '>' + value + '</' + self.xml_tag + '>'
        return xml_result

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        xml_result = ''
        if 'data[]' in request.POST:
            for value in dict(request.POST)['data[]']:
                xml_result += '<' + self.xml_tag + '>' + value + '</' + self.xml_tag + '>'
        return xml_result


class NamePIDModule(Module):
    """
    Name PID Module
    """
    def __init__(self):        
        Module.__init__(self, scripts=[os.path.join(SCRIPTS_PATH, 'namepid.js')])

    def _get_module(self, request):
        with open(os.path.join(TEMPLATES_PATH, 'name_pid.html'), 'r') as template_file:
            template_content = template_file.read()
            template = Template(template_content)

            self.params = {}
            if 'data' in request.GET:
                self.params['name'] = request.GET['data']
            if 'attributes' in request.GET:
                if 'pid' in request.GET['attributes']:
                    self.params['pid'] = request.GET['attributes']['pid']

            xml_xpath = request.GET['xml_xpath']
            xml_xpath = xml_xpath.split('/')[-1]
            idx = xml_xpath.rfind("[")
            xml_xpath = xml_xpath[0:idx]

            self.params['tag'] = xml_xpath

            context = Context({'form': NamePIDForm(self.params)})
            return template.render(context)

    def _get_display(self, request):
        return ''

    def _get_result(self, request):
        pid = ' pid="' + self.params['pid'] + '"' if 'pid' in self.params else ''
        name = self.params['name'] if 'name' in self.params else ''
        return '<' + self.params['tag'] + pid + '>' + name + '</' + self.params['tag'] + '>'

    def _post_display(self, request):
        form = NamePIDForm(request.POST)
        if not form.is_valid():
            return '<p style="color:red;">Entered values are not correct.</p>'
        return ''

    def _post_result(self, request):
        result_xml = ''

        form = NamePIDForm(request.POST)
        if form.is_valid():
            if 'name' in request.POST and request.POST['name'] != '':
                pid = ' pid="' + request.POST['pid'] + '"' if 'pid' in request.POST and len(
                    request.POST['pid']) > 0 else ''
                return '<' + request.POST['tag'] + pid + '>' + request.POST['name'] + '</' + request.POST['tag'] + '>'

        return '<' + request.POST['tag'] + '></' + request.POST['tag'] + '>'


class RelevantDateModule(Module):
    """
    Relevant Date Module
    """
    def __init__(self):
        Module.__init__(self, scripts=[os.path.join(SCRIPTS_PATH, 'relevantdate.js')])

    def _get_module(self, request):
        with open(os.path.join(TEMPLATES_PATH, 'relevant_date.html'), 'r') as template_file:
            template_content = template_file.read()
            template = Template(template_content)

            self.params = {}
            if 'data' in request.GET:
                self.params['date'] = request.GET['data']
            if 'attributes' in request.GET:
                if 'role' in request.GET['attributes']:
                    self.params['role'] = request.GET['attributes']['role']

            xml_xpath = request.GET['xml_xpath']
            xml_xpath = xml_xpath.split('/')[-1]
            idx = xml_xpath.rfind("[")
            xml_xpath = xml_xpath[0:idx]

            self.params['tag'] = xml_xpath

            context = Context({'form': DateForm(self.params)})
            return template.render(context)

    def _get_display(self, request):
        return ''

    def _get_result(self, request):
        role = ' role="' + self.params['role'] + '"' if 'role' in self.params else ''
        date = self.params['date'] if 'date' in self.params else ''
        return '<' + self.params['tag'] + role + '>' + date + '</' + self.params['tag'] + '>'

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        result_xml = ''

        form = DateForm(request.POST)
        if form.is_valid():
            if 'date' in request.POST and request.POST['date'] != '':
                role = ' role="' + request.POST['role'] + '"' if 'role' in request.POST and len(
                    request.POST['role']) > 0 else ''
                return '<' + request.POST['tag'] + role + '>' + request.POST['date'] + '</' + request.POST['tag'] + '>'

        return '<' + request.POST['tag'] + '></' + request.POST['tag'] + '>'


class StatusModule(OptionsModule):
    """
    Module to manage the status attribute
    """
    def __init__(self):
        self.options = {
            'inactive': 'Inactive',
            'active': 'Active',
            'deleted': 'Deleted',
        }

        OptionsModule.__init__(self, options=self.options, disabled=True)

    def _get_module(self, request):
        self.selected = "active"
        if 'data' in request.GET:
            if request.GET['data'] in self.options.keys():
                self.disabled = False
                self.selected = request.GET['data']
        return OptionsModule.get_module(self, request)

    def _get_display(self, request):
        return ''

    def _get_result(self, request):
        return self.selected

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        return str(request.POST['data'])


class LocalIDModule(InputModule):
    """
    Module to manage the Local ID attribute
    """
    def __init__(self):
        InputModule.__init__(self, disabled=True)

    def _get_module(self, request):
        if 'data' in request.GET:
            self.default_value = request.GET['data']
        else:
            # create a connection
            client = MongoClient(MONGODB_URI)
            # connect to the db 'mgi'
            db = client[MGI_DB]
            # get the xmldata collection
            xmldata = db['xmldata']
            # find all objects of the collection
            cursor = xmldata.find()
            # build a list with the objects
            existing_localids = []
            for result in cursor:
                try:
                    existing_localids.append(result['content']['Resource']['@localid'])
                except:
                    pass

            N = 20
            localid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
            while localid in existing_localids:
                localid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

            self.default_value = localid
        return InputModule.get_module(self, request)

    def _get_display(self, request):
        return ''

    def _get_result(self, request):
        return self.default_value

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        return str(request.POST['data'])


class DescriptionModule(TextAreaModule):
    """
    Module to replace description fields by textareas
    """

    def __init__(self):
        self.data = ''
        TextAreaModule.__init__(self)

    def _get_module(self, request):
        if 'data' in request.GET:
            self.data = str(request.GET['data'])
        return TextAreaModule.get_module(self, request)

    def _get_display(self, request):
        return ''

    def _get_result(self, request):
        # return '<description>' + self.data + '</description>'
        return self.data

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        # return '<description>' + request.POST['data'] + '</description>'
        return request.POST['data']


class TypeModule(InputModule):
    """
    Module to lock type field to selected resource type
    """

    templates = {
        'organization': 'Organization',
        'datacollection': 'Data Collection',
        'repository': 'Repository',
        'projectarchive': 'Project Archive',
        'database': 'Database',
        'dataset': 'Dataset',
        'service': 'Service',
        'informational': 'Informational',
        'software': 'Software',
    }

    def __init__(self):
        self.default_value = ''
        InputModule.__init__(self, disabled=True)

    def _get_module(self, request):
        if 'data' in request.GET:
            self.default_value = request.GET['data']
            # if data present and not in enumeration, can be edited
            if self.default_value not in self.templates.values():
                self.disabled = False
        else:
            if 'currentTemplateID' in request.session:
                try:
                    template = mgi_models.Template.objects().get(pk=request.session['currentTemplateID'])
                    template_name = template.title
                    try:
                        self.default_value = self.templates[template_name]
                    except:
                        self.disabled = False
                        self.default_value = ''
                except:
                    self.disabled = False
                    self.default_value = ''
            else:
                self.disabled = False
                self.default_value = ''
        return InputModule.get_module(self, request)

    def _get_display(self, request):
        if self.default_value not in self.templates.values():
            return '<span style="color:red;">Type should be in ' + ','.join(self.templates.values()) + ' </span>'
        return ''

    def _get_result(self, request):
        return self.default_value

    def _post_display(self, request):
        if request.POST['data'] not in self.templates.values():
            return '<span style="color:red;">Type should be in ' + ', '.join(self.templates.values()) + ' </span>'
        return ''

    def _post_result(self, request):
        return str(request.POST['data'])
