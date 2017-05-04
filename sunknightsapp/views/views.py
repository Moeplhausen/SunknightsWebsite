import json
from datetime import timedelta

import django
from django.views.decorators.csrf import ensure_csrf_cookie
from ..models.discord_server import DiscordServer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..decorators.login_decorators import points_manager_required
from ..enums.AjaxActions import AjaxAction
from ..forms.misc_forms import ChangeDesc
from ..forms.daily_quests_forms import SubmitQuestTaskForm, RequestQuestsForm, EditQuestTaskForm, DeleteQuestTaskForm, \
    DeleteMultiplierForm, DeleteQuestBuildForm, EditMultiplierForm, EditQuestBuildForm, SubmitMultiplierForm, \
    SubmitBuildForm
from ..forms.points_forms import SubmitPointsForm, RetrieveUserSubmissionsPointsForm, DecideUserPointSubmissionForm, \
    SubmitFightsForm, RetrieveFightsSubmissionsForm, DecideFightsSubmissionForm, RevertSubmissionForm, \
    RetrieveUsersLeaderPointForm, RetrieveUsersToFightAgainstForm, SubmitEventsQuestsForm, \
    DecideEventQuestsSubmissionForm, RetrieveEventQuestsSubmissionsForm,RetrieveDecidedScoreSubmissionsForm
from ..forms.preferences_forms import SavePreferencesForm
from ..forms.tournaments_forms import CreateTournamentForm, DeleteTournamentForm, RequestTournamentsForm
from ..models.clan_user import ClanUser
from ..models.diep_gamemode import DiepGamemode
from ..models.diep_tank import DiepTankInheritance, DiepTank
from ..models.discord_roles import DiscordRole
from ..models.help_info import HelpInfo
from ..models.points_info import PointsInfo
from ..models.daily_quest import Quest, QuestTask
import datetime
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@ensure_csrf_cookie
def index(request):
    if request.user.is_authenticated():
        from django.contrib.gis.geoip2 import GeoIP2
        from slugify import slugify
        g = GeoIP2()
        try:

            country_code=slugify(str(g.country_code(get_client_ip(request))).lower())
            if request.user.country_tag!=country_code:
                request.user.country_tag=country_code
                request.user.save()

        except:
            pass
        gamemodes = DiepGamemode.objects.filter(diep_isDeleted=False)

        tanks = DiepTank.objects.filter(diep_isDeleted=False)
        try:
            permed = Quest.objects.filter(permed=True).get()
        except Quest.DoesNotExist:
            permed = Quest.objects.create(permed=True)

        now = (datetime.datetime.utcnow()).replace(hour=0, minute=0, second=0, microsecond=0)
        try:
            quest = Quest.objects.filter(date=now).get()
        except Quest.DoesNotExist:
            quest = Quest.objects.create()
            quest.date = now
            quest.save()

        validtill = now + datetime.timedelta(days=1) - datetime.datetime.utcnow().replace(microsecond=0)

        permcooldown = None
        if request.user.pointsinfo.permquestcd >= timezone.now():
            permcooldown = (request.user.pointsinfo.permquestcd - timezone.now())
            permcooldown = permcooldown - datetime.timedelta(microseconds=permcooldown.microseconds)

        context = {
            'permcooldown': permcooldown,
            'daily': quest,
            'permdaily': permed,
            'validtill': validtill,
            'tanks': tanks,
            'gamemodes': gamemodes,
            'submitpointsform': SubmitPointsForm,
            'submitfightsform': SubmitFightsForm,
            'submiteventsquestsform': SubmitEventsQuestsForm,
            'revertsubmissionid': AjaxAction.REVERTSUBMISSION.value,
            'savepreferences':SavePreferencesForm,
            'lookuser': ClanUser.objects.prefetch_related('pointsinfo', 'pointsinfo__masteries').get(
                id=request.user.id)}

        return render(request, 'sunknightsapp/userview.html', context)


    context = {}
    try:
        server=DiscordServer.objects.get(id=1)#should be main server
    except DiscordServer.DoesNotExist:
        pass
    else:
        context['server']=server


    return render(request, 'sunknightsapp/index.html', context)



def goodbye(request):
    return render(request,'sunknightsapp/goodbye.html')


def logoutview(request):
    logout(request)
    return redirect('index')


@login_required
def user(request, id):
    try:
        print("id")
        print(id)
        fuser = ClanUser.objects.prefetch_related('pointsinfo', 'pointsinfo__masteries').get(discord_id=id)
    except ClanUser.DoesNotExist:
        return render(request, 'sunknightsapp/index.html')
    else:
        context = {}
        context['lookuser'] = fuser
        context['revertsubmissionid'] = AjaxAction.REVERTSUBMISSION.value
        return render(request, 'sunknightsapp/public_userview.html', context)


