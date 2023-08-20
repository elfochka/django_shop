# Generated by Django 4.2.3 on 2023-08-20 16:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deliver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512, verbose_name='название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
            ],
            options={
                'verbose_name': 'доставка',
                'verbose_name_plural': 'доставки',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment', models.CharField(choices=[('cash', 'Наличные'), ('card', 'Карта')], max_length=10, verbose_name='способ оплаты')),
                ('status', models.CharField(choices=[('created', 'Сформирован'), ('unpaid', 'Не оплачен'), ('paid', 'Оплачен'), ('shipped', 'В пути'), ('delivered', 'Доставлен'), ('returned', 'Возвращен')], default='created', max_length=10, verbose_name='статус заказа')),
                ('is_paid', models.BooleanField(default=False, verbose_name='оплачен')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='удален')),
                ('name', models.CharField(max_length=255, verbose_name='имя')),
                ('email', models.EmailField(max_length=254, verbose_name='электронная почта')),
                ('phone', models.CharField(max_length=11, verbose_name='телефон')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='создан')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='обновлен')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='клиент')),
                ('delivery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.deliver', verbose_name='доставка')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('quantity', models.PositiveIntegerField(verbose_name='количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='заказ')),
            ],
            options={
                'verbose_name': 'позиция заказа',
                'verbose_name_plural': 'позиции заказа',
            },
        ),
    ]
