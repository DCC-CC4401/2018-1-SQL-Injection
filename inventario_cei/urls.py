from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='home'),
    path('espacios', views.spaces, name='espacios'),

    # long
    path('login', views.handleLogin, name='handleLogin'),
    path('logout', views.handleLogout, name='handleLogout'),
    path('register', views.handleRegister, name='handleRegister'),

    # helping urls
    path('testdata', views.testdata, name='testdata'),
    path('createtestdata', views.createtestdata, name='createtestdata'),
    re_path(r'^objetos/$', views.objects, name='search_item')
]
