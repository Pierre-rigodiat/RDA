from modules.builtin.models import CheckboxesModule, OptionsModule, InputModule,\
    TextAreaModule
from modules.models import Module
from django.conf import settings
import os
from forms import NamePIDForm, DateForm
import lxml.etree as etree
from django.template import Context, Template
from pymongo import MongoClient
from mgi.settings import MONGODB_URI
import random
import string

RESOURCES_PATH = os.path.join(settings.SITE_ROOT, 'modules', 'registry', 'resources')
TEMPLATES_PATH = os.path.join(RESOURCES_PATH, 'html')
SCRIPTS_PATH = os.path.join(RESOURCES_PATH, 'js')
STYLES_PATH = os.path.join(RESOURCES_PATH, 'css')

class RegistryCheckboxesModule(CheckboxesModule):
    
    def __init__(self, xml_tag):
                 
        self.xml_tag = xml_tag
        CheckboxesModule.__init__(self, options={}, label='', name='')

    def _get_module(self, request):
        # get the values of the enumeration
        namespaces = request.session['namespaces']
        defaultPrefix = request.session['defaultPrefix']
        xmlDocTreeStr = request.session['xmlDocTree']
        xmlDocTree = etree.fromstring(xmlDocTreeStr)
    
        namespace = namespaces[defaultPrefix]
    
        xpath_namespaces = {}
        for prefix, ns in request.session['namespaces'].iteritems():
            xpath_namespaces[prefix] = ns[1:-1]
        
        # get the element where the module is attached
        xsd_element = xmlDocTree.xpath(request.GET['xsd_xpath'], namespaces=xpath_namespaces)[0]
        xsd_element_type = xsd_element.attrib['type']
        xpath_type = "./{0}simpleType[@name='{1}']".format(namespace, xsd_element_type)
        elementType = xmlDocTree.find(xpath_type)
        enumeration_list = elementType.findall('./{0}restriction/{0}enumeration'.format(namespace))
        
        for enumeration in enumeration_list:
            self.options[enumeration.attrib['value']] = enumeration.attrib['value']
        
        return CheckboxesModule.get_module(self, request)

    def _get_display(self, request):
        return '<div class="error_nmrr">The element ' + self.xml_tag + ' should be removed if no checkboxes are checked.</div>'

    def _get_result(self, request):
        return ''

    def _post_display(self, request):
        display = ''
        if not 'data[]' in request.POST:
            return '<div class="error_nmrr">The element ' + request.xml_tag + ' should be removed if no checkboxes are checked.</div>'
        return display
                

    def _post_result(self, request):
        xml_result = ''        
        if 'data[]' in request.POST:        
            for value in dict(request.POST)['data[]']:
                xml_result += '<' + self.xml_tag + '>' + value + '</' + self.xml_tag + '>'    
        return xml_result
    
    
class NamePIDModule(Module):
    
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
        pid = ' pid="'+ self.params['pid'] +'"' if 'pid' in self.params else ''
        name = self.params['name'] if 'name' in self.params else ''
        return '<' + self.params['tag'] + pid + '>' +  name + '</' + self.params['tag'] + '>'


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
                pid = ' pid="'+ request.POST['pid'] +'"' if 'pid' in request.POST and len(request.POST['pid']) > 0 else ''
                return '<' + request.POST['tag'] + pid + '>' +  request.POST['name'] + '</' + request.POST['tag'] + '>'
            
        return result_xml


  
class RelevantDateModule(Module):
    
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
        return '<div class="error_nmrr">The element ' + self.params['tag'] + ' should respect the following format yyyy-mm-dd.</div>'


    def _get_result(self, request):
        role = ' role="'+ self.params['role'] +'"' if 'role' in self.params else ''
        date = self.params['date'] if 'date' in self.params else ''
        return '<' + self.params['tag'] + role + '>' +  date + '</' + self.params['tag'] + '>'


    def _post_display(self, request):
        form = DateForm(request.POST)
        if not form.is_valid():
            return '<div class="error_nmrr">The element ' + self.params['tag'] + ' should respect the following format yyyy-mm-dd.</div>'
        return ''


    def _post_result(self, request):
        result_xml = ''
        
        form = DateForm(request.POST)
        if form.is_valid():
            if 'date' in request.POST and request.POST['date'] != '':
                role = ' role="'+ request.POST['role'] +'"' if 'role' in request.POST and len(request.POST['role']) > 0 else ''
                return '<' + request.POST['tag'] + role + '>' +  request.POST['date'] + '</' + request.POST['tag'] + '>'
            
        return result_xml
    


class StatusModule(OptionsModule):
    
    def __init__(self):
        self.options = {
            'inactive': 'Inactive',
            'active': 'Active',
            'deleted': 'Deleted',
        }
                
        OptionsModule.__init__(self, options=self.options, disabled=True)

    def _get_module(self, request):
        self.selected = "inactive"
        return OptionsModule.get_module(self, request)

    def _get_display(self, request):
        self.selected = "inactive"
        if 'data' in request.GET:
            if request.GET['data'] in self.options.keys():
                self.selected = request.GET['data']
        return ''

    def _get_result(self, request):
        return self.selected

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        return str(request.POST['data'])
    

class LocalIDModule(InputModule):
    
    def __init__(self):               
        InputModule.__init__(self, disabled=True)

    def _get_module(self, request):
        # create a connection
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client['mgi']
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
        if 'data' in request.GET:
            self.default_value = request.GET['data']
        return ''

    def _get_result(self, request):
        return self.default_value

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        return str(request.POST['data'])
    

class DescriptionModule(TextAreaModule):
    
    def __init__(self):                
        TextAreaModule.__init__(self)

    def _get_module(self, request):
        return TextAreaModule.get_module(self, request)

    def _get_display(self, request):
        if 'data' in request.GET:
            self.data = request.GET['data']
        return ''

    def _get_result(self, request):
        return self.data

    def _post_display(self, request):
        return ''

    def _post_result(self, request):
        return str(request.POST['data'])