from django.urls import path

from . import views

urlpatterns = [
    # long
    path('login', views.handleLogin, name='handleLogin'),
    path('logout', views.handleLogout, name='handleLogout'),
    path('register', views.handleRegister, name='handleRegister'),
    # helping urls
    path('testdata', views.testdata, name='testdata'),
    path('createtestdata', views.createtestdata, name='createtestdata')
]