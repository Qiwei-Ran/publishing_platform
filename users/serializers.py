from users.models import DepartmentMode, CustomUser
from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin


class DepartmentModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMode
        fields = ('id', 'department_name', 'description', 'desc_gid')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        list_serializer_class = BulkListSerializer
        exclude = ['password', 'first_name', 'last_name', 'session_key', 'menu_status']

    def get_field_names(self, declared_fields, info):
        fields = super(CustomUserSerializer, self).get_field_names(declared_fields, info)
        fields.extend(['is_valid'])
        return fields
