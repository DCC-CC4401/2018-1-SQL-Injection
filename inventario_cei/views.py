from django.template import loader
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .models import Object, Space, Reserve, Item
from django.utils.dateparse import parse_datetime
from datetime import datetime
import datetime


from django.contrib.auth.models import User, Group

from inventario_cei.models import Object, Space

from .testdata import createClient,createHalls,createReservations,createObjects


def index(request):
    context = {}
    template = loader.get_template('index.html')

    return HttpResponse(template.render(context, request))


def objects(request):
    made_search = False
    # nombre
    search_terms = request.GET.get('search_terms')
    if search_terms is None or search_terms == '':
        items = Object.objects.all()
    else:
        items = Object.objects.filter(item__name__icontains=search_terms)
        made_search = True
    # id
    item_id = request.GET.get('id')
    if item_id is None or item_id == '':
        pass
    else:
        items = items.filter(id=item_id)
        made_search = True
    # estado
    estado = request.GET.get('estado')
    if estado is None or estado not in ['d', 'p', 'r', 'l']:
        pass
    else:
        items = items.filter(condition=estado)
        made_search = True
    # tiempo

    fin = request.GET.get('fin')
    ini = request.GET.get('ini')
    try:
        datetime_fin = parse_datetime(fin)
        datetime_ini = parse_datetime(ini)
    except ValueError:
        datetime_fin = None
        datetime_ini = None
    except TypeError:
        datetime_fin = None
        datetime_ini = None
    if datetime_ini is None or datetime_fin is None or (datetime_fin < datetime_ini):
        pass
    else:
        made_search = True
        reservas_dentro_del_rango = Reserve.objects.all()
        reservas_dentro_del_rango = reservas_dentro_del_rango.filter(start__range=[datetime_ini, datetime_fin]).filter(
            finish__range=[datetime_ini, datetime_fin])
        reservas_dentro_del_rango_por_fuera = Reserve.objects.all()
        reservas_dentro_del_rango_por_fuera = reservas_dentro_del_rango_por_fuera.filter(start__lt=datetime_ini).filter(
            finish__gt=datetime_fin)
        reservas_dentro_del_rango.values()


    context = {
        'search_terms': search_terms,
        'item_state': estado,
        'item_id': item_id,
        'made_search': made_search,
        'items': items,
        'objects_style': 'btn-success',
        'spaces_style': 'btn-secondary',
    }
    template = loader.get_template('item_display.html')
    return HttpResponse(template.render(context, request))


def spaces(request):
    rooms = [MockSala(), MockSala(), MockSala(), MockSala()]

    # all week reserves
    today = datetime.date.today()
    start_week = today - datetime.timedelta(today.weekday())
    end_week = start_week + datetime.timedelta(7)
    # weekReserves = Space.objects.filter(item__reserve__start__range=[start_week, end_week]).values(
    #     'item__reserve__id', 'item__reserve__user__profile__name','item__reserve__user__profile__rut','item__name', 'item__description','item__reserve__start','item__reserve__finish').order_by('-item__reserve__created')

    weekReserves = Space.objects.values(
        'item__reserve__id', 'item__reserve__user__profile__name', 'item__reserve__user__profile__rut', 'item__name',
        'item__description', 'item__reserve__start', 'item__reserve__finish').order_by('-item__reserve__created')

    # Pending reserves
    pendingHeaders = ['Id', 'Usuario', 'Articulo', 'Fecha de prestamo', 'Fecha de solicitud']
    pending = Object.objects.filter(item__reserve__state='p').values(
        'item__reserve__id', 'item__reserve__user__username', 'item__name', 'item__reserve__start',
        'item__reserve__finish').order_by('-item__reserve__created')

    # Lending
    lendingHeaders = ['Id', 'Usuario', 'Articulo', 'Fecha de prestamo', 'Fecha de solicitud']
    lendings = Object.objects.filter(item__reserve__state='a').values(
        'item__reserve__id', 'item__reserve__user__username', 'item__name', 'item__reserve__start',
        'item__reserve__finish', 'condition').order_by('-item__reserve__updated')

    context = {'message': "Hello world!",
               'weekReserves': weekReserves,
               'pendingHeaders': pendingHeaders,
               'pendings': list(pending),
               'lendingHeaders': lendingHeaders,
               'lendings': list(lendings),
               'rooms': rooms,
               'objects_style': 'btn-secondary',
               'spaces_style': 'btn-success'
               }
    template = loader.get_template('calendar_user.html')
    return HttpResponse(template.render(context, request))


