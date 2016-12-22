from django.db import models
from .guildfight import GuildFight


class Tournament(models.Model):
    name=models.CharField(max_length=20)
    description=models.TextField(max_length=500)
    finished=models.BooleanField(default=False)


    def __str__(self):
        return self.name+": "+self.description


    @property
    def registered_fights(self):
        fight_connectors_count= TournamentFightConnector.objects.filter(tournament=self).count()
        return fight_connectors_count

    @property
    def finished_fights(self):
        fight_connectors= TournamentFightConnector.objects.filter(tournament=self).exclude(fight__status=1).count()#exclude undecided fights
        return fight_connectors

class TournamentFightConnector(models.Model):
    tournament=models.ForeignKey(Tournament,related_name="fight_connectors")
    fight=models.ForeignKey(GuildFight, related_name="fight_connector")