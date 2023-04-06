from django.db import models
from django.contrib.auth.models import User
#REVISAR MODELOS PARA 
# Create your models here.
class CustomUser(User):
    picture = models.ImageField(blank=True, null=True, max_length=100, default="UserPictureDefault.png")
    



