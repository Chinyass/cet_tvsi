from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ATS,OLT,ONT,RSSI,OPERATIONS
from .serializers import ATSSerializer,OLTSerializer,ONTSerializer,RSSISerializer,OPERATIONSSerializer,RSSISSerializer_graph
from rest_framework import generics
from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
from .Snmp import Snmp
from django.http import JsonResponse
import json
import os 
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import time
from .get_inform import info
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import concurrent.futures
import math
from .get_switch_models import get_models_switch, get_check_auth, get_check_auth_many, execute_many, execute
from django.contrib.admin.views.decorators import staff_member_required
from .set.Cisco import Cisco
from .set.tln import change_ip,get_ip_router
from .Gepon9011 import get_data_gepon
#from .NSnmp import Snmp

def gepon_optical(request):
    if request.method == 'GET':
       data = get_data_gepon('10.254.38.86')
       return render(request,"customers/gepon.html",context={'data':data})

def login_auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
          return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    else:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


def change_vlan_and_ip_tehpod(request):
    if request.method == 'GET':
       a = Cisco('10.3.0.28','test','private_set')
       vlan = a.ports[6].get_access_vlan()
       ip = get_ip_router()
       return render(request,"customers/tehpod.html",context={'vlan':vlan,'ip':ip})

    elif request.method == 'POST':
       vlan = request.POST['vlan']
       ip = request.POST['ip']
       a = Cisco('10.3.0.28','test','private_set')
       print( a.ports[6].get_access_vlan() )
       print( a.ports[6].set_access_vlan(vlan) )
       print( a.ports[6].get_access_vlan() )
       change_ip(ip)
       return redirect("tehpod")
def logout_view(request):
    logout(request)

@login_required
def index(request):
	ip=''
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')	
	print(f'user in gponset:{request.user} {ip}')

	return render(request, "customers/index.html")
	
def sandbox(request):
    return render(request, "customers/sandbox.html")
	
@csrf_exempt
def get_nulls(request):
		received_json_data = json.loads(request.body)
		ips = received_json_data['ips']
		
		send_nulls = []
		for ip in ips:
			sw = Snmp(ip,'161','private_otu')
			nulls = sw.get_null_acs_login()
			print(nulls)
			if nulls:
				print('СѓСЃРїРµС€РЅРѕ')
				send_nulls.append(nulls)
		if not nulls:
			print('РЅРµ СѓСЃРїРµС€РЅРѕ')

		print(send_nulls)
		return JsonResponse({'data': send_nulls})

@csrf_exempt
def inform_ports(request):
	ip=''
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')	
	print(f'user in portget:{request.user} {ip}')

	received_json_data = json.loads(request.body)
	ip = received_json_data['ip']
	if ip.startswith('10.7'):
		return JsonResponse({'error':'true','message':'Р—Р°РїСЂРµС‰РµРЅРѕ' }, status=500)

	data = info(ip)
	if not data:
		return JsonResponse({'error':'true','message':'РќРµС‚ РґР°РЅРЅС‹С…' }, status=500)
	
	return JsonResponse(data)

@csrf_exempt
def findpersonal(request):
	if request.method == 'POST':
		received_json_data = json.loads(request.body)
		ips = received_json_data['ips']
		personal = received_json_data['personal']
		inform = {}
		for ip in ips:
			sw = Snmp(ip,'161','private_otu')
			inform = sw.get_inform_acs_user(personal)

			if inform:
				print('СѓСЃРїРµС€РЅРѕ')
				return JsonResponse(inform)


		if not inform:
			print('РЅРµ СѓСЃРїРµС€РЅРѕ')
			return JsonResponse({'error':'true','message':'ont РЅРµ РЅР°Р№РґРµРЅРѕ' }, status=500)

		return JsonResponse(inform)

@csrf_exempt
def find_ont(request):
    if request.method == 'POST':
        received_json_data=json.loads(request.body)
        print(received_json_data)

        ips = received_json_data['ips']
        serial = received_json_data['serial']

        send_data = {

        }
        found = False
        mes_err = 'ont РЅРµ РЅР°Р№РґРµРЅРѕ'
        err_ip = ''
        for ip in ips:
            if found:
                break

            sw = Snmp(ip,'161','private_otu')
            send_data = {}
            a = sw.get_OntChannel7_One(serial)
            if a['error']:
                err_ip = ip
                print(ip,a['error'])
                if a['error'] == 'status 13':
                    mes_err = f'ont {serial} unactivated'
                continue
            else:
                send_data = a
                send_data['ip'] = ip
                found = True
        
        if not found:
            olt = OLT.objects.get(ip=err_ip)
            try:
                ont = ONT.objects.get(serial=serial,olt=olt)
            except ONT.DoesNotExist:
                ont = ONT(serial=serial,port=-1,pon_id=-1,personal='unknown',olt=olt)
                ont.save()
            try: 
                operation = OPERATIONS(
                        author=request.user,
                        author_ip=ip,
                        status='danger',
                        message = mes_err,
                        ont=ont
                    )
            except ValueError:
                user = User.objects.get(username="AnonymousUser")
                operation = OPERATIONS(
                        author=user,
                        author_ip=ip,
                        status='danger',
                        message = mes_err,
                        ont=ont
                    )

            operation.save()
            return JsonResponse({'error':'true','message': mes_err }, status=500)

        return JsonResponse(send_data)

