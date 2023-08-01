from django.shortcuts import render
from elCanario.utils import render_login_required
# Create your views here.
# # ORDERS SECTION

def orders(request):

    template = "orders.html"

    return render_login_required(request, template,context={})