from django.contrib.auth.models import AbstractUser
from django.db import models


def get_default_profile_image():
    return "../static/assets/img/icons/loon-icon.svg"


class CustomUser(AbstractUser):
    """Represents user of the shop."""

    middle_name = models.CharField(
        verbose_name="отчество",
        max_length=20,
        null=True,
        blank=True,
    )
    image = models.ImageField(
        verbose_name="изображение профиля",
        upload_to="avatars/",
        blank=True,
        null=False,
        default=get_default_profile_image,
    )
    phone = models.CharField(
        verbose_name="телефон",
        max_length=11,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["id"]),
        ]
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def get_full_name(self):
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}".strip()
        return full_name

    def __str__(self):
        return self.email
