from .base_form import BaseForm
from ..models.daily_quest import DailyQuest
from ..enums.AjaxActions import AjaxAction
from ..serializers.daily_quest_serializer import DailyQuestSerializer


class SubmitQuestForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SubmitQuestForm, self).__init__(AjaxAction.SUBMITQUEST, *args, **kwargs)

        def handle(self, request):

            if not request.user.is_war_manager:
                return self.noPermission()

            try:
                quest = self.save(commit=False)
                quest.creator = request.user
                quest.save()
            except:
                return self.response(False, 'Something went wrong')  # TODO better exception
            else:
                serializer = DailyQuestSerializer(quest)
                print(serializer.data)
                return self.response(True, {'data': (serializer.data)})

    class Meta:
        model = DailyQuest
        fields = ('tier', 'questtext', 'permed')

class RequestDailyQuestsForm(BaseForm):
    def __init__(self,*args, **kwargs):
        super(RequestDailyQuestsForm, self).__init__(AjaxAction.RETRIEVEDAILYQUESTS, *args, **kwargs)


    def handle(self,request):
        try:
            quests=DailyQuest.objects.all()
            serializer=DailyQuestSerializer(quests,many=True)
        except BaseException as e:
            return self.response(False,'Something went wrong: '+str(e))
        else:

            return self.response(True,{'data':(serializer.data)})


    class Meta:
        model=DailyQuest
        fields=()
