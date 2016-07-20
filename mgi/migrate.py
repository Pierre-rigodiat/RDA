# IMPORTS
import os
from subprocess import check_output
import time
from pymongo import MongoClient
import sys
from bson.objectid import ObjectId
import argparse
import platform
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
BACKUPS_DIR = os.path.join(BASE_DIR, 'backups')

WARNINGS_ENABLED = True
BACKUP_ENABLED = True


# UTILS FUNCTIONS
def _error(msg=''):
    print '\n*** MIGRATION FAILED ***'
    print msg
    sys.exit()


def _build_cmd(cmd, path=''):
    """
    Build the command with path
    :param cmd:
    :param path:
    :return:
    """
    if len(path) > 0:
        if platform.system() == "Windows":
            cmd = os.path.join(path, '{}.exe'.format(cmd))
        else:
            cmd = os.path.join(path, cmd)

    return cmd


def _get_user_validation(msg):
    print msg + '\nContinue? (Y/n):'
    user_input = raw_input()
    if user_input == 'Y':
        return True
    elif user_input == 'n':
        return False
    else:
        return _get_user_validation(msg)


def _warn_user(msg):
    if WARNINGS_ENABLED:
        return _get_user_validation(msg)
    return True


def _dump_database(mongo_admin_user, mongo_admin_password, mongo_path):
    if BACKUP_ENABLED:
        # generate time string
        time_str = time.strftime("%Y%m%d_%H%M%S")
        # backup directory name
        backup_dir_name = 'backup_{}'.format(time_str)
        # backup_directory_path
        backup_dir_path = os.path.join(BACKUPS_DIR, backup_dir_name)

        if not _warn_user('A backup folder will be created at : {}'.format(backup_dir_path)):
            _error()

        # create the backup directory if not present
        print "Create backup directory: " + backup_dir_path
        if not os.path.exists(backup_dir_path):
            os.makedirs(backup_dir_path)
        else:
            _error('A backup directory with the same name already exists')

        cmd = _build_cmd('mongodump', mongo_path)

        if not _warn_user('A dump of the data will be crated using the following command : {}'.format(cmd)):
            _error()

        print "Dumping the database..."

        try:
            output = check_output(
                    [
                        cmd,
                        '--out',
                        backup_dir_path,
                        '-u',
                        mongo_admin_user,
                        '-p',
                        mongo_admin_password
                    ]
                )

            # Test that the dump created files
            if len(os.listdir(backup_dir_path)) == 0:
                _error('Dump failed')

            if not _warn_user('Please check the console for any eventual undetected problem during the dump.'):
                _error()
        except Exception, e:
            _error(e.message)

        return backup_dir_path
    else:
        return ''


def _restore_dump(backup_dir_path, mongo_admin_user, mongo_admin_password, mongo_path):
    """
    Restore a dump
    :param backup_dir_path:
    :return:
    """
    if BACKUP_ENABLED:
        print "*** RESTORE DUMP ***"

        cmd = _build_cmd('mongorestore', mongo_path)

        output = check_output(
            [
                cmd,
                backup_dir_path,
                '--drop',
                '-u',
                mongo_admin_user,
                '-p',
                mongo_admin_password
            ]
        )


def _connect():
    """
    Connect to the database
    :return: database connection
    """
    try:
        # Connect to mongodb
        print 'Attempt connection to database...'
        client = MongoClient(MONGODB_URI)
        print 'Connected to database with success.'
        try:
            # connect to the db 'mgi'
            print 'Attempt connection to collection...'
            db = client[MGI_DB]
            return db
            print 'Connected to collection with success.'
        except Exception, e:
            _error('Unable to connect to the collection. ')
    except Exception, e:
        _error('Unable to connect to MongoDB. '
               'Please check that mongod is currently running and connected to the MDCS data.')


def _migrate(mongo_admin_user, mongo_admin_password, mongo_path, warnings=True, backup=True):
    """
    APPLY CHANGES FROM 1.3 TO 1.4

    :return:
    """
    # /!\ DON"T CREATE THE DATA FOLDER IN THE INSTALLERS
    # /!\ CHECK WHEN GETTING THE CODE FROM GITHUB TOO

    print '*** START MIGRATION ***'

    msg = 'You are about to run the Curator Migration Tool. ' \
          'This will update the database from version 1.3 to work for version 1.4. ' \
          'Changes will be applied to the database such addition/deletion/modification of fields/collections/records.'

    if not _warn_user(msg):
        _error()

    # /!\ PROMPT TO CREATE A ZIP OF THE DATA FIRST
    msg = 'Please be sure that you made a copy of your data before starting.'

    if not _warn_user(msg):
        _error()

    # connect to the database
    db = _connect()

    # TODO: /!\ CHECK IF THE RESULT OF THE DUMP LOOKS GOOD
    # Create a dump of the database
    backup_dir_path = _dump_database(mongo_admin_user=mongo_admin_user,
                                     mongo_admin_password=mongo_admin_password,
                                     mongo_path=mongo_path)

    print '*** START MIGRATING DATA ***'
    try:
        if not _warn_user('The changes on the database are about to be applied.'):
            _error()

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
                    # restore dump
                    _restore_dump(backup_dir_path=backup_dir_path,
                                  mongo_admin_user=mongo_admin_user,
                                  mongo_admin_password=mongo_admin_password,
                                  mongo_path=mongo_path)
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
                payload = {'lastmodificationdate': result['_id'].generation_time}
                xml_data_col.update({'_id': result['_id']}, {"$set": payload}, upsert=False)

        # CLEAN THE DATABASE
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
        _restore_dump(backup_dir_path=backup_dir_path,
                      mongo_admin_user=mongo_admin_user,
                      mongo_admin_password=mongo_admin_password,
                      mongo_path=mongo_path)
        _error(e.message)

    print "*** MIGRATION COMPLETE ***"


def main(argv):
    parser = argparse.ArgumentParser(description="Curator Data Migration Tool")
    required_arguments = parser.add_argument_group("required arguments")

    # add required arguments
    required_arguments.add_argument('-u',
                                    '--mongo-admin-user',
                                    help='Username of MongoDB Admin',
                                    nargs=1,
                                    required=True)
    required_arguments.add_argument('-p',
                                    '--mongo-admin-password',
                                    help='Password of MongoDB Admin',
                                    nargs=1,
                                    required=True)

    # add optional arguments
    parser.add_argument('-path',
                        '--mongo-path',
                        help='Path to MongoDB bin folder (if not in PATH)',
                        nargs=1)
    parser.add_argument('-y',
                        '--yes-to-all',
                        help='Does not show warnings')
    parser.add_argument('-n',
                        '--no-backup',
                        help='Does not create a backup of the database before starting migration.')

    # parse arguments
    args = parser.parse_args()

    # get required arguments
    mongo_admin_user = args.mongo_admin_user[0]
    mongo_admin_password = args.mongo_admin_password[0]

    # get optional arguments
    if args.mongo_path:
        mongo_path = args.mongo_path[0]
    else:
        mongo_path = ''

    # if args.yes_to_all:
    #     WARNINGS_ENABLED = False
    #
    # if args.no_backup:
    #     BACKUP_ENABLED = False

    # Start migration
    _migrate(mongo_admin_user=mongo_admin_user,
             mongo_admin_password=mongo_admin_password,
             mongo_path=mongo_path)

if __name__ == "__main__":
    main(sys.argv[1:])
