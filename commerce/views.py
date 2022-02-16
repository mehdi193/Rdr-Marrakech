from contextvars import Context

from django import template



from django.db.models import Count, Q, F
from django.shortcuts import render, redirect
from commerce.models import *
from django.http import JsonResponse
from django.views.generic import View


# Create your views here.



def showCat(request):
    cat = Categorie.objects.all()
    return render(request, 'register.html', {'cat': cat})


def single(request, pk):
    cat = Categorie.objects.all()
    pr = Produit.objects.get(id=pk)
    b = False
    if request.session.get('user_id') is not None:
        c = assoc.objects.filter(idU_id=request.session.get('user_id')).count()
        if request.method == 'POST':
            if request.POST.get('qte') == None:
                return render(request, 'commerce/single.html', {'pr': pr,'count':c})

            try:

                if assoc.objects.get(Q(idP_id=pk) & Q(idU_id=request.session.get('user_id'))):
                    p = assoc.objects.get(Q(idP_id=pk) & Q(idU_id=request.session.get('user_id')))
                    pa = Panier.objects.get(id=p.idPa_id)
                    pa.qte +=int(request.POST.get('qte'))
                    pa.save()
                    b = True
                    return redirect('panierO')
            except:
                    pass

            if b == False:
                pa = Panier.objects.create(qte=request.POST.get('qte'))
                pa.save()
                a = assoc.objects.create(idP=Produit.objects.get(id=pk),
                                         idU=User.objects.get(id=request.session.get('user_id')),
                                         idPa=Panier.objects.get(id=pa.id))
                a.save()


                return redirect('panierO')
    else:

        if request.method == 'POST':
            if request.POST.get('qte') == None:
                return render(request, 'commerce/single.html', {'pr': pr,'cat':cat})
            if request.session.get('produit') is None:
                request.session['qte'] = request.POST.get('qte')
                request.session['produit'] = pk

            else:
                request.session['qte'] += ";" + (request.POST.get('qte'))
                request.session['produit'] += ";" + pk

            return redirect('allproduit')
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
                    return render(request, 'commerce/single.html', {'pr': pr, 'cat': cat, 'k': o})

                else:
                    o = 0
                    return render(request, 'commerce/single.html', {'pr': pr, 'cat': cat, 'k': o})

            else:
                o = 0
                return render(request, 'commerce/single.html', {'pr': pr, 'cat': cat, 'k': o})
    return render(request, 'commerce/single.html', {'pr': pr,'cat':cat,'count':c})


i = 0


def addCart(request, pk):
    b= False
    if request.session.get('user_id') is not None:

       try:

        if  assoc.objects.get(Q(idP_id=pk) & Q(idU_id=request.session.get('user_id'))):
         p=assoc.objects.get(Q(idP_id=pk) & Q(idU_id=request.session.get('user_id')))
         pa=Panier.objects.get(id=p.idPa_id)
         pa.qte+=1
         pa.save()
         b=True
       except:
        pass

        if b == False:
         pa = Panier.objects.create(qte=1)
         pa.save()
         a = assoc.objects.create(idP=Produit.objects.get(id=pk),
                                 idU=User.objects.get(id=request.session.get('user_id')),
                                 idPa=Panier.objects.get(id=pa.id))
         a.save()
        return redirect('allproduit')
    else:
        if request.session.get('produit') is None:
            request.session['qte'] = "1"
            request.session['produit'] = pk

        else:
            request.session['qte'] += ";" + "1"
            request.session['produit'] += ";" + pk

        return redirect('allproduit')

    return redirect('allproduit')

def wishlist(request, pk):

    if request.session.get('user_id') is not None:

         if not wish.objects.filter(idPr=pk, idUs= request.session.get('user_id')):
          wis = wish.objects.create(idPr_id=pk, idUs_id=request.session.get('user_id'))
          wis.save()
         else:
           w = wish.objects.filter(idUs_id=request.session.get('user_id'), idPr=pk)
           w.delete()

    return redirect('allproduit')





