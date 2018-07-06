# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Object, Space


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
