from task_manager.models import Comments
from task_manager.v1.serializers.comment import CommentSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["Comments"])
class CommentListApiView(APIView):
    serializer_class = CommentSerializer

    @extend_schema(
        summary="Get all comments",
        description="Get all comments",
        responses={200: CommentSerializer},
    )
    def get(self, request, format=None):
        comments = Comments.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create comment",
        description="Create comment",
        request=CommentSerializer,
        responses={201: CommentSerializer},
    )
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=["Comments"])
class CommentDetailApiView(APIView):
    serializer_class = CommentSerializer

    def get_object(self, pk):
        try:
            return Comments.objects.get(pk=pk)
        except Comments.DoesNotExist:
            raise Http404

    @extend_schema(
        responses={200: CommentSerializer},
    )
    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @extend_schema(
        request=CommentSerializer,
        responses={200: CommentSerializer},
    )
    def put(self, request, pk, format=None):
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)