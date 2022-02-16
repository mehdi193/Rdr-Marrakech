from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
import socket
# Create your views here.
from accueil.models import blog, blogTags, tags, Contact
from commerce.models import Categorie, Panier, assoc
import datetime

def home(request):

    cat = Categorie.objects.all()
    c=assoc.objects.filter(idU_id=request.session.get('user_id')).count()
    b = blog.objects.order_by('-id')[:6]
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
            return render(request, 'Accueil/home.html', {'cat': cat, 'k': o, 'blog': b})
        else:
            o = 0
            return render(request, 'Accueil/home.html', {'cat': cat,'k':o,'blog':b})
    else:
        o = 0
        return render(request, 'Accueil/home.html', {'cat': cat,'k':o,'blog':b})
    return render(request, 'Accueil/home.html', {'cat': cat,'count':c,'blog':b})
def contact(request):
    cat = Categorie.objects.values('id','nom')
    c=assoc.objects.filter(idU_id=request.session.get('user_id')).count()
    if request.method == 'POST':
        c=Contact.objects.create(contenu=request.POST.get('message'))
        c.save()
        message = "Message envoyé"




        return redirect('contact')
    if request.session.get('user_id') is  None:
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
                return render(request, 'Accueil/contact.html', {'cat': cat, 'k': o})
            else:
                o = 0
                return render(request, 'Accueil/contact.html', {'cat': cat, 'k': o})
        else:
            o = 0
            return render(request, 'Accueil/contact.html', {'cat': cat, 'k': o})


    return render(request, 'Accueil/contact.html', {'cat': cat,'count':c})
def header(request):
    cat = Categorie.objects.all()
    if request.method=='POST':
        return redirect('allproduit')
    return render(request,'header.html',{'cat':cat})

def singleBlog(request,pk):
    b=blog.objects.get(id=pk)
    bt=blogTags.objects.select_related('idB', 'idT').filter(idB=pk)
    t=tags.objects.filter(idT__in=bt.filter(idB=pk))
    last_b = blog.objects.order_by('-id')[:3]
    best = blog.objects.order_by('-id')[:1]
    last_t = tags.objects.order_by('-id')[:5]
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
                return render(request, 'Accueil/singleBlog.html',
                              {'cat': cat, 'b': b, 'bt': t, 'last': last_b, 'lates_t': last_t, 'best': best,
                               'k': o})

            else:
                o = 0
                return render(request, 'Accueil/singleBlog.html',
                              {'cat': cat, 'b': b, 'bt': t, 'last': last_b, 'lates_t': last_t, 'best': best,
                               'k': o})

        else:
            o = 0
            return render(request, 'Accueil/singleBlog.html',
                          {'cat': cat, 'b': b, 'bt': t, 'last': last_b, 'lates_t': last_t, 'best': best, 'k': o})

    return render(request,'Accueil/singleBlog.html',{'cat':cat,'b':b,'bt':t,'last':last_b,'lates_t':last_t,'best':best,'count':c})


def blogs(request):
    b=blog.objects.all()
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
                return  render(request,'Accueil/blogs.html',{'blog':b,'cat':cat,'k':o})

            else:
                o = 0
                return render(request, 'Accueil/blogs.html', {'blog': b, 'cat': cat, 'k': o})

        else:
            o = 0
            return render(request, 'Accueil/blogs.html', {'blog': b, 'cat': cat, 'k': o})

    return  render(request,'Accueil/blogs.html',{'blog':b,'cat':cat,'count':c})
def btags(request,pk):


    bt=blogTags.objects.select_related('idB', 'idT').filter(idT_id=pk)
    b=blog.objects.filter(idB__in=bt.filter(idT=pk))
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
                return render(request, 'Accueil/tags.html', {'b': b, 'cat': cat, 'k': o})

            else:
                o = 0
                return render(request, 'Accueil/tags.html', {'b': b, 'cat': cat, 'k': o})

        else:
            o = 0
            return render(request, 'Accueil/tags.html', {'b': b, 'cat': cat, 'k': o})

    return render(request,'Accueil/tags.html',{'b':b,'cat':cat,'count':c})