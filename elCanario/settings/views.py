from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from authentication.models import UserProfileExtends
class GeneralSettingsView(TemplateView):
    template_name = 'settings.html'




@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        user_profile = UserProfileExtends.objects.get_or_create(user=request.user)[0]
        user_profile.profile_picture = request.FILES['profile_picture']
        user_profile.save()
        return JsonResponse({'message': 'Imagen de perfil actualizada con éxito.'})
    return JsonResponse({'message': 'Error al cargar la imagen de perfil.'}, status=400)