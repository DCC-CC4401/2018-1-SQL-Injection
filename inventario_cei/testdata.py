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
# from models import User

# Create your views here.

# TODO: delete this method for production
# The next methods are created to test de data base
def testdata(request):
    data = Space.objects.values('name').distinct()
    users = User.objects.values('username','id').distinct()

    
    return JsonResponse({"data": list(data), 
                            "users":list(users),
                            'profile':list(Profile.objects.values('name','user_id','rut').distinct())}
                        ,safe=False)
    # return redirect('/administrator')


def createtestdata(request):
    clients = createClient()
    halls = createHalls()
    reservations = createReservations(clients, halls)
    return JsonResponse({'result':'1'}, safe=False)

def createReservations(clients, halls):
    data = []
    for i in range(0, len(clients)):
        r = Reserve()
        r.user = clients[i].user
        r.space = halls[i]
        r.start = datetime.now()
        r.finish = datetime.now() + timedelta(hours=9)
        r.state = 'p'
        r.save()
        data.append(r)
    return 

def createClient():
    data = [
        {'rut': 987654331, 'username': 'bart', 'email': 'bart@simpson.net', 'password':'12345678', 'name': 'bart simpson'},
        {'rut': 387654322, 'username': 'lisa', 'email': 'lisa@simpson.net', 'password':'12345678', 'name': 'bart simpson'},
        {'rut': 487654313, 'username': 'milhouse', 'email': 'milhouse@simpson.net', 'password':'12345678', 'name': 'bart simpson'},
    ]
    datas = []
    for d in data: 
        
        user, created = User.objects.get_or_create(
                                username=d['username'],
                                email=d['email']
                            )
        profile = Profile()
        if created:
            user.set_password(d['password'])
            user.save()
            profile.user = user
            profile.name = d['name']
            profile.rut = d['rut']
            profile.mail = d['email']
            profile.save()
        else:
            profile = user.profile
        
        datas.append(profile)

    return datas

def createUser(username, email, password):
    
    user, created = User.objects.get_or_create(username=username,
                                                   email=email)
    if created:
        user.set_password(password)
        # user.save()
    return user

def createUser2(username, email, password):
    u = User.objects.create_user(username=username,
                                 email=email,
                                 password=password)
    u.save()                       
    return u

def createHalls():
    data = [
        {'name': 'sala01', 'capacity': 100, 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        {'name': 'sala02', 'capacity': 100, 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        {'name': 'sala03', 'capacity': 100, 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
    ]
    datas = []
    for d in data:
        datas.append(createHall(Space, d))
    return datas

def createHall(clazz, data):
    instance = clazz()
    for k,v in data.items(): 
        setattr(instance, k, v)
    instance.save()
    return instance

def createObject(clazz, data):
    instance = clazz()
    for k,v in data.items(): 
        setattr(instance, k, v)
    instance.save()
    return instance