@csrf_exempt
def RegisterOnline(request):
	if request.method == 'POST':
		received_data = json.loads(request.body)
		print(received_data)
		rec_ont_model = received_data['model']
		rec_ont_serial = received_data['serial']
		rec_olt_ip = received_data['ip']
		rec_ont_personal = received_data['personal']
		rec_ont_login = received_data['login']
		rec_ont_password = received_data['pass']
		rec_ont_voip = received_data['phone']
		rec_ont_voip_number = received_data['voip_number']
		rec_ont_voip_pass = received_data['voip_pass']
		rec_ont_template_change = received_data['template_change']
		rec_ont_template = received_data['template']
		rec_olt_port = received_data['port']
		rec_olt_id = received_data['id']

		ont_template = 'err'
		ont_acs = 'errr'

		if rec_ont_model in 'NTP-2':
			ont_template = 'ntp'
			ont_acs = 'ntp2'
		elif rec_ont_model in 'NTU-2W':
			ont_template = 'ntu-rg'
			ont_acs = 'ntu-2w'
		elif rec_ont_model in 'NTU-RG-5421G-Wac' or rec_ont_model in 'NTU5421GWAC' or rec_ont_model in 'NTU-RG-5421G-Wac:rev.B' or rec_ont_model in 'NTU-RG-5420G-Wac':
			ont_template = 'ntu-rg'
			ont_acs = 'ntu5421'
		elif rec_ont_model in 'NTU-RG-1402G-W:rev.C':
			ont_template = 'ntu-rg'
			ont_acs = 'ntu-rg'
		elif rec_ont_model in 'NTU-RG-1421':
			ont_template = 'ntu-rg'
			ont_acs = 'ntu1421'
            
		set_user = False
		set_login = False
		set_profile = False
		set_reconf = False
		set_saved = False
		set_passw = False

		sw = Snmp(rec_olt_ip,'161','private_set')

		set_delete = sw.set_delete_user(rec_ont_serial)
		if rec_ont_personal != '':
			print(rec_ont_personal)     
			set_user = sw.set_acs_user_personal(rec_ont_serial,rec_ont_personal)
			set_login = sw.set_acs_user_login(rec_ont_serial,rec_ont_login)
			set_passw = sw.set_acs_user_password(rec_ont_serial,rec_ont_password)
			set_profile = sw.set_acs_user_profile(rec_ont_serial,ont_acs)
		#set_voip_enable = False
		#set_voip_number = False
		#set_voip_passw = False
		datax={}
		if rec_ont_voip:
			set_voip_enable = sw.set_voip_enable(rec_ont_serial)
			set_voip_number = sw.set_voip_number(rec_ont_serial,rec_ont_voip_number)
			set_voip_passw = sw.set_voip_pass(rec_ont_serial, rec_ont_voip_pass)
			set_voip_sip = sw.set_voip_sip_server(rec_ont_serial,'94.230.240.28')
			datax['voip_enable'] = set_voip_enable
			datax['voip_number'] = set_voip_number
			datax['voip_passw'] = set_voip_passw

		set_template = False
		if rec_ont_template_change:
			set_template = sw.set_template_profile(rec_ont_serial,rec_ont_template)

		set_reconf = sw.set_acs_user_reconf(rec_ont_serial)
		
		set_saved = sw.set_save()

		

		datax['olt_ip'] = rec_olt_ip
		datax['serial'] = rec_ont_serial
		datax['port'] = rec_olt_port
		datax['id'] = rec_olt_id
		datax['user'] = set_user
		datax['login'] = set_login
		datax['passw'] = set_passw
		datax['profile'] = set_profile
		datax['model'] = rec_ont_model
		datax['reconf'] = set_reconf
		datax['saved'] = set_saved

		if rec_ont_template_change:
			datax['template'] = set_template 
		
		ip=''
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		olt = OLT.objects.get(ip=rec_olt_ip)
		try:
			ont = ONT.objects.get(serial=rec_ont_serial,port=rec_olt_port,pon_id=rec_olt_id,personal=rec_ont_personal,olt=olt)
			if ont.id == -1:
				raise ONT.DoesNotExist
		except ONT.DoesNotExist:
			ont,_ = ONT.objects.update_or_create(serial=rec_ont_serial,port=rec_olt_port,pon_id=rec_olt_id,personal=rec_ont_personal,olt=olt)
			print(ont)
			ont.save()

		status = "success"
		if (not set_user or not set_login or not set_passw ):
    			status= "danger"
		elif (not set_reconf or not set_saved):
    			status = "warning"

		#username = User.objects.get_or_create(username=request.user)
		print(request.user.username == 'AnonymousUser')
		try: 
			operation = OPERATIONS(
					author=request.user,
					author_ip=ip,
					status=status,
					ch_user=set_user,
					ch_login=set_login,
					ch_password=set_passw,
					ch_profile=set_profile,
					ch_reconf=set_reconf,
					ch_saved=set_saved,
					ont=ont
				)
		except ValueError:
			user = User.objects.get(username="AnonymousUser")
			operation = OPERATIONS(
					author=user,
					author_ip=ip,
					status=status,
					ch_user=set_user,
					ch_login=set_login,
					ch_password=set_passw,
					ch_profile=set_profile,
					ch_reconf=set_reconf,
					ch_saved=set_saved,
					ont=ont
				)

		operation.save()
		print(datax)
		return JsonResponse(datax)
