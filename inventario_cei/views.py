from django.shortcuts import render, redirect
import json
from django.http import JsonResponse

from inventario_cei.models import Space

# Create your views here.

def testdata(request):
    # return JsonResponse({'a':Space.name.toString})
    data = [] 
    for i in Space.objects.all():
        data.append(i.name)
    return JsonResponse(data,safe=False)
    return redirect('/administrator')


def createtestdatas(request):
    s = Space() 
    s.name = 'sala01'
    s.image = 'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'
    s.capacity = 100
    return JsonResponse({'result':s.values('name','image','capacity')}, safe=False)

def createtestdata(request):
    createHalls()


def createHalls():
    s = Space() 
    data = [
        {'name': 'sala02', 'capacity': 100, 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        {'name': 'sala02', 'capacity': 100, 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
        {'name': 'sala02', 'capacity': 100, 'image':'https://www.hotelsaratoga.com/.imaging/stk/hTtGeneric/bootstrapGalleryImageBig/dms/monoHotel-Hotel-Saratoga/servicios/sala-conferencias/saladeconferencias/document/saladeconferencias.jpg'},
    ]
    for d in data: 
        createObject(Space, d)

    return JsonResponse({'result':data}, safe=False)

def createObject(clazz, data):
    instance = clazz()
    for k,v in data.items(): 
        setattr(instance, k, v)
    instance.save()



