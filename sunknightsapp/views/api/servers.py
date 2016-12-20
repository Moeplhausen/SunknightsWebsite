from rest_framework import viewsets
from ...serializers.discord_server_serializer import DiscordServerSerializer
from ...models.discord_server import DiscordServer
from rest_framework_bulk import BulkModelViewSet

class ServersViewSet(BulkModelViewSet):
    serializer_class = DiscordServerSerializer
    queryset = DiscordServer.objects.all()
    lookup_field = 'discord_id'



