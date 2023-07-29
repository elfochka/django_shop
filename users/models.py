from django.db import models
from django.contrib.auth.models import AbstractUser


def get_default_image():
    return 'assets/img/DEF_IMG.png'


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=20, null=False, blank=False)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='images/', default=get_default_image)
    phone = models.CharField(max_length=11)
    email = models.EmailField(max_length=200, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []