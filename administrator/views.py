from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


from inventario_cei.models import Reserve

def index(request):
    pendingHeaders = ['id', 'usuario', 'space','Fecha Pres', 'Fecha Sol']
    pending = Reserve.objects.values('user','space','start','finish','id').distinct()

    salas = [MockSala(), MockSala(), MockSala(), MockSala()]

    context = {'message' : "Hello world!",
                'orderHeaders': pendingHeaders,
                'pendingHeaders': pendingHeaders,
                'orders': pending,
                'pending': pending,
                'salas': salas,
            }
    template = loader.get_template('administrator/index.html')
    
    return HttpResponse(template.render(context, request))


# Esta fue creada para visualizar el header y nada mas. Debe ser eliminada luego del testing.
def index_beta(request):
    # return HttpResponse("Hello, world. You're at the polls index.")

    headers = ['id', 'Usuario', 'Fecha Pres', 'Fecha Sol']
    
    pending = Reserve.objects.all()
    for a in pending:
        a.user
        a.space
    articles = [MockSala(), MockSala(), MockSala(), MockSala()]

    context = {'message': "Hello world!",
               'orderHeaders': headers,
               'pendingHeaders': headers,
               'orders': articles,
               'pending': pending,
               'salas': salas,
               }
    template = loader.get_template('base2.html')

    return HttpResponse(template.render(context, request))


class MockData():
    id = 1
    article = 'Article 1'
    lendingDate = '27/12/2018'
    returnDate = '27/12/2019'

class MockSala():
    id = 1
    name = 'Sala #'
