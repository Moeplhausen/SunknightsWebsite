from django.db import models
from .diep_tank import DiepTank
from .points_info import PointsInfo, ClanUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .point_submission import BasicUserPointSubmission
from ..backgroundTask.webhook_spam import mastery_unlock
from .utility.little_things import MASTERY_TIER_OPTIONS,getMasteryRankByPoints


class Badge(models.Model):

    tank = models.ForeignKey(DiepTank, on_delete=models.CASCADE)
    pointsinfo = models.ForeignKey(PointsInfo, on_delete=models.CASCADE, related_name='badges')
    manager = models.ForeignKey(ClanUser)


    def __str__(self):
        return self.tank.name

    class Meta:
        ordering = ['tank']
        unique_together = ('tank', 'pointsinfo')
