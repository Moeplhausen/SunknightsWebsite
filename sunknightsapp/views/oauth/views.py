from allaccess.views import OAuthCallback,OAuthRedirect
from allaccess.clients import OAuth2Client, OAuthClient,BaseOAuthClient
import logging
import json
from requests.exceptions import RequestException
from django.shortcuts import redirect
from ...models.clan_user import ClanUser
from allaccess.models import AccountAccess
from django.contrib.auth import authenticate, login
from django.contrib.messages import error
from django.shortcuts import render,render_to_response




logger = logging.getLogger('allaccess.clients')


def get_client(provider, token=''):
    "Return the API client for the given provider."
    cls = DiscordOuth2Client
    if provider.request_token_url:
        cls = OAuthClient
    return cls(provider, token)


class DiscordOuth2Client(OAuth2Client):
    

    

    def get_profile_info(self, raw_token):
        "Fetch user profile information."
        try:
            bearer=(json.loads(raw_token)['access_token'])
            headers={'Authorization': 'Bearer ' + bearer}
            response = self.request('get', self.provider.profile_url, headers=headers,token=raw_token)
            response.raise_for_status()
        except RequestException as e:
            print('What?')
            logger.error('Unable to fetch user profile: {0}'.format(e))
            return None
        else:
            return response.json() or response.text
        
    def request(self, method, url, **kwargs):
        "Build remote url request. Constructs necessary auth."
        user_token = kwargs.pop('token', self.token)
        token, _ = self.parse_raw_token(user_token)
        if token is not None:
            params = kwargs.get('params', {})
            params['access_token'] = token
            kwargs['params'] = params
        return BaseOAuthClient(DiscordOuth2Client,self).request(method, url, **kwargs)
        
        
        

class OAuthRedirectDiscord(OAuthRedirect):
    def get_client(self, provider):
        "Get instance of the OAuth client for this provider."
        if self.client_class is not None:
            return self.client_class(provider)
        return get_client(provider)


    

class OAuthCallbackDiscord(OAuthCallback):
        def get_client(self, provider):
            "Get instance of the OAuth client for this provider."
            if self.client_class is not None:
                return self.client_class(provider)
            return get_client(provider)

        def handle_new_user(self, provider, access, info):
            "Redirect new users to homepage because every new User has to be on discord first"
            
            user=self.get_or_create_user(provider,access,info)
            if user is None or not user.is_active:
                return render_to_response('sunknightsapp/index.html',{'errors':['You are not an approved member in the SK Clan']})
            access.user = user
            AccountAccess.objects.filter(pk=access.pk).update(user=user)
            user = authenticate(provider=access.provider, identifier=access.identifier)
            login(self.request, user)
            return redirect(self.get_login_redirect(provider, user, access, True))


        def handle_existing_user(self, provider, user, access, info):
            "Login user and redirect."

            if not user.is_active:
                return render_to_response('sunknightsapp/index.html',{'errors':['You are not an approved member in the SK Clan']})

            login(self.request, user)
            return redirect(self.get_login_redirect(provider, user, access))

        def get_or_create_user(self, provider, access, info):
            "Actually, we just try to get an existing user"
            
            id=info['id']
            try:
                user= ClanUser.objects.get(discord_id=id)
                return user
            except ClanUser.DoesNotExist:
                return None
            


            

