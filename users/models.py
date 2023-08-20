from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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


class Action(models.Model):
    """
    Model to store user actions in connection with "target" database models.

    user: user who made the action
    verb: what was done; use constants from Action model
    created: date/time of action
    target_ct: this will tell us the model for the relationship
    target_id: a field to store primary key of the related object
    target: a field to define and manage the generic relation using two previous fields
    """

    VIEW_PRODUCT = "просмотрен товар"

    user = models.ForeignKey(
        verbose_name="пользователь",
        to=CustomUser,
        related_name="actions",
        on_delete=models.CASCADE,
    )
    verb = models.CharField(
        verbose_name="действие",
        max_length=256,
    )
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
    )
    target_id = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    target = GenericForeignKey(
        ct_field="target_ct",
        fk_field="target_id",
    )
    created = models.DateTimeField(
        verbose_name="время события",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "действие"
        verbose_name_plural = "действия"
        ordering = ["-created"]
