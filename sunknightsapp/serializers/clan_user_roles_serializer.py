from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from ..models.clan_user import ClanUserRoles
from .discord_roles_serializer import DiscordRolesFastSerializer


class ClanUserRolesSerializer(BulkSerializerMixin,serializers.ModelSerializer):



    class Meta:
        model=ClanUserRoles
        fields='__all__'
        list_serializer_class = BulkListSerializer



class ClanUserRolesDetailedSerializer(BulkSerializerMixin,serializers.ModelSerializer):

    role=DiscordRolesFastSerializer(many=False,read_only=True)

    class Meta:
        model=ClanUserRoles
        fields=('id','role')
        list_serializer_class = BulkListSerializer


