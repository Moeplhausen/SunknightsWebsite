from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 
from django.db import connection 
from ..models.clan_user import ClanUser 
from ..views.oauth.views import get_client


def index(request):
    users=ClanUser.objects.all()
    context={'noobs':users}
    if request.user.is_authenticated():
        try:
            access = request.user.accountaccess_set.all()[0]
        except IndexError:
            access = None
        else:
            client = get_client(access.provider,access.access_token or '')
            context['info'] = client.get_profile_info(raw_token=access.access_token)
    return render(request,'index.html',context)


def home(request):
    context={}
    return render(request,'userview.html',context)

