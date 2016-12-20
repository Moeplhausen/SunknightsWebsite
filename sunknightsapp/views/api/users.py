from rest_framework import viewsets
from ...serializers.clan_user_serializer import ClanUserSerializer
from ...models.clan_user import ClanUser
from rest_framework import viewsets

class ClanUsersViewSet(viewsets.ModelViewSet):
    serializer_class = ClanUserSerializer
    queryset = ClanUser.objects.all()
    lookup_field = 'discord_id'