def article_sheet(request):
    if request.method == 'POST':
        article_id = request.POST.get('article_id')
        article_type_style = request.POST.get('article_type_style')
        if article_type_style:
            article_is_object = "success" in article_type_style
        else:
            article_is_object = "object" in request.POST.get('article_type')

        if article_is_object:
            article = Object.objects.get(id=article_id)

        else:
            article = Space.objects.get(id=article_id)

        reserves_history = None

        context = {
            'article': article,
            'reserves_history': reserves_history,
        }

        template = loader.get_template('article_sheet.html')
        return HttpResponse(template.render(context, request))


# register 
def handleRegister(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/userprofile')

    context = {}
    if request.method == 'GET':
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context, request))

    if request.method != 'POST':
        return HttpResponseRedirect('/cei/register')

    name = request.POST['name']
    rut = request.POST['rut']
    email = request.POST['email']
    password = request.POST['password']
    re_password = request.POST['re_password']

    if password != re_password: 
        context = {'error': 'Contrase&ntilde;as no coinciden'}
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context, request))


    if User.objects.filter(username=email).exists():
        context = {'error': 'Usuario "%s" ya existe' %email }
        template = loader.get_template('register.html')
        return HttpResponse(template.render(context, request))

    
    user, created = User.objects.get_or_create(
                            username=email,
                            email=email
                        )


    if created:
        profile = Profile()
        user.set_password(password)
        user.save()

        profile.user = user
        profile.name = name
        profile.rut = rut
        profile.mail = email
        profile.save()
        
        client_group, created = Group.objects.get_or_create(name='client_group')
        client_group.user_set.add(user)

        # success
        context = {'success': 'Usuario "%s" exitosamente registrado' %email }
        template = loader.get_template('register.html')

        return HttpResponse(template.render(context, request))

    else:
        # error
        context = {'error': 'Un error inesperado ha sucedido'}
        template = loader.get_template('register.html')

        return HttpResponse(template.render(context, request))


# login
def handleLogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/userprofile')

    context = {}
    if request.method == 'GET':
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context, request))

    if request.method != 'POST':
        return HttpResponseRedirect('/cei/login')

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/userprofile')
    else:
        context = {'error': 'Credenciales Invalidas'}
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context, request))
        
# logout
def handleLogout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/userprofile')
    
    logout(request)
    return HttpResponseRedirect('/cei/login')


# TODO: delete this method for production
# The next methods are created to test de data base
def testdata(request):
    today = datetime.date.today()
    start_week = today - datetime.timedelta(today.weekday())
    end_week = start_week + datetime.timedelta(7)
    return JsonResponse(
        {
            # 'items': list(Item.objects.values('id', 'name').distinct()),
            # 'spaces': list(Space.objects.values('id', 'item__name', 'item_id').distinct()),
            # 'users': list(User.objects.values('id', 'username').distinct()),
            # 'profile': list(Profile.objects.values('name', 'user_id', 'rut').distinct()),
            # 'reservations': list(Reserve.objects.values('item_id', 'user_id', 'start', 'finish').distinct())},

            'start_week': start_week,
            'end_week': end_week,
            'spaces': list(Space.objects.filter(item__reserve__start__range=[start_week, end_week]).values(
                'item__reserve__id',
                'item__reserve__user__username',
                'item__name',
                'item__reserve__start',
                'item__reserve__finish').order_by('-item__reserve__created')
                           ),
            'spaces_all': list(Space.objects.values('id', 'item__reserve__start').distinct()),
        },
        safe=False)


def createtestdata(request):
    clients = createClient()
    objects = createObjects()
    reservations = createReservations(clients, objects)
    return JsonResponse({'result': 'successfully completed!'}, safe=False)

class MockSala:
    id = 1
    name = 'Sala #'
