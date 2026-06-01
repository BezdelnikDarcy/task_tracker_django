from rest_framework import serializers
from task_manager.models import Tasks, Projects
from account.models.users import User
from task_manager.v1.serializers.comment import CommentSerializer
from django_filters import OrderingFilter
import django_filters

class TaskQueryFilterSerializer(django_filters.FilterSet):
    name__icontains = django_filters.CharFilter(field_name='name',lookup_expr='icontains')
    description__icontains = django_filters.CharFilter(field_name='description',lookup_expr='icontains')
    created_at__gte = django_filters.DateFilter(field_name='created_at',lookup_expr='gte')
    created_at__lt = django_filters.DateFilter(field_name='created_at',lookup_expr='lte')
    priority__gt = django_filters.NumberFilter(field_name='priority', lookup_expr='gt')
    priority__lt = django_filters.NumberFilter(field_name='priority', lookup_expr='lt')
    ordering = OrderingFilter(
        fields=(
            ('priority','priority'),
            ('created_at','created_at'),
        )
    )

    class Meta:
        model = Tasks
        fields = ['name', 'status','priority', 'description', 'created_at']

class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    description = serializers.CharField(required=False, allow_blank=True, max_length=255)
    priority = serializers.IntegerField()
    status = serializers.CharField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comments = CommentSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Tasks.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.save()
        return instance