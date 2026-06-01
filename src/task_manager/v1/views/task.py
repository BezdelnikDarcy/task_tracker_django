from task_manager.models import Tasks
from task_manager.v1.serializers.task import TaskSerializer, TaskQueryFilterSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework import generics, mixins
from config.pagination import CustomPagination



# @extend_schema(tags=["Tasks"])
# class TaskListApiView(APIView):
#     serializer_class = TaskSerializer
#     permission_classes = (IsAdminUser,)
#
#
#     @extend_schema(
#         summary="Get all tasks",
#         description="Get all tasks",
#         responses={200: TaskSerializer},
#     )
#     def get(self, request, format=None):
#         tasks = Tasks.objects.all()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)
#
#     @extend_schema(
#         summary="Create task",
#         description="Create task",
#         request=TaskSerializer,
#         responses={201: TaskSerializer},
#     )
#     def post(self, request, format=None):
#         serializer = TaskSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @extend_schema(tags=["Tasks"])
# class TaskDetailApiView(APIView):
#     serializer_class = TaskSerializer
#     permission_classes = (IsAdminUser,)
#
#     def get_object(self, pk):
#         try:
#             return Tasks.objects.get(pk=pk)
#         except Tasks.DoesNotExist:
#             raise Http404
#
#     @extend_schema(
#         responses={200: TaskSerializer},
#     )
#     def get(self, request, pk, format=None):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
#
#     @extend_schema(
#         request=TaskSerializer,
#         responses={200: TaskSerializer},
#     )
#     def put(self, request, pk, format=None):
#         task = self.get_object(pk)
#         serializer = TaskSerializer(task, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         task = self.get_object(pk)
#         task.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=['Task'])
class TaskListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    filterset_class = TaskQueryFilterSerializer

    def get_queryset(self):
        queryset = Tasks.objects.filter(assignee=self.request.user)

        gte = self.request.query_params.get('created_at__gte',)
        if gte:
            queryset = queryset.filter(created_at__gte=gte)

        lte = self.request.query_params.get('created_at__lte',)
        if lte:
            queryset = queryset.filter(created_at__lte=lte)
        return queryset



    @extend_schema(
        summary='Get all tasks',
        description='Get all tasks',
        request=TaskQueryFilterSerializer,
        responses={200: TaskSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        summary='Create task',
        description='Create task',
        request=TaskSerializer,
        responses={201: TaskSerializer},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@extend_schema(tags=['Task'])
class TaskDetailApiView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer


    @extend_schema(
        responses={200: TaskSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


    @extend_schema(
        request=TaskSerializer,
        responses={200: TaskSerializer},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)