@login_required
@ensure_csrf_cookie
def leaderboard(request):
    context = {}
    userpoints = PointsInfo.objects.filter(user__is_active=True).prefetch_related('user', 'masteries').order_by(
        '-totalpoints')  # the '-' is for reversing the order (so the one who has most points will be on top
    context['userpoints'] = userpoints
    context['retrieveusers'] = AjaxAction.RETRIEVELEADERBOARD.value

    t = render(request, 'sunknightsapp/leaderboard.html', context)

    return t


@login_required
def masteries(request):
    tanks = DiepTank.objects.filter(diep_isDeleted=False).prefetch_related('mastery_set', 'mastery_set__fromSubmission',
                                                                           'mastery_set__pointsinfo',
                                                                           'mastery_set__pointsinfo__user')

    t = render(request, 'sunknightsapp/masteriesboard.html', {'tanks': tanks})

    return t


@login_required
def guilds(request):
    context = {}
    guilds = DiscordRole.objects.filter(is_clan_guild=True, discord_isDeleted=False).order_by('name')
    context['guilds'] = guilds
    return render(request, 'sunknightsapp/guilds.html', context)


def about_us(request):
    context = {}
    return render(request, 'sunknightsapp/about_us.html', context)


@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
def helppage(request, helpstr=""):
    try:
        help = HelpInfo.objects.get(name=helpstr)
    except HelpInfo.DoesNotExist:

        return render(request, 'sunknightsapp/info.html')
    else:

        # if it was a post request, we assume that the users wants to update the help content
        # so we check that 'newcontent' is in the request and that the user has permissions to modify the pagehel
        if request.method == 'POST' and request.user.can_edit_info and 'newcontent' in request.POST:
            newcontent = request.POST['newcontent']
            help.helpinfo = newcontent
            help.last_modifier = request.user
            help.save()

        context = {'helpcontent': json.dumps(help.helpinfo)}
        return render(request, 'sunknightsapp/helppage.html', context)


@login_required
def guild(request, id):
    return render(request, 'sunknightsapp/index.html')


@login_required
def pointrole(request, id):
    try:
        role = DiscordRole.objects.get(discord_id=id)
    except DiscordRole.DoesNotExist:
        pass
    else:
        return render(request, 'sunknightsapp/points_by_role.html', {'role': role})
    return render(request, 'sunknightsapp/index.html')


@points_manager_required
@ensure_csrf_cookie
def manage_submissions(request):
    context = {
        'retrieveuserspointssubmissionsid': AjaxAction.RETRIEVEUSERSUBMISSIONS.value,
        'decideuserpointsubmissionid': AjaxAction.DECIDEUSERPOINTUSUBMISSION.value,
        'decideeventquestssubmissionid': AjaxAction.DECIDEEVENTQUESTS.value,
        'decidefightsubmissionid': AjaxAction.DECIDEFIGHTSSUBMISSION.value,
        'retrieveuserfightssubmissionsid': AjaxAction.RETRIEVEFIGHTSSUBMISSIONS.value,
        'retrieveeventsquestsssubmissionsid': AjaxAction.RETRIEVEEVENTQUESTSSUBMISSIONS.value}
    return render(request, 'sunknightsapp/managesubmissions.html', context)


