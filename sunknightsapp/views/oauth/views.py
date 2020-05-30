from ...models.clan_user import ClanUser
from django.contrib.auth import authenticate, login

            

def get_profile(backend, user, response, *args, **kwargs):
    if 'id' in response:
        try:
            id=response['id']
            user=ClanUser.objects.get(discord_id=id)
            login(kwargs.get('request'),user,backend='django.contrib.auth.backends.ModelBackend')
        except ClanUser.DoesNotExist:
            return



