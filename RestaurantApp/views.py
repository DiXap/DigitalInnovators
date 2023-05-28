from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

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
    return render(request, 'menu.html')