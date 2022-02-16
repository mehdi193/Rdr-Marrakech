from django.contrib import admin
from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/',views.login,name="log"),
    path('register/',views.reg, name="inscription" ),
    path('logout/',views.logout , name="logout"),
    path('espace/',views.espace, name="espace"),
    path('password_change/',views.change_password, name="password_change"),

]
