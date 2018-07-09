from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from inventario_cei.models import Reserve


def index(request):
    list = Reserve.objects.all() # need to select acording to the user logged in
    context = {
        'list': list.order_by('-start')[0:10]
    }
    template = loader.get_template('userprofile/index.html')
    return HttpResponse(template.render(context, request))


def delete(request):
    if request.method == 'POST':
        l_id = request.POST.getlist('l_id')
        for i in l_id:
            Reserve.objects.filter(id=i).delete()
        return redirect('/userprofile')
    else:
        return render(request, 'userprofile/index.html')


def administrator(request):
    context = {'message': "Hello world!"}
    template = loader.get_template('administrator/index.html')
    return HttpResponse(template.render(context, request))