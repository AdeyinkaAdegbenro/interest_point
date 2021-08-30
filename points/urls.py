from django.urls import path

from . import views

urlpatterns = [
    path('share', views.share, name="share"),
    path('users', views.users, name="users"),
    path('index', views.index, name='index'),
    path('', views.home, name='home'),
]