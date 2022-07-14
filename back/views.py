from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .LTP import LTP
import back.serializer as serializer
import json
import back.Node as Node

def index(request):
    return render(request,"back/index.html")

def get_ats(request):
    if request.method == 'GET':
        return JsonResponse(serializer.get_ats(),safe=False)

@csrf_exempt
def search_vlan(request):
    if request.method == 'POST':
        res = json.loads(request.body)
        ports = Node.get_ports_on_vlan(res)
        return JsonResponse({ 'ports' : ports })

@csrf_exempt
def save_map(request):
    if request.method == 'POST':
        res = json.loads(request.body)
        Node.save_map(res)
        return JsonResponse({})

@csrf_exempt
def get_nodes(request):
    if request.method == 'POST':
        res = json.loads(request.body)
        print(res)
        map_name = res['map_name']
        print(map_name)
        if not map_name:
            return JsonResponse(Node.get_all_data_on_map('Ring rayons'),safe=False)
        else:
            return JsonResponse(Node.get_all_data_on_map(f'{map_name}'),safe=False)

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
def find_by_user(request):
    if request.method == 'POST':
        res = json.loads(request.body)
        user = res['user']
        ips = res['ips']
        errors = []
        if user:
            for ip in ips:
                ltp = LTP(ip,'private_set')
                user_info = ltp.find_ont_by_user(user)
                print(user_info)
                if not user_info['error']:
                    user_info['ip'] = ip
                    return JsonResponse([user_info],safe=False)
                else:
                    user_info['ip'] = ip
                    errors.append(user_info)
            
            return JsonResponse(errors,safe=False)
        else:
            return JsonResponse({'error': 'Null request'})

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
        delete_user = (False,)
        if res['acs_login']:
            all_users = ltp.get_ont_acs_user_all()
            user_exists = tuple(filter(lambda x: x[1] == res['acs_login'],all_users))
            if user_exists:
                delete_user = ltp.set_ont_delete_user(user_exists[0][0])

            print('DELETE USER',delete_user)
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
            print(set_template)
        
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

