from django.db import models
from .tournament import Tournament
from .fight import Fight

class TournamentFightConnector(models.Model):
    tournament=models.ForeignKey(Tournament)
    fight=models.ForeignKey(Fight)