################################################################################
#
# File Name: MDCSMigration.py
# Purpose: Migration from unknown to 1
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from MDCSMigration import MDCSMigration

# 1.0 model:
# - Restricted to valid XSD/XML
# - could upload files with include/imports
# - no flat files
# - no dependency management
# - Repositories: Basic auth
class MDCSMigrationTo1(MDCSMigration):
    def __init__(self, db_orig, server_dest, user_dest, pswd_dest):
        MDCSMigration.__init__(self, db_orig, server_dest, user_dest, pswd_dest)
    
    def migrate(self):
        return MDCSMigration.migrate(self)