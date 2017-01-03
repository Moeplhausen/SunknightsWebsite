from .base_form import BaseForm
from ..enums.AjaxActions import AjaxAction
from ..models.point_submission import BasicUserPointSubmission, BasicPointSubmission
from ..serializers.pointsubmissions_serializer import BasicUserPointSubmissionSerializer, \
    BasicPointsSubmissionSerializer
from django import forms
from ..models.utility.little_things import getPointsByScore


class SubmitPointsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SubmitPointsForm, self).__init__(AjaxAction.SUBMITPOINTS, *args, **kwargs)

    def handle(self, request):

        try:
            submission = self.save(commit=False)
            submission.points=getPointsByScore(submission.score)
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
            submission.manager=request.user
            submission.decided=True
            print('saved')
            submission.save()
            serializer = BasicPointsSubmissionSerializer(submission)
            return self.response(True, {'data': (serializer.data)})


    class Meta:
        model = BasicPointSubmission
        fields = ('pk_id', 'accepted', 'managerText')
