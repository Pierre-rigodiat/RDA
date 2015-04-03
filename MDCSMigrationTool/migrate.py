################################################################################
#
# File Name: migrate.py
# Purpose: Runs migration from command line   
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

# 1- Stop all running jobs (mongo, mdcs, jena...)
# 2- Copy the db.sqlite3 file from your previous MDCS and paste it in the installation folder of the new one
# 3- Run the new version of the MDCS
# 4- Run the migration program
# 5- Check the log file for errors

import sys
from MDCSMigrationTo11 import MDCSMigrationTo11

def usage():
    print "Usage:"
    print 'python migrate.py -from version -to version -from_db "path/to/db/folder" -to_mdcs_addr url -mdcs_user username -mdcs_pswd password'
    print "available migrations : from 1 to 1.1"



if len(sys.argv) != 13:
    print "ERROR: Bad number of arguments."
    usage()
elif (sys.argv[1] != '-from' or 
    sys.argv[3] != '-to' or
    sys.argv[5] != '-from_db' or
    sys.argv[7] != '-to_mdcs_addr' or
    sys.argv[9] != '-mdcs_user' or
    sys.argv[11] != '-mdcs_pswd'):
    print "ERROR: Bad argument names or bad argument order."
    usage()
else:
    arg_from = sys.argv[2]
    arg_to = sys.argv[4]
    arg_from_db = sys.argv[6]
    arg_to_mdcs_addr = sys.argv[8]
    arg_mdcs_user = sys.argv[10]
    arg_mdcs_pswd = sys.argv[12]
    # select the good migration
    if arg_from == '1' and arg_to == '1.1':
        migrator = MDCSMigrationTo11(arg_from_db, arg_to_mdcs_addr, arg_mdcs_user, arg_mdcs_pswd)
        migrator.run()
    else:
        print "ERROR: The following migration is not available : from " + str(arg_from) + " to " +str(arg_to)
        print "available migrations : from 1 to 1.1"
        usage()
    