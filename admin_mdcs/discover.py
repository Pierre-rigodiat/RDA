################################################################################
#
# File Name: discover.py
# Purpose:
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
#         Pierre Francois RIGODIAT
#		  pierre-francois.rigodiat@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################
from django.contrib.auth.models import Permission, Group
from mgi.rights import anonymous_group, default_group, explore_access, curate_access, \
    curate_edit_document, curate_delete_document, api_access
from pymongo import MongoClient
import os
from django.utils.importlib import import_module
settings_file = os.environ.get("DJANGO_SETTINGS_MODULE")
settings = import_module(settings_file)
MONGODB_URI = settings.MONGODB_URI
SITE_ROOT = settings.SITE_ROOT
MGI_DB = settings.MGI_DB
from mgi.models import Template, Type, create_template, create_type, TemplateVersion
from utils.XSDhash import XSDhash
STATIC_DIR = os.path.join(SITE_ROOT, 'static', 'resources', 'xsd')

def init_rules():
    """
    Init of group and permissions for the application.
    If the anonymous group does not exist, creation of the group with associate permissions
    If the default group does not exist, creation of the group with associate permissions
    """
    try:
        ###########################################
        #### Get or Create the Group anonymous ####
        ###########################################
        anonymousGroup, created = Group.objects.get_or_create(name=anonymous_group)
        if not created:
            anonymousGroup.permissions.clear()

        #We add the exploration_access by default
        explore_access_perm = Permission.objects.get(codename=explore_access)
        anonymousGroup.permissions.add(explore_access_perm)

        # Get or Create the default basic
        defaultGroup, created = Group.objects.get_or_create(name=default_group)
        if not created:
            defaultGroup.permissions.clear()
        explore_access_perm = Permission.objects.get(codename=explore_access)
        curate_access_perm = Permission.objects.get(codename=curate_access)
        curate_edit_perm = Permission.objects.get(codename=curate_edit_document)
        curate_delete_perm = Permission.objects.get(codename=curate_delete_document)
        defaultGroup.permissions.add(explore_access_perm)
        defaultGroup.permissions.add(curate_access_perm)
        defaultGroup.permissions.add(curate_edit_perm)
        defaultGroup.permissions.add(curate_delete_perm)

        #### API ####
        api_access_perm = Permission.objects.get(codename=api_access)
        defaultGroup.permissions.add(api_access_perm)
        #### END API ####
    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)


def load_templates():
    """
    Loads templates/xslt for NMRR the first time
    """  
    # if templates are already present, initialization already happened
    existing_templates = Template.objects()
    if len(existing_templates) == 0:
        templates = {
            'all':'AllResources.xsd',
            'organization': 'Organization.xsd',
            'datacollection': 'DataCollection.xsd',
            'repository': 'Repository.xsd',
            'projectarchive': 'ProjectArchive.xsd',
            'database': 'Database.xsd',
            'dataset': 'Dataset.xsd',
            'service': 'Service.xsd',
            'informational': 'Informational.xsd',
            'software': 'Software.xsd',
        }    
        
        template_ids = []
        
        template_results = {
            'full': 'nmrr-full_demo.xsl',
            'detail': 'nmrr-detail_demo.xsl',
        }
        
        template_results_id = {
            'full': None,
            'detail': None,
        }
        
        # connect to mongo
        client = MongoClient(MONGODB_URI)
        # connect to the db 'mgi'
        db = client[MGI_DB]
        
        # Add the templates
        for template_name, template_path in templates.iteritems():
            file = open(os.path.join(SITE_ROOT, 'static', 'resources', 'xsd', template_path),'r')
            templateContent = file.read()
            hash = XSDhash.get_hash(templateContent)
            
            #create template/ template version
            objectVersions = TemplateVersion(nbVersions=1, isDeleted=False).save()
            object = Template(title=template_name, filename=template_path, content=templateContent, version=1, templateVersion=str(objectVersions.id), hash=hash).save()
            objectVersions.versions = [str(object.id)]
            objectVersions.current = str(object.id)
            objectVersions.save()    
            object.save()
        
            # save template id
            template_ids.append(str(object.id))
    
    

        # Add xslt
        xsl_col = db['result_xslt']
        for xsl_name, xsl_path in template_results.iteritems():
            file = open(os.path.join(SITE_ROOT, 'static', 'resources', 'xsl', xsl_path),'r')
            fileContent = file.read()
            
            xsl = {}
            xsl['name'] = xsl_name
            xsl['filename'] = xsl_path
            xsl['content'] = fileContent
            xsl_id = xsl_col.insert(xsl)
            
            template_results_id[xsl_name] = str(xsl_id)
                
        
        templates = db['template']
        results_xslt = {'ResultXsltList': template_results_id['full'], 'ResultXsltDetailed': template_results_id['detail']}
        templates.update({}, {"$set":results_xslt}, upsert=False, multi=True)


    def scan_static_resources():
        """
        Dynamically load templates/types in resource folder
        :return:
        """
        try:
            # if templates are already present, initialization already happened
            existing_templates = Template.objects()
            existing_types = Type.objects()

            if len(existing_templates) == 0 and len(existing_types) == 0:
                templates_dir = os.path.join(STATIC_DIR, 'templates')
                if os.path.exists(templates_dir):
                    for filename in os.listdir(templates_dir):
                        if filename.endswith(".xsd"):
                            file_path = os.path.join(templates_dir, filename)
                            file = open(file_path, 'r')
                            file_content = file.read()
                            try:
                                name_no_extension = filename.split(".xsd")[0]
                                create_template(file_content, name_no_extension, name_no_extension)
                            except Exception, e:
                                print "ERROR: Unable to load {0} ({1})".format(filename, e.message)
                        else:
                            print "WARNING: {0} not loaded because extension is not {1}".format(filename, ".xsd")

                types_dir = os.path.join(STATIC_DIR, 'types')
                if os.path.exists(types_dir):
                    for filename in os.listdir(types_dir):
                        if filename.endswith(".xsd"):
                            file_path = os.path.join(types_dir, filename)
                            file = open(file_path, 'r')
                            file_content = file.read()
                            try:
                                name_no_extension = filename.split(".xsd")[0]
                                create_type(file_content, name_no_extension, name_no_extension)
                            except Exception, e:
                                print "ERROR: Unable to load {0} ({1})".format(filename, e.message)
                        else:
                            print "WARNING: {0} not loaded because extension is not {1}".format(filename, ".xsd")
        except Exception:
            print "ERROR: An unexpected error happened during the scan of static resources"
