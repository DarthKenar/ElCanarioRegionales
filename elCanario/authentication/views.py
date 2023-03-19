from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
# Create your views here.
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
            context = {"answer_error":"<p> Usuario o contraseña incorrectos</p>"}
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def login_view(request):
    return render(request, template_name='login.html', context={})

@login_required
def home(request):
    return render(request, template_name='home.html')
