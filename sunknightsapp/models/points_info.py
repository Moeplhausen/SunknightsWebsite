from django.db import models
from .clan_user import ClanUser

class PointsInfo(models.Model):
    user = models.OneToOneField(ClanUser)
    oldpoints = models.IntegerField()
    currentpoints = models.IntegerField()

    def __str__(self):
        return self.user.nickname