from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('postpending', views.post_pending, name='postPending'),
    path('postlending', views.post_lending, name='postLending'),
]