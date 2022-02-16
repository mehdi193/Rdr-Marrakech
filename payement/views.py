import json

from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

from django.conf import settings

from commerce.models import Commande, Commande_Produit_User, Panier, assoc, Categorie


def payement_complete(request):
   if request.session.get('user_id') is not None:
        header=json.loads(request.body)


        obj = Commande_Produit_User.objects.select_related('idCommande', 'idProduit', 'idUser').filter(
            idUser=request.session.get('user_id')).order_by('-idCommande')[0]

        Com = Commande.objects.filter(idCommande__idCommande=obj.idCommande)
        Com.trans = header['payID']
        Com.statusT = header['status']
        for object in Com:
            object.trans = header['payID']
            object.statusT = header['status']
            object.type= "En ligne"
            object.save()
        op = assoc.objects.select_related('idP', 'idPa', 'idU').filter(idU=request.session.get('user_id'))
        for o in op:
            pan = Panier.objects.filter(idPa__idPa=o.idPa)
            pan.delete()
        op.delete()


        return redirect('thank')
   else:
       return redirect('home')

def delivery(request):
   if request.session.get('user_id') is not None:
        obj = Commande_Produit_User.objects.select_related('idCommande', 'idProduit', 'idUser').filter(
            idUser=request.session.get('user_id')).order_by('-idCommande')[0]

        Com = Commande.objects.filter(idCommande__idCommande=obj.idCommande)

        for object in Com:
            object.type= "En livraison"
            object.save()
        op = assoc.objects.select_related('idP', 'idPa', 'idU').filter(idU=request.session.get('user_id'))
        for o in op:
            pan = Panier.objects.filter(idPa__idPa=o.idPa)
            pan.delete()
        op.delete()


        return redirect('thank')
   else:
       return redirect('home')
def thank(request):
   if request.session.get('user_id') is not None:
    c = assoc.objects.filter(idU_id=request.session.get('user_id')).count()
    cat = Categorie.objects.all()
    return render(request,'payement/thank.html',{'cat':cat,'count':c})
   return redirect('log')
def donation(request):
    c = assoc.objects.filter(idU_id=request.session.get('user_id')).count()
    cat = Categorie.objects.all()
    if request.session.get('user_id') is None:
        if request.session.get('produit') is not None:
            prod = request.session['produit']

            list = []
            x = 0
            while x < len(prod):

                if prod[x] != ";":
                    i = prod[x]
                    list.append(int(i))

                x += 1
            x = 0
            while x <= len(list):
                cmp = x + 1
                while cmp < len(list):
                    if list[x] == list[cmp]:
                        list.pop(cmp)
                        cmp = x

                    cmp += 1
                x += 1
            o = len(list)
            print(o)
            if o != "":
                return render(request, 'payement/donation.html', {'cat': cat, 'k': o})

            else:
                o = 0
                return render(request, 'payement/donation.html', {'cat': cat, 'k': o})


        else:
            o = 0
            return render(request, 'payement/donation.html', {'cat': cat, 'k': o})
    return render(request,'payement/donation.html',{'cat':cat,'count':c})