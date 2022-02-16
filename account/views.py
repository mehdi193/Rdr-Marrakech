import hashlib
from hashlib import md5

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import models
from django.contrib.auth import authenticate, login, logout
from account.forms import SignUpForm
from commerce.models import Produit, assoc, Panier, Commande_Produit_User, Categorie


def login(request):
    if request.session.get('user_id') is not None:
        return redirect('allproduit')
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if authenticate(username=username, password=password):
            user = User.objects.get(username=username)
            request.session['user_id'] = user.id
            auth.login(request,user)
            if user is  None:
                return render(request, 'login.html')
            else:
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

                    k=len(list)
                    for a in listQ:
                        p=Panier.objects.create(qte=a)
                        p.save()
                    p=Panier.objects.all().order_by('-id')[:len(listQ)][::-1]
                    x=0
                    for a in p:
                        q=assoc.objects.create(idU_id=request.session.get('user_id'),idP_id=list[x],idPa_id=a.id)
                        x+=1
                        q.save()

                    auth.logout(request)
                return redirect('home')

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
        return render(request, 'login.html',{'k':o})
    o=0
    return render(request, 'login.html',{'k':o})

def reg(request):
    form = SignUpForm(data=request.POST)
    if request.method=="POST":
        if form.is_valid():
           form.save()
           user=User.objects.get(username=form.data['username'])
           request.session['user_id'] = user.id
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

               k = len(list)
               for a in listQ:
                   p = Panier.objects.create(qte=a)
                   p.save()
               p = Panier.objects.all().order_by('-id')[:len(listQ)][::-1]
               x = 0
               for a in p:
                   q = assoc.objects.create(idU_id=request.session.get('user_id'), idP_id=list[x], idPa_id=a.id)
                   x += 1
                   q.save()

           return redirect('home')

    if request.session.get('user_id') is not None:
        return redirect('home')
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
        return render(request, 'register.html', {'form': form,'k': o})
    o = 0
    return render(request, 'register.html', {'form': form,'k': o})

def espace(request):
   if request.session.get('user_id') is not None:
    cat = Categorie.objects.all()
    u=User.objects.get(id=request.session.get('user_id'))
    c=Commande_Produit_User.objects.filter(idUser_id=request.session.get('user_id'))
    co = assoc.objects.filter(idU_id=request.session.get('user_id')).count()
    print(request.method)
    form = PasswordChangeForm(data=request.GET, user=request.user)
    if request.method== 'POST':
        u.first_name=request.POST.get('fname')
        u.last_name=request.POST.get('fname')
        u.email=request.POST.get('email')
        u.username=request.POST.get('pswd')
        u.save()

    elif request.method == 'GET':
        request.method=''
        form = PasswordChangeForm(data=request.GET, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

        else:
            return render(request, 'account/espace.html', {'u':u,'pr':c,'form':form,'cat':cat,'count':co})
    else:
        form = PasswordChangeForm(user=request.user)


    return render(request,'account/espace.html',{'u':u,'pr':c,'form':form,'cat':cat,'count':co})
   return redirect('log')


def change_password(request):
        return render(request,'account/password_change.html')
def logout(request):
    auth.logout(request)
    return redirect('log')