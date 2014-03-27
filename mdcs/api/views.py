################################################################################
#
# File Name: views.py
# Application: api
# Purpose:   
#
# Author: Sharief Youssef
#         sharief.youssef@nist.gov
#
# Sponsor: National Institue of Standards and Technology
#
################################################################################

from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

#from rest_framework.generics import (
#    ListCreateAPIView, RetrieveUpdateDestroyAPIView)

from curate.models import Task
from api.serializers import TaskSerializer
from api.permissions import IsOwnerOrReadOnly

# Create your views here.

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

    if reqeust.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Rsponse(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


