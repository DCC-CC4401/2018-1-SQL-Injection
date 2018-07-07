from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


from inventario_cei.models import Reserve

def index(request):
    pendingHeaders = ['Id', 'Articulo', 'Usuario', 'Fecha de prestamo', 'Fecha de solicitud']
    pending = Reserve.objects.all().values() 
    salas = [MockSala(), MockSala(), MockSala(), MockSala()]

    pending = Reserve.objects.values_list('id', 'user__username','space__name','start','finish').distinct()
    context = {'message' : "Hello world!",
                'orderHeaders': pendingHeaders,
                'pendingHeaders': pendingHeaders,
                'orders': list(map(list, pending)),
                'pending': list(map(list, pending)),
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
