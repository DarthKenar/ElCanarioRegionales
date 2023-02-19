from django.shortcuts import render

# Create your views here.

def productos(request):
    return render(request,template_name='productos.html', context={}) #request = HttpRequest
