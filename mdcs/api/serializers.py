################################################################################
#
# File Name: serializers.py
# Application: api
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
#         Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from rest_framework import serializers
from rest_framework_mongoengine.serializers import MongoEngineModelSerializer
from mgi.models import SavedQuery, Template, Type, TemplateVersion, TypeVersion, Instance
from django.contrib.auth.models import User

################################################################################
# 
# Class Name: jsonDataSerializer
#
# Description:   Serializer for JSON data
# 
################################################################################
class jsonDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    schema = serializers.CharField()
    content = serializers.CharField()
    _id = serializers.CharField(required=False)

################################################################################
# 
# Class Name: savedQuerySerializer
#
# Description:   Serializer for saved queries
# 
################################################################################
class savedQuerySerializer(MongoEngineModelSerializer):
    class Meta:
        model = SavedQuery
        
################################################################################
# 
# Class Name: resSavedQuerySerializer
#
# Description:   Serializer for result set of saved queries 
# 
################################################################################
class resSavedQuerySerializer(serializers.Serializer):
    user = serializers.CharField()
    template = serializers.CharField()
    query = serializers.CharField()
    displayedQuery = serializers.CharField()
    id = serializers.CharField(required=False)

################################################################################
# 
# Class Name: querySerializer
#
# Description:   Serializer for queries
# 
################################################################################
class querySerializer(serializers.Serializer):
    query = serializers.CharField()

################################################################################
# 
# Class Name: sparqlQuerySerializer
#
# Description:   Serializer for SPARQL queries
# 
################################################################################
class sparqlQuerySerializer(serializers.Serializer):
    query = serializers.CharField()
    format = serializers.CharField(required=False)

################################################################################
# 
# Class Name: sparqlResultsSerializer
#
# Description:   Serializer for result set of SPARQL queries
# 
################################################################################
class sparqlResultsSerializer(serializers.Serializer):
    content = serializers.CharField()


################################################################################
# 
# Class Name: schemaSerializer
#
# Description:   Serializer for schema with dependencies
# 
################################################################################
class schemaSerializer(MongoEngineModelSerializer):
    class Meta:
        model = Template
        exclude = (['templateVersion','version','hash'])


################################################################################
# 
# Class Name: templateSerializer
#
# Description:   Serializer for result set of schemas
# 
################################################################################
class templateSerializer(serializers.Serializer):
    title = serializers.CharField()
    filename = serializers.CharField()
    content = serializers.CharField()
    templateVersion = serializers.CharField()
    version = serializers.IntegerField()
    hash = serializers.CharField()
    dependencies = serializers.CharField()
    id = serializers.CharField(required=False)

################################################################################
# 
# Class Name: TemplateVersionSerializer
#
# Description:   Serializer for templates versions
# 
################################################################################
class TemplateVersionSerializer(MongoEngineModelSerializer):
    class Meta:
        model = TemplateVersion

################################################################################
# 
# Class Name: typeSerializer
#
# Description:   Serializer for types
# 
################################################################################
class typeSerializer(MongoEngineModelSerializer):
    class Meta:
        model = Type
        exclude = (['typeVersion','version','hash'])

################################################################################
# 
# Class Name: TypeVersionSerializer
#
# Description:   Serializer for types versions
# 
################################################################################      
class TypeVersionSerializer(MongoEngineModelSerializer):
    class Meta:
        model = TypeVersion

################################################################################
# 
# Class Name: resTypeSerializer
#
# Description:   Serializer for result set of types
# 
################################################################################     
class resTypeSerializer(serializers.Serializer):
    title = serializers.CharField()
    filename = serializers.CharField()
    content = serializers.CharField()
    typeVersion = serializers.CharField()
    version = serializers.IntegerField()
    hash = serializers.CharField()
    dependencies = serializers.CharField()
    id = serializers.CharField(required=False)
  
################################################################################
# 
# Class Name: instanceSerializer
#
# Description:   Serializer for repository instance
# 
################################################################################  
class instanceSerializer(MongoEngineModelSerializer):
    class Meta:
        model = Instance

################################################################################
# 
# Class Name: mewInstanceSerializer
#
# Description:   Serializer for new repository instance
# 
################################################################################  
class newInstanceSerializer(serializers.Serializer):
    name = serializers.CharField()
    protocol = serializers.CharField()
    address = serializers.CharField()
    port = serializers.IntegerField()
    user = serializers.CharField()
    password = serializers.CharField()
    client_id = serializers.CharField()
    client_secret = serializers.CharField()

################################################################################
# 
# Class Name: resInstanceSerializer
#
# Description:   Serializer for result set of instances
# 
################################################################################
class resInstanceSerializer(serializers.Serializer):
    name = serializers.CharField()
    protocol = serializers.CharField()
    address = serializers.CharField()
    port = serializers.IntegerField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    expires = serializers.CharField()
    id = serializers.CharField(required=False)

################################################################################
# 
# Class Name: UserSerializer
#
# Description:   Serializer for users
# 
################################################################################   
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()

################################################################################
# 
# Class Name: insertUserSerializer
#
# Description:   Serializer for users to add
# 
################################################################################
class insertUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)

################################################################################
# 
# Class Name: updateUserSerializer
#
# Description:   Serializer for users to update
# 
################################################################################
class updateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
