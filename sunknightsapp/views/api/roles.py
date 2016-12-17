from rest_framework import viewsets
from ...serializers.discord_roles_serializer import DiscordRolesSerializer
from ...models.discord_roles import DiscordRole


class RolesViewSet(viewsets.ModelViewSet):
    serializer_class = DiscordRolesSerializer
    queryset = DiscordRole.objects.all()
    lookup_field = 'discord_id'