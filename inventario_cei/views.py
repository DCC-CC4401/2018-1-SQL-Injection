from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime, timedelta
import json

from django.contrib.auth.models import User

from inventario_cei.models import Space
from inventario_cei.models import Client
from inventario_cei.models import Reserve
from inventario_cei.models import Profile

from .testdata import createClient,createHalls,createReservations
# from models import User

# Create your views here.

# TODO: delete this method for production
# The next methods are created to test de data base
def testdata(request):
    return JsonResponse(
            {"data": list(Space.objects.values('id','name').distinct()), 
            "users":list(User.objects.values('id','username').distinct()),
            'profile':list(Profile.objects.values('name','user_id','rut').distinct()),
            'reservations':list(Reserve.objects.values('space_id','user_id','start', 'finish').distinct())}
            ,safe=False)
    # return redirect('/administrator')


def createtestdata(request):
    clients = createClient()
    halls = createHalls()
    reservations = createReservations(clients, halls)
    return JsonResponse({'result':'successfully completed!'}, safe=False)
