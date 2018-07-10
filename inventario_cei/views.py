from django.template import loader
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


from datetime import datetime
import datetime

from inventario_cei.models import Object, Space

from .testdata import createClient, createReservations, createObjects


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
