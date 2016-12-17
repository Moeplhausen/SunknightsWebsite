from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager)
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, discord_id, discord_nickname, password=None):
        """
        Creates and saves a User with the given discord_id, discord_nickname and password.
        """
        if not discord_id:
            raise ValueError('Users must have an email address')

        user = self.model(
            discord_id=discord_id,
            discord_nickname=discord_nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, discord_id, discord_nickname, password):
        """
        Creates and saves a superuser with the given discord_id, discord_nickname and password.
        """
        user = self.create_user(
            discord_id,
            password=password,
            discord_nickname=discord_nickname,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user