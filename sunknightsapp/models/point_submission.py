from django.db import models
from .points_info import PointsInfo
from .clan_user import ClanUser


class BasicPointSubmission(models.Model):
    manager = models.ForeignKey(ClanUser)
    accepted = models.BooleanField(default=False)
    decided = models.BooleanField(default=False)
    managerText = models.TextField(max_length=200, default="")
    date = models.DateTimeField(auto_now_add=True)
    pointsinfo = models.ForeignKey(PointsInfo, related_name="winner")
    points = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.pointsinfo.user.nickname + ": " + self.points



class BasicUserPointSubmission(BasicPointSubmission):
    submitterText = models.TextField(max_length=200, default="")
    proof = models.CharField(max_length=200, unique=True)


class PointsManagerAction(BasicPointSubmission):
    def __init__(self, points: int, reason=""):
        self.accepted = True
        self.decided = True
        self.points = points
        self.reason = reason


class OneOnOneFightSubmission(BasicUserPointSubmission):
    pointsinfoloser = models.ForeignKey(PointsInfo, related_name="loser")





