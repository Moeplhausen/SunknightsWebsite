from django.contrib.auth.decorators import login_required
from ..decorators.login_decorators import points_manager_required
from django.contrib.auth.views import logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..enums.AjaxActions import AjaxAction
from ..forms.tournaments_forms import CreateTournamentForm,DeleteTournamentForm,RequestTournamentsForm
from ..forms.points_forms import SubmitPointsForm,RetriveUserSubmissionsPointsForm,DecideUserPointSubmissionForm,SubmitFightsForm,RetrieveFightsSubmissionsForm,DecideFightsSubmissionForm,RevertSubmissionForm,RetrieveUsersLeaderPointForm,RetrieveUsersToFightAgainstForm

from ..models.diep_tank import DiepTankInheritance,DiepTank
from ..models.discord_roles import DiscordRole
from ..models.points_info import PointsInfo
from ..models.clan_user import ClanUser
from ..models.diep_gamemode import DiepGamemode


def index(request):

    if request.user.is_authenticated():
        tanks=DiepTank.objects.all()
        gamemodes=DiepGamemode.objects.all()


        context={'tanks':tanks,'gamemodes':gamemodes,'submitpointsform':SubmitPointsForm,'submitfightsform':SubmitFightsForm}
        context['revertsubmissionid']=AjaxAction.REVERTSUBMISSION.value
        context['lookuser']=ClanUser.objects.prefetch_related('pointsinfo','pointsinfo__masteries').get(id=request.user.id)

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
        fuser=ClanUser.objects.prefetch_related('pointsinfo','pointsinfo__masteries').get(discord_id=id)
    except ClanUser.DoesNotExist:
        return render(request, 'sunknightsapp/index.html')
    else:
        context={}
        context['lookuser']=fuser
        context['revertsubmissionid']=AjaxAction.REVERTSUBMISSION.value
        return render(request, 'sunknightsapp/public_userview.html',context)




@login_required
def leaderboard(request):
    context = {}
    userpoints = PointsInfo.objects.filter(user__is_active=True).prefetch_related('user','masteries').order_by(
        '-totalpoints')  # the '-' is for reversing the order (so the one who has most points will be on top
    context['userpoints'] = userpoints
    context['retrieveusers']=AjaxAction.RETRIEVELEADERBOARD.value

    t=render(request, 'sunknightsapp/leaderboard.html', context)



    return t

@login_required
def guilds(request):
    context = {}
    guilds = DiscordRole.objects.filter(is_clan_guild=True,discord_isDeleted=False).order_by('name')
    context['guilds'] = guilds
    return render(request, 'sunknightsapp/guilds.html', context)


def about_us(request):
    context = {}
    return render(request, 'sunknightsapp/about_us.html', context)

def rules(request):
    context = {}
    return render(request, 'sunknightsapp/rules.html', context)

def info(request):
    context = {}
    return render(request, 'sunknightsapp/info.html', context)

def newguide(request):
    return render(request, 'sunknightsapp/newguide.html', {})

def pointguide(request):
    return render(request, 'sunknightsapp/pointguide.html', {})

def ranks(request):
    return render(request, 'sunknightsapp/ranks.html', {})

def commands(request):
    return render(request, 'sunknightsapp/commands.html', {})

def faq(request):
    return render(request, 'sunknightsapp/faq.html', {})

def yt(request):
    return render(request, 'sunknightsapp/yt.html', {})

def invites(request):
    return render(request, 'sunknightsapp/invites.html', {})

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
    elif actionid is AjaxAction.REVERTSUBMISSION.value:
        form=RevertSubmissionForm(request.POST)
    elif actionid is AjaxAction.RETRIEVELEADERBOARD.value:
        form=RetrieveUsersLeaderPointForm(request.POST)
    elif actionid is AjaxAction.RETRIEVEUSERSTOFIGHTAGAINST.value:
        form=RetrieveUsersToFightAgainstForm(request.POST)

    if form is None:
        return sendFailure(request,"No handler for this action installed.")



    if not form.is_valid():
        return sendFailure(request,form.errors)

    return form.handle(request)


def sendFailure(request,message):
    return JsonResponse({'status':'failure','message':message})
