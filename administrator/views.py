from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    
    headers = ['id', 'Usuario', 'Fecha Pres','Fecha Sol']
    articles = [MockData(), MockData()]

    salas = [MockSala(), MockSala(), MockSala(), MockSala()]

    context = {'message' : "Hello world!",
                'orderHeaders': headers,
                'pendingHeaders': headers,
                'orders': articles,
                'pending': articles,
                'salas': salas,
            } 
    template = loader.get_template('administrator/index.html')
    
    return HttpResponse(template.render(context, request))


class MockData():
    id = 1
    article = 'Article 1'
    lendingDate = '27/12/2018'
    returnDate = '27/12/2019'

class MockSala():
    id = 1
    name = 'Sala #'
