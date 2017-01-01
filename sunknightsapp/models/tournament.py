from django.db import models
from .guildfight import GuildFight
from .clan_user import ClanUser


class Tournament(models.Model):
    name=models.CharField(max_length=20)
    description=models.TextField(max_length=500)
    finished=models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)

    creator=models.ForeignKey(ClanUser)


    #TODO get winner guild, distribute points for winning tournament


    def __str__(self):
        return self.name+": "+self.description


    @property
    def all_registered_fights(self):
        return GuildFight.objects.filter(fight_connector__tournament=self)

    @property
    def unfinished_registered_fights(self):
        return GuildFight.objects.filter(fight_connector__tournament=self,status=1)

    @property
    def finished_registered_fights(self):
        return GuildFight.objects.filter(fight_connector__tournament=self).exclude(status=1)


    @property
    def num_registered_fights(self):
        fight_connectors_count= TournamentFightConnector.objects.filter(tournament=self).count()
        return fight_connectors_count

    @property
    def num_finished_fights(self):
        fight_connectors= TournamentFightConnector.objects.filter(tournament=self).exclude(fight__status=1).count()#exclude undecided fights
        return fight_connectors





class TournamentFightConnector(models.Model):
    tournament=models.ForeignKey(Tournament,related_name="fight_connectors",on_delete=models.CASCADE)
    fight=models.ForeignKey(GuildFight, related_name="fight_connector",on_delete=models.CASCADE)


    class Meta:
        unique_together=('tournament','fight')

    def __str__(self):
        return self.tournament.name+" fight"