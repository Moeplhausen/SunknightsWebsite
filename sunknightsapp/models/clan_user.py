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
            discord_id=models.PositiveIntegerField(unique=True,default=0,)

            discord_nickname=models.CharField(max_length=50,default='')

            provider=models.CharField(max_length=20,default='Discord')


            is_active=models.BooleanField(default=True)
            is_superuser=models.BooleanField(default=False)

            avatar=models.CharField(max_length=150,default='')



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
                return self.pointsinfo.masteries

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




            @receiver(post_save, sender=settings.AUTH_USER_MODEL)
            def create_auth_token(sender, instance=None, created=False, **kwargs):
                if created:
                    Token.objects.create(user=instance)



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