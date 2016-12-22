from rest_framework import viewsets
from ...serializers.tournament_serializer import TournamentSerializer,TournamentFightConnectorSerializer
from ...models.tournament import Tournament,TournamentFightConnector
from rest_framework_bulk import BulkModelViewSet

class TournamentsViewSet(BulkModelViewSet):
    serializer_class = TournamentSerializer
    queryset = Tournament.objects.all()

class TournamentsFightsConnectorViewSet(BulkModelViewSet):
    serializer_class = TournamentFightConnectorSerializer
    queryset = TournamentFightConnector.objects.all()

