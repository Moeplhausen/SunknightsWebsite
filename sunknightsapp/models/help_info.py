from django.db import models
from .clan_user import ClanUser

class HelpInfo(models.Model):
    date = models.DateTimeField(auto_now_add=True,db_index=True)
    name=models.CharField(max_length=30,unique=True)
    helpinfo=models.TextField()
    last_modifier=models.ForeignKey(ClanUser)



    def __str__(self):
            return self.name

