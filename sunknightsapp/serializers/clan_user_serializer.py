from rest_framework import serializers
from ..models.clan_user import ClanUser
from rest_framework_bulk import BulkListSerializer
from .clan_user_roles_serializer import ClanUserRolesSerializer


class ClanUserSerializer(serializers.ModelSerializer):

    roles=ClanUserRolesSerializer(many=True,read_only=True)

    class Meta:
        model=ClanUser
        fields=('id','discord_id','discord_nickname','is_active','is_manager','roles')
        list_serializer_class = BulkListSerializer

