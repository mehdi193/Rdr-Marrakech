from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [

    path('home/',views.home,name="home"),
    path('blogs/',views.blogs,name="blogs"),
    path('contact/',views.contact,name="contact"),
    path('singleBlog/<str:pk>',views.singleBlog,name="singleBlog"),
    path('tags/<str:pk>',views.btags,name="tags"),

]
