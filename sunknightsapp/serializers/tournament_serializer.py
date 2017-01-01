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

    all_registered_fights=GuildFightSerializer(many=True, read_only=True)
    unfinished_registered_fights=GuildFightSerializer(many=True, read_only=True)
    finished_registered_fights=GuildFightSerializer(many=True, read_only=True)

    class Meta:
        model=Tournament
        fields=('id','name','description', 'finished','num_registered_fights','num_finished_fights','all_registered_fights','unfinished_registered_fights','finished_registered_fights')
        list_serializer_class = BulkListSerializer