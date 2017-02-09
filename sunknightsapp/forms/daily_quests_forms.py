from .base_form import BaseForm
from ..models.daily_quest import Quest, QuestTask
from ..enums.AjaxActions import AjaxAction
from ..serializers.daily_quest_serializer import QuestSerializer, QuestTaskSerializer


class SubmitQuestTaskForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SubmitQuestTaskForm, self).__init__(AjaxAction.SUBMITQUESTTASK, *args, **kwargs)

    def handle(self, request):

        if not request.user.is_war_manager:
            return self.noPermission()

        try:
            quest = self.save(commit=False)
            quest.manager = request.user
            quest.save()
        except:
            return self.response(False, 'Something went wrong')  # TODO better exception
        else:
            serializer = QuestTaskSerializer(quest)
            print(serializer.data)
            return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = QuestTask
        fields = ('quest', 'tier', 'questtext')


class RequestQuestsForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(RequestQuestsForm, self).__init__(AjaxAction.RETRIEVEQUESTS, *args, **kwargs)

    def handle(self, request):
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
