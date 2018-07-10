# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Object, Space, Reserve
from django.utils.dateparse import parse_datetime


def index(request):
    context = {}
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))


def objects(request):
    made_search = False
    # nombre
    search_terms = request.GET.get('search_terms')
    if search_terms is None or search_terms == '':
        items = Object.objects.all()
    else:
        items = Object.objects.filter(name__icontains=search_terms)
        made_search = True
    # id
    item_id = request.GET.get('id')
    if item_id is None or item_id == '':
        pass
    else:
        items = items.filter(id=item_id)
        made_search = True
    #estado
    estado = request.GET.get('estado')
    if estado is None or estado not in ['d', 'p', 'r', 'l']:
        pass
    else:
        items = items.filter(condition=estado)
        made_search = True
    #tiempo

    fin = request.GET.get('fin')
    ini = request.GET.get('ini')
    try:
        datetime_fin = parse_datetime(fin)
        datetime_ini = parse_datetime(ini)
    except ValueError:
        datetime_fin = None
        datetime_ini = None
    except TypeError:
        datetime_fin = None
        datetime_ini = None
    if datetime_ini is None or datetime_fin is None or (datetime_fin < datetime_ini):
        pass
    else:
        made_search = True
        reservas_dentro_del_rango = Reserve.objects.all()
        reservas_dentro_del_rango = reservas_dentro_del_rango.filter(start__range=[datetime_ini, datetime_fin]).filter(finish__range=[datetime_ini, datetime_fin])
        reservas_dentro_del_rango_por_fuera = Reserve.objects.all()
        reservas_dentro_del_rango_por_fuera = reservas_dentro_del_rango_por_fuera.filter(start__lt=datetime_ini).filter(finish__gt=datetime_fin)
        reservas_dentro_del_rango.values()

    context = {
        'search_terms': search_terms,
        'item_state' : estado,
        'item_id': item_id,
        'made_search': made_search,
        'items': items,
        'objects_style': 'btn-success',
        'spaces_style': 'btn-secondary',
    }
    template = loader.get_template('item_display.html')
    return HttpResponse(template.render(context, request))


def spaces(request):
    items = Space.objects.all()
    context = {
        'items': items,
        'objects_style': 'btn-secondary',
        'spaces_style': 'btn-success',
    }
    template = loader.get_template('item_display.html')

    return HttpResponse(template.render(context, request))
