
##===================================## preferences_forms.py ##===================================##

##================================================================================================##
##{{{begin imports

#--
from .base_form import BaseForm
#--
from ..enums.AjaxActions import AjaxAction
#--
from ..models.clan_user import ClanUserPreferences
#--
from ..serializers.clan_user_serializer import ClanUserPreferencesSerializer
#--

##end imports}}}
##================================================================================================##

##================================================================================================##
##{{{begin class SubmitPreferencesForm:
class SavePreferencesForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(SavePreferencesForm, self).__init__(AjaxAction.SAVEPREFERENCES, *args, **kwargs)

    def handle(self, request):

        try:
            pref = ClanUserPreferences.objects.get(clan_user=request.user)
        except ClanUserPreferences.DoesNotExist:
            pref=ClanUserPreferences.objects.create(clan_user=request.user)

        pref.custom_background_enabled=self.cleaned_data['custom_background_enabled']
        pref.custom_background_url=self.cleaned_data['custom_background_url']
        pref.save()
        serializer = ClanUserPreferencesSerializer(pref)
        print(serializer.data)
        return self.response(True, {'data': (serializer.data)})

    ##============================================================================================##
    ##{{{begin class Meta:
    class Meta:
        model = ClanUserPreferences
        fields = ('custom_background_enabled', 'custom_background_url',)
    ##end class Meta}}}
    ##============================================================================================##

##end class SubmitPreferencesForm}}}
##================================================================================================##
