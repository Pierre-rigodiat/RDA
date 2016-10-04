# MongoDB configuration

This document provides explanations about the configuration of MongoDB.
Please use the configuration file provided with the MDCS (mdcs/conf/mongodb.conf), to be sure to have the minimum required security for your database.
You can find more information about MongoDB security: http://docs.mongodb.org/manual/administration/security-checklist/

## Setup 
**Required:** Edit the file path/to/mdcs/conf/mongodb.conf and replace the value of dbPath by the path on your system (path/to/mdcs/data/db).

**Required:** Please follow these instructions to set up authentication for your database:
- Add mongodb/bin folder to your path for more convenience
- In a first command prompt, run the following command:
```
mongod --config path/to/mdcs/conf/mongodb.conf
```

In another command prompt, type the following commands, replacing the parameters below, by some of your choice:
- **mongo_admin_user:** choose a username for the administrator of mongodb
- **mongo_admin_password:** choose a password for the administrator of mongodb
- **mongo_mgi_user:** choose a username for the user of mgi database
- **mongo_mgi_password:** choose a password for the user of mgi database

**Create an admin user:**
```
mongo
use admin
db.createUser(
{
user: "<mongo_admin_user>",
pwd: "<mongo_admin_password>",
roles: [ { role: "userAdminAnyDatabase", db: "admin"},"backup","restore"]
}
)
exit
```

**Create a user:**
```
mongo --port 27017 -u "<mongo_admin_user>" -p "<mongo_admin_password>" --authenticationDatabase admin
use mgi
db.createUser(
{
user: "<mongo_mgi_user>",
pwd: "<mongo_mgi_password>",
roles: ["readWrite"]
}
)
exit
```

Edit the file path/to/mdcs/mgi/settings.py, and set the following parameters to the values you chose earlier:
- MONGO_MGI_USER = "mongo_mgi_user"
- MONGO_MGI_PASSWORD = "mongo_mgi_password"
