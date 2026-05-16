from rest_framework import serializers
from task_manager.models import ProjectDetails

class ProjectDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectDetails
        fields = ('id', 'info', 'serial_id', 'project',)
        read_only_fields = ('id',)