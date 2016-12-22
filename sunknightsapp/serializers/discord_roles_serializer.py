from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from ..models.discord_roles import SunKnightsGuild, DiscordRole


class DiscordRolesSerializer(BulkSerializerMixin,serializers.ModelSerializer):




    class Meta:
        model=DiscordRole
        fields='__all__'
        list_serializer_class = BulkListSerializer





class GuildRolesSerializer(DiscordRolesSerializer):


    class Meta:
        model=SunKnightsGuild
        fields=('id','name','discord_id','discord_color','discord_server')


