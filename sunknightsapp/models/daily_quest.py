from django.db import models
from ..models.clan_user import ClanUser
from .diep_tank import DiepTank
from .utility.little_things import QUEST_TIER_OPTIONS

class Quest(models.Model):
    date = models.DateTimeField(auto_now_add=True,db_index=True)
    permed=models.BooleanField(default=False)



    @property
    def validtasks(self):
        return self.tasks.filter(deleted=False).order_by('points')

    def __str__(self):
                    return str(self.date)


class QuestTask(models.Model):

    quest=models.ForeignKey(Quest,related_name='tasks',on_delete=models.CASCADE)
    tier=models.PositiveSmallIntegerField(choices=QUEST_TIER_OPTIONS,default=QUEST_TIER_OPTIONS[0][0])
    questtext=models.CharField(max_length=500)
    deleted=models.BooleanField(default=False)
    manager=models.ForeignKey(ClanUser, on_delete=models.CASCADE)
    points=models.PositiveSmallIntegerField(default=0)
    cooldown=models.PositiveIntegerField(default=24)#24 hours

    @property
    def questtext_html(self):
        import markdown_deux
        return markdown_deux.markdown(self.questtext)[3:-5]




    def __str__(self):
        return self.questtext


class QuestTankMultiplier(models.Model):
    quest=models.ForeignKey(Quest,related_name='multipliers',on_delete=models.CASCADE)
    tank=models.ForeignKey(DiepTank,default=1)
    multiplier=models.DecimalField(decimal_places=2, max_digits=4, default=1)
    manager=models.ForeignKey(ClanUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.tank.name


class QuestBuild(models.Model):
    quest=models.ForeignKey(Quest,related_name='builds',on_delete=models.CASCADE)
    build=models.CharField(max_length=500)
    manager=models.ForeignKey(ClanUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.build