from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from ..views.oauth.views import get_client
from ..models.clan_user import ClanUser
from ..models.discord_roles import DiscordRole
from ..models.points_info import PointsInfo
from ..forms.tournaments_forms import CreateTournamentForm,DeleteTournamentForm,RequestTournamentsForm
from ..models.tournament import Tournament
from ..enums.AjaxActions import AjaxAction
from ..models.diep_tank import DiepTankInheritance,DiepTank


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
    return render(request, 'sunknightsapp/index.html', context)


@login_required
def home(request):
    if request.method=='POST':
        print(request.POST)

        ajax_id=request.POST['ajax_action_id']
        print(ajax_id)


        form=CreateTournamentForm(request.POST)
        if (form.is_valid()):
            form.save()
        else:
            print('inavalid')
            print('---')
            print(form.non_field_errors())
            field_errors = [ (field.label, field.errors) for field in form]
            print(field_errors)
            print('---')




    tours=Tournament.objects.filter(finished=False).order_by('name')
    context = {'new_tournament_form':CreateTournamentForm(),
               'delete_tournament_form':DeleteTournamentForm,
               'request_tournaments_form':RequestTournamentsForm,
               'tours':tours
               }  # user object is always stored in the context automatically
    return render(request, 'sunknightsapp/userview.html', context)


@login_required
def user(request,id):
    try:
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


    if form is None:
        return sendFailure(request,"No handler for this action installed.")



    if not form.is_valid():
        return sendFailure(request,form.errors)

    return form.handle(request)


def sendFailure(request,message):
    return JsonResponse({'status':'failure','message':message})
