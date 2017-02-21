from django.db import models


class DiscordServer(models.Model):
    discord_id=models.CharField(max_length=20,unique=True)
    name=models.CharField(max_length=30)
    invite_link=models.CharField(max_length=50,default='')


    def __str__(self):
        return self.name


