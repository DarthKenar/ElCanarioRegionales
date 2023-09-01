from django.shortcuts import render
from elCanario.utils import render_login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from orders.models import Order
# Create your views here.
# # ORDERS SECTION

class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders.html'

