from django.db import models
from .points_info import PointsInfo
from .clan_user import ClanUser

class PointSubmission(models.Model):
    pointsinfo = models.ForeignKey(PointsInfo)
    points = models.IntegerField()
    proof = models.CharField(max_length=200)
    manager=models.ForeignKey(ClanUser)
    accepted=models.BooleanField(default=False)
    decided=models.BooleanField(default=False)

    submitterText=models.TextField(max_length=200,default="")
    managerText=models.TextField(max_length=200,default="")


    date=models.DateTimeField()


    def __str__(self):
        return self.pointsinfo.user.nickname + ": " + self.points