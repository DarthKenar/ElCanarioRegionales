from django.shortcuts import render
from productos.models import Producto
from django.http import HttpResponse
# Create your views here.

def productos(request):
    return render(request,template_name='productos.html', context={}) #request = HttpRequest

# def buscar(request):
#     producto = f"El producto buscado es: {request.GET['producto_input']}"
#     return HttpResponse(producto)


def buscar(request):

    producto = request.GET['producto_input']
    
    if producto:

        articulos = Producto.objects.filter(nombre__icontains=producto)
        return render(request,"productos.html",context={"articulos":articulos,"query":producto, "respuesta": "No se encuentra ningun artículo para el nombre buscado:"})
    
    else:
        
        return HttpResponse("""
        <h1>Debe ingresar un artículo en el campo de búsqueda</h1>

        """)
    