@points_manager_required
@ensure_csrf_cookie
def manage_quests(request):
    tanks = DiepTank.objects.filter(diep_isDeleted=False)
    try:
        permed = Quest.objects.filter(permed=True).get()
    except Quest.DoesNotExist:
        permed = Quest.objects.create(permed=True)
    from ..models.utility.little_things import QUEST_TIER_OPTIONS

    tiers = QUEST_TIER_OPTIONS

    time = []
    for i in range(0, 4):
        now = (datetime.datetime.utcnow() + timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        try:
            quest = Quest.objects.filter(date=now).get()
        except Quest.DoesNotExist:
            quest = Quest.objects.create()
            quest.date = now
            quest.save()

        time.append(quest)
    time.append(permed)

    context = {
        'tanks': tanks,
        'dailies': time,
        'tiers': tiers,
        'submitquesttask': SubmitQuestTaskForm,
        'requestquests': RequestQuestsForm,
        'editquesttask': EditQuestTaskForm,
        'submitmultiplier': SubmitMultiplierForm,
        'editmultiplier': EditMultiplierForm,
        'submitbuild': SubmitBuildForm,
        'editbuild': EditQuestBuildForm,
    }
    return render(request, 'sunknightsapp/managequests.html', context)


@login_required
def tankboard(request):
    context = {}
    inheritance = DiepTankInheritance.objects.all()
    tanks = DiepTank.objects.filter(diep_isDeleted=False)
    context['inheritance'] = inheritance
    context['tanks'] = tanks
    return render(request, 'sunknightsapp/tankdraw.html', context)


@login_required
@require_http_methods(["POST"])
def ajaxhandler(request):
    # print(request.POST)

    if "ajax_action_id" not in request.POST:
        return sendFailure(request, "No Ajax action specified.")

    form = None
    actionid = request.POST['ajax_action_id']
    if actionid.isdigit():
        actionid = int(actionid)

    if actionid is AjaxAction.CREATETOURNAMENT.value:
        form = CreateTournamentForm(request.POST)
    elif actionid is AjaxAction.DELETETOURNAMENT.value:
        form = DeleteTournamentForm(request.POST)
    elif actionid is AjaxAction.GETTOURNAMENTS.value:
        form = RequestTournamentsForm(request.POST)
    elif actionid is AjaxAction.SUBMITPOINTS.value:
        form = SubmitPointsForm(request.POST)
    elif actionid is AjaxAction.SUBMITEVENTSQUESTS.value:
        form = SubmitEventsQuestsForm(request.POST)
    elif actionid is AjaxAction.RETRIEVEUSERSUBMISSIONS.value:
        form = RetrieveUserSubmissionsPointsForm(request.POST)
    elif actionid is AjaxAction.DECIDEUSERPOINTUSUBMISSION.value:
        form = DecideUserPointSubmissionForm(request.POST)
    elif actionid is AjaxAction.DECIDEEVENTQUESTS.value:
        form = DecideEventQuestsSubmissionForm(request.POST)
    elif actionid is AjaxAction.RETRIEVEFIGHTSSUBMISSIONS.value:
        form = RetrieveFightsSubmissionsForm(request.POST)
    elif actionid is AjaxAction.SUBMITFIGHTS.value:
        form = SubmitFightsForm(request.POST)
    elif actionid is AjaxAction.DECIDEFIGHTSSUBMISSION.value:
        form = DecideFightsSubmissionForm(request.POST)
    elif actionid is AjaxAction.REVERTSUBMISSION.value:
        form = RevertSubmissionForm(request.POST)
    elif actionid is AjaxAction.RETRIEVELEADERBOARD.value:
        form = RetrieveUsersLeaderPointForm(request.POST)
    elif actionid is AjaxAction.RETRIEVEUSERSTOFIGHTAGAINST.value:
        form = RetrieveUsersToFightAgainstForm(request.POST)
    elif actionid is AjaxAction.RETRIEVEEVENTQUESTSSUBMISSIONS.value:
        form = RetrieveEventQuestsSubmissionsForm(request.POST)
    elif actionid is AjaxAction.CHANGEDESC.value:
        form = ChangeDesc(request.POST)
    elif actionid is AjaxAction.SUBMITQUESTTASK.value:
        form = SubmitQuestTaskForm(request.POST)
    elif actionid is AjaxAction.RETRIEVEQUESTS.value:
        form = RequestQuestsForm(request.POST)
    elif actionid is AjaxAction.DELETEQUESTTASK.value:
        form = DeleteQuestTaskForm(request.POST)
    elif actionid is AjaxAction.EDITQUESTTASK.value:
        form = EditQuestTaskForm(request.POST)
    elif actionid is AjaxAction.ADDMULTIPLIER.value:
        form = SubmitMultiplierForm(request.POST)
    elif actionid is AjaxAction.DELETEQUESTBUILD.value:
        form = DeleteQuestBuildForm(request.POST)
    elif actionid is AjaxAction.EDITQUESTBUILD.value:
        form = EditQuestBuildForm(request.POST)
    elif actionid is AjaxAction.ADDQUESTBUILD.value:
        form = SubmitBuildForm(request.POST)
    elif actionid is AjaxAction.REMOVEMULTIPLIER.value:
        form = DeleteMultiplierForm(request.POST)
    elif actionid is AjaxAction.EDITMULTIPLIER.value:
        form = EditMultiplierForm(request.POST)
    elif actionid is AjaxAction.SAVEPREFERENCES.value:
        form=SavePreferencesForm(request.POST)
    elif actionid is AjaxAction.RETRIEVEDECIDEDSCORE.value:
        form=RetrieveDecidedScoreSubmissionsForm(request.POST)


    if form is None:
        return sendFailure(request, "No handler for this action installed.")

    if not form.is_valid():
        return sendFailure(request, form.errors)

    return form.handle(request)


def sendFailure(request, message):
    return JsonResponse({'status': 'failure', 'message': message})
