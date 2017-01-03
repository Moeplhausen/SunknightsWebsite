from django.db import models
from .discord_server import DiscordServer


class DiscordRole(models.Model):
    name = models.CharField(max_length=30)
    discord_server = models.ForeignKey(DiscordServer, on_delete=models.CASCADE)
    discord_id = models.CharField(max_length=20,default=0, unique=True)
    discord_color = models.IntegerField(default=0)
    can_manage_points = models.BooleanField(default=False)
    can_manage_wars = models.BooleanField(default=False)
    discord_isDeleted = models.BooleanField(default=False)
    guild_leader_role = models.BooleanField(default=False)
    is_clan_guild=models.BooleanField(default=False)


    @property
    def members(self):
        from .clan_user import ClanUser

        print(ClanUser.objects.filter(roles__role=self))

        return ClanUser.objects.filter(roles__role=self)

    @property
    def guild_leader(self):
        if not self.is_clan_guild:
            return None
        from .clan_user import ClanUser
        user = None
        try:
            user = ClanUser.objects.filter(roles__role__clan_leader=True).get(roles__role=self)
        except ClanUser.DoesNotExist:
            return None
        return user


    def __str__(self):
        return self.name

class SunKnightsGuild(DiscordRole):
    pass


