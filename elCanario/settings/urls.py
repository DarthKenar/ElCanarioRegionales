from django.urls import path
from settings.views import GeneralSettingsView

app_name = 'settings'
urlpatterns = [
    path('settings', GeneralSettingsView.as_view(), name='settings'),
]