def allproduit(request):
    pr = Produit.objects.all()

    ca = (Produit.objects
           .values('idCat', 'idCat__nom')
           .annotate(dcount=Count('idCat'))
           .order_by()
           )
    cat = Categorie.objects.all()

    w = wish.objects.filter(idUs_id=request.session.get('user_id'))

    best = Commande_Produit_User.objects.values('idProduit_id').annotate(
        total=Count('idProduit_id')).order_by('total').last()
    produit= Produit.objects.get(id=best.get('idProduit_id'))
    c=assoc.objects.filter(idU_id=request.session.get('user_id')).count()



    if request.method == 'POST':
        min = int(request.POST.get('min'))
        max = int(request.POST.get('max'))
        p = Produit.objects.filter(Q(prix__lte=max) & Q(prix__gte=min))

        return render(request, 'commerce/produit.html', {'pr': p, 'cat': cat,'ca':ca, 'w': w,'best': produit,'count':c})
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
                return render(request, 'commerce/produit.html',
                              {'pr': pr, 'cat': cat, 'ca': ca, 'w': w, 'best': produit, 'k': o})

            else:
                o = 0
                return render(request, 'commerce/produit.html',
                              {'pr': pr, 'cat': cat, 'ca': ca, 'w': w, 'best': produit, 'k': o})


        else:
            o = 0
            return render(request, 'commerce/produit.html',
                          {'pr': pr, 'cat': cat, 'ca': ca, 'w': w, 'best': produit, 'k': o})

    return render(request, 'commerce/produit.html', {'pr': pr, 'cat': cat,'ca':ca,'w':w,'best': produit,'count':c})


def categorie(request, pk):
    ca = Categorie.objects.get(id=pk)
    cat = Categorie.objects.all()
    c = (Produit.objects
         .values('idCat', 'idCat__nom')
         .annotate(dcount=Count('idCat'))
         .order_by()
         )
    co= assoc.objects.filter(idU_id=request.session.get('user_id')).count()
    pr = Produit.objects.filter(idCat=ca.id)
    best = Commande_Produit_User.objects.values('idProduit_id').annotate(
        total=Count('idProduit_id')).order_by('total').last()
    produit = Produit.objects.get(id=best.get('idProduit_id'))
    if request.method == 'POST':
        min = int(request.POST.get('min'))
        max = int(request.POST.get('max'))
        p = Produit.objects.filter(Q(prix__lte=max) & Q(prix__gte=min))

        return render(request, 'commerce/produit.html', {'pr': p, 'ca': c,'cat':cat,'best':produit,'count':c})
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
                return render(request, 'commerce/categorie.html', {'k':o,'pr': pr, 'ca': c,'cat':cat,'best':produit})

            else:
                o = 0
                return render(request, 'commerce/categorie.html', {'k':o,'pr': pr, 'ca': c, 'cat': cat, 'best': produit})


        else:
            o = 0
            return render(request, 'commerce/categorie.html', {'k':o,'pr': pr, 'ca': c,'cat':cat,'best':produit})
    return render(request, 'commerce/categorie.html', {'count':co,'pr': pr, 'ca': c,'cat':cat,'best':produit})


def panierO(request):
    cat = Categorie.objects.all()
    c = assoc.objects.filter(idU_id=request.session.get('user_id')).count()
    if request.session.get('user_id') is not None:
        if request.method == 'POQT':
            m = request.POST.get('m')
            Panier.objects.update(qte=m)
            return redirect('panierO')
        pubs = assoc.objects.select_related('idP', 'idPa', 'idU').filter(idU_id=request.session.get('user_id'))
        total = 0
        for a in pubs:
            total += a.idP.prix * a.idPa.qte
        return render(request, 'commerce/panier.html', {'pr': pubs, 'total': total,'cat':cat,'count':c})
    else:
        if request.session.get('user_id') is None:
            if request.session.get('produit') is not None:
                prod = request.session['produit']
                qt = request.session['qte']
                listQ = []
                list = []
                x = 0
                while x < len(prod):

                    if prod[x] != ";":
                        i = prod[x]
                        list.append(int(i))

                    x += 1
                x = 0
                while x < len(qt):
                    if qt[x] != ";":
                        a = qt[x]
                        listQ.append(int(a))

                    x += 1
                x = 0

                while x <= len(list):
                    cmp = x + 1
                    while cmp < len(list):
                        if list[x] == list[cmp]:
                            listQ[x] += listQ[cmp]
                            listQ.pop(cmp)
                            list.pop(cmp)
                            cmp = x

                        cmp += 1
                    x += 1

                produit = Produit.objects.filter(id__in=list)
                tot = 0
                x=0

                k = len(list)
                if k == "":
                    k=0
                for a in produit :
                    tot += a.prix * listQ[x]
                    x+=1
                c = ({
                    'zipped': zip(produit, listQ),
                    'total': tot,
                    'list': list,
                    'listQ': listQ,
                    'cat': cat,
                    'k': k
                })
                return render(request, 'commerce/panier.html', c)
            else:
                o = 0
                return render(request, 'commerce/panier.html', {'cat': cat,'k':o})

    return render(request, 'commerce/panier.html',{'cat':cat,'count':c})


