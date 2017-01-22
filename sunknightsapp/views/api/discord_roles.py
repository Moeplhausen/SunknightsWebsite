from rest_framework import viewsets
from ...serializers.discord_roles_serializer import DiscordRolesSerializer,SunKnightsBadgeRoleSerializer
from ...models.discord_roles import DiscordRole,SunKnightsBadgeRole
from rest_framework_bulk import BulkModelViewSet

class DiscordRolesViewSet(BulkModelViewSet):
    serializer_class = DiscordRolesSerializer
    queryset = DiscordRole.objects.all()


