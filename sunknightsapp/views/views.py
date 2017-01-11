from django.contrib.auth.decorators import login_required
from ..decorators.login_decorators import points_manager_required
from django.contrib.auth.views import logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..enums.AjaxActions import AjaxAction
from ..forms.tournaments_forms import CreateTournamentForm,DeleteTournamentForm,RequestTournamentsForm
from ..forms.points_forms import SubmitPointsForm,RetriveUserSubmissionsPointsForm,DecideUserPointSubmissionForm,SubmitFightsForm,RetrieveFightsSubmissionsForm,DecideFightsSubmissionForm
from ..models.clan_user import ClanUser
from ..models.diep_tank import DiepTankInheritance,DiepTank
from ..models.discord_roles import DiscordRole
from ..models.points_info import PointsInfo
from ..models.clan_user import ClanUser
from ..models.diep_gamemode import DiepGamemode


def index(request):

    if request.user.is_authenticated():
        tanks=DiepTank.objects.all()
        gamemodes=DiepGamemode.objects.all()

        users = ClanUser.objects.filter(is_active=True).exclude(id=request.user.id).order_by(
            '-discord_nickname')

        context={'tanks':tanks,'gamemodes':gamemodes,'submitpointsform':SubmitPointsForm,'submitfightsform':SubmitFightsForm,'users':users}

        return render(request, 'sunknightsapp/userview.html', context)

    context = {}

    return render(request, 'sunknightsapp/index.html', context)


def logoutview(request):
    logout(request)
    return redirect('index')



@login_required
def user(request,id):
    try:
        print("id")
        print(id)
        user=ClanUser.objects.get(discord_id=id)
    except ClanUser.DoesNotExist:
        return render(request, 'sunknightsapp/index.html')
    else:
        context={}
        context['lookuser']=user
        return render(request, 'sunknightsapp/public_userview.html',context)




@login_required
def leaderboard(request):
    context = {}
    userpoints = PointsInfo.objects.filter(user__is_active=True).order_by(
        '-currentpoints')  # the '-' is for reversing the order (so the one who has most points will be on top
    context['userpoints'] = userpoints
    return render(request, 'sunknightsapp/leaderboard.html', context)

@login_required
def guilds(request):
    context = {}
    guilds = DiscordRole.objects.filter(is_clan_guild=True,discord_isDeleted=False).order_by('name')
    context['guilds'] = guilds
    return render(request, 'sunknightsapp/guilds.html', context)


@login_required
def guild(request,id):
    return render(request, 'sunknightsapp/index.html')

@points_manager_required
def manage_submissions(request):
    context={'retrieveuserspointssubmissionsid':AjaxAction.RETRIEVEUSERSUBMISSIONS.value,'decideuserpointsubmissionid':AjaxAction.DECIDEUSERPOINTUSUBMISSION.value,'decidefightsubmissionid':AjaxAction.DECIDEFIGHTSSUBMISSION.value,'retrieveuserfightssubmissionsid':AjaxAction.RETRIEVEFIGHTSSUBMISSIONS.value}
    return render(request,'sunknightsapp/managesubmissions.html',context)


@login_required
def tankboard(request):
    context={}
    inheritance=DiepTankInheritance.objects.all()
    tanks=DiepTank.objects.all()
    context['inheritance']=inheritance
    context['tanks']=tanks
    return render(request, 'sunknightsapp/tankdraw.html',context)


@login_required
@require_http_methods(["POST"])
def ajaxhandler(request):
    print(request.POST)

    if "ajax_action_id" not in request.POST:
        return sendFailure(request,"No Ajax action specified.")

    form=None
    actionid=request.POST['ajax_action_id']
    if actionid.isdigit():
        actionid=int(actionid)
    print(AjaxAction.CREATETOURNAMENT.value)
    if actionid is AjaxAction.CREATETOURNAMENT.value:
        form=CreateTournamentForm(request.POST)
    elif actionid is AjaxAction.DELETETOURNAMENT.value:
        form=DeleteTournamentForm(request.POST)
    elif actionid is AjaxAction.GETTOURNAMENTS.value:
        form=RequestTournamentsForm(request.POST)
    elif actionid is AjaxAction.SUBMITPOINTS.value:
        form=SubmitPointsForm(request.POST)
    elif actionid is AjaxAction.RETRIEVEUSERSUBMISSIONS.value:
        form=RetriveUserSubmissionsPointsForm(request.POST)
    elif actionid is AjaxAction.DECIDEUSERPOINTUSUBMISSION.value:
        form=DecideUserPointSubmissionForm(request.POST)
    elif actionid is AjaxAction.RETRIEVEFIGHTSSUBMISSIONS.value:
        form=RetrieveFightsSubmissionsForm(request.POST)
    elif actionid is AjaxAction.SUBMITFIGHTS.value:
        form=SubmitFightsForm(request.POST)
    elif actionid is AjaxAction.DECIDEFIGHTSSUBMISSION.value:
        form=DecideFightsSubmissionForm(request.POST)


    if form is None:
        return sendFailure(request,"No handler for this action installed.")



    if not form.is_valid():
        return sendFailure(request,form.errors)

    return form.handle(request)


def sendFailure(request,message):
    return JsonResponse({'status':'failure','message':message})
