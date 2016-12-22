from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from ..models.clan_user import ClanUserRoles


class ClanUserRolesSerializer(BulkSerializerMixin,serializers.ModelSerializer):



    class Meta:
        model=ClanUserRoles
        fields='__all__'
        list_serializer_class = BulkListSerializer


