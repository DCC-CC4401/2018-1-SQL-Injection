from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


from inventario_cei.models import Reserve

def index(request):
    
    rooms = [MockSala(), MockSala(), MockSala(), MockSala()]

    # Pending reserves
    pendingHeaders = ['Id', 'Articulo', 'Usuario', 'Fecha de prestamo', 'Fecha de solicitud']
    pending = Reserve.objects.filter(state='p').values_list(
        'id', 'user__username','space__name','start','finish','state').order_by('-created')
    
    # Lending
    lendingHeaders = ['Id', 'Articulo', 'Usuario', 'Fecha de prestamo', 'Fecha de solicitud']
    lendings = Reserve.objects.filter(state='a').values_list(
        'id', 'user__username','space__name','start','finish','state').order_by('-created')

    context = {'message' : "Hello world!",
                'pendingHeaders': pendingHeaders,
                'pending': list(map(list, pending)),
                'lendingHeaders': lendingHeaders,
                'lendings': list(map(list, lendings)),
                'rooms': rooms,
            }
    template = loader.get_template('administrator/index.html')
    
    return HttpResponse(template.render(context, request))

class MockSala():
    id = 1
    name = 'Sala #'
