from rest_framework import serializers
from ..models.discord_role_points import DiscordRolePoints
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin


class DiscordMee6PointsRoleSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model=DiscordRolePoints
        fields=('__all__')
        list_serializer_class = BulkListSerializer


