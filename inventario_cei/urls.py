from django.urls import path

from . import views

urlpatterns = [
    # long
    path('login', views.login, name='login'),
    # helping urls
    path('testdata', views.testdata, name='testdata'),
    path('createtestdata', views.createtestdata, name='createtestdata')
]