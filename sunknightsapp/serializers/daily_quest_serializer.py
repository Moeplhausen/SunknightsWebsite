from rest_framework import serializers
from ..models.daily_quest import DailyQuest
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin

class DailyQuestSerializer(BulkSerializerMixin, serializers.ModelSerializer):


    class Meta:
            model=DailyQuest
            fields=('__all__')
            list_serializer_class = BulkListSerializer

