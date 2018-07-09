# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Object, Space


def index(request):
    context = {}
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))


def objects(request):
    made_search = False

    search_terms = request.GET.get('search_terms')
    if search_terms is None:
        items = Object.objects.all()
    else:
        items = Object.objects.filter(name__icontains=search_terms)
        made_search = True

    item_id = request.GET.get('id')
    if item_id == '':
        pass
    else:
        items = items.filter(id=item_id)
        made_search = True

    estado = request.GET.get('estado')
    if estado == 't':
        pass
    else:
        items = items.filter(condition=estado)

    context = {
        'search_terms': search_terms,
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
