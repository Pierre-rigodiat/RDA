################################################################################
#
# File Name: views.py
# Application: api
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################

# REST Framework
from rest_framework.decorators import api_view
from rest_framework import generics
# Models
from mgi.models import SavedQuery, Jsondata
# Serializers
from api.serializers import savedQuerySerializer, jsonDataSerializer

@api_view(['GET','POST'])
def savedQuery_list(request):
    if request.method == 'GET':
        savedQueries = SavedQuery.objects
        serializer = savedQuerySerializer(savedQueries)
        return Response(serializer.data)

    elif request.method == 'POST':        
        serializer = savedQuerySerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def savedQuery_detail(request, pk):
    """
    Retrieve, update or delete a saved query instance.
    """              
    try:
        savedQuery = SavedQuery.objects.get(pk=pk)
    except SavedQuery.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = savedQuerySerializer(savedQuery)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = savedQuerySerializer(savedQuery, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        savedQuery.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class JsonDataList(generics.ListCreateAPIView):
#     serializer_class = jsonDataSerializer
#     
#     def get_queryset(self):
#         return Jsondata.objects()

@api_view(['GET','POST'])
def jsonData_list(request):
    if request.method == 'GET':
        jsonData = Jsondata.objects()
        serializer = jsonDataSerializer(jsonData)
        return Response(serializer.data)
 
    elif request.method == 'POST':        
        serializer = jsonDataSerializer(data=request.DATA)
        if serializer.is_valid():
            jsondata = Jsondata(schemaID = request.DATA['schema'], json = request.DATA['content'], title = request.DATA['title'])
            jsondata.save()
#             serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def jsonData_detail(request, pk):
    """
    Retrieve, update or delete a saved query instance.
    """              

    jsonData = Jsondata.get(pk)
    if jsonData is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = jsonDataSerializer(jsonData)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = jsonDataSerializer(jsonData, data=request.DATA)
        if serializer.is_valid():
            Jsondata.update(pk, request.DATA)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        Jsondata.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)





# Previous work
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

#from rest_framework.generics import (
#    ListCreateAPIView, RetrieveUpdateDestroyAPIView)

from curate.models import Task
from api.serializers import TaskSerializer
from api.permissions import IsOwnerOrReadOnly


#class TaskMixin(object):
#    queryset = Task.objects.all()
#    serializer_class = TaskSerializer
#    permission_classes = (IsOwnerOrReadOnly,)

#    def pre_save(self,obj):
#        obj.owner = self.request.user

#class TaskList(TaskMixin, ListCreateAPIView):
#    pass

#class TaskDetail(TaskMixin, RetrieveUpdateDestroyAPIView):
#    pass

@api_view(['GET', 'POST'])
def task_list(request):
    """
    List all tasks, or creat a new task.
    """

    if request.method == 'GET':
        print "task_list GET request"
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks)
        return Response(serializers.data)

    elif request.method == 'POST':
        print "task_list POST request"
        serializer = TaskSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response (
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def task_detail(request, pk):
    """
    Get, update, or delete a specific task
    """

    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


