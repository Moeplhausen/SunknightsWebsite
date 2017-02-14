from django import template
register = template.Library()
from ..models.daily_quest import QuestTask


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

@register.simple_tag
def task_checked(user, task:QuestTask):
        q=QuestTask.objects.filter(id=task.id,eventquest__pointsinfo__user_id=user.id)

        if not q and task.tier==4:
            return '<i class="fa fa-question-circle" aria-hidden="true" data-toggle="tooltip" data-placement="top" title="Bonus quests can be selected when at least 3 other daily quests have been finished"></i>'

        if not q:
            return ""

        if q.filter(eventquest__accepted=True):
            return '<i class="fa fa-check" aria-hidden="true" data-toggle="tooltip" data-placement="top" title="You already completed that quest :)"></i>'


        return '<i class="fa fa-question-circle" aria-hidden="true" data-toggle="tooltip" data-placement="top" title="Your submission will be handled by a Points Manager shortly"></i>'


