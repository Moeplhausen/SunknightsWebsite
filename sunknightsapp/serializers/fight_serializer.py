from rest_framework import serializers
from ..models.guildfight import GuildFight
from rest_framework_bulk import BulkListSerializer
from .discord_roles_serializer import GuildRolesSerializer,BulkSerializerMixin
from .guild_fight_participant_serializer import GuildfightParticpantSerializer

class GuildFightSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    team1=GuildRolesSerializer(many=False,read_only=True)
    team2=GuildRolesSerializer(many=False,read_only=True)

    team1fightparticipants=GuildfightParticpantSerializer(many=True,read_only=True)
    team2fightparticipants=GuildfightParticpantSerializer(many=True,read_only=True)


    class Meta:
            model=GuildFight
            fields=('id','date','status','team1','team2','decided','team1fightparticipants','team2fightparticipants')
            list_serializer_class = BulkListSerializer

