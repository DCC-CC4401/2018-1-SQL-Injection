from django.http import HttpResponse, JsonResponse
from django.template import loader
from datetime import datetime

import datetime

from inventario_cei.models import Object, Space

from .testdata import createClient, createReservations, createObjects


def index(request):
    context = {}
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))


def objects(request):
    items = Object.objects.all()
    context = {
        'items': items,
        'objects_style': 'btn-success',
        'spaces_style': 'btn-secondary',
    }
    template = loader.get_template('items_display.html')

    return HttpResponse(template.render(context, request))


def spaces(request):
    items = Space.objects.all()
    context = {
        'items': items,
        'objects_style': 'btn-secondary',
        'spaces_style': 'btn-success',
    }
    template = loader.get_template('items_display.html')

    return HttpResponse(template.render(context, request))


# The next methods are created to test de data base
def testdata(request):
    today = datetime.date.today()
    start_week = today - datetime.timedelta(today.weekday())
    end_week = start_week + datetime.timedelta(7)
    return JsonResponse(
            {
                # 'items': list(Item.objects.values('id', 'name').distinct()),
                # 'spaces': list(Space.objects.values('id', 'item__name', 'item_id').distinct()),
                # 'users': list(User.objects.values('id', 'username').distinct()),
                # 'profile': list(Profile.objects.values('name', 'user_id', 'rut').distinct()),
                # 'reservations': list(Reserve.objects.values('item_id', 'user_id', 'start', 'finish').distinct())},

                'start_week': start_week,
                'end_week': end_week,
                'spaces': list(Space.objects.filter(item__reserve__start__range=[start_week, end_week]).values(
                    'item__reserve__id',
                    'item__reserve__user__username',
                    'item__name',
                    'item__reserve__start',
                    'item__reserve__finish').order_by('-item__reserve__created')
                ),
                'spaces_all': list(Space.objects.values('id', 'item__reserve__start').distinct()),
            },
            safe=False)


def createtestdata(request):
    clients = createClient()
    objects = createObjects()
    reservations = createReservations(clients, objects)
    return JsonResponse({'result': 'successfully completed!'}, safe=False)
