from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from ..models.diep_gamemode import DiepGamemode


class GamemodeSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model=DiepGamemode
        fields=('id','name')
        list_serializer_class = BulkListSerializer




