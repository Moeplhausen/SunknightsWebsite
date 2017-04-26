from django.db import models


class DiscordServer(models.Model):
    discord_id=models.CharField(max_length=20,unique=True)
    name=models.CharField(max_length=30)


    def __str__(self):
        return self.name


