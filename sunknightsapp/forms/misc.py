from .base_form import BaseForm
from ..enums.AjaxActions import AjaxAction
class ChangeDesc(BaseForm):
  def __init__(self, *args, **kwargs):
    super(ChangeDesc, self).__init__(AjaxAction.CHANGEDESC, *args, **kwargs)

  def handle(self, request):
    try:
      newdesc = request.POST['newdesc']
      # TODO register the stuff
    except BaseException as e:
      return self.response(False, 'Something went wrong: ' + str(e))  # TODO better exception
    else:
      return self.response(True, {'newdesc': request.POST['newdesc']})

  class Meta:
    fields = ('newdesc',)
