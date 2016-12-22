from django.http import HttpResponse
from django.template import RequestContext, Template
import json
from ..enums.AjaxActions import AjaxAction

def ajaxactions(request):
    data={}
    
    for name,member in AjaxAction.__members__.items():
        data[str(name)]=member.value
    
    return {
        
        
        'ajaxactions':json.dumps(data)
    }
    