# Generated by Django 4.2.3 on 2023-08-08 05:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0003_offer"),
    ]

    operations = [
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField(verbose_name="описание")),
                ("created", models.DateTimeField(auto_now_add=True, verbose_name="создан")),
                ("updated", models.DateTimeField(auto_now=True, verbose_name="обновлён")),
            ],
        ),
        migrations.AlterModelOptions(
            name="offer",
            options={"ordering": ["-created"], "verbose_name": "скидка", "verbose_name_plural": "скидки"},
        ),
        migrations.AlterField(
            model_name="offer",
            name="created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="создана"),
        ),
        migrations.AlterField(
            model_name="offer",
            name="is_active",
            field=models.BooleanField(default=False, verbose_name="активна"),
        ),
        migrations.AlterField(
            model_name="offer",
            name="updated",
            field=models.DateTimeField(auto_now=True, verbose_name="обновлена"),
        ),
        migrations.AddIndex(
            model_name="offer",
            index=models.Index(fields=["id"], name="products_of_id_9ebed4_idx"),
        ),
        migrations.AddIndex(
            model_name="offer",
            index=models.Index(fields=["-created"], name="products_of_created_b90585_idx"),
        ),
        migrations.AddField(
            model_name="review",
            name="author",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews",
                                    to=settings.AUTH_USER_MODEL, verbose_name="Автор"),
        ),
        migrations.AddField(
            model_name="review",
            name="product",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews",
                                    to="products.product", verbose_name="товар"),
        ),
    ]
