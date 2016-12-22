from rest_framework import serializers
from ..models.tournament import Tournament
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin


class TournamentSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model=Tournament
        fields='__all__'
        list_serializer_class = BulkListSerializer

