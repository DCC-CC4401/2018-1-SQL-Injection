from django.http import HttpResponse, JsonResponse
from django.template import loader

from django.contrib.auth.models import User

from inventario_cei.models import Item
from inventario_cei.models import Object, Space
from inventario_cei.models import Profile
from inventario_cei.models import Reserve

from .testdata import createClient, createHalls, createReservations


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
    return JsonResponse(
            {'items': list(Item.objects.values('id', 'name').distinct()),
             'spaces': list(Space.objects.values('id', 'item__name', 'item_id').distinct()),
             'users': list(User.objects.values('id', 'username').distinct()),
             'profile': list(Profile.objects.values('name', 'user_id', 'rut').distinct()),
             'reservations': list(Reserve.objects.values('item_id', 'user_id', 'start', 'finish').distinct())},
            safe=False)


def createtestdata(request):
    clients = createClient()
    halls = createHalls()
    reservations = createReservations(clients, halls)
    return JsonResponse({'result': 'successfully completed!'}, safe=False)
