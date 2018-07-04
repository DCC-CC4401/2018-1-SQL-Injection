from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='home'),
    path('objetos', views.objects, name='objetos'),
    path('espacios', views.spaces, name='espacios'),
]