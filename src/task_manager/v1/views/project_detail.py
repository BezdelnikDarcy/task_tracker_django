from task_manager.models import ProjectDetails
from task_manager.v1.serializers.project_detail import ProjectDetailsSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser


@extend_schema(tags=["ProjectDetails"])
class ProjectDetailsListApiView(APIView):
    serializer_class = ProjectDetailsSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(
        summary="Get all projects",
        description="Get all projects",
        responses={200: ProjectDetailsSerializer},
    )
    def get(self, request, format=None):
        project_detail = ProjectDetails.objects.all()
        serializer = ProjectDetailsSerializer(project_detail, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create project",
        description="Create project",
        request=ProjectDetailsSerializer,
        responses={201: ProjectDetailsSerializer},
    )
    def post(self, request, format=None):
        serializer = ProjectDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["ProjectDetails"])
class ProjectDetailsDetailApiView(APIView):
    serializer_class = ProjectDetailsSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self, pk):
        try:
            return ProjectDetails.objects.get(pk=pk)
        except ProjectDetails.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={200: ProjectDetailsSerializer},
    )
    def get(self, request, pk, format=None):
        project_detail = self.get_object(pk)
        serializer = ProjectDetailsSerializer(project_detail)
        return Response(serializer.data)

    @extend_schema(
        request=ProjectDetailsSerializer,
        responses={200: ProjectDetailsSerializer},
    )
    def put(self, request, pk, format=None):
        project_detail = self.get_object(pk)
        serializer = ProjectDetailsSerializer(project_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project_detail = self.get_object(pk)
        project_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)