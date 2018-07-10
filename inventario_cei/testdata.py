from django.shortcuts import render, redirect
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime, timedelta,date
import json

from django.contrib.auth.models import User,Group

from inventario_cei.models import Item
from inventario_cei.models import Space
from inventario_cei.models import Object
from inventario_cei.models import Client
from inventario_cei.models import Reserve
from inventario_cei.models import Profile
# from models import User

# Create your views here.

def createReservations(clients, halls):
    data = []
    for i in range(0, min(len(halls), len(clients))):
        r = Reserve()
        r.user = clients[i].user
        r.item = halls[i].item
        r.start = datetime.now() 
        r.finish = datetime.now() + timedelta(hours=1)
        r.state = 'p'
        r.save()
        # a = date.today() + timedelta(days=2)
        # b
        data.append(r)
    return 

def createClient():
    data = [
        {'rut': 987654331, 'username': 'bart@simpson.net', 'email': 'bart@simpson.net', 'password':'12345678', 'name': 'bart simpson'},
        {'rut': 387654322, 'username': 'lisa@simpson.net', 'email': 'lisa@simpson.net', 'password':'12345678', 'name': 'bart simpson'},
        {'rut': 487654313, 'username': 'milhouse@simpson.net', 'email': 'milhouse@simpson.net', 'password':'12345678', 'name': 'bart simpson'},
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

        administrator_group, created = Group.objects.get_or_create(name='administrator_group')
        administrator_group.user_set.add(user)
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
    itemsdata = [
        {'item': {'name': 'sala01'},
        'space': {'capacity': 100, 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        },
        {'item': {'name': 'sala02'},
        'space': {'capacity': 100, 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        }
    ]
    datas = []
    for d in itemsdata:
        
        item = createObject(Item, d['item'])
        d['space']['item_id'] = item.id
        
        datas.append(createObject(Space, d['space']))
    return datas

def createObjects():
    itemsdata = [
        {'item': {'name': 'escoba2'},
        'object': {'condition': 'l', 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        },
        {'item': {'name': 'saxofon'},
        'object': {'condition': 'p', 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        },
        {'item': {'name': 'microfono'},
        'object': {'condition': 'd', 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        },
        {'item': {'name': 'escoba1'},
        'object': {'condition': 'r', 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        }
    ]
    datas = []
    for d in itemsdata:
        
        item = createObject(Item, d['item'])
        d['object']['item_id'] = item.id
        
        datas.append(createObject(Object, d['object']))
    return datas

def createObject(clazz, data):
    instance = clazz()
    for k,v in data.items(): 
        setattr(instance, k, v)
    instance.save()
    return instance


