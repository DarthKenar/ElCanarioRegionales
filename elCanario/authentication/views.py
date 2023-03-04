from django.shortcuts import render
from .models import User
# Create your views here.
def search_register(request):
    """
    Cuando el usuario se registra primero se debe comprobar que no exista ningun usuario con ese nombre 
    (hay que ver en un futuro como comprobar esto en tiempo real mientras el usuario escribe en el input.
    luego comprobar que no esté registrado el correo
    luego compribar que la contraseña sea segura
    )"""
    
    pass
def search_user(request):
    """
    Primero comprobar:
        - que el usuario esté en la base de datos
        - que la contraseña elegida para el usuario sea correcta
        responder a cualquiera de las dos. "El usuario o contraseña son incorrectos."
    """
    username_or_email_input = request.GET['username_input']
    password_input = request.GET['password_input']

    try:
        
        user = User.objects.get(nombre = username_or_email_input, contrasenia = password_input)

    except User.DoesNotExist:

        

        return render(request,'login.html', context={"respuesta":"No se ha podido ingresar al sistema, revise los datos ingresados."})
        #return render(request,"productos.html",context={"articulos":articulos,"query":producto})
    return render(request, template_name='index.html', context={"user": user})
        
def index(request):

    return render(request, template_name='index.html', context={})

def login(request):
    
    return render(request, template_name='login.html', context={})

def register(request):
    
    return render(request, template_name='register.html', context={})
"""

def productos(request):
    return render(request,template_name='productos.html', context={}) #request = HttpRequest

# def buscar(request):
#     producto = f"El producto buscado es: {request.GET['producto_input']}"
#     return HttpResponse(producto)


def buscar(request):

    producto = request.GET['producto_input']
    
    if producto:

        articulos = Producto.objects.filter(nombre__icontains=producto)
        return render(request,"productos.html",context={"articulos":articulos,"query":producto})
    
    else:
        
        return HttpResponse("Debe ingresar un artículo en el campo de búsqueda")"""