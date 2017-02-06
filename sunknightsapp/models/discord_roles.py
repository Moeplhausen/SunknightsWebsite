from django.db import models

from .discord_server import DiscordServer


class DiscordRole(models.Model):
    name = models.CharField(max_length=30)
    discord_server = models.ForeignKey(DiscordServer, on_delete=models.CASCADE)
    discord_id = models.CharField(max_length=20,default=0, unique=True)
    discord_color = models.IntegerField(default=0)
    can_manage_points = models.BooleanField(default=False)
    can_manage_wars = models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    discord_isDeleted = models.BooleanField(default=False)
    guild_leader_role = models.BooleanField(default=False)
    is_clan_guild=models.BooleanField(default=False)


    @property
    def members(self):
        from .clan_user import ClanUser

        return ClanUser.objects.filter(roles__role=self)

    @property
    def guild_leader(self):
        if not self.is_clan_guild:
            return None
        from .clan_user import ClanUser
        user = None
        try:
            user = ClanUser.objects.filter(roles__role__guild_leader_role=True).get(roles__role=self)
        except ClanUser.DoesNotExist:
            return None
        return user

    def submitted_users(self,week=0):
        import datetime
        date = datetime.date.today()
        date=date-datetime.timedelta(7*week)
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        from .point_submission import BasicUserPointSubmission
        from .clan_user import ClanUser

        subsubs=BasicUserPointSubmission.objects.filter(accepted=True,decided=True,date__range=[start_week,end_week])

        users=ClanUser.objects.filter(roles__role=self,pointsinfo__basicpointsubmission__in=subsubs).distinct()
        return users

    def submitted_points(self,week=0):
        from .point_submission import BasicUserPointSubmission
        from .clan_user import ClanUser
        from django.db.models import Sum
        import datetime
        date = datetime.date.today()
        date=date-datetime.timedelta(7*week)
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)

        users=ClanUser.objects.filter(roles__role=self)
        sumpoints=BasicUserPointSubmission.objects.filter(pointsinfo__user__in=users,accepted=True,decided=True,date__range=[start_week,end_week]).aggregate(sum=Sum('points'))['sum'] or 0


        return sumpoints

    @property
    def submitted_points_cur_week(self):
        return self.submitted_points()

    @property
    def submitted_users_cur_week(self):
        return self.submitted_users()

    @property
    def submitted_points_week_1(self):
        return self.submitted_points(1)

    @property
    def submitted_users_week_1(self):
        return self.submitted_users(1)

    def __str__(self):
        return self.name

class SunKnightsRole(DiscordRole):
    pass


class SunKnightsBadgeRole(DiscordRole):
    from .diep_tank import DiepTank
    tank = models.ForeignKey(DiepTank, on_delete=models.CASCADE)