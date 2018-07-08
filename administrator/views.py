from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


from inventario_cei.models import Reserve

def index(request):
    
    rooms = [MockSala(), MockSala(), MockSala(), MockSala()]

    # Pending reserves
    pendingHeaders = ['Id', 'Articulo', 'Usuario', 'Fecha de prestamo', 'Fecha de solicitud']
    pending = Reserve.objects.filter(state='p').values_list(
        'id', 'user__username','space__name','start','finish').order_by('-created')
    
    # Lending
    lendingHeaders = ['Id', 'Articulo', 'Usuario', 'Fecha de prestamo', 'Fecha de solicitud']
    lendings = Reserve.objects.filter(state='a').values_list(
        'id', 'user__username','space__name','start','finish').order_by('-updated')

    context = {'message' : "Hello world!",
                'pendingHeaders': pendingHeaders,
                'pending': list(map(list, pending)),
                'lendingHeaders': lendingHeaders,
                'lendings': list(map(list, lendings)),
                'rooms': rooms,
            }
    template = loader.get_template('administrator/index.html')
    
    return HttpResponse(template.render(context, request))

def postPending(request):
    if request.method != 'POST':
        return HttpResponseRedirect('/administrator')

    selectedIds = request.POST.getlist('pre-selected')
    
    if len(selectedIds) == 0:
        return HttpResponseRedirect('/administrator')
    resvs = Reserve.objects.filter(pk__in=selectedIds)
    if 'accept' in request.POST : 
        for r in resvs:
            r.state = 'a'
            r.save()
    elif 'negate' in request.POST : 
        for r in resvs:
            r.state = 'r'
            r.save()
    
    return HttpResponseRedirect('/administrator')

def postPendingR(request):
    prod = Product()
    try: 
        # pjson = json.loads(request.body)
        # form = ProductForm(request.POST)
        if request.method != 'POST':
            return HttpResponseRedirect('/products')

        id = request.POST.get("id", 0)
        prod = Product.objects.get(pk=id)
            
        if 'rmv' in request.POST : 
            prod.delete()
        elif  'dec' in request.POST :  
            if ( prod.quantity == 0 ): 
                return HttpResponseRedirect('/products')
            prod.quantity = prod.quantity - 1
            prod.full_clean()
            prod.save()
        elif  'inc' in request.POST :  
            prod.full_clean()
            prod.quantity = prod.quantity + 1
            prod.save()
        else:
            return HttpResponseRedirect('/products')
    except Product.DoesNotExist:
        # raise Http404()
        return HttpResponseRedirect('/products')

    return HttpResponseRedirect('/products')

class MockSala():
    id = 1
    name = 'Sala #'
