################################################################################
#
# File Name: serializers.py
# Application: api
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

from rest_framework import serializers
from rest_framework_mongoengine.serializers import MongoEngineModelSerializer
from mgi.models import SavedQuery

class jsonDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    schema = serializers.CharField()
    content = serializers.CharField()
    _id = serializers.CharField(required=False)
    
class savedQuerySerializer(MongoEngineModelSerializer):
    class Meta:
        model = SavedQuery
        
        
# Previous work
from curate.models import Task
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'description', 'completed') 