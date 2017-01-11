from django.db import models
from .discord_roles import DiscordRole
from .diep_tank import DiepTank,DiepTankInheritance
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .clan_user import ClanUser,ClanUserRoles




class GuildFight(models.Model):

    STATUS_OPTIONS=(
        (1,'Not Finished'),
        (2,'Team 1 won'),
        (3,'Team 2 won'),
        (4,'Draw')
    )

    RULES_OPTIONS=(
        (1,'No Rules'),
        (2,'Only lvl 45tanks with each from a unique lvl 30 tank'),
        (3,'Only unique lvl 45tanks'),
        (4,'Only lvl 45tanks')

    )


    team1=models.ForeignKey(DiscordRole, related_name="team1",on_delete=models.CASCADE)
    team2=models.ForeignKey(DiscordRole, related_name="team2",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status=models.PositiveSmallIntegerField(choices=STATUS_OPTIONS)
    rules=models.PositiveSmallIntegerField(choices=RULES_OPTIONS,default=RULES_OPTIONS[0][0])
    number_of_players=models.PositiveIntegerField(default=6)

    manager=models.ForeignKey(ClanUser,related_name='manager')

    pointswinner=models.PositiveSmallIntegerField(default=10)
    pointsloser=models.PositiveSmallIntegerField(default=5)



    def get_available_tanks(self,team):
        if self.rules==2:#only level 45 tanks allowed and the parent tank (level 30) is banned for other level 45 tanks
            #first get current participations for this team
            currentlyusedtanksparticipations=GuildFightParticipation.objects.filter(fight=self,guild=team)
            #Get the tanks for those participations
            currentlyusedtanks=DiepTank.objects.filter(fightparticipationtank__fight__participant=currentlyusedtanksparticipations)
            #now get the relations
            inheritances=DiepTankInheritance.objects.filter(me=currentlyusedtanks)
            #we get the ids for each parent from those relations
            parentids=set()
            for inheritance in inheritances:
                parentids.add(inheritance.parent.id)
            #get every tier 3 tank and filter those with the ids we just got
            currentlyusedparenttanks=DiepTank.objects.filter(tier=3).filter(pk__in=parentids)
            #get all tier4 tanks and filter those out that have a parent that is already used
            return DiepTank.objects.filter(tier=4).exclude(inheritance__parent=currentlyusedparenttanks)
        elif self.rules==3:#unique lvl 45 tanks
            #first get current participations for this team
            currentlyusedtanksparticipations=GuildFightParticipation.objects.filter(fight=self,guild=team)
            #Get the tanks for those participations
            currentlyusedtanks=DiepTank.objects.filter(fightparticipationtank__fight__participant=currentlyusedtanksparticipations)
            return DiepTank.objects.filter(tier=4).exclude(fightparticipationtank=currentlyusedtanksparticipations)

        elif self.rules==4:
            return DiepTank.objects.filter(tier=4)


        return DiepTank.objects.all()


    @property
    def available_tanks_team1(self):
        return self.get_available_tanks(self.team1)


    @property
    def available_tanks_team2(self):
        return self.get_available_tanks(self.team2)


    @property
    def winner(self):
        "Get's the winner or None if not decided"
        if self.status==2:
            return self.team1
        elif self.status==3:
            return self.team2
        return None

    @property
    def loser(self):
        "Get's the winner or None if not decided"
        if self.status==2:
            return self.team2
        elif self.status==3:
            return self.team1
        return None


    @property
    def team1fightparticipants(self):
        return GuildFightParticipation.objects.filter(fight=self,guild=self.team1)


    @property
    def team2fightparticipants(self):
        return GuildFightParticipation.objects.filter(fight=self,guild=self.team2)

    @property
    def winnerparticipants(self):


        if self.status==2:
            return self.team1fightparticipants
        elif self.status==3:
            return self.team2fightparticipants
        else:
            return self.team1fightparticipants

    @property
    def loserparticipants(self):

        if self.status==2:
            return self.team2fightparticipants
        elif self.status==3:
            return self.team1fightparticipants
        else:
            return self.team2fightparticipants


    @property
    def decided(self):
        return self.status!=1


    @property
    def has_winner(self):
        return self.status==1 or self.status==2

    @property
    def name(self):
        try:
            if self.team1 and self.team2:
                pass
        except:
            return "team1"+' vs '+"team2"
        else:
            return self.team1.name+' vs '+self.team2.name


    def __str__(self):
        return str(self.date)+": "+self.name


class GuildFightParticipation(models.Model):
    fight=models.ForeignKey(GuildFight,related_name="participant",on_delete=models.CASCADE)
    user=models.ForeignKey(ClanUser,related_name="guildfight",on_delete=models.CASCADE)
    tank=models.ForeignKey(DiepTank,related_name='fightparticipationtank')
    guild=models.ForeignKey(DiscordRole,related_name="guildfight_guild",on_delete=models.CASCADE)

    class Meta:
        unique_together=('fight','user')

    def __str__(self):
        return self.fight.__str__()


    @receiver(pre_delete, sender=ClanUserRoles)
    def delete_guildfightparticipation(sender, instance=None, created=False, **kwargs):
        """Deletes fight participations for unfinished fights"""
        clanuserrole=instance
        role=clanuserrole.role#discord_role
        user=clanuserrole.clan_user#clan_user

        if role.is_clan_guild:
            GuildFightParticipation.objects.filter(fight__status=1,user=user,guild=role).delete()


