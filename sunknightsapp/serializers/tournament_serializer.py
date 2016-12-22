from rest_framework import serializers
from ..models.tournament import Tournament,TournamentFightConnector
from .fight_serializer import GuildFightSerializer

from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin




class TournamentFightConnectorSerializer(BulkSerializerMixin,serializers.ModelSerializer):


    fight=GuildFightSerializer(many=False, read_only=True)


    class Meta:
                model=TournamentFightConnector
                fields=('__all__')
                list_serializer_class = BulkListSerializer


class TournamentSerializer(BulkSerializerMixin,serializers.ModelSerializer):

    fight_connectors=TournamentFightConnectorSerializer(many=True,read_only=True)


    class Meta:
        model=Tournament
        fields=('id','name','description', 'finished','fight_connectors','registered_fights','finished_fights')
        list_serializer_class = BulkListSerializer