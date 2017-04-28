from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.utils import timezone


from ..managers.user_manager import UserManager
from .discord_roles import DiscordRole

class ClanUser(AbstractBaseUser):
            discord_id=models.CharField(max_length=20,unique=True,default=0,)

            discord_nickname=models.CharField(max_length=50,default='')

            discord_discriminator=models.PositiveIntegerField(default=0)

            provider=models.CharField(max_length=20,default='Discord')

            is_active=models.BooleanField(default=True)
            is_superuser=models.BooleanField(default=False)

            avatar=models.CharField(max_length=150,default='')

            country_tag=models.CharField(max_length=10,default='red-cross')


            description=models.CharField(max_length=1500, blank="", default="")



            objects=UserManager()


            USERNAME_FIELD='discord_id'
            REQUIRED_FIELDS = ['discord_nickname']



            def __str__(self):  # __unicode__ on Python 2
                return self.discord_nickname


            def get_full_name(self):
                return str(self.discord_id)

            def get_short_name(self):
                return str(self.discord_id)

            def has_perm(self, perm, obj=None):
               return True

            def has_module_perms(self, app_label):
              "Does the user have permissions to view the app `app_label`?"
              # Simplest possible answer: Yes, always
              return True

            @property
            def is_staff(self):
                "Is the user a member of staff?"
                return self.is_superuser

            @property
            def is_points_manager(self):
                """
                Checks if the user is a superuser or if they have a role that gives points_manager rights
                """
                clan_user_roles= ClanUserRoles.objects.filter(clan_user=self).filter(role__can_manage_points=True).filter(role__discord_isDeleted=False)
                if clan_user_roles.exists() or self.is_staff:
                    return True
                return False

            @property
            def can_edit_info(self):
                clan_user_roles= ClanUserRoles.objects.filter(clan_user=self).filter(role__is_admin=True).filter(role__discord_isDeleted=False)
                if clan_user_roles.exists() or self.is_staff:
                    return True
                return False

            @property
            def avatar_url(self):
                if self.avatar is "":
                    return "https://discordapp.com/assets/322c936a8c8be1b803cd94861bdfa868.png"
                else:
                    return "https://cdn.discordapp.com/avatars/"+str(self.discord_id)+"/"+self.avatar


            @property
            def is_war_manager(self):
                """
                Checks if the user is a superuser or if they have a role that gives points_manager rights
                """
                clan_user_roles= ClanUserRoles.objects.filter(clan_user=self).filter(role__can_manage_wars=True).filter(role__discord_isDeleted=False)
                if clan_user_roles.exists() or self.is_staff:
                    return True
                return False

            @property
            def total_points(self):
                return self.pointsinfo.totalpoints

            @property
            def masteries(self):
                return self.pointsinfo.masteries.prefetch_related("tank")


            @property
            def masteries_t1(self):
                return self.pointsinfo.masteries.filter(tier=1)

            @property
            def masteries_t2(self):
                return self.pointsinfo.masteries.filter(tier=2)

            @property
            def masteries_t3(self):
                return self.pointsinfo.masteries.filter(tier=3)

            @property
            def masteries_t4(self):
                return self.pointsinfo.masteries.filter(tier=4)

            @property
            def masteries_t5(self):
                return self.pointsinfo.masteries.filter(tier=5)

            @property
            def badges(self):
                from .discord_roles import SunKnightsBadgeRole
                return SunKnightsBadgeRole.objects.filter(clanuserroles__clan_user=self)

            @property
            def open_fights(self):
                return guild_fight_searcher(self, False)

            @property
            def finished_fights(self):
                return guild_fight_searcher(self, True)


            @property
            def leaderboard_place(self):
                return self.pointsinfo.leaderboard_place

            @property
            def last_accepted_submissions(self):
                from .point_submission import BasicPointSubmission
                return BasicPointSubmission.objects.filter(pointsinfo=self.pointsinfo,decided=True,accepted=True)


            @property
            def last_decided_userpoint_submissions(self):
                from .point_submission import BasicUserPointSubmission
                return BasicUserPointSubmission.objects.filter(pointsinfo=self.pointsinfo,decided=True)

            @property
            def last_decided_eventquests_submissions(self):
                from .point_submission import EventQuestSubmission
                return EventQuestSubmission.objects.filter(pointsinfo=self.pointsinfo,decided=True).prefetch_related('questtask','questtask__manager','questtask__quest','pointsinfo','manager','pointsinfo__user')

            @property
            def last_decided_custom_submissions(self):
                from .point_submission import PointsManagerAction
                return PointsManagerAction.objects.filter(pointsinfo=self.pointsinfo,decided=True).prefetch_related('pointsinfo','pointsinfo__user','manager')


            @property
            def last_decided_fights_submissions(self):
                from .point_submission import OneOnOneFightSubmission
                from django.db.models import Q
                return OneOnOneFightSubmission.objects.filter(Q(pointsinfo=self.pointsinfo)|Q(pointsinfoloser=self.pointsinfo)).filter(decided=True).prefetch_related('pointsinfo','pointsinfo__user','manager','pointsinfoloser','pointsinfoloser__user')


            @property
            def last_open_score_submissions(self):
                from .point_submission import BasicUserPointSubmission
                return BasicUserPointSubmission.objects.filter(pointsinfo=self.pointsinfo,decided=False).prefetch_related('pointsinfo','tank')

            @property
            def last_open_event_submissions(self):
                from .point_submission import EventQuestSubmission
                return EventQuestSubmission.objects.filter(pointsinfo=self.pointsinfo,decided=False).prefetch_related('questtask','questtask__manager','questtask__quest','pointsinfo','pointsinfo__user')

            @property
            def last_open_fights_submissions(self):
                from .point_submission import OneOnOneFightSubmission
                from django.db.models import Q
                return OneOnOneFightSubmission.objects.filter(Q(pointsinfo=self.pointsinfo)|Q(pointsinfoloser=self.pointsinfo)).filter(decided=False).filter(decided=True).prefetch_related('pointsinfo','pointsinfo__user','pointsinfoloser','pointsinfoloser__user')


            @property
            def points_cur_week(self):
                return self.submitted_points()

            @property
            def points_week_1(self):
                return self.submitted_points(1)


            @property
            def get_perm_tasks(self):
                from ..models.daily_quest import Quest,QuestTask
                import datetime
                permed = Quest.objects.filter(permed=True).get()
                if self.pointsinfo.permquestcd.timestamp() < datetime.datetime.now().timestamp():
                    return QuestTask.objects.filter(quest=permed,deleted=False).order_by('tier')
                return QuestTask.objects.none()

            @property
            def get_daily_tasks(self):
                import datetime
                from .utility.little_things import QUEST_TIER_OPTIONS
                from ..models.daily_quest import Quest,QuestTask
                from django.db.models import Q
                now = (datetime.datetime.utcnow()).replace(hour=0, minute=0, second=0, microsecond=0)
                quest = Quest.objects.filter(date=now,permed=False)
                # tasks=QuestTask.objects.filter(quest=quest).exclude(Q(eventquest__pointsinfo=self.pointsinfo) &(Q(eventquest__decided=False)|(Q(eventquest__accepted=True)&Q(eventquest__decided=True))))
                # if QuestTask.objects.filter(quest=quest).exclude(eventquest__pointsinfo=self.pointsinfo,eventquest__accepted=True).exclude(tier=QUEST_TIER_OPTIONS[3][0]):#as long as not all non bonus quests are accepted, no bonus quest will be displayed
                #     tasks=tasks.exclude(tier=QUEST_TIER_OPTIONS[3][0])

                tasks=QuestTask.objects.filter(quest=quest,deleted=False).exclude(Q(eventquest__pointsinfo=self.pointsinfo) &(Q(eventquest__decided=False)|(Q(eventquest__accepted=True)&Q(eventquest__decided=True))))
                if QuestTask.objects.filter(quest=quest,eventquest__pointsinfo=self.pointsinfo,eventquest__accepted=True,deleted=False).count()<3:#as long as not at least 3 tier1-tier3 quests are done, one cannot do a bonus quest
                    tasks=tasks.exclude(tier=QUEST_TIER_OPTIONS[3][0])

                return tasks.order_by('tier')




            def submitted_points(self,week=0):
                import datetime
                from django.db.models import F,Sum
                date = datetime.date.today()
                date=date-datetime.timedelta(7*week)
                start_week = date - datetime.timedelta(date.weekday())
                end_week = start_week + datetime.timedelta(7)
                from .point_submission import BasicUserPointSubmission

                return BasicUserPointSubmission.objects.filter(accepted=True,decided=True,date__range=[start_week,end_week],pointsinfo=self.pointsinfo).aggregate(sum=Sum('points'))['sum'] or 0



            @receiver(post_save, sender=settings.AUTH_USER_MODEL)
            def create_auth_token(sender, instance=None, created=False, **kwargs):
                if created:
                    Token.objects.create(user=instance)




class ClanUserPreferences(models.Model):
    clan_user=models.OneToOneField(ClanUser,related_name='preferences',on_delete=models.CASCADE,unique=True)

    custom_background_enabled=models.BooleanField(default=False)
    custom_background_url=models.CharField(max_length=300)




    def __str__(self):
        return self.clan_user.discord_nickname


class ClanUserRoles(models.Model):
    clan_user=models.ForeignKey(ClanUser,related_name='roles',on_delete=models.CASCADE)
    role=models.ForeignKey(DiscordRole,on_delete=models.CASCADE)


    class Meta:
        unique_together=('clan_user','role')#user can have a role only once


    def __str__(self):
        return self.clan_user.discord_nickname+': '+self.role.name



def guild_fight_searcher(user:ClanUser, finished=False):
    """
    Searches for guildfights the user can/has joined
    :param user: User to search for
    :param finished: if the fight is finished or not
    :return: queryset of GuildFights
    """
    from .guildfight import GuildFight
    from django.db.models import Q
    fights=GuildFight.objects.filter(Q(team1__clanuserroles__clan_user=user)|Q(team2__clanuserroles__clan_user=user))
    if finished:
        return fights.exclude(status=1)
    return fights.filter(status=1)