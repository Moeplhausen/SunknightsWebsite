from .base_form import BaseForm
from  ..models.clan_user import ClanUser
from ..enums.AjaxActions import AjaxAction
class ChangeDesc(BaseForm):
  def __init__(self, *args, **kwargs):
    super(ChangeDesc, self).__init__(AjaxAction.CHANGEDESC, *args, **kwargs)

  def handle(self, request):
    try:
      newdescription=self.cleaned_data['description']
      request.user.description=newdescription
      request.user.save()
      # TODO register the stuff
    except BaseException as e:
      return self.response(False, 'Something went wrong: ' + str(e))  # TODO better exception
    else:
      return self.response(True, {'description': request.user.description})

  class Meta:
    model = ClanUser
    fields = ('description',)
