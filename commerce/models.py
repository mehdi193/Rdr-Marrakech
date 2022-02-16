from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Create your models here.



class Categorie(models.Model):
    nom=models.CharField(max_length=50, null= True)
    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    qte = models.IntegerField( null=True)
    prix = models.FloatField( null=True)
    image = models.CharField(max_length=500, null=True)
    idCat = models.ForeignKey(Categorie,  on_delete=models.CASCADE,related_name="idCat",null="True")
    def __str__(self):
        return self.nom


class Panier(models.Model):
    qte=models.IntegerField(null=True)

class assoc(models.Model):
    idP=models.ForeignKey(Produit, on_delete=models.CASCADE,related_name="idP",null="True")
    idPa = models.ForeignKey(Panier,  on_delete=models.CASCADE,related_name="idPa",null="True")
    idU = models.ForeignKey(User,  on_delete=models.CASCADE,related_name="idU",null="True")

class wish(models.Model):
    idPr=models.ForeignKey(Produit, on_delete=models.CASCADE,related_name="idPr",null="True")
    idUs = models.ForeignKey(User,  on_delete=models.CASCADE,related_name="idUs",null="True")


class Commande(models.Model):
    type=models.CharField(max_length=500, null=True)
    montant =models.FloatField( null=True)
    adresse = models.CharField(max_length= 150,null=True)
    region = models.CharField(max_length=50,null=True)
    postal= models.IntegerField(max_length=9,null=True)
    phone = models.IntegerField(max_length=10,null=True)
    first = models.CharField(max_length=20,null=True)
    last = models.CharField(max_length=20,null=True)
    notes = models.CharField(max_length=1000,null=True)
    trans = models.CharField(max_length=20,null=True)
    statusT = models.CharField(max_length=20,null=True)

class Commande_Produit_User(models.Model):
    idCommande=models.ForeignKey(Commande, on_delete=models.CASCADE,related_name="idCommande",null="True")
    idProduit=models.ForeignKey(Produit, on_delete=models.CASCADE,related_name="idProduit",null="True")
    idUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="idUser", null="True")
    qte = models.IntegerField(null=True)