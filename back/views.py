from django.shortcuts import render
from django.http import JsonResponse
from .NSnmp import Snmp

def index(request):
    return render(request,"back/index.html")