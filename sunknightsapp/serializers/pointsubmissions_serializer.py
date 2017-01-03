from rest_framework import serializers
from ..models.point_submission import PointsManagerAction,BasicUserPointSubmission,BasicPointSubmission
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from .clan_user_serializer import ClanUserSerializerDiscord_id
from .daily_quest_serializer import DailyQuestSerializer
from .tank_serializer import DiepTankSimpleSerializer
from .gamemode_serializer import GamemodeSerializer
from .clan_user_serializer import PointsInfoBasicSerializer



class PointsManagerActionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    daily_quest=DailyQuestSerializer(many=False,read_only=True)

    class Meta:
            model=PointsManagerAction
            fields=('id','manager','managerText','points','managerText','pointsinfo','accepted','decided','daily_quest')
            list_serializer_class = BulkListSerializer

class BasicPointsSubmissionSerializer(BulkSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model=BasicPointSubmission
        fields=('id','manager','managerText','points','managerText','pointsinfo','accepted','decided')
        list_serializer_class = BulkListSerializer

class BasicUserPointSubmissionSerializer(BulkSerializerMixin, serializers.ModelSerializer):



    daily_quest=DailyQuestSerializer(many=False,read_only=True)
    tank=DiepTankSimpleSerializer(many=False,read_only=True)
    gamemode=GamemodeSerializer(many=False,read_only=True)
    pointsinfo=PointsInfoBasicSerializer(many=False,read_only=True)

    class Meta:
        model=BasicUserPointSubmission
        fields=('id','date','manager','managerText','points','submitterText','gamemode','pointsinfo','accepted','decided','daily_quest','proof','tank','score')
        list_serializer_class = BulkListSerializer

