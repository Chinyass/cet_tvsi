from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .NSnmp import Snmp
import back.serializer as serializer

def index(request):
    return render(request,"back/index.html")

@csrf_exempt
def get_ats(request):
    return JsonResponse(serializer.get_ats(),safe=False)

