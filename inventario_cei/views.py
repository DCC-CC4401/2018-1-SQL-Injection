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