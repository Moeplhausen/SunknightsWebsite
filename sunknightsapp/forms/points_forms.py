from .base_form import BaseForm
from ..enums.AjaxActions import AjaxAction
from ..models.point_submission import BasicUserPointSubmission, BasicPointSubmission,OneOnOneFightSubmission,PointsManagerAction
from ..serializers.pointsubmissions_serializer import BasicUserPointSubmissionSerializer, \
    BasicPointsSubmissionSerializer,OneOnOneFightSubmissionSerializer
from django import forms
from ..models.utility.little_things import getPointsByScore,getPointsByFight,manageElo


class SubmitPointsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SubmitPointsForm, self).__init__(AjaxAction.SUBMITPOINTS, *args, **kwargs)

    def handle(self, request):

        try:
            import decimal
            submission = self.save(commit=False)
            submission.points=getPointsByScore(submission.score)*decimal.Decimal(submission.tank.multiplier)
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


class SubmitFightsForm(BaseForm):
    whowon = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(SubmitFightsForm, self).__init__(AjaxAction.SUBMITFIGHTS, *args, **kwargs)

    def handle(self, request):

        try:
            submission = self.save(commit=False)

            if request.user.pointsinfo.id==submission.pointsinfoloser.id:#something fishy is happenening...
                return self.noPermission()

            submission.points=getPointsByFight(True)
            submission.pointsloser=getPointsByFight(False)
            if self.cleaned_data['whowon']=='1':
                submission.pointsinfo = request.user.pointsinfo
            else:
                submission.pointsinfo=submission.pointsinfoloser
                submission.pointsinfoloser=request.user.pointsinfo
            submission.save()
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:
            serializer = OneOnOneFightSubmissionSerializer(submission)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = OneOnOneFightSubmission
        fields = ('proof', 'pointsinfoloser','whowon')







class RetriveUserSubmissionsPointsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(RetriveUserSubmissionsPointsForm, self).__init__(AjaxAction.RETRIEVEUSERSUBMISSIONS, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            submissions = BasicUserPointSubmission.objects.filter(decided=False)
            serializer = BasicUserPointSubmissionSerializer(submissions, many=True)
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = BasicUserPointSubmission
        fields = ()


class RetrieveFightsSubmissionsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(RetrieveFightsSubmissionsForm, self).__init__(AjaxAction.RETRIEVEFIGHTSSUBMISSIONS, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            submissions = OneOnOneFightSubmission.objects.filter(decided=False)
            serializer = OneOnOneFightSubmissionSerializer(submissions, many=True)
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = BasicUserPointSubmission
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
            submission.manager=request.user
            submission.decided=False
            submission.reverted=True

            try:
                x = PointsManagerAction.objects.get(pk=int(self.cleaned_data['pk_id']))
            except PointsManagerAction.DoesNotExist:
                pass
            else:
                x.decided=False

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
            submission.managerText = self.cleaned_data['managerText']
            submission.points = self.cleaned_data['points']
            submission.manager=request.user
            submission.decided=True
            submission.reverted=False
            print('saved')
            submission.save()
            serializer = BasicPointsSubmissionSerializer(submission)
            return self.response(True, {'data': (serializer.data)})


    class Meta:
        model = BasicPointSubmission
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
            submission.managerText = self.cleaned_data['managerText']
            submission.manager=request.user
            submission.decided=True
            submission.reverted=False
            print('saved')
            submission.save()

            if submission.accepted:
                manageElo(submission.pointsinfo,submission.pointsinfoloser)



            serializer = OneOnOneFightSubmissionSerializer(submission)
            return self.response(True, {'data': (serializer.data)})


    class Meta:
        model = BasicPointSubmission
        fields = ('pk_id', 'accepted', 'managerText')

