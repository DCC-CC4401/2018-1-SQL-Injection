from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    context = {'message' : "Hello world!"} 
    template = loader.get_template('administrator/index.html')

    return HttpResponse(template.render(context, request))