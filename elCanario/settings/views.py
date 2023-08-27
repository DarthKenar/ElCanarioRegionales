from django.shortcuts import render
from django.views.generic import TemplateView
class GeneralSettingsView(TemplateView):
    template_name = 'settings.html'


