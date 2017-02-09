from rest_framework import viewsets
from ...serializers.daily_quest_serializer import QuestSerializer
from ...models.daily_quest import Quest


class QuestsViewSet(viewsets.ModelViewSet):
    serializer_class = QuestSerializer
    queryset = Quest.objects.all()
