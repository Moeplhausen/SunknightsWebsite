from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..views.oauth.views import get_client
from ..models.clan_user import ClanUser
from ..models.points_info import PointsInfo
from ..forms.fights_forms import TournamentForm
from ..models.tournament import Tournament

def index(request):
    context = {}
    # if request.user.is_authenticated():
    #     try:
    #         access = request.user.accountaccess_set.all()[0]
    #     except IndexError:
    #         access = None
    #     else:
    #         client = get_client(access.provider,access.access_token or '')
    #         context['info'] = client.get_profile_info(raw_token=access.access_token)
    return render(request, 'index.html', context)


@login_required
def home(request):
    if request.method=='POST':
        form=TournamentForm(request.POST)
        if (form.is_valid()):
            form.save()




    tours=Tournament.objects.filter(finished=False).order_by('name')
    context = {'new_tournament_form':TournamentForm(),'tours':tours}  # user object is always stored in the context automatically
    return render(request, 'userview.html', context)


@login_required
def leaderboard(request):
    context = {}
    userpoints = PointsInfo.objects.all().order_by(
        '-currentpoints')  # the '-' is for reversing the order (so the one who has most points will be on top
    context['userpoints'] = userpoints
    return render(request, 'leaderboard.html', context)
