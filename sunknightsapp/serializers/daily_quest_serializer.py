from rest_framework import serializers
from ..models.daily_quest import Quest,QuestBuild,QuestTankMultiplier,QuestTask
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from .tank_serializer import DiepTankSerializer
class QuestBuildSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model=QuestBuild
        fields=('__all__')
        list_serializer_class = BulkListSerializer

class QuestTankMultiplierSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    tank=DiepTankSerializer(many=False,read_only=True)

    class Meta:
        model=QuestTankMultiplier
        fields=('id','quest','tank','multiplier','manager')
        list_serializer_class = BulkListSerializer


class QuestTaskSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model=QuestTask
        fields=('__all__')
        list_serializer_class = BulkListSerializer


class QuestSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    tasks=QuestTaskSerializer(many=True,read_only=True)
    multipliers=QuestTankMultiplierSerializer(many=True,read_only=True)
    builds=QuestBuildSerializer(many=True,read_only=True)

    class Meta:
            model=Quest
            fields=('id','date','permed','tasks','multipliers','builds')
            list_serializer_class = BulkListSerializer

