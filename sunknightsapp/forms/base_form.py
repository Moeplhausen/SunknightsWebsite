from django import forms
from django.forms import ModelForm
from django.http import JsonResponse

from ..enums.AjaxActions import AjaxAction


class BaseForm(ModelForm):
    ajax_action_id = forms.IntegerField(min_value=0, widget=forms.HiddenInput(), required=True)
    id_value=0

    def __init__(self, id, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self.fields['ajax_action_id'].widget.attrs['value'] = id.value
        self.id_value=id.value

    def handle(self, request):
        raise NotImplementedError("Please Implement this method")

    def noPermission(self):
        return self.response(False, "You do not have sufficient Permissions for this action")

    def response(self, noErrors=True, message=""):
        return JsonResponse({'status': 'success' if noErrors else 'failure', 'message': message,'action':self.id_value})

    class Meta:
        fields = ('ajax_action_id',)
        pass
