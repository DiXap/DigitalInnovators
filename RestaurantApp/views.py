from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from .models import Menu, Categories

# Create your views here.
def home(request):
    return render(request, 'home.html')

def table_init(request):
    if request.method == 'GET':
        return render(request, 'table_init.html', {
            'form': AuthenticationForm,
        })
    
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, 'table_init.html', {
                'form': AuthenticationForm,
                'error': 'Información incorrecta'
            })
        
        login(request, user)
        return redirect('menu')

def menu(request):
    # menu = Menu.objects.all()
    categories = Categories.objects.values('name')
    # print(menu)
    # print(categories)
    # for e in categories:
        # print(e['name'])

    # d = {e['name']:[] for e in categories}
    d = [e['name'] for e in categories]
    print(d)
    # print(Menu.objects.filter(category=d[0]))
    c = {e:Menu.objects.filter(category=e) for e in d}
    print(c)
    for item in c:
        print(c[item])
        for i in c[item]:
            print(i.name)


    return render(request, 'menu.html', {
        'menu': c,
        'categories': d
    })