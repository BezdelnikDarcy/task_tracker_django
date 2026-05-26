from task_manager.models import Tasks
from task_manager.v1.serializers import TaskSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser



@extend_schema(tags=["Tasks"])
class TaskListApiView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAdminUser,)


    @extend_schema(
        summary="Get all tasks",
        description="Get all tasks",
        responses={200: TaskSerializer},
    )
    def get(self, request, format=None):
        tasks = Tasks.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create task",
        description="Create task",
        request=TaskSerializer,
        responses={201: TaskSerializer},
    )
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Tasks"])
class TaskDetailApiView(APIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self, pk):
        try:
            return Tasks.objects.get(pk=pk)
        except Tasks.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={200: TaskSerializer},
    )
    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    @extend_schema(
        request=TaskSerializer,
        responses={200: TaskSerializer},
    )
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

