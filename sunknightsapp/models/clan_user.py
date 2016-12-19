from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.utils import timezone


from ..managers.user_manager import UserManager

class ClanUser(AbstractBaseUser):
            discord_id=models.BigIntegerField(unique=True,default=0,)

            discord_nickname=models.CharField(max_length=50,default='')

            provider=models.CharField(max_length=20,default='Discord')


            is_active=models.BooleanField(default=True)
            is_superuser=models.BooleanField(default=False)
            is_manager=models.BooleanField(default=False)


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
                return self.is_manager or self.is_superuser



            @receiver(post_save, sender=settings.AUTH_USER_MODEL)
            def create_auth_token(sender, instance=None, created=False, **kwargs):
                if created:
                    Token.objects.create(user=instance)





