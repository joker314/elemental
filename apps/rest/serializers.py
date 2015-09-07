from django.core.exceptions import PermissionDenied

from rest_framework import routers, serializers, viewsets

from apps.projects.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('username', 'shared', 'id', 'data', 'name', )

    def get_username(self, obj):
        return obj.user.username

    def update(self, instance, validated_data):
        get = validated_data.get
        if self.context['request'].user == instance.user:
            print get('data')
            instance.data = get('data', instance.data)
            instance.save()
            return instance
        raise PermissionDenied


class ProjectCreateSerializer(serializers.ModelSerializer):

    def create(self, kwargs):
        kwargs['user'] = self.context['request'].user
        return Project.objects.create(**kwargs)

    class Meta:
        model = Project
        fields = ('data', 'name', 'id', )