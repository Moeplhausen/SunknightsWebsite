from django.db import models
from .discord_roles import DiscordRole
from .clan_user import ClanUser

class GuildFight(models.Model):

    STATUS_OPTIONS=(
        (1,'Not Finished'),
        (2,'Team 1 won'),
        (3,'Team 2 won'),
        (4,'Draw')
    )


    team1=models.ForeignKey(DiscordRole, related_name="team1")
    team2=models.ForeignKey(DiscordRole, related_name="team2")
    date=models.DateTimeField()
    status=models.PositiveSmallIntegerField(choices=STATUS_OPTIONS)



    @property
    def winner(self):
        "Get's the winner or None if not decided"
        if self.status==2:
            return self.team1
        elif self.status==3:
            return self.team2
        return None


    @property
    def team1fightparticipants(self):
        return GuildFightParticipation.objects.filter(fight=self).filter(guild=self.team1)


    @property
    def team2fightparticipants(self):
        return GuildFightParticipation.objects.filter(fight=self).filter(guild=self.team2)


    @property
    def decided(self):
        return self.status!=1


    @property
    def has_winner(self):
        return self.status==1 or self.status==2


    def __str__(self):
        try:
            if self.team1 and self.team2:
                pass
        except:
            return str(self.date)+": "+"team1"+' vs '+"team2"
        else:
            return str(self.date)+": "+self.team1.name+' vs '+self.team2.name


class GuildFightParticipation(models.Model):
    fight=models.ForeignKey(GuildFight,related_name="participant")
    user=models.ForeignKey(ClanUser,related_name="guildfight")
    guild=models.ForeignKey(DiscordRole,related_name="guildfight_guild")

    def __str__(self):
        return self.fight.__str__()

