from rest_framework import viewsets
from rest_framework_bulk import BulkModelViewSet

from ...models.discord_roles import DiscordRole,SunKnightsBadgeRole
from ...serializers.discord_roles_serializer import DiscordRolesSerializer,SunKnightsBadgeRoleSerializer


class RolesViewSet(viewsets.ModelViewSet):
    serializer_class = DiscordRolesSerializer
    queryset = DiscordRole.objects.all()
    lookup_field = 'discord_id'




class SunKnightsBadgeRoleViewSet(BulkModelViewSet):
    serializer_class = SunKnightsBadgeRoleSerializer
    queryset = SunKnightsBadgeRole.objects.all()