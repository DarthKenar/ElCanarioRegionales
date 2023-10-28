from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from elCanario.utils import render_login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from PIL import Image
class GeneralSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'
