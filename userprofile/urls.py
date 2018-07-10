from django.urls import path, re_path
from . import views

urlpatterns = [
    # single menu
    path('delete/', views.delete, name='delete'),
    path('', views.index, name='index'),
]
