from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer
from ..models.discord_roles import DiscordRole


class DiscordRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model=DiscordRole
        fields='__all__'
        list_serializer_class = BulkListSerializer
