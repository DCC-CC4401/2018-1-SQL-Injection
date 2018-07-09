from django.urls import path
from . import views

urlpatterns = [
    # single menu
    path('delete/', views.delete, name='delete'),
    path('', views.index, name='index'),
    path('administrator/', views.administrator, name='administrator')
]
