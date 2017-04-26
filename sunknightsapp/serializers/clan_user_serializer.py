from rest_framework import serializers
from ..models.clan_user import ClanUser,ClanUserPreferences
from ..models.points_info import PointsInfo
from rest_framework_bulk import BulkListSerializer
from .clan_user_roles_serializer import ClanUserRolesSerializer,BulkSerializerMixin,ClanUserRolesDetailedSerializer
from .mastery_serializer import MasterySerializer
from ..models.guildfight import GuildFight


class SmallGuildFightSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model=GuildFight
        fields=('id','name','date','status')
        list_serializer_class = BulkListSerializer




class ClanUserSerializerDiscord_id(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model=ClanUser
        fields=('discord_id',)
        list_serializer_class = BulkListSerializer


class ClanUserSerializerBasic(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model=ClanUser
        fields=('id','discord_id','discord_nickname','discord_discriminator','avatar','country_tag')
        list_serializer_class = BulkListSerializer


class ClanUserSerializer(BulkSerializerMixin,serializers.ModelSerializer):

    roles=ClanUserRolesDetailedSerializer(many=True,read_only=True)
    masteries=MasterySerializer(many=True,read_only=True)

    #open_fights=SmallGuildFightSerializer(many=True,read_only=True)
    # finished_fights=SmallGuildFightSerializer(many=True,read_only=True)

    class Meta:
        model=ClanUser
        fields=('id','leaderboard_place','avatar','discord_id','discord_nickname','is_active','is_points_manager','is_war_manager','roles','total_points','masteries','discord_discriminator')
        list_serializer_class = BulkListSerializer


class PointsInfoSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user=ClanUserSerializerBasic(many=False,read_only=True)

    masteries=MasterySerializer(many=True,read_only=True)

    class Meta:
        model=PointsInfo
        fields=('id','oldpoints','currentpoints','totalpoints','leaderboard_place','masterypoints','user','masteries','elo')
        list_serializer_class = BulkListSerializer

class PointsInfoFastSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user=ClanUserSerializerBasic(many=False,read_only=True)

    masteries=MasterySerializer(many=True,read_only=True)

    class Meta:
        model=PointsInfo
        fields=('id','oldpoints','currentpoints','totalpoints','masterypoints','user','masteries','elo')
        list_serializer_class = BulkListSerializer


class ClanUserFasterSerializer(BulkSerializerMixin,serializers.ModelSerializer):

    class PointsInfoFasterSerializer(BulkSerializerMixin,serializers.ModelSerializer):
        masteries=MasterySerializer(many=True,read_only=True)
        class Meta:
            model=PointsInfo
            fields=('id','currentpoints','totalpoints','masterypoints','oldpoints','masterypoints','masteries')
            list_serializer_class = BulkListSerializer


    roles=ClanUserRolesDetailedSerializer(many=True,read_only=True)
    pointsinfo=PointsInfoFasterSerializer(many=False,read_only=True)



    class Meta:
        model=ClanUser
        fields=('id','avatar','discord_id','discord_nickname','is_active','roles','discord_discriminator','pointsinfo','is_superuser',)
        list_serializer_class = BulkListSerializer





class PointsInfoBasicSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user=ClanUserSerializerBasic(many=False,read_only=True)

    class Meta:
        model=PointsInfo
        fields=('id','user')
        list_serializer_class = BulkListSerializer


class ClanUserPreferencesSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    clan_user=ClanUserSerializerBasic(many=False,read_only=True)

    class Meta:
        model=ClanUserPreferences
        fields=('id','clan_user','custom_background_enabled','custom_background_url')
        list_serializer_class = BulkListSerializer
