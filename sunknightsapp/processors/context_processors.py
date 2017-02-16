from django.http import HttpResponse
from django.template import RequestContext, Template
import json
from ..enums.AjaxActions import AjaxAction
from ..models.diep_tank import DiepTank
from ..serializers.tank_serializer import DiepTankSimpleSerializer

def ajaxactions(request):
    data={}
    
    for name,member in AjaxAction.__members__.items():
        data[str(name)]=member.value
    
    return {
        'ajaxactions':json.dumps(data)
    }


def dieptanks(request):

    tanks=DiepTank.objects.filter(diep_isDeleted=False)
    tankserialized=DiepTankSimpleSerializer(tanks,many=True)

    return {
        'jsontanks':json.dumps((tankserialized.data))
    }