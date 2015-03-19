################################################################################
#
# File Name: MDCSMigrationTo11.py
# Purpose: Migration from 1 to 1.1   
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from MDCSMigration import MDCSMigration, ORIG_DB_PORT
from pymongo import MongoClient
from collections import OrderedDict
import requests
import logging
from bson.objectid import ObjectId
import xmltodict
import json

# 1 -> 1.1
#
# 1.1 model:
# - Manage dependencies (don't keep track)
# - Flat files
# - Repositories: Basic auth
# - hash improved
class MDCSMigrationTo11(MDCSMigration):
    def __init__(self, db_orig, server_dest, user_dest, pswd_dest):
        MDCSMigration.__init__(self, db_orig, server_dest, user_dest, pswd_dest)
    
    def migrate(self):
        
        # connect to the current mongodb instance
        client = MongoClient('localhost', ORIG_DB_PORT)
        
        # connect to the db 'mgi'
        db = client['mgi']
        
        try:
            self.migrateTypes(db)
            self.migrateTemplates(db)
            self.migrateData(db)
            self.migrateVersions(db)
            self.migrateSavedQueries(db)
        except Exception, e:
            logging.critical("Exception occurred. Migration stops.")
            logging.critical(e.message)
            
        
    def migrateTypes(self, db):
        logging.info("Starting to migrate types...")
        col_versions = db['type_version']
        col_type = db['type']
        cursor_versions = col_versions.find()
        url = self.server_dest + "/rest/types/add"
        
        for version in cursor_versions:
            typeVersion = None
            for type_id in version['versions']:
                type = col_type.find_one({"_id": ObjectId(type_id)})
                data = {"title": type['title'], 
                        "filename": type['filename'],
                        "content": type['content']}
                # add a type
                if typeVersion == None:                                                            
                    r = requests.post(url, data, auth=(self.user_dest,self.pswd_dest))     
                    # 2xx code: SUCCESS           
                    if r.status_code not in range(200,299):
                        logging.error("Error when trying to migrate:")
                        logging.error(str(data))
                        logging.error("Error:")
                        logging.error(r.text)
                        self.identifiers[type_id] = None
                    else:
                        self.identifiers[type_id] = eval(r.text)['_id']['$oid']
                        typeVersion = eval(r.text)['typeVersion']  
                        self.identifiers[str(version['_id'])] = typeVersion              
                else:
                    # add a version of a type
                    data['typeVersion'] = typeVersion             
                    r = requests.post(url, data, auth=(self.user_dest,self.pswd_dest)) 
                    # 2xx code: SUCCESS                   
                    if r.status_code not in range(200,299):
                        logging.error("Error when trying to migrate:")
                        logging.error(str(data))
                        logging.error("Error:")
                        logging.error(r.text)
                        self.identifiers[type_id] = None
                    else:
                        self.identifiers[type_id] = eval(r.text)['_id']['$oid']
        logging.info("End of types migration.")
    
        
    def migrateTemplates(self, db):
        logging.info("Starting to migrate templates...")
        col_versions = db['template_version']
        col_temp = db['template']
        cursor_versions = col_versions.find()
        url = self.server_dest + "/rest/templates/add"
        for version in cursor_versions:
            templateVersion = None
            for temp_id in version['versions']:
                temp = col_temp.find_one({"_id": ObjectId(temp_id)})
                data = {"title": temp['title'], 
                        "filename": temp['filename'],
                        "content": temp['content']}
                # add a template
                if templateVersion == None:                                        
                    r = requests.post(url, data, auth=(self.user_dest,self.pswd_dest)) 
                    # 2xx code: SUCCESS               
                    if r.status_code not in range(200,299):
                        logging.error("Error when trying to migrate:")
                        logging.error(str(data))
                        logging.error("Error:")
                        logging.error(r.text)
                        self.identifiers[temp_id] = None
                    else:
                        self.identifiers[temp_id] = eval(r.text)['_id']['$oid']
                        templateVersion = eval(r.text)['templateVersion']
                        self.identifiers[str(version['_id'])] = templateVersion
                else:
                    # add a version of the template                    
                    data['templateVersion'] = templateVersion             
                    r = requests.post(url, data, auth=(self.user_dest,self.pswd_dest))   
                    # 2xx code: SUCCESS                 
                    if r.status_code not in range(200,299):
                        logging.error("Error when trying to migrate:")
                        logging.error(str(data))
                        logging.error("Error:")
                        logging.error(r.text)
                        self.identifiers[temp_id] = None
                    else:
                        self.identifiers[temp_id] = eval(r.text)['_id']['$oid']
        logging.info("End of templates migration.")
        
    def migrateData(self, db):
        logging.info("Starting to migrate XML data...")
        col_data = db['xmldata']
        cursor = col_data.find(as_class = OrderedDict)
        
        for data in cursor:
            # get template id
            template_id = data['schema']
            # was template inserted in new db? its id should be in identifiers
            if template_id in self.identifiers.keys() and self.identifiers[template_id] is not None:
                new_template_id = self.identifiers[template_id]
                # template -> current to allow insertion of data
                logging.info("Set current template to allow insertion.")
                url = self.server_dest + "/rest/templates/versions/current?id=" + new_template_id
                r = requests.get(url, auth=(self.user_dest,self.pswd_dest))
                # get data and transform to XML str
                xmlStr = xmltodict.unparse(data['content']).replace('<?xml version="1.0" encoding="utf-8"?>\n',"")
                # insert in new db
                url = self.server_dest + "/rest/curate"
                data = {"title": data['title'], 
                        "schema": new_template_id,
                        "content": xmlStr}
                logging.info("Start inserting data...")
                r = requests.post(url,data, auth=(self.user_dest,self.pswd_dest))
                if r.status_code not in range(200,299):
                        logging.error("Error when trying to migrate:")
                        logging.error(str(data))
                        logging.error("Error:")
                        logging.error(r.text)
                else:
                    logging.info("Data inserted...")
            else:
                logging.error("The XML document (XML id: "+ str(data['_id']) + ") can't be migrated because, its template was not migrated with success (Template id: (" + template_id + ").")
            
        logging.info("End of XML data migration.")
        
    def migrateVersions(self,db):
        logging.info("Starting to migrate versions information...")
        col_template_version = db['template_version']
        cursor = col_template_version.find()
        
        
        logging.info("Templates")
        for version in cursor:
            version_id = str(version['_id']) 
            if version_id in self.identifiers and self.identifiers[version_id] is not None:
                new_version_id = self.identifiers[version_id]
                logging.info("Old id:" +version_id+", New id:"+new_version_id)
                logging.info("Set current template version...")
                old_current = version['current']
                if old_current in self.identifiers and self.identifiers[old_current] is not None:
                    new_current = self.identifiers[old_current]
                    url = self.server_dest + "/rest/templates/versions/current?id=" + new_current
                    r = requests.get(url, auth=(self.user_dest,self.pswd_dest))
                    if r.status_code not in range(200,299):
                        if 'message' in eval(r.text) and eval(r.text)['message'] == "The selected template is already the current template.":
                            logging.info("Template version set to current with success.")
                        else:
                            logging.error("Error when trying to set current:")
                            logging.error(str(new_current))
                            logging.error("Error:")
                            logging.error(r.text)
                    else:
                        logging.info("Template version set to current with success.")
                
                logging.info("Set deleted template versions...")
                for old_deleted_id in version['deletedVersions']:
                    if old_deleted_id in self.identifiers and self.identifiers[old_deleted_id] is not None:
                        new_deleted = self.identifiers[old_deleted_id]
                        url = self.server_dest + "/rest/templates/delete?id=" + new_deleted
                        r = requests.get(url, auth=(self.user_dest,self.pswd_dest))
                        if r.status_code not in range(200,299):
                            logging.error("Error when trying to set delete version:")
                            logging.error(str(new_deleted))
                            logging.error("Error:")
                            logging.error(r.text)
                        else:
                            logging.info("Template version deleted with success.")
                
                logging.info("Set deleted template...")
                if version['isDeleted'] == True:
                    url = self.server_dest + "/rest/templates/delete?templateVersion=" + new_version_id
                    r = requests.get(url, auth=(self.user_dest,self.pswd_dest))
                    if r.status_code not in range(200,299):
                        logging.error("Error when trying to set delete template:")
                        logging.error(str(new_deleted))
                        logging.error("Error:")
                        logging.error(r.text)
                    else:
                        logging.info("Template deleted with success.")
        
        
        col_type_version = db['type_version']
        cursor = col_type_version.find()
        
        logging.info("Types")
        for version in cursor:
            version_id = str(version['_id']) 
            if version_id in self.identifiers and self.identifiers[version_id] is not None:
                new_version_id = self.identifiers[version_id]
                logging.info("Old id:" +version_id+", New id:"+new_version_id)
                logging.info("Set current type version...")
                old_current = version['current']
                if old_current in self.identifiers and self.identifiers[old_current] is not None:
                    new_current = self.identifiers[old_current]
                    url = self.server_dest + "/rest/types/versions/current?id=" + new_current
                    r = requests.get(url, auth=(self.user_dest,self.pswd_dest))
                    if r.status_code not in range(200,299):
                        if 'message' in eval(r.text) and eval(r.text)['message'] == "The selected type is already the current type.":
                            logging.info("Template version set to current with success.")
                        else:
                            logging.error("Error when trying to set current:")
                            logging.error(str(new_current))
                            logging.error("Error:")
                            logging.error(r.text)
                
                logging.info("Set deleted type versions...")
                for old_deleted_id in version['deletedVersions']:
                    if old_deleted_id in self.identifiers and self.identifiers[old_deleted_id] is not None:
                        new_deleted = self.identifiers[old_deleted_id]
                        url = self.server_dest + "/rest/types/delete?id=" + new_deleted
                        r = requests.get(url, auth=(self.user_dest,self.pswd_dest))
                        if r.status_code not in range(200,299):                            
                            logging.error("Error when trying to set delete version:")
                            logging.error(str(new_deleted))
                            logging.error("Error:")
                            logging.error(r.text)
                        else:
                            logging.info("Type version deleted with success.")
                
                logging.info("Set deleted type...")
                if version['isDeleted'] == True:
                    url = self.server_dest + "/rest/types/delete?typeVersion=" + new_version_id
                    r = requests.get(url, auth=(self.user_dest,self.pswd_dest))
                    if r.status_code not in range(200,299):
                        logging.error("Error when trying to set delete type:")
                        logging.error(str(new_deleted))
                        logging.error("Error:")
                        logging.error(r.text)
                    else:
                        logging.info("Type deleted with success.")
                
        logging.info("End of migration of versions information.")
    
    def migrateSavedQueries(self,db):
        col_queries = db['saved_query']
        queries = col_queries.find()
        
        logging.info("Starting to migrate saved queries...")
        
        for query in queries:
            if query['template'] in self.identifiers and self.identifiers[query['template']] is not None:
                url = self.server_dest + "/rest/saved_queries/add"
                data = {"query": query['query'].replace("'",'"'), 
                        "user": query['user'],
                        "template": self.identifiers[query['template']],
                        "displayedQuery": query['displayedQuery'],
                        }
                logging.info("Start inserting query...")
                r = requests.post(url,data, auth=(self.user_dest,self.pswd_dest))
                if r.status_code not in range(200,299):
                        logging.error("Error when trying to migrate:")
                        logging.error(str(data))
                        logging.error("Error:")
                        logging.error(r.text)
                else:
                    logging.info("Query inserted...")
            else:
                logging.error("The query can't be migrated because the template it refers to could not be migrated.")
             
        
        logging.info("End of migration of saved queries.")
        