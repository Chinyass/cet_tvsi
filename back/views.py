from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .LTP import LTP
import back.serializer as serializer
import json

def index(request):
    return render(request,"back/index.html")

def get_ats(request):
    if request.method == 'GET':
        return JsonResponse(serializer.get_ats(),safe=False)

@csrf_exempt
def find_ont(request):
    if request.method == 'POST':
        res = json.loads(request.body)
        ips = res['ips']
        serial = res['serial']
        
        errors = []
        for ip in ips:
            ltp = LTP(ip,'private_set')
            data = ltp.find_ont(serial)
            print(data)
            if not data['error']:
                data['ip'] = ip
                return JsonResponse([data],safe=False)
            else:
                data['ip'] = ip
                errors.append(data)
        
        return JsonResponse(errors,safe=False)