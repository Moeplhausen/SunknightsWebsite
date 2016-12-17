from rest_framework import serializers
from ..models.discord_server import DiscordServer
from rest_framework_bulk import BulkListSerializer


class DiscordServerSerializer(serializers.ModelSerializer):
    class Meta:
        model=DiscordServer
        fields='__all__'
        list_serializer_class = BulkListSerializer

