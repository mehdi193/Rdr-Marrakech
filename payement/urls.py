from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [

    path('payement_complete',views.payement_complete, name="payement_complete"),
    path('delivery',views.delivery, name="delivery"),
    path('thank',views.thank, name="thank"),
    path('donation',views.donation, name="donation")

]
