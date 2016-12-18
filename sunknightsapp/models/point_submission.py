from django.db import models
from .points_info import PointsInfo
from .clan_user import ClanUser

class PointSubmission(models.Model):
    pointsinfo = models.ForeignKey(PointsInfo)
    points = models.IntegerField()


    def __str__(self):
        return self.pointsinfo.user.nickname + ": " + self.points