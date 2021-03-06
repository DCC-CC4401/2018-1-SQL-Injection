from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from inventario_cei.models import Reserve, Space


def index(request):
    if request.user.is_authenticated:
        space = Space.objects.all()
        list = Reserve.objects.filter(item__space__in=space).select_related()
        context = {
            'list': list.filter(user=request.user).order_by('-start')[0:10]
        }
        template = loader.get_template('userprofile/index.html')
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/cei/login')


def delete(request):
    if request.method == 'POST':
        l_id = request.POST.getlist('l_id')
        for i in l_id:
            Reserve.objects.filter(id=i).delete()
        return redirect('/userprofile')
    else:
        return render(request, 'userprofile/index.html')
