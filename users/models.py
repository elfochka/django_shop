from django.contrib.auth.models import AbstractUser
from django.db import models


def get_default_image():
    return "../static/assets/img/DEF_IMG.png"


class CustomUser(AbstractUser):
    middle_name = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        upload_to="avatars/",
        default=get_default_image,
    )
    phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.email
