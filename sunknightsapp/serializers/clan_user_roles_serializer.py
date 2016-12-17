from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer
from ..models.clan_user_roles import ClanUserRoles


class ClanUserRolesSerializer(serializers.ModelSerializer):



    class Meta:
        model=ClanUserRoles
        fields='__all__'
        list_serializer_class = BulkListSerializer
