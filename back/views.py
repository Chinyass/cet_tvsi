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

@csrf_exempt
def setting_ont(request):
    if request.method == 'POST':
        res = json.loads(request.body)
        print(res)
        ip = res['ip']
        ltp = LTP(ip,'private_set')
        dec_serial = ltp.convert_hex_serial_to_dec(res['serial'])

        set_acs_user = (False,)
        set_acs_login = (False,)
        set_acs_password = (False,)
        if res['acs_login']:
            delete_user = ltp.set_ont_delete_user(dec_serial)
            set_acs_user = ltp.set_ont_acs_user(dec_serial,res['acs_login'])
            set_acs_login = ltp.set_ont_acs_login(dec_serial,res['acs_login'])
            set_acs_password = ltp.set_ont_acs_password(dec_serial,res['acs_password'])
        
        set_voip_number = (False,)
        set_voip_password = (False,)
        set_voip_server = (False,)
        if res['voip_selected']:
            set_voip_number  = ltp.get_ont_voip_number(dec_serial,res['voip_number'])
            set_voip_password = ltp.set_ont_voip_password(dec_serial,res['voip_password'])
            set_voip_server = ltp.set_ont_voip_server(dec_serial,res['voip_server'])
        
        profile = 'ntu5421'
        if '542' in res['model']:
            profile = 'ntu5421'
        elif '1402' in res['model']:
            profile = 'ntu-rg'
        elif '1421' in res['model']:
            profile = 'ntu1421'
        elif 'NTP-2' in res['model']:
            profile = 'ntp2'
        elif 'NTU-2W' in res['model']:
            profile = 'ntu-2w'
        
        set_acs_profile = ltp.set_ont_acs_profile(dec_serial,profile)

        set_template = (False,)
        if res['template_change']:
            set_template = ltp.set_ont_template(dec_serial,res['template'])
        
        set_reconf = ltp.set_ont_reconfigurate(dec_serial)

        set_save = ltp.set_olt_save()

        jdata = {
            'acs_user' : set_acs_user[0],
            'acs_login' : set_acs_login[0],
            'acs_password' : set_acs_password[0],
            'voip_number' : set_voip_number[0],
            'voip_password' : set_voip_password[0],
            'voip_server' : set_voip_server[0],
            'profile' : set_acs_profile[0],
            'template' : set_template[0],
            'reconf' : set_reconf[0],
            'save' : set_save[0]
        }
        print('JDATA',jdata)
        return JsonResponse(jdata)