from rest_framework import viewsets
from ...serializers.daily_quest_serializer import QuestSerializer
from ...models.daily_quest import Quest
import datetime

def getCorrectTime(date=None):
    if date is None:
        return datetime.datetime.utcnow()

class QuestsViewSet(viewsets.ModelViewSet):




    serializer_class = QuestSerializer

    from django.db.models import Q

    queryset = Quest.objects.filter(Q(permed=True)|Q(date=(getCorrectTime(None)).replace(hour=0, minute=0, second=0, microsecond=0)))
