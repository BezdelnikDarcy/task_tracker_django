from task_manager.models import Projects
from task_manager.v1.serializers.project import ProjectSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Projects"])
class ProjectListApiView(APIView):
    serializer_class = ProjectSerializer

    @extend_schema(
        summary="Get all projects",
        description="Get all projects",
        responses={200: ProjectSerializer},
    )
    def get(self, request, format=None):
        project = Projects.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create project",
        description="Create project",
        request=ProjectSerializer,
        responses={201: ProjectSerializer},
    )
    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Projects"])
class ProjectDetailApiView(APIView):
    serializer_class = ProjectSerializer

    def get_object(self, pk):
        try:
            return Projects.objects.get(pk=pk)
        except Projects.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={200: ProjectSerializer},
    )
    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    @extend_schema(
        request=ProjectSerializer,
        responses={200: ProjectSerializer},
    )
    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)