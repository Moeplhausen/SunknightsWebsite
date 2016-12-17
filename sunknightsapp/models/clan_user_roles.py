from django.db import models
from .discord_roles import DiscordRole
from .clan_user import ClanUser

class ClanUserRoles(models.Model):
    clan_user=models.ForeignKey(ClanUser,related_name='roles')
    role=models.ForeignKey(DiscordRole)

    class Meta:
        unique_together=('clan_user','role')


    def __str__(self):
        return self.clan_user.discord_nickname+': '+self.role.name