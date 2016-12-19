from django.db import models
from .discord_server import DiscordServer

class DiscordRole(models.Model):
    name=models.CharField(max_length=30)
    discord_server=models.ForeignKey(DiscordServer)
    discord_id=models.BigIntegerField(default=0)
    discord_color=models.IntegerField(default=0)
    is_clanguild=models.BooleanField(default=False)
    discord_isDeleted=models.BooleanField(default=False)

    def __str__(self):
        return self.name
