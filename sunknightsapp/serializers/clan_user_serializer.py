from rest_framework import serializers
from ..models.clan_user import ClanUser
from rest_framework_bulk import BulkListSerializer
from .clan_user_roles_serializer import ClanUserRolesSerializer,BulkSerializerMixin


class ClanUserSerializerBasic(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model=ClanUser
        fields=('id','discord_id','discord_nickname')
        list_serializer_class = BulkListSerializer


class ClanUserSerializer(BulkSerializerMixin,serializers.ModelSerializer):

    roles=ClanUserRolesSerializer(many=True,read_only=True)

    class Meta:
        model=ClanUser
        fields=('id','discord_id','discord_nickname','is_active','is_points_manager','is_war_manager','roles')
        list_serializer_class = BulkListSerializer


