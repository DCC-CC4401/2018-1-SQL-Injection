from django.urls import path,re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='home'),
    path('objetos', views.objects, name='objetos'),
    path('espacios', views.spaces, name='espacios'),
    re_path(r'^searchItem/$',views.search_item, name='search_item')
]