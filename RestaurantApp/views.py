from django.shortcuts import render, redirect, get_object_or_404
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
    categories = Categories.objects.values('name')
    cat_list = [e['name'] for e in categories]
    menu = {e: Menu.objects.filter(category=e) for e in cat_list}

    return render(request, 'menu.html', {
        'menu': menu,
    })

def menu_item_detail(request, category_id, item_id):
    item = get_object_or_404(Menu, pk=item_id)
    return render(request, 'item_detail.html', {
        'item': item,
    })

def menu_category(request, category_id):
    category = get_object_or_404(Categories, pk=category_id)
    items = Menu.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'items': items,
    })