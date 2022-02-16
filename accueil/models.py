from datetime import datetime

from django.db import models
from datetime import datetime, date
# Create your models here.
class blog(models.Model):
    text = models.TextField( null=True)
    image=models.ImageField()
    titre=models.CharField(max_length=500, null=True)
    date= models.CharField(max_length=10,null=True, default= date.today())
    def __str__(self):
        return self.text

class tags(models.Model):
    nom=models.CharField(max_length=50, null= True)
    def __str__(self):
        return self.nom

class blogTags(models.Model):
    idB=models.ForeignKey(blog, on_delete=models.CASCADE,related_name="idB",null="True")
    idT = models.ForeignKey(tags,  on_delete=models.CASCADE,related_name="idT",null="True")
class Contact(models.Model):
    contenu = models.TextField(null=True)