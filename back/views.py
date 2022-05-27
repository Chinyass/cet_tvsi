from django.shortcuts import render
import random
import time
from django.http import JsonResponse
from .NSnmp import Snmp

def index(request):
    return render(request,"back/index.html")

def get_traffic_ont(request):
    serial = 'ELTX83000CC4'
    snmp = Snmp('10.2.0.48','private_set')
    data = {
        'rx': snmp.get_traffic_ont(serial)[0]
    }
    return JsonResponse(data)