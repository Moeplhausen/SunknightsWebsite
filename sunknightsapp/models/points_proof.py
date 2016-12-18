from django.db import models
from .point_submission import PointSubmission
from .clan_user import ClanUser

class PointsProof(models.Model):
    proof = models.CharField(max_length=200)
    submission=models.OneToOneField(PointSubmission)
    manager=models.ForeignKey(ClanUser)
    accepted=models.BooleanField(default=False)
    decided=models.BooleanField(default=False)



    def __str__(self):
        return self.submission.pointsinfo.user.nickname + ": " + self.proof