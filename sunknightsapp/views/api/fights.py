from rest_framework import viewsets
from ...serializers.fight_serializer import GuildFightSerializer
from ...models.guildfight import GuildFight


class GuildFightsViewSet(viewsets.ModelViewSet):
    serializer_class = GuildFightSerializer
    queryset = GuildFight.objects.all()
