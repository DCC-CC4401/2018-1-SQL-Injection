from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import datetime

from inventario_cei.models import Object
from inventario_cei.models import Space
from inventario_cei.models import Reserve

from django.contrib.auth.models import User, Group

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/cei/login')

    if not (request.user.groups.values_list('name',flat=True).first() == 'administrator_group'):
        return HttpResponseRedirect('/cei/login')
    
    rooms = [MockSala(), MockSala(), MockSala(), MockSala()]

    # all week reserves
    today = datetime.date.today()
    start_week = today - datetime.timedelta(today.weekday())
    end_week = start_week + datetime.timedelta(7)
    # weekReserves = Space.objects.filter(item__reserve__start__range=[start_week, end_week]).values(
    #     'item__reserve__id', 'item__reserve__user__profile__name','item__reserve__user__profile__rut','item__name', 'item__description','item__reserve__start','item__reserve__finish').order_by('-item__reserve__created')

    weekReserves = Space.objects.values(
         'item__reserve__id', 'item__reserve__user__email', 'item__reserve__user__profile__name', 'item__reserve__user__profile__rut', 'item__name',
         'item__description', 'item__reserve__start', 'item__reserve__finish', 'item__reserve__state').order_by('-item__reserve__created')

    # weekReserves = Space.objects.order_by('-item__reserve__created')

    # Pending reserves
    pendingHeaders = ['Id', 'Usuario', 'Articulo', 'Fecha de prestamo', 'Fecha de solicitud']
    pending = Object.objects.filter(item__reserve__state='p').values(
        'item__reserve__id', 'item__reserve__user__username', 'item__name', 'item__reserve__start',
        'item__reserve__finish').order_by('-item__reserve__created')

    # Lending
    lendingHeaders = ['Id', 'Usuario', 'Articulo', 'Fecha de prestamo', 'Fecha de solicitud']
    lendings = Object.objects.filter(item__reserve__state='a').values(
        'item__reserve__id', 'item__reserve__user__username', 'item__name', 'item__reserve__start',
        'item__reserve__finish', 'condition').order_by('-item__reserve__updated')

    context = { 
                'user_group' : request.user.groups.values_list('name',flat=True).first(),
                'weekReserves':weekReserves,
                'pendingHeaders': pendingHeaders,
                'pendings': list(pending),
                'lendingHeaders': lendingHeaders,
                'lendings': list(lendings),
                'rooms': rooms,
            }
    template = loader.get_template('administrator/index.html')
    return HttpResponse(template.render(context, request))


# this method handles only post requests
# changes the 'state' of Reserves
def post_pending(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/administrator')

    selectedIds = request.POST.getlist('pre-selected')
    if len(selectedIds) == 0:
        return HttpResponseRedirect('/administrator')

    resvs = Reserve.objects.filter(pk__in=selectedIds)
    if 'accept' in request.POST:
        for r in resvs:
            r.state = 'a'
            r.save()
    elif 'negate' in request.POST:
        for r in resvs:
            r.state = 'r'
            r.save()

    return HttpResponseRedirect('/administrator')


# TODO: define behavior
def post_lending(request):
    return HttpResponseRedirect('/administrator')


class MockSala:
    id = 1
    name = 'Sala #'
