# from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Object, Space


def index(request):
    objects = Object.objects.all()
    spaces = Space.objects.all()
    context = {
        'objects': objects,
        'spaces': spaces,
    }
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))


def objects(request):
    objects = Object.objects.all()
    context = {
        'objects': objects,
    }
    template = loader.get_template('objects.html')

    return HttpResponse(template.render(context, request))


def spaces(request):
    spaces = Space.objects.all()
    context = {
        'spaces': spaces,
    }
    template = loader.get_template('spaces.html')

    return HttpResponse(template.render(context, request))
