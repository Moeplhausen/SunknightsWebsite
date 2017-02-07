from django.db import models
from ..models.clan_user import ClanUser

class DailyQuest(models.Model):

    TIER_OPTIONS=(
        (1,'Tier 1'),
        (2,'Tier 2'),
        (3,'Tier 3'),
    )



    date = models.DateTimeField(auto_now_add=True,db_index=True)
    tier=models.PositiveSmallIntegerField(choices=TIER_OPTIONS,default=TIER_OPTIONS[0][0])
    questtext=models.CharField(max_length=500)
    permed=models.BooleanField(default=False)
    creator=models.OneToOneField(ClanUser, on_delete=models.CASCADE)


    def __str__(self):
            return self.name
