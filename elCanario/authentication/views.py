from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from elCanario.utils import render_login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
import aiohttp
from authentication.utils import get_today_date_all
from dollar.models import DollarGraph

# Create your views here.

def login_view(request):
    return render(request, template_name='login.html', context={})

def search_register(request):
    """
    Cuando el usuario se registra primero se debe comprobar que no exista ningun usuario con ese nombre 
    (hay que ver en un futuro como comprobar esto en tiempo real mientras el usuario escribe en el input.
    luego comprobar que no esté registrado el correo
    luego compribar que la contraseña sea segura
    )"""
    
    pass

@csrf_protect
def search_user(request):
    
    if request.method == 'POST':

        username_input = request.POST['username_input']
        password_input = request.POST['password_input']
    
        user = authenticate(request, username=username_input, password=password_input)

        if user is not None:

            login(request, user)
            return redirect('home')
        
        else:
            context = {"answer_error":"Usuario o contraseña incorrectos"}
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

@login_required
def home(request):
    day, month, year = get_today_date_all()
    print(day)
    print(month)
    print(year)
    # si no se guardasen repetidos podría usar este metodo
    # dollar_price = get_object_or_404(DollarGraph, date = f"{year}-{month}-{day}")
    #SE USA ESTA FORMA PORQJUE SE GUARDAN REPETIDOS:.. porque se guardan repetidos?
    try:
        
        dollar_price = DollarGraph.objects.filter(date = f"{year}-{month}-{day}")
        dollar_price = dollar_price.first()
        context = {"dollar_price": dollar_price.price}
    except:
        print("No se encuentra un precio para el dolar")
        context = {"dollar_price": 'No hay precios para mostrar'}

    #Agrego este codigo para evitar el error de ejecuccion por primera vez
    
    template = "home.html"
    return render_login_required(request, template, context)

    



