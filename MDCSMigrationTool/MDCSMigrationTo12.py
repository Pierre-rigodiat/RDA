################################################################################
#
# File Name: MDCSMigration.py
# Purpose: Migration from 1.1 to 1.2
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################


from MDCSMigration import MDCSMigration

# 1.2 model:
# - Restricted to valid XSD/XML
# - Manage dependencies (keep track), but not 1.1, so have to extract them from Meta data
# - Repositories: OAuth2
class MDCSMigrationTo12(MDCSMigration):
    def __init__(self, db_orig, server_dest, user_dest, pswd_dest):
        MDCSMigration.__init__(self, db_orig, server_dest, user_dest, pswd_dest)
    
    def migrate(self):
        return MDCSMigration.migrate(self)