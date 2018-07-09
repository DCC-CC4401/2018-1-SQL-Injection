from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime, timedelta
import json
import datetime

from django.contrib.auth.models import User

from inventario_cei.models import Item
from inventario_cei.models import Space
from inventario_cei.models import Object
from inventario_cei.models import Client
from inventario_cei.models import Reserve
from inventario_cei.models import Profile

from .testdata import createClient,createHalls,createReservations,createObjects


# TODO: delete this method for production
# The next methods are created to test de data base
def testdata(request):
    today = datetime.date.today()
    start_week = today - datetime.timedelta(today.weekday()) 
    # start_week = today - datetime.timedelta(days=1) 
    end_week = start_week + datetime.timedelta(7)
    return JsonResponse(
            {
            # "items": list(Item.objects.values('id','name').distinct()), 
            # "objects": list(Object.objects.values('id','item__name','item_id').distinct()), 
            "start_week": start_week,
            "end_week": end_week,
            "spaces": list(Space.objects.filter(item__reserve__start__range=[start_week, end_week]).values(
                    'item__reserve__id', 'item__reserve__user__username','item__name','item__reserve__start','item__reserve__finish').order_by('-item__reserve__created')), 
            "spaces_all": list(Space.objects.values('id','item__reserve__start').distinct()), 
            # "users":list(User.objects.values('id','username').distinct()),
            # 'profile':list(Profile.objects.values('name','user_id','rut').distinct()),
            # 'reservations':list(Reserve.objects.values('item_id','user_id','start', 'finish').distinct())
            }
            ,safe=False)
    # return redirect('/administrator')


def createtestdata(request):
    clients = createClient()
    halls = createHalls()
    reservations = createReservations(clients, halls)
    objects = createObjects()
    reservations = createReservations(clients, objects)
    return JsonResponse({'result':'successfully completed!'}, safe=False)
