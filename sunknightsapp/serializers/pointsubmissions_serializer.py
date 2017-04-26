from rest_framework import serializers
from ..models.point_submission import PointsManagerAction, BasicUserPointSubmission, BasicPointSubmission, \
    OneOnOneFightSubmission
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from .clan_user_serializer import ClanUserSerializerDiscord_id,ClanUserFasterSerializer,ClanUserSerializerBasic
from .daily_quest_serializer import QuestSerializer,QuestBuildSerializer,QuestTankMultiplierSerializer
from .tank_serializer import DiepTankSimpleSerializer
from .gamemode_serializer import GamemodeSerializer
from .clan_user_serializer import PointsInfoBasicSerializer


class PointsManagerActionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    daily_quest = QuestSerializer(many=False, read_only=True)

    class Meta:
        model = PointsManagerAction
        fields = (
        'id', 'manager', 'managerText', 'points', 'managerText', 'pointsinfo', 'accepted', 'decided', 'daily_quest')
        list_serializer_class = BulkListSerializer


class BasicPointsSubmissionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = BasicPointSubmission
        fields = ('id', 'manager', 'managerText', 'points', 'managerText', 'pointsinfo', 'accepted', 'decided')
        list_serializer_class = BulkListSerializer






class BasicUserPointSubmissionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    daily_quest = QuestSerializer(many=False, read_only=True)
    tank = DiepTankSimpleSerializer(many=False, read_only=True)
    gamemode = GamemodeSerializer(many=False, read_only=True)
    pointsinfo = PointsInfoBasicSerializer(many=False, read_only=True)
    manager = ClanUserFasterSerializer(many=False, read_only=True)

    class Meta:
        model = BasicUserPointSubmission
        fields = (
        'id', 'date', 'manager', 'managerText', 'points', 'submitterText', 'gamemode', 'pointsinfo', 'accepted',
        'decided', 'daily_quest', 'proof', 'tank', 'score')
        list_serializer_class = BulkListSerializer


class BasicUserPointSubmissionSerializerMinimal(BulkSerializerMixin, serializers.ModelSerializer):
    tank = DiepTankSimpleSerializer(many=False, read_only=True)
    pointsinfo = PointsInfoBasicSerializer(many=False, read_only=True)
    manager = ClanUserSerializerBasic(many=False, read_only=True)

    class Meta:
        model = BasicUserPointSubmission
        fields = (
            'id', 'date', 'manager', 'managerText', 'points', 'submitterText', 'pointsinfo', 'accepted',
            'decided', 'proof', 'tank', 'score')
        list_serializer_class = BulkListSerializer


class BasicUserPointSubmissionWithSimilarSubsSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    daily_quest = QuestSerializer(many=False, read_only=True)
    tank = DiepTankSimpleSerializer(many=False, read_only=True)
    gamemode = GamemodeSerializer(many=False, read_only=True)
    pointsinfo = PointsInfoBasicSerializer(many=False, read_only=True)
    similarsubs=BasicUserPointSubmissionSerializer(many=True,read_only=True)
    get_daily_builds=QuestBuildSerializer(many=True,read_only=True)
    get_daily_multiplier=QuestTankMultiplierSerializer(many=True,read_only=True)

    class Meta:
        model = BasicUserPointSubmission
        fields = (
            'id', 'date', 'manager', 'managerText', 'points', 'submitterText', 'gamemode', 'pointsinfo', 'accepted',
            'decided', 'daily_quest', 'proof', 'tank', 'score','similarsubs','get_daily_builds','get_daily_multiplier')
        list_serializer_class = BulkListSerializer




class SmallEventQuestsSubmissionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    from .daily_quest_serializer import QuestTaskSerializer
    pointsinfo = PointsInfoBasicSerializer(many=False, read_only=True)

    class Meta:
        model = BasicUserPointSubmission
        fields = (
            'id', 'date', 'manager', 'managerText', 'points', 'submitterText',  'pointsinfo', 'accepted',
            'decided', 'proof',)
        list_serializer_class = BulkListSerializer



class BasicEventQuestsSubmissionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    from .daily_quest_serializer import QuestTaskSerializer
    daily_quest = QuestSerializer(many=False, read_only=True)
    pointsinfo = PointsInfoBasicSerializer(many=False, read_only=True)
    questtask=QuestTaskSerializer(many=False,read_only=True)
    proofused=SmallEventQuestsSubmissionSerializer(many=True,read_only=True)

    class Meta:
        model = BasicUserPointSubmission
        fields = (
            'id', 'date', 'manager', 'managerText', 'points', 'submitterText',  'pointsinfo', 'accepted',
            'decided', 'daily_quest', 'proof','questtask','proofused')
        list_serializer_class = BulkListSerializer



class SmallOneOnOneFightSubmissionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    pointsinfo = PointsInfoBasicSerializer(many=False, read_only=True)
    pointsinfoloser = PointsInfoBasicSerializer(many=False, read_only=True)

    class Meta:
        model = OneOnOneFightSubmission
        fields = ('id', 'date', 'manager', 'managerText', 'points', 'pointsinfo', 'accepted', 'decided', 'proof',
                  'pointsinfoloser', 'pointsloser')
        list_serializer_class = BulkListSerializer




class OneOnOneFightSubmissionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    pointsinfo = PointsInfoBasicSerializer(many=False, read_only=True)
    pointsinfoloser = PointsInfoBasicSerializer(many=False, read_only=True)
    proofused=SmallOneOnOneFightSubmissionSerializer(many=True,read_only=True)

    class Meta:
        model = OneOnOneFightSubmission
        fields = ('id', 'date', 'manager', 'managerText', 'points', 'pointsinfo', 'accepted', 'decided', 'proof',
                  'pointsinfoloser', 'pointsloser','proofused')
        list_serializer_class = BulkListSerializer
