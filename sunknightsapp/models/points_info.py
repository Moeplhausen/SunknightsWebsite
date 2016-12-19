from django.db import models
from .clan_user import ClanUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver



class PointsInfo(models.Model):
    user = models.OneToOneField(ClanUser,on_delete=models.CASCADE)
    oldpoints = models.IntegerField(default=0)
    currentpoints = models.IntegerField(default=0)

    def __str__(self):
        return self.user.discord_nickname+": "+str(self.currentpoints)+" ("+str(self.oldpoints)+")"

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_postinfo(sender, instance=None, created=False, **kwargs):
        if created: PointsInfo.objects.create(user=instance)