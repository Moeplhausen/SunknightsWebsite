from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from ..models.clan_user import ClanUser

def index(request):
    users=ClanUser.objects.all()
    context={'noobs':users}
    return render(request,'index.html',context)