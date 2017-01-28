from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from ..models.discord_roles import SunKnightsRole, DiscordRole,SunKnightsBadgeRole
from .discord_mee6_points_serializer import DiscordMee6PointsRoleSerializer
from ..models.clan_user import ClanUser

class DiscordRolesSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class ClanUserSerializerPointsBasic(BulkSerializerMixin,serializers.ModelSerializer):
        class Meta:
            model=ClanUser
            fields=('id','discord_id','discord_nickname','discord_discriminator','avatar',)
            list_serializer_class = BulkListSerializer


    rolepoints=DiscordMee6PointsRoleSerializer(many=True,read_only=True)
    class Meta:
        model=DiscordRole
        fields=('id','name','discord_id','discord_color','can_manage_points','can_manage_wars','discord_isDeleted','guild_leader_role','is_clan_guild','discord_server','rolepoints')

        list_serializer_class = BulkListSerializer




class DiscordRolesFastSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model=DiscordRole
        fields='__all__'
        list_serializer_class = BulkListSerializer


class SunKnightsBadgeRoleSerializer(BulkSerializerMixin,serializers.ModelSerializer):

    class Meta:
        model=SunKnightsBadgeRole
        fields='__all__'
        list_serializer_class = BulkListSerializer


class GuildRolesSerializer(DiscordRolesSerializer):


    class Meta:
        model=SunKnightsRole
        fields=('id','name','discord_id','discord_color','discord_server')


