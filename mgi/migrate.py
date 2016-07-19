# IMPORTS
import os
from subprocess import check_output
import time
from pymongo import MongoClient
import sys
from bson.objectid import ObjectId
from settings import MONGODB_URI, MGI_DB, BASE_DIR

# PREREQUISITES:
# - mongo in path
# - mongod running
# - mongod connected to data\db

# PROCEDURE:
# - stop mongogod, stop runserver
# - save data/db in a different location
# - Update the code
# - run mongod
# - run migration
# - runserver


# PARAMETERS
MONGO_ADMIN = "admin"
MONGO_PASSWORD = "admin"
BACKUPS_DIR = os.path.join(BASE_DIR, 'backups')


# MIGRATION OPTIONS
# True: delete the elements that are not needed anymore in the new version
CLEAN_DATABASE = True


# UTILS FUNCTIONS
def _error(msg):
    print '\n*** MIGRATION FAILED ***'
    print msg
    sys.exit()


def _dump_database():
    # generate time string
    time_str = time.strftime("%Y%m%d_%H%M%S")
    # backup directory name
    backup_dir_name = 'backup_{}'.format(time_str)
    # backup_directory_path
    backup_dir_path = os.path.join(BACKUPS_DIR, backup_dir_name)

    # create the backup directory if not present
    print "Create backup directory: " + backup_dir_path
    if not os.path.exists(backup_dir_path):
        os.makedirs(backup_dir_path)
    else:
        _error('A backup directory with the same name already exists')

    print "Dump database..."
    try:
        output = check_output(
                [
                    'mongodump',
                    '--out',
                    backup_dir_path,
                    '-u',
                    MONGO_ADMIN,
                    '-p',
                    MONGO_PASSWORD
                ]
            )
    except Exception, e:
        _error(e.message)
    return backup_dir_path


def _restore_dump(backup_dir_path):
    """
    Restore a dump
    :param backup_dir_path:
    :return:
    """
    print "*** RESTORE DUMP ***"
    output = check_output(
        [
            'mongorestore',
            backup_dir_path,
            '-u',
            MONGO_ADMIN,
            '-p',
            MONGO_PASSWORD
        ]
    )
print '*** START MIGRATION ***'

try:
    # Connect to mongodb
    print 'Attempt connection to database...'
    client = MongoClient(MONGODB_URI)
    print 'Connected to database with success.'
    try:
        # connect to the db 'mgi'
        print 'Attempt connection to collection...'
        db = client[MGI_DB]
        print 'Connected to collection with success.'
    except Exception, e:
        _error('Unable to connect to the collection. ')
except Exception, e:
    _error('Unable to connect to MongoDB. '
           'Please check that mongod is currently running and connected to the MDCS data.')

# /!\ PROMPT TO CREATE A ZIP OF THE DATA FIRST
# /!\ DON"T CREATE THE DATA FOLDER IN THE INSTALLERS
# /!\ CHECK WHEN GETTING THE CODE FROM GITHUB TOO

# Create a dump of the database
backup_dir_path = _dump_database()

# /!\ ASK IF DUMP RESULTS LOOK GOOD

# TODO: test that false when empty
# Test that the dump created files
if len(os.listdir(backup_dir_path)) == 0:
    _error('Dump failed')

# /!\ AT THIS POINT RESTORE THE BACKUP IF AN ERROR OCCURS

# Start migration
# if something goes wrong restore the dump

# APPLY CHANGES FROM 1.3 TO 1.4

print '*** START MIGRATING DATA ***'

try:
    # GET COLLECTIONS NEEDED FOR MIGRATION
    meta_schema_col = db['meta_schema']
    template_col = db['template']
    type_col = db['type']
    form_data_col = db['form_data']
    xml_data_col = db['xmldata']

    # METASCHEMA COLLECTION REMOVED:
    # NEED TO UPDATE THE CONTENT OF TEMPLATES/TYPES
    print "Updating templates/types with meta_schema collection..."

    # find all meta_schema of the collection
    cursor = meta_schema_col.find()

    # Browse meta_schema collection
    for result in cursor:
        # get the template/type id
        schema_id = result['schemaId']
        # get the content stored in meta_schema
        api_content = result['api_content']
        # create a payload to update the template/type
        payload = {'content': api_content}

        # get the template/type to update
        to_update = template_col.find_one({'_id': ObjectId(schema_id)})
        template_col.update({'_id': ObjectId(schema_id)}, {"$set": payload}, upsert=False)
        if to_update is None:
            to_update = type_col.find_one({'_id': ObjectId(schema_id)})
            if to_update is None:
                # TODO: restore dump
                _error('Trying to update the content of ' + schema_id + ' but it cannot be found')
            else:
                type_col.update({'_id': ObjectId(schema_id)}, {"$set": payload}, upsert=False)

    # XMLDATA CHANGES:
    print "Updating xml_data..."
    # print "Adding deleted property to all records (False by default)..."
    # xml_data_col.update({}, {"$set": {"deleted": False}}, upsert=False, multi=True)
    print "Adding lastmodificationdate/oai_datestamp to records..."
    xml_data_col.update({}, {"$set": {"deleted": False}}, upsert=False, multi=True)
    # find all meta_schema of the collection
    cursor = xml_data_col.find()
    # Browse xml_data collection
    for result in cursor:
        # xml data has a publication date
        if 'publicationdate' in result:
            publication_date = result['publicationdate']
            # set last modification date and oai_datestamp to publication date
            payload = {'lastmodificationdate': publication_date, 'oai_datestamp': publication_date}
            xml_data_col.update({'_id': result['_id']}, {"$set": payload}, upsert=False)
        else:
            # set last modification date to datetime.MIN
            import bson
            payload = {'lastmodificationdate': result['_id'].generation_time}
            xml_data_col.update({'_id': result['_id']}, {"$set": payload}, upsert=False)

    if CLEAN_DATABASE:
        # CLEAN DATABASE
        print "*** CLEAN THE DATABASE ***"
        # remove elements from Form_data (not used in 1.4)
        print "Removing elements from form_data collection..."
        form_data_col.update({}, {"$unset": {"elements": 1}}, multi=True)
        # drop form_element collection (not used in 1.4)
        print "Dropping form_element collection..."
        db.drop_collection('form_element')
        # drop meta_schema collection (not used in 1.4)
        print "Dropping meta_schema collection..."
        db.drop_collection('meta_schema')
except Exception, e:
    _restore_dump(backup_dir_path)
    _error(e.message)

print "*** MIGRATION COMPLETE ***"
