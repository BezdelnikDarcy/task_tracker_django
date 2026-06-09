from rest_framework import generics, mixins
from config.pagination import CustomUserPagination
from account.models import User
from task_manager.v1.serializers.user import UserSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Users'])
class UserListApiView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomUserPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)