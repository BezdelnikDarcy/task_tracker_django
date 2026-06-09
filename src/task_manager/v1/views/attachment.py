from task_manager.models import Attachments
from task_manager.v1.serializers.attachment import AttachmentSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Attachments"])
class AttachmentListApiView(APIView):
    serializer_class = AttachmentSerializer

    @extend_schema(
        summary="Get all attachments",
        description="Get all attachments",
        responses={200: AttachmentSerializer},
    )
    def get(self, request, format=None):
        attach = Attachments.objects.all()
        serializer = AttachmentSerializer(attach, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create attachment",
        description="Create attachment",
        request=AttachmentSerializer,
        responses={201: AttachmentSerializer},
    )
    def post(self, request, format=None):
        serializer = AttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Attachments"])
class AttachmentDetailApiView(APIView):
    serializer_class = AttachmentSerializer

    def get_object(self, pk):
        try:
            return Attachments.objects.get(pk=pk)
        except Attachments.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={200: AttachmentSerializer},
    )
    def get(self, request, pk, format=None):
        attach = self.get_object(pk)
        serializer = AttachmentSerializer(attach)
        return Response(serializer.data)

    @extend_schema(
        request=AttachmentSerializer,
        responses={200: AttachmentSerializer},
    )
    def put(self, request, pk, format=None):
        attach = self.get_object(pk)
        serializer = AttachmentSerializer(attach, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        attach = self.get_object(pk)
        attach.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)