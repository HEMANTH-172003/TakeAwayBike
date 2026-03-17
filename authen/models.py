from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    mobile = models.CharField(max_length=15)
    address = models.TextField()

    profile_image = models.ImageField(upload_to='profile_images/')
    document = models.FileField(upload_to='documents/')