from rest_framework import viewsets
from ...serializers.clan_user_roles_serializer import ClanUserRolesSerializer
from ...models.clan_user import ClanUserRoles
from rest_framework_bulk import BulkModelViewSet

class UserRolesViewSet(BulkModelViewSet):
    serializer_class = ClanUserRolesSerializer
    queryset = ClanUserRoles.objects.all()


