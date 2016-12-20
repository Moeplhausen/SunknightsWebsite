from django.forms import ModelForm
from ..models.tournament import Tournament

class TournamentForm(ModelForm):
    class Meta:
        model=Tournament
        fields=['name','description']