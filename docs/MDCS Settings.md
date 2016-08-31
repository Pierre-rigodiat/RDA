# MDCS Settings

This document provides a list of settings specific to the MDCS. Additional information regarding settings can be found on the Django documentation and on the documentation of individual python package.

## General Settings

**MDCS_URI:** *http://127.0.0.1:8000*
URI of the server.

## MongoDB

**MONGO_MGI_USER:**
Set the user used by Django to connect to MongoDB.

**MONGO_MGI_PASSWORD:**
Set the password used by Django to connect to MongoDB.

**MGI_DB:**
Set the name of the collection used to store MDCS data.

**MONGODB_URI:**
Set the MongoDB connection URI.


## BLOB Hoster

**BLOB_HOSTER:** GridFS
Set the system that will host the large files.

**BLOB_HOSTER_URI:**
Set the URI of the server where the BLOB Hoster is running.

**BLOB_HOSTER_USER:**
Set the user to connect to the BLOB Hoster.

**BLOB_HOSTER_PSWD:**
Set the password to connect to the BLOB Hoster.


## Template Customization

**CUSTOM_TITLE:**
Change the main title.

**CUSTOM_SUBTITLE:**
Change the subtitle.

**CUSTOM_ORGANIZATION:**
Change the name of the organization. 

**CUSTOM_URL:** 
Change the organization website URL.

**CUSTOM_NAME:**
Change the name of the application.

**CUSTOM_DATA:**
Change the name of the data stored in the system.

**CUSTOM_CURATE:**
Change the name of the 'Curate' section.

**CUSTOM_EXPLORE:**
Change the name of the 'Explore' section.

**CUSTOM_COMPOSE:**
Change the name of the 'Compose' section.


## XSD PARSER

**PARSER_MIN_TREE:** *True|False*
If True, the parser will only generate the first levels of the XML Schema. If set to False, may not work for XML schemas using recursive definitions.

**PARSER_IGNORE_MODULES:** *True|False*
If True, the parser will not generate the modules set in the XML Schema.

**PARSER_COLLAPSE:** *True|False*
If True, the form will allow to collapse/expand sections.

**PARSER_AUTO_KEY_KEYREF:** *True|False*
If True, lookups will be done during the parsing to register key/keyref elements. Set to False if uploaded XML Schemas are not making use of key/keyref elements.

**PARSER_IMPLICIT_EXTENSION_BASE:** *True|False*
If True, the parser will display the base type and its extensions when polymorphic extensions are used. Set to False to only display extensions.

**PARSER_DOWNLOAD_DEPENDENCIES:** *True|False*
If True, the parser will download dependencies (include/import) to render them in the form.