@csrf_exempt
def OPERATIONS_lasts(request):
	operations = OPERATIONS.objects.all().order_by('-created')[:3]

	serializer = OPERATIONSSerializer(operations,many=True)
	return JsonResponse({
		'data':serializer.data,
		}, safe=False)

@csrf_exempt
def OPERATIONS_list(request):
	operations = OPERATIONS.objects.all().order_by('-created')
	col_item = 5
	length = math.ceil(len(operations) / col_item)
	paginator = Paginator(operations, col_item)
	body = json.loads(request.body)
	print(body)
	page = body['page']
	operations = paginator.get_page(page)
	print(operations)
	serializer = OPERATIONSSerializer(operations,many=True)
	return JsonResponse({
		'data':serializer.data,
		'rows': length
		}, safe=False)

@csrf_exempt
def rssi_get(request):
	data = RSSI.objects.all().order_by('-created')
	times = list(map(lambda x: x.created.replace(second=0,microsecond=0),data))
	times = list(set(times))
	categories = [times[0]]
	filtered_data = RSSI.objects.filter(created__contains=times.pop(0).date())
	ser_data = list(map(lambda x: {
		'rx': [x.rx],
		'tx': [x.tx],
		'port': x.ont.port,
		'pon_id': x.ont.pon_id,
		'ip': x.ont.olt.ip
	},filtered_data))
	categories +=times
	for time in times:
		f_data = RSSI.objects.filter(created__contains=time.date())
		for search_data in ser_data:
			for finded_data in f_data:
				if finded_data.ont.port == search_data['port'] and finded_data.ont.pon_id == search_data['pon_id']:
					search_data['rx'].append(finded_data.rx)
					search_data['tx'].append(finded_data.tx)
					break
	return JsonResponse({
		'data': ser_data,
		'categories':categories
	},safe=False)

@csrf_exempt
@staff_member_required
def get_models(request):
	rec_data = json.loads(request.body)
	ips = rec_data['ips']
	models = get_models_switch(ips)
	return JsonResponse({
		'models': models,
	},safe=False)

@csrf_exempt
@staff_member_required
def telnet_check(request):
	rec_data = json.loads(request.body)
	print(rec_data)
	login = rec_data['login']
	password = rec_data['password']
	ips_a_ind = rec_data['ips']
	
	data = get_check_auth( login,password,ips_a_ind )
	return JsonResponse({
		'status':data,
	},safe=False)

@csrf_exempt
@staff_member_required
def telnet_check_many(request):
	rec_data = json.loads(request.body)
	data = rec_data['data']
	res = get_check_auth_many(data)
	return JsonResponse({
		'status': res
	})

@csrf_exempt
@staff_member_required
def telnet_execute(request):
	rec_data = json.loads(request.body)['data']
	res = execute(rec_data)
	return JsonResponse({
		'data': res
	})
	
@csrf_exempt
@staff_member_required
def telnet_execute_many(request):
	rec_data = json.loads(request.body)
	login = rec_data['login']
	password = rec_data['password']
	data = rec_data['data']
	res = execute_many(login,password,data)
	return JsonResponse({
		'data': res
	})


class ats_list(generics.ListCreateAPIView):
    queryset = ATS.objects.all()
    serializer_class = ATSSerializer

class ATSDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ATS.objects.all()
    serializer_class = ATSSerializer


class olt_list(generics.ListCreateAPIView):
    queryset = OLT.objects.all()
    serializer_class = OLTSerializer

class OLTDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OLT.objects.all()
    serializer_class = OLTSerializer


class ont_list(generics.ListCreateAPIView):
    queryset = ONT.objects.all()
    serializer_class = ONTSerializer

class ONTDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ONT.objects.all()
    serializer_class = ONTSerializer


class rssi_list(generics.ListCreateAPIView):
    queryset = RSSI.objects.all()
    serializer_class = RSSISerializer

class RSSIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RSSI.objects.all()
    serializer_class = RSSISerializer
