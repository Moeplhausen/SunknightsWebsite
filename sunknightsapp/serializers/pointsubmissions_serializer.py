from rest_framework import serializers
from ..models.point_submission import PointsManagerAction
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from .clan_user_serializer import ClanUserSerializerDiscord_id
from .daily_quest_serializer import DailyQuestSerializer
class PointsManagerActionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    daily_quest=DailyQuestSerializer(many=False,read_only=True)

    class Meta:
            model=PointsManagerAction
            fields=('id','manager','managerText','points','managerText','pointsinfo','accepted','decided','daily_quest')
            list_serializer_class = BulkListSerializer

