from django.shortcuts import render, redirect
from django.core import serializers
from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


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

# register 
def handleRegister(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/userprofile')

    context = {}
    if request.method == 'GET':
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context, request))

    if request.method != 'POST':
        return HttpResponseRedirect('/cei/register')

    name = request.POST['name']
    rut = request.POST['rut']
    email = request.POST['email']
    password = request.POST['password']
    re_password = request.POST['re_password']

    if password != re_password: 
        context = {'error': 'Contrase&ntilde;as no coinciden'}
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context, request))


    if User.objects.filter(username=email).exists():
        context = {'error': 'Usuario "%s" ya existe' %email }
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context, request))

    
    user, created = User.objects.get_or_create(
                            username=email,
                            email=email
                        )


    if created:
        profile = Profile()
        user.set_password(password)
        user.save()
        profile.user = user
        profile.name = name
        profile.rut = rut
        profile.mail = email
        profile.save()
        # success
        context = {'success': 'Usuario "%s" exitosamente registrado' %email }
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context, request))
    else:
        # error
        context = {'error': 'Un error inesperado ha sucedido'}
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context, request))


# login
def handleLogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/userprofile')

    context = {}
    if request.method == 'GET':
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context, request))

    if request.method != 'POST':
        return HttpResponseRedirect('/cei/login')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/userprofile')
    else:
        context = {'error': 'Credenciales Invalidas'}
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context, request))
        
# logout
def handleLogout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/userprofile')
    
    logout(request)
    return HttpResponseRedirect('/cei/login')

def handleLogout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/userprofile')
    
    logout(request)
    return HttpResponseRedirect('/cei/login')


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
