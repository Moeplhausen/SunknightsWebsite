from django.db import models
from .clan_user import ClanUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count
from .utility.little_things import ELO_DEFAULT
import decimal


class PointsInfo(models.Model):
    user = models.OneToOneField(ClanUser, on_delete=models.CASCADE, unique=True)
    oldpoints = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    currentpoints = models.DecimalField(decimal_places=2, max_digits=19, default=0)
    masterypoints = models.DecimalField(decimal_places=2, max_digits=19, default=0, db_index=True)
    totalpoints = models.DecimalField(decimal_places=2, max_digits=19, default=0, db_index=True)

    permquestcd=models.DateTimeField(auto_now_add=True,db_index=True)

    elo = models.PositiveIntegerField(default=ELO_DEFAULT)

    @property
    def leaderboard_place(self):
        aggregate = PointsInfo.objects.filter(user__is_active=True).filter(totalpoints__gt=self.totalpoints).aggregate(
            ranking=Count('totalpoints'))
        return aggregate['ranking'] + 1

    def __str__(self):
        return self.user.discord_nickname + ": " + str(self.totalpoints) + "pts"

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_postinfo(sender, instance=None, created=False, **kwargs):
        if created:
            PointsInfo.objects.create(id=instance.id,user=instance)


    @property
    def daily_quests(self):
        from .daily_quest import Quest
        from datetime import timedelta
        import django
        now=django.utils.timezone.now()
        datesubtract =  now- timedelta(days=1)
        quests = Quest.objects.filter(permed=False,date__range=(datesubtract, now)).order_by('-date')
        return quests

    @property
    def next_rank(self):
        from .discord_role_points import DiscordRolePoints
        t= DiscordRolePoints.objects.filter(points__gte=self.totalpoints).order_by('points').first()
        return t



@receiver(post_save, sender=PointsInfo)
def create_postinfo(sender, instance=None, created=False, **kwargs):
    pointsinfo = instance

    calcpoints = pointsinfo.oldpoints + decimal.Decimal(pointsinfo.currentpoints) + decimal.Decimal(
        pointsinfo.masterypoints)
    if calcpoints != pointsinfo.totalpoints:
        pointsinfo.totalpoints = calcpoints
        pointsinfo.save()
