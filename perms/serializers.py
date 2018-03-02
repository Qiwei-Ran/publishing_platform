from perms.models import AuthGroup
from rest_framework import serializers
from users.models import CustomUser


class AuthGroupSerializer(serializers.ModelSerializer):
    group_user = serializers.SlugRelatedField(many=True, read_only=True, slug_field='first_name')

    class Meta:
        model = AuthGroup
        fields = '__all__'


class RoleUpdateUserGroupSerializer(serializers.ModelSerializer):
    """Update the Roles group_user"""
    group_user = serializers.PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all())

    class Meta:
        model = AuthGroup
        fields = ['group_name', 'group_user']
