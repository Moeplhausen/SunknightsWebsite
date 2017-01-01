from django import forms

from .base_form import *
from ..enums.AjaxActions import AjaxAction
from ..models.tournament import Tournament
from ..serializers.tournament_serializer import TournamentSerializer


class RequestTournamentsForm(BaseForm):
    def __init__(self,*args, **kwargs):
        super(RequestTournamentsForm, self).__init__(AjaxAction.GETTOURNAMENTS, *args, **kwargs)


    def handle(self,request):
        try:
            tours=Tournament.objects.all()
            serializer=TournamentSerializer(tours,many=True)
        except BaseException as e:
            return self.response(False,'Something went wrong: '+str(e))
        else:

            return self.response(True,{'data':(serializer.data)})


    class Meta:
        model=Tournament
        fields=()



class CreateTournamentForm(BaseForm):
    def __init__(self,*args, **kwargs):
        super(CreateTournamentForm, self).__init__(AjaxAction.CREATETOURNAMENT, *args, **kwargs)


    def handle(self,request):
        
        if not request.user.is_war_manager:
            return self.noPermission()
            
        try:
            tour=self.save(commit=False)
            tour.creator=request.user
            tour.save()
        except:
            return self.response(False,'Something went wrong')#TODO better exception
        else:
            serializer=TournamentSerializer(tour)
            print(serializer.data)
            return self.response(True,{'data':(serializer.data)})


    class Meta:
        model=Tournament
        fields=('name','description')


class EditTournamentForm(BaseForm):
    
    
    
    pk_id=forms.IntegerField(min_value=0,widget=forms.HiddenInput(),required=True)

    def __init__(self,*args, **kwargs):
        super(EditTournamentForm, self).__init__(AjaxAction.EDITTOURNAMENT, *args, **kwargs)

    def handle(self, request):
        if not request.user.is_war_manager:
            return self.noPermission()
        try:
            tour = Tournament.objects.get(pk=int(self.cleaned_data['pk_id']))
            tour.name=self.cleaned_data['name']
            tour.description=self.cleaned_data['description']
        except BaseException as e:
            return self.response(False, 'Something went wrong: ' + str(e))  # TODO better exception

        else:

            serializer=TournamentSerializer(tour)
            return self.response(True,{'data':(serializer.data)})

    class Meta:
        model=Tournament
        fields=('pk_id','name','description')


class DeleteTournamentForm(BaseForm):
    pk_id=forms.IntegerField(min_value=0,widget=forms.HiddenInput(),required=True)

    
    def __init__(self,*args, **kwargs):
        super(DeleteTournamentForm, self).__init__(AjaxAction.DELETETOURNAMENT, *args, **kwargs)


    def handle(self,request):
        if not request.user.is_war_manager:
            return self.noPermission()
        try:
            tour=Tournament.objects.get(pk=int(self.cleaned_data['pk_id']))
            serializer = TournamentSerializer(tour)
            tour.delete()
        except BaseException as e:
            return self.response(False, 'Something went wrong: '+str(e))  # TODO better exception
        
        else:
            return self.response(True,{'data':(serializer.data)})

    class Meta:
        model=Tournament
        fields=('pk_id',)