from django.forms import ModelForm,Form
from ..enums.AjaxActions import AjaxAction
from django import forms

from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer

class BaseForm(ModelForm):

    ajax_action_id=forms.IntegerField(min_value=0,widget=forms.HiddenInput(),required=True)




    def __init__(self,id:AjaxAction,*args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self.fields['ajax_action_id'].widget.attrs['value']=id.value


    def handle(self,request):
        raise NotImplementedError("Please Implement this method")

    def noPermission(self):
        return self.response(False,"You do not have sufficient Permissions for this action")


    def response(self,noErrors=True,message=""):
        return JsonResponse({'status':'success' if noErrors else 'failure','message':message})


    class Meta:
        fields=('ajax_action_id',)
        pass
