from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [

    path('produit/',views.allproduit, name="allproduit"),
    path('categorie/<str:pk>',views.categorie,name="categorie"),
    path('panier/',views.panierO,name="panierO"),
    path('panier/',views.panierO,name="panierO"),
    path('panier/<str:pk>',views.deletP,name="dpanier"),
    path('wishlist/<str:pk>',views.wishlist,name="wishlist"),
    path('panier/<str:pk>',views.updateP,name="upanier"),
    path('single/<str:pk>',views.single,name="single"),
    path('addCart/<str:pk>',views.addCart,name="addCart"),
    path('commande',views.commande, name="commande"),
    path('payement',views.payement, name="payement"),


]
