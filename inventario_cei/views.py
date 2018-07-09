# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Object, Space


def index(request):
    context = {}
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))


def objects(request):
    search_terms = request.GET.get('search_terms')
    made_search = False
    if search_terms is None:
        items = Object.objects.all()
    else:
        items = Object.objects.filter(name__icontains=search_terms)
        made_search = True
    context = {
        'search_terms' : search_terms,
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
