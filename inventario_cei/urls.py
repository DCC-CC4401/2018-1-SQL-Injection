from django.urls import path,re_path

from . import views

urlpatterns = [
    path('list', views.index, name='index'),
    path('index', views.index, name='home'),
    path('espacios', views.spaces, name='espacios'),
    re_path(r'^objetos/$',views.objects, name='search_item')
]