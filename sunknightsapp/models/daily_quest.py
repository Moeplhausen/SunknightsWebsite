from django.db import models
from ..models.clan_user import ClanUser
from .diep_tank import DiepTank
from .utility.little_things import QUEST_TIER_OPTIONS

class Quest(models.Model):
    date = models.DateTimeField(auto_now_add=True,db_index=True)
    permed=models.BooleanField(default=False)


    def __str__(self):
                    return str(self.date)


class QuestTask(models.Model):

    quest=models.ForeignKey(Quest,related_name='tasks',on_delete=models.CASCADE)
    tier=models.PositiveSmallIntegerField(choices=QUEST_TIER_OPTIONS,default=QUEST_TIER_OPTIONS[0][0])
    questtext=models.CharField(max_length=500)
    deleted=models.BooleanField(default=False)
    manager=models.ForeignKey(ClanUser, on_delete=models.CASCADE)
    points=models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.questtext




class QuestTankMultiplier(models.Model):
    dailyquest=models.ForeignKey(Quest,related_name='multipliers',on_delete=models.CASCADE)
    tank=models.ForeignKey(DiepTank)
    multiplier=models.DecimalField(decimal_places=2, max_digits=4, default=1)

    def __str__(self):
        return self.tank.name


class Questbuild(models.Model):
    dailyquest=models.ForeignKey(Quest,related_name='builds',on_delete=models.CASCADE)
    build=models.DecimalField(decimal_places=2, max_digits=4, default=1)

    def __str__(self):
        return self.build