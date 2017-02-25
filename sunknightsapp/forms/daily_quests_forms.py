from .base_form import BaseForm
from ..models.daily_quest import Quest, QuestTask,QuestBuild,QuestTankMultiplier
from ..enums.AjaxActions import AjaxAction
from ..serializers.daily_quest_serializer import QuestSerializer, QuestTaskSerializer,QuestBuildSerializer,QuestTankMultiplierSerializer
from django import forms

class SubmitQuestTaskForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SubmitQuestTaskForm, self).__init__(AjaxAction.SUBMITQUESTTASK, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            task = self.save(commit=False)
            task.manager = request.user
            points=0

            if task.tier==1:
                points=3
                if task.quest.permed:
                    task.cooldown=12
            elif task.tier==2:
                points=6
                if task.quest.permed:
                    task.cooldown=24
            elif task.tier==3:
                points=10
                if task.quest.permed:
                    task.cooldown=24*2
            elif task.tier==4:
                points=0
            task.points=points


            task.save()
        except:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestTaskSerializer(task)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestTask
        fields = ('quest', 'tier', 'questtext')


class SubmitBuildForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SubmitBuildForm, self).__init__(AjaxAction.ADDQUESTBUILD, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            build = self.save(commit=False)
            build.manager = request.user
            build.save()
        except:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestBuildSerializer(build)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestBuild
        fields = ('quest', 'build')

class EditQuestBuildForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    def __init__(self, *args, **kwargs):
        super(EditQuestBuildForm, self).__init__(AjaxAction.EDITQUESTBUILD, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            task = QuestBuild.objects.get(pk=int(self.cleaned_data['pk_id']))
            task.manager=request.user
            task.build=self.cleaned_data['build']
            task.save()
        except QuestBuild.DoesNotExist:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestBuildSerializer(task)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestBuild
        fields = ('pk_id', 'build')

class DeleteQuestBuildForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    def __init__(self, *args, **kwargs):
        super(DeleteQuestBuildForm, self).__init__(AjaxAction.DELETEQUESTBUILD, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            task = QuestBuild.objects.get(pk=int(self.cleaned_data['pk_id']))


        except QuestTask.DoesNotExist:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestBuildSerializer(task)
            task.delete()

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestBuild
        fields = ('pk_id',)


class EditQuestTaskForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    def __init__(self, *args, **kwargs):
        super(EditQuestTaskForm, self).__init__(AjaxAction.EDITQUESTTASK, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            task = QuestTask.objects.get(pk=int(self.cleaned_data['pk_id']))
            task.manager=request.user
            task.points=self.cleaned_data['points']
            task.questtext=self.cleaned_data['questtext']
            task.save()
        except QuestTask.DoesNotExist:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestTaskSerializer(task)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestTask
        fields = ('pk_id', 'points', 'questtext')


class DeleteQuestTaskForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    def __init__(self, *args, **kwargs):
        super(DeleteQuestTaskForm, self).__init__(AjaxAction.DELETEQUESTTASK, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            task = QuestTask.objects.get(pk=int(self.cleaned_data['pk_id']))
            task.manager=request.user
            task.deleted=True
            task.save()

        except QuestTask.DoesNotExist:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestTaskSerializer(task)

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestTask
        fields = ('pk_id',)



class RequestQuestsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(RequestQuestsForm, self).__init__(AjaxAction.RETRIEVEQUESTS, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_points_manager:
            return self.noPermission()
        try:
            quests = Quest.objects.all()
            serializer = QuestSerializer(quests, many=True)
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))
        else:

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = Quest
        fields = ()







class SubmitMultiplierForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SubmitMultiplierForm, self).__init__(AjaxAction.ADDMULTIPLIER, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            build = self.save(commit=False)
            build.manager = request.user
            build.save()
        except:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestTankMultiplierSerializer(build)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestTankMultiplier
        fields = ('quest',)

class EditMultiplierForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    def __init__(self, *args, **kwargs):
        super(EditMultiplierForm, self).__init__(AjaxAction.EDITMULTIPLIER, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            task = QuestTankMultiplier.objects.get(pk=int(self.cleaned_data['pk_id']))
            task.manager=request.user
            task.tank=self.cleaned_data['tank']
            task.multiplier=self.cleaned_data['multiplier']
            task.save()
        except QuestTankMultiplier.DoesNotExist:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestTankMultiplierSerializer(task)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestTankMultiplier
        fields = ('pk_id', 'tank','multiplier')

class DeleteMultiplierForm(BaseForm):
    pk_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    def __init__(self, *args, **kwargs):
        super(DeleteMultiplierForm, self).__init__(AjaxAction.REMOVEMULTIPLIER, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_points_manager:
            return self.noPermission()

        try:
            task = QuestTankMultiplier.objects.get(pk=int(self.cleaned_data['pk_id']))


        except QuestTankMultiplier.DoesNotExist:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestTankMultiplierSerializer(task)
            task.delete()

            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestTankMultiplier
        fields = ('pk_id',)
