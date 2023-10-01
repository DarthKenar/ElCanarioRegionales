from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from elCanario.utils import render_login_required
from PIL import Image
class GeneralSettingsView(TemplateView):
    template_name = 'settings.html'
