from .base_form import BaseForm
from django.utils.html import strip_tags
from ..enums.AjaxActions import AjaxAction
from ..models.point_submission import BasicUserPointSubmission, BasicPointSubmission, OneOnOneFightSubmission, \
    PointsManagerAction, EventQuestSubmission
from ..serializers.pointsubmissions_serializer import BasicUserPointSubmissionSerializer, \
    BasicPointsSubmissionSerializer, OneOnOneFightSubmissionSerializer, BasicEventQuestsSubmissionSerializer, \
    BasicUserPointSubmissionWithSimilarSubsSerializer,BasicUserPointSubmissionSerializerMinimal
from ..serializers.clan_user_serializer import PointsInfoSerializer, PointsInfoFastSerializer, ClanUserSerializerBasic
from django import forms
from ..models.utility.little_things import getPointsByScore, getPointsByFight, manageElo
from ..models.points_info import PointsInfo, ClanUser
from django.core.paginator import Paginator
from django.db.models import Count
from ..models.utility.little_things import float_or_0
import datetime
from django.db.models import Q
MAX_OPEN_SUBS=40

def check_open_subs(user):
    subs=BasicPointSubmission.objects.filter(pointsinfo=user.pointsinfo,decided=False).count()
    return subs



class SubmitPointsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SubmitPointsForm, self).__init__(AjaxAction.SUBMITPOINTS, *args, **kwargs)

    def handle(self, request):


        try:
            if check_open_subs(request.user) >= MAX_OPEN_SUBS:
                return self.response(False, 'Too many undecided submissions')
            import decimal
            submission = self.save(commit=False)
            submission.points = decimal.Decimal(
                getPointsByScore(submission))  # *decimal.Decimal(submission.tank.multiplier)

            submission.date = datetime.datetime.utcnow()
            submission.submitterText = strip_tags(submission.submitterText)

            for mult in submission.get_daily_multiplier:
                if mult.tank.id == submission.tank.id:
                    submission.points *= mult.multiplier
                    break

            submission.pointsinfo = request.user.pointsinfo
            submission.save()




        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:
            serializer = BasicUserPointSubmissionSerializer(submission)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = BasicUserPointSubmission
        fields = ('proof', 'gamemode', 'tank', 'score', 'submitterText')


class SubmitEventsQuestsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SubmitEventsQuestsForm, self).__init__(AjaxAction.SUBMITEVENTSQUESTS, *args, **kwargs)

    def handle(self, request):


        try:
            if check_open_subs(request.user) >= MAX_OPEN_SUBS:
                return self.response(False, 'Too many undecided submissions')
            from ..models.daily_quest import QuestTask
            import decimal
            submission = self.save(commit=False)
            submission.points = 0
            submission.pointsinfo = request.user.pointsinfo
            submission.submitterText = strip_tags(submission.submitterText)

            questtask = submission.questtask
            if questtask:
                submission.points = questtask.points
                if questtask.quest.permed:
                    if questtask not in request.user.get_perm_tasks:
                        return self.response(False,
                                             'Quest is still on cooldown. You can submit at this point again: ' + request.user.pointsinfo.permquestcd)
                    request.user.pointsinfo.permquestcd = datetime.datetime.now() + datetime.timedelta(
                        hours=questtask.cooldown)
                    request.user.pointsinfo.save()
                else:
                    if questtask not in request.user.get_daily_tasks:
                        return self.response(False,
                                             'You may not do this task yet ' + request.user.pointsinfo.permquestcd)

            submission.save()
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:
            serializer = BasicEventQuestsSubmissionSerializer(submission)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = EventQuestSubmission
        fields = ('proof', 'submitterText', 'questtask')


