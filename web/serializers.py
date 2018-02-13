from rest_framework import serializers
from web.models import PpProjectDetail


class PpProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PpProjectDetail
        fields = ('id', 'project_name')