def deletP(request, pk):
    if request.session.get('user_id') is not None:
        op = assoc.objects.get(id=pk)
        pan = Panier.objects.get(id=op.idPa_id)
        op.delete()
        pan.delete()

    else:
        prod = request.session['produit']
        qt = request.session['qte']
        x = 0
        while x < len(request.session['produit']):
            cmp = x + 1
            while cmp <= len(prod):
                if prod[x] == pk:
                    prod = prod[:x] + prod[x + 2:]
                    qt = qt[:x] + qt[x + 2:]
                    cmp = x
                cmp += 1
            x += 1
            request.session['produit'] = prod
            request.session['qte'] = qt
    return redirect('panierO')


def updateP(request, pk):
    op = assoc.objects.get(id=pk)
    i = op.idPa_id
    pan = Panier.objects.get(id=i)
    pan.qte = request.POST.get('qte')
    pan.save()
    return redirect('panierO')


def commande(request):
    if request.session.get('user_id') is not None:
        co = assoc.objects.filter(idU_id=request.session.get('user_id')).count()
        pubs = assoc.objects.select_related('idP', 'idPa', 'idU').filter(idU_id=request.session.get('user_id'))
        ca = (Produit.objects
               .values('idCat', 'idCat__nom')
               .annotate(dcount=Count('idCat'))
               .order_by()
               )
        cat = Categorie.objects.all()
        total = 0
        for a in pubs:
            total += a.idP.prix * a.idPa.qte
        if request.method== "POST":
            first = request.POST.get('fname')
            last = request.POST.get('lname')
            address = request.POST.get('address')
            region = request.POST.get('region')
            postal = request.POST.get('postal')
            phone = request.POST.get('phone')
            notes = request.POST.get('notes')
            com=Commande.objects.create(first=first,last=last,adresse=address,region=region,postal=postal,
                                        phone=phone,notes=notes,
                                        montant=total)
            com.save()
            for a in pubs:
             c=Commande_Produit_User(idCommande_id=com.id,idProduit=a.idP,idUser_id=request.session.get('user_id'),
                                     qte=a.idPa.qte)
             c.save()
            return redirect('payement')


        return render(request, 'commerce/commande.html', {'pr': pubs, 'total': total,'cat':cat, 'ca':ca,'count':co})
    return redirect('log')


def payement(request):
    if request.session.get('user_id') is not None:
        pubs = assoc.objects.select_related('idP', 'idPa', 'idU').filter(idU_id=request.session.get('user_id'))
        total = 0
        ca = (Produit.objects
               .values('idCat', 'idCat__nom')
               .annotate(dcount=Count('idCat'))
               .order_by()
               )
        cat= Categorie.objects.all()
        for a in pubs:
            total += a.idP.prix * a.idPa.qte
        obj = Commande_Produit_User.objects.select_related('idCommande', 'idProduit', 'idUser').filter(
            idUser=request.session.get('user_id')).order_by('-idCommande')[0]
        c = assoc.objects.filter(idU_id=request.session.get('user_id')).count()
        cat = Categorie.objects.all()
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
                return render(request, 'payement/payement.html',
                              {'total': total, 'objet': pubs, 'com': obj, 'cat': cat, 'ca': ca,'k':o})

            else:
                o = 0
                return render(request, 'payement/payement.html',
                              {'total': total, 'objet': pubs, 'com': obj, 'cat': cat, 'ca': ca,'k':o})

        return render(request, 'payement/payement.html', {'total':total, 'objet':pubs, 'com':obj,'cat':cat
            ,'ca':ca,'count':c})
    return redirect('log')
