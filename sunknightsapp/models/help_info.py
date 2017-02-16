from django.db import models
from .clan_user import ClanUser
import datetime

class HelpInfo(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    name=models.CharField(max_length=30,unique=True)
    helpinfo=models.TextField()
    last_modifier=models.ForeignKey(ClanUser)



    def __str__(self):
            return self.name

