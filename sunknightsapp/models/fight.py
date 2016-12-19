from django.db import models
from .discord_roles import DiscordRole

class Fight(models.Model):
    winner=models.ForeignKey(DiscordRole, related_name="winner")
    loser=models.ForeignKey(DiscordRole, related_name="loser")
    date=models.DateTimeField()
    finished=models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)+": "+self.winner.name+' vs '+self.loser.name