from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from authentication.models import UserProfileExtends
from elCanario.utils import render_login_required
from PIL import Image
class GeneralSettingsView(TemplateView):
    template_name = 'settings.html'

@csrf_protect
def upload_profile_picture(request):
    template = "upload_image_profile_form.html"
    if request.method == 'POST':
        user_profile = UserProfileExtends.objects.get_or_create(user=request.user)[0]
        
        # Verificar que se haya enviado un archivo
        try:
            image_file = request.FILES['profile_picture']
        except:
            context={'upload_image_answer_error': 'No se ha proporcionado una imagen.'}
            return render_login_required(request, template, context)
        
        # Verificar el tipo de archivo de imagen
        allowed_formats = ['png', 'jpg', 'jpeg', 'webp']
        if not image_file.name.split('.')[-1].lower() in allowed_formats:
            context = {'upload_image_answer_error': 'Formato de imagen no permitido.'}
            return render_login_required(request, template, context)
        else:
            print("El tipo de archivo es imagen - válido")

        # Abrir la imagen y verificar su tamaño
        try:
            img = Image.open(image_file)
            if img.width > 160 or img.height > 160:
                context = {'upload_image_answer_error': 'La imagen debe tener un tamaño máximo de 160x160 píxeles.'}
                return render_login_required(request, template, context)
        except Exception as e:
            context = {'upload_image_answer_error': f'Error al procesar la imagen: {str(e)}'}
            return render_login_required(request, template, context)
        try:
            user_profile.profile_picture = image_file
            user_profile.save()
            context = {'upload_image_answer_right': 'Imagen de perfil actualizada con éxito.'}
            return render_login_required(request, template, context)
        except Exception as e:
            context = {'upload_image_answer_error': 'Error al cargar la imagen de perfil.'}
            return render_login_required(request, template, context)
