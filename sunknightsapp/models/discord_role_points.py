from django.db import models
from .discord_server import DiscordServer
from .discord_roles import DiscordRole


class DiscordRolePoints(models.Model):
    discord_role = models.ForeignKey(DiscordRole,on_delete=models.CASCADE,related_name='rolepoints')
    points=models.PositiveIntegerField(default=0)



    def __str__(self):
        return self.discord_role.name
