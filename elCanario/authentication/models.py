from django.db import models
from django.contrib.auth.models import User

class UserProfileExtends(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile-pictures', null=True, blank=True, default="elcanarioregionales-logo-160x160.png")