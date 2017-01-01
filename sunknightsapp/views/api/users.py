from rest_framework import viewsets
from ...serializers.clan_user_serializer import ClanUserSerializer,PointsInfoSerializer
from ...models.clan_user import ClanUser
from ...models.points_info import PointsInfo
from rest_framework import viewsets

class ClanUsersViewSet(viewsets.ModelViewSet):
    serializer_class = ClanUserSerializer
    queryset = ClanUser.objects.all()
    lookup_field = 'discord_id'

class ClanUserPointsInfoViewSet(viewsets.ModelViewSet):
    serializer_class = PointsInfoSerializer
    queryset = PointsInfo.objects.all()
