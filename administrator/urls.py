from django.urls import path

from . import views

urlpatterns = [
    # single menu
    path('', views.index, name='index'),
    path('2', views.index_beta, name='index_beta'), # Esta fue creada para visualizar el header y nada mas. Debe ser eliminada luego del testing.
]