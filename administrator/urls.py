from django.urls import path

from . import views

urlpatterns = [
    # single menu
    path('', views.index, name='index'),
    path('postpending', views.postPending, name='postPending'),
]