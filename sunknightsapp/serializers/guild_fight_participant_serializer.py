from rest_framework import serializers
from ..models.guildfight import GuildFightParticipation
from rest_framework_bulk import BulkListSerializer
from .clan_user_roles_serializer import ClanUserRolesSerializer,BulkSerializerMixin
from .clan_user_serializer import ClanUserSerializerBasic


class GuildfightParticpantSerializer(BulkSerializerMixin,serializers.ModelSerializer):

    user=ClanUserSerializerBasic(many=False,read_only=True)


    class Meta:
        model=GuildFightParticipation
        fields=('__all__')
        list_serializer_class = BulkListSerializer

