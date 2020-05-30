from rest_framework import viewsets
from ...serializers.clan_user_serializer import ClanUserSerializer,PointsInfoSerializer,ClanUserFasterSerializer, PointsInfoLBSerializer
from ...models.clan_user import ClanUser
from ...models.points_info import PointsInfo
from rest_framework import viewsets

class ClanUsersViewSet(viewsets.ModelViewSet):
    serializer_class = ClanUserSerializer
    queryset = ClanUser.objects.filter(provider='Discord').prefetch_related('pointsinfo','roles','roles__role','pointsinfo__masteries')
    lookup_field = 'discord_id'


class ClanUsersShortSet(viewsets.ModelViewSet):
    serializer_class = ClanUserFasterSerializer
    queryset = ClanUser.objects.filter(provider='Discord').select_related('pointsinfo').prefetch_related('roles','roles__role','pointsinfo__masteries')
    lookup_field = 'discord_id'

class ClanUserPointsInfoViewSet(viewsets.ModelViewSet):
    serializer_class = PointsInfoSerializer
    queryset = PointsInfo.objects.prefetch_related('user','masteries').all()

class ClanUserLeaderboardViewSet(viewsets.ModelViewSet):
    serializer_class = PointsInfoLBSerializer
    queryset = PointsInfo.objects.filter(totalpoints__gt=0).filter(user__is_active=True).order_by('-totalpoints')  
    # the '-' is for reversing the order (so the one who has most points will be on top