from rest_framework import viewsets
from ...serializers.clan_user_serializer import ClanUserSerializer,PointsInfoSerializer,ClanUserFasterSerializer
from ...models.clan_user import ClanUser
from ...models.points_info import PointsInfo
from rest_framework import viewsets

class ClanUsersViewSet(viewsets.ModelViewSet):
    serializer_class = ClanUserSerializer
    queryset = ClanUser.objects.filter(provider='Discord').prefetch_related('pointsinfo')
    lookup_field = 'discord_id'


class ClanUsersShortSet(viewsets.ModelViewSet):
    serializer_class = ClanUserFasterSerializer
    queryset = ClanUser.objects.filter(provider='Discord').prefetch_related('pointsinfo','roles')
    lookup_field = 'discord_id'

class ClanUserPointsInfoViewSet(viewsets.ModelViewSet):
    serializer_class = PointsInfoSerializer
    queryset = PointsInfo.objects.all()
