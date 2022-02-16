from django.contrib import admin

# Register your models here.
from commerce.models import Commande_Produit_User, Commande, assoc, Panier, Produit, Categorie

admin.site.register(Commande_Produit_User)
admin.site.register(Commande)
admin.site.register(assoc)
admin.site.register(Panier)
admin.site.register(Produit)
admin.site.register(Categorie)