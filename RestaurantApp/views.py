from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required

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

@login_required
def menu(request):
    categories = Categories.objects.values('name')
    cat_list = [e['name'] for e in categories]
    menu = {e: Menu.objects.filter(category=e) for e in cat_list}

    return render(request, 'menu.html', {
        'menu': menu,
    })

@login_required
def menu_item_detail(request, category_id, item_id):
    item = get_object_or_404(Menu, pk=item_id)
    return render(request, 'item_detail.html', {
        'item': item,
    })

@login_required
def menu_category(request, category_id):
    category = get_object_or_404(Categories, pk=category_id)
    items = Menu.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'items': items,
    })

@login_required
def cart(request):
    if request.method == 'GET':  # TODO. Try to use a query
        try:
            # Query
            cart = CartItem.objects.filter(table= request.user)

            # Get dupes
            a = [e.item.name for e in cart]
            dupes = dict(Counter(a))
            b = {key: value for key, value in dupes.items()}

            # Get item prices
            c = {key.item.name: key.item.price for key in cart}

            # Build a dict with relevant info to display in template
            breakdown = {i: [decimal.Decimal(v)] for i, v in b.items()}

            for i in c.keys():
                breakdown[i].append(c[i])

            # Get cart total per item
            for i in b.keys():
                c[i] = decimal.Decimal(b[i]) * c[i]

            # Calculate order total
            total = decimal.Decimal(0)
            for i, price in c.items():
                total += price

            return render(request, 'cart.html', {
                'breakdown': breakdown,
                'total': total,
            })
        except:
            pass
    return render(request, 'cart.html')


@login_required
def cart_add_item(request, category_id, item_id):
    try:
        menu_item = get_object_or_404(Menu, pk=item_id)
        cart_item = CartItem(item=menu_item, table=request.user)
        cart_item.save()

        return redirect('item_detail')
    except:
        return menu_item_detail(request, category_id, item_id)

@login_required
def modify_order(request):
    if request.method == 'GET':  # TODO. Try to use a query
        try:
            # Query
            cart = CartItem.objects.filter(table= request.user).order_by('-time')

            # Build a dict with relevant info to display in template
            order_items = [(i.item.name, i.item.price, i.pk) for i in cart]

            # Calculate order total
            total = decimal.Decimal(0)
            for i, price, _ in order_items:
                total += price

            # print(cart)

            return render(request, 'modify_order.html', {
                'breakdown': order_items,
                'total': total,
            })
        except:
            pass
    return render(request, 'modify_order.html')

@login_required
def cart_remove_item(request, item_id):
    try:
        cart_item = get_object_or_404(CartItem, pk=item_id)
        cart_item.delete()
        # print(f'item {cart_item}')

        return redirect('modify_order')
    except:
        return render(request, 'modify_order.html', {
            'error': 'No se ha podido completar la solicitud'
        })