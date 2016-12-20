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
                clan_user_roles= ClanUserRoles.objects.filter(clan_user=self).filter(role__can_manage_points=True)
                if clan_user_roles.exists() or self.is_staff:
                    return True
                return False


            @property
            def is_war_manager(self):
                clan_user_roles= ClanUserRoles.objects.filter(clan_user=self).filter(role__can_manage_wars=True)
                if clan_user_roles.exists() or self.is_staff:
                    return True
                return False



            @receiver(post_save, sender=settings.AUTH_USER_MODEL)
            def create_auth_token(sender, instance=None, created=False, **kwargs):
                if created:
                    Token.objects.create(user=instance)



class ClanUserRoles(models.Model):
    clan_user=models.ForeignKey(ClanUser,related_name='roles',on_delete=models.CASCADE)
    role=models.ForeignKey(DiscordRole)


    class Meta:
        unique_together=('clan_user','role')


    def __str__(self):
        return self.clan_user.discord_nickname+': '+self.role.name

