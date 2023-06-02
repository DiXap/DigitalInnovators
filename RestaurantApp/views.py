from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count, Sum

from .models import Menu, Categories, CartItem

from collections import Counter
import decimal

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

def cart(request):
    if request.method == 'GET':  # TODO. Try to use a query
        try:
            cart = CartItem.objects.filter(table= request.user)

            a = [e.item.name for e in cart]
            dupes = dict(Counter(a))
            b = {key: value for key, value in dupes.items()}
                
            c = {key.item.name: key.item.price for key in cart}
            print(c)
            x = {i: [decimal.Decimal(v)] for i, v in b.items()}
            print(x)

            for i in c.keys():
                x[i].append(c[i])

            print(x)

            for i in b.keys():
                c[i] = decimal.Decimal(b[i]) * c[i]


            d = [(i.item.name, i.item.price) for i in cart]

            # print(cart)
            # print(cart[0].item.price)
            # print(order[0]['item'])
            # print(order)

            # print(a)
            # print(f'b {b}')
            # print(f'c {c}')
            # print(f'd {d}')

            f = {'Limon': [1, 2], 'Naranja': [4, 5]}

                

            t = decimal.Decimal(0)
            for i, price in d:
                t += price

            # print(t)

            return render(request, 'cart.html', {
                'cart': b,
                'order': c,
                'orderKeys': b.keys(),
                'breakdown': d,
                'total': t,
                'debug': x,
            })
        except:
            pass
    return render(request, 'cart.html')


def cart_add_item(request, category_id, item_id):
    # menu_item = get_object_or_404(Menu, pk=item_id)
    # print(menu_item)
    # return menu_item_detail(request, category_id, item_id)
    try:
        menu_item = get_object_or_404(Menu, pk=item_id)
        cart_item = CartItem(item=menu_item, table=request.user)
        cart_item.save()

        print(menu_item)
        print(cart_item)

        return redirect('menu')
    except:
        return menu_item_detail(request, category_id, item_id)