class SubmitFightsForm(BaseForm):
    whowon = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(SubmitFightsForm, self).__init__(AjaxAction.SUBMITFIGHTS, *args, **kwargs)

    def handle(self, request):

        try:
            if check_open_subs(request.user) >= MAX_OPEN_SUBS:
                return self.response(False, 'Too many undecided submissions')


            submission = self.save(commit=False)

            if request.user.pointsinfo.id == submission.pointsinfoloser.id:  # something fishy is happenening...
                return self.noPermission()

            submission.points = getPointsByFight(True)
            submission.pointsloser = getPointsByFight(False)
            if self.cleaned_data['whowon'] == '1':
                submission.pointsinfo = request.user.pointsinfo
            else:
                submission.pointsinfo = submission.pointsinfoloser
                submission.pointsinfoloser = request.user.pointsinfo
            submission.save()
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:
            serializer = OneOnOneFightSubmissionSerializer(submission)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = OneOnOneFightSubmission
        fields = ('proof', 'pointsinfoloser', 'whowon')


class RetrieveUserSubmissionsPointsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(RetrieveUserSubmissionsPointsForm, self).__init__(AjaxAction.RETRIEVEUSERSUBMISSIONS, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()

        similars = {}

        try:
            similarsubs = BasicUserPointSubmission.objects.values('id', 'proof', 'score', 'tank').filter(
                decided=False).distinct()

            for p in similarsubs:
                proofused = BasicUserPointSubmission.objects.filter(score=p['score'], tank=p['tank'])
                similars[p['id']] = proofused

            submissions = BasicUserPointSubmission.objects.filter(decided=False,pointsinfo__user__is_active=True)[:30]

            for sub in submissions:
                sub.similarsubs = similars[sub.id].exclude(id=sub.id)

            serializer = BasicUserPointSubmissionWithSimilarSubsSerializer(submissions, many=True)
        except BaseException as e:

            return self.response(False, 'Something went wrong: ' + str(e))
        else:

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = BasicUserPointSubmission
        fields = ()


class RetrieveEventQuestsSubmissionsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(RetrieveEventQuestsSubmissionsForm, self).__init__(AjaxAction.RETRIEVEEVENTQUESTSSUBMISSIONS, *args,
                                                                 **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()

        proofsbylink = {}
        try:
            submissions = EventQuestSubmission.objects.filter(decided=False)[:30]

            proofused = EventQuestSubmission.objects.values('proof').filter(decided=False).distinct()

            for p in proofused:
                link = p['proof']
                proofused = EventQuestSubmission.objects.filter(proof=link)
                proofsbylink[link] = proofused

            for sub in submissions:
                sub.proofused = proofsbylink[sub.proof]

            serializer = BasicEventQuestsSubmissionSerializer(submissions, many=True)
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = EventQuestSubmission
        fields = ()


class RetrieveUsersLeaderPointForm(BaseForm):
    draw = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    start = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    length = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(RetrieveUsersLeaderPointForm, self).__init__(AjaxAction.RETRIEVELEADERBOARD, *args, **kwargs)

    def handle(self, request):

        try:
            drawnr = self.cleaned_data['draw']
            lengthreq = self.cleaned_data['length']
            start = self.cleaned_data['start']
            searchstr = ""

            orderstr = "totalpoints"
            dir = 'desc'

            if 'search[value]' in request.POST:
                searchstr = request.POST['search[value]']
            if 'order[0][column]' in request.POST:
                ordercolumn = int(request.POST['order[0][column]'])
            if 'order[0][dir]' in request.POST:
                dir = request.POST['order[0][dir]']

            if ordercolumn == 0:
                orderstr = "user__discord_nickname"
            elif ordercolumn == 1:
                orderstr = "user__country_tag"
            elif ordercolumn == 2:
                orderstr = "oldpoints"
            elif ordercolumn == 3:
                orderstr = "totalpoints"
            elif ordercolumn == 5:
                orderstr = "elo"

            if dir == 'desc':
                orderstr = '-' + orderstr

            userpoints = PointsInfo.objects.filter(user__is_active=True).prefetch_related('user', 'masteries')
            allrecords = userpoints.count()
            if searchstr != "":
                userpoints = userpoints.filter(user__discord_nickname__icontains=searchstr)
            userpoints = userpoints.order_by(
                orderstr)  # the '-' is for reversing the order (so the one who has most points will be on top
            p = Paginator(userpoints, lengthreq)

            filtered = p.count

            page = p.page(start / lengthreq + 1)

            serializer = PointsInfoSerializer(page.object_list, many=True)
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:

            return self.datatables_leaderboard_response(
                {'draw': drawnr, 'recordsTotal': allrecords, 'recordsFiltered': filtered, 'data': (serializer.data)})

    class Meta:
        model = PointsInfo
        fields = ('draw', 'start', 'length')


class RetrieveDecidedScoreSubmissionsForm(BaseForm):
    draw = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    start = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    length = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(RetrieveDecidedScoreSubmissionsForm, self).__init__(AjaxAction.RETRIEVEDECIDEDSCORE, *args, **kwargs)

    def handle(self, request):

        try:
            drawnr = self.cleaned_data['draw']
            lengthreq = self.cleaned_data['length']
            start = self.cleaned_data['start']
            searchstr = ""

            orderstr = "id"
            dir = 'desc'

            if 'search[value]' in request.POST:
                searchstr = request.POST['search[value]']
            if 'order[0][column]' in request.POST:
                ordercolumn = int(request.POST['order[0][column]'])
            if 'order[0][dir]' in request.POST:
                dir = request.POST['order[0][dir]']

            if ordercolumn == 0:
                orderstr = "id"
            elif ordercolumn == 1:
                orderstr = "tank__name"
            elif ordercolumn == 2:
                orderstr = "accepted"
            elif ordercolumn == 3:
                orderstr = "score"
            elif ordercolumn == 4:
                orderstr = "points"
            elif ordercolumn == 5:
                orderstr = "submitterText"
            elif ordercolumn == 6:
                orderstr = "managerText"
            elif ordercolumn == 7:
                orderstr = "manager__discord_nickname"
            elif ordercolumn == 8:
                orderstr = "proof"
            elif ordercolumn == 9:
                orderstr = "date"

            if dir == 'desc':
                orderstr = '-' + orderstr


            submissions = BasicUserPointSubmission.objects.filter(
                pointsinfo=self.cleaned_data['pointsinfo'],decided=True).prefetch_related('tank','gamemode','pointsinfo','manager','pointsinfo__user')
            allsubs = submissions.count()
            if searchstr!="":
                numbersearch=float_or_0(searchstr)
                submissions=submissions.filter(Q(id=numbersearch)|Q(tank__name__icontains=searchstr)|Q(points=numbersearch)|Q(submitterText__icontains=searchstr)|Q(managerText__icontains=searchstr)|Q(manager__discord_nickname__icontains=searchstr)|Q(proof__icontains=searchstr))
            submissions = submissions.order_by(
                orderstr)  # the '-' is for reversing the order (so the one who has most points will be on top
            p = Paginator(submissions, lengthreq)

            filtered = p.count

            page = p.page(start / lengthreq + 1)

            serializer = BasicUserPointSubmissionSerializerMinimal(page.object_list, many=True)
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:

            return self.datatables_leaderboard_response(
                {'draw': drawnr, 'recordsTotal': allsubs, 'recordsFiltered': filtered, 'data': (serializer.data)})

    class Meta:
        model = BasicUserPointSubmission
        fields = ('draw', 'start', 'length', 'pointsinfo')


class RetrieveUsersToFightAgainstForm(BaseForm):
    searchusers = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(RetrieveUsersToFightAgainstForm, self).__init__(AjaxAction.RETRIEVEUSERSTOFIGHTAGAINST, *args, **kwargs)

    def handle(self, request):

        try:
            searchstring = self.cleaned_data['searchusers']
            users = ClanUser.objects.filter(is_active=True, discord_nickname__icontains=searchstring).exclude(
                id=request.user.id).order_by(
                '-discord_nickname')[:10]

            serializer = ClanUserSerializerBasic(users, many=True)
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = ClanUser
        fields = ('searchusers',)


class RetrieveFightsSubmissionsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(RetrieveFightsSubmissionsForm, self).__init__(AjaxAction.RETRIEVEFIGHTSSUBMISSIONS, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()
        proofsbylink = {}

        try:
            submissions = OneOnOneFightSubmission.objects.filter(decided=False)[:30]

            proofused = OneOnOneFightSubmission.objects.values('proof').filter(decided=False).distinct()

            for p in proofused:
                link = p['proof']
                proofused = OneOnOneFightSubmission.objects.filter(proof=link)
                proofsbylink[link] = proofused

            for sub in submissions:
                sub.proofused = proofsbylink[sub.proof]

            serializer = OneOnOneFightSubmissionSerializer(submissions, many=True)
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = OneOnOneFightSubmission
        fields = ()


class RevertSubmissionForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(RevertSubmissionForm, self).__init__(AjaxAction.REVERTSUBMISSION, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()
        try:
            submission = BasicPointSubmission.objects.get(pk=int(self.cleaned_data['pk_id']))

        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))  # TODO better exception
        else:

            submission.accepted = False
            submission.manager = request.user
            submission.decided = False
            submission.reverted = True

            try:
                x = PointsManagerAction.objects.get(pk=int(self.cleaned_data['pk_id']))
            except PointsManagerAction.DoesNotExist:
                pass
            else:
                x.decided = False

            print('saved')
            submission.save()
            serializer = BasicPointsSubmissionSerializer(submission)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = BasicPointSubmission
        fields = ('pk_id',)


class DecideUserPointSubmissionForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(DecideUserPointSubmissionForm, self).__init__(AjaxAction.DECIDEUSERPOINTUSUBMISSION, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()
        try:
            submission = BasicUserPointSubmission.objects.get(pk=int(self.cleaned_data['pk_id']))

        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))  # TODO better exception

        else:
            submission.accepted = self.cleaned_data['accepted']
            submission.score=self.cleaned_data['score']
            submission.managerText = strip_tags(self.cleaned_data['managerText'])
            submission.points = self.cleaned_data['points']
            if submission.points<0:
                submission.points=0
            submission.manager = request.user
            submission.decided = True
            submission.reverted = False
            print('saved')
            submission.save()
            serializer = BasicPointsSubmissionSerializer(submission)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = BasicUserPointSubmission
        fields = ('pk_id', 'accepted', 'managerText', 'points','score')


class DecideEventQuestsSubmissionForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(DecideEventQuestsSubmissionForm, self).__init__(AjaxAction.DECIDEEVENTQUESTS, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()
        try:
            submission = EventQuestSubmission.objects.get(pk=int(self.cleaned_data['pk_id']))

        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))  # TODO better exception

        else:
            submission.accepted = self.cleaned_data['accepted']
            submission.managerText = strip_tags(self.cleaned_data['managerText'])
            submission.points = self.cleaned_data['points']
            if submission.points<0:
                submission.points=0
            submission.manager = request.user
            submission.decided = True
            submission.reverted = False
            if submission.questtask and not submission.accepted and submission.questtask.quest.permed:
                import datetime
                submission.pointsinfo.permquestcd = datetime.datetime.utcnow()
            submission.save()

            serializer = BasicEventQuestsSubmissionSerializer(submission)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = EventQuestSubmission
        fields = ('pk_id', 'accepted', 'managerText', 'points')


class DecideFightsSubmissionForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)

    def __init__(self, *args, **kwargs):
        super(DecideFightsSubmissionForm, self).__init__(AjaxAction.DECIDEFIGHTSSUBMISSION, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()
        try:
            submission = OneOnOneFightSubmission.objects.get(pk=int(self.cleaned_data['pk_id']))

        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))  # TODO better exception

        else:
            submission.accepted = self.cleaned_data['accepted']
            submission.managerText = strip_tags(self.cleaned_data['managerText'])
            submission.manager = request.user
            submission.decided = True
            submission.reverted = False
            print('saved')

            if submission.accepted:
                manageElo(submission)
            submission.save()

            serializer = OneOnOneFightSubmissionSerializer(submission)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = BasicPointSubmission
        fields = ('pk_id', 'accepted', 'managerText')
