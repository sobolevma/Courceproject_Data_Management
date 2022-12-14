# Generated by Django 2.1.3 on 2018-12-20 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ecomapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=20)),
                ('item_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('third_name', models.CharField(max_length=200)),
                ('order_phone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=250)),
                ('buying_type', models.CharField(choices=[('?? ??????????', '?? ??????????'), ('????????????????', '????????????????')], default='?? ??????????', max_length=40)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('???????????? ?? ??????????????????', '???????????? ?? ??????????????????'), ('??????????????????????', '??????????????????????'), ('??????????????', '??????????????')], default='???????????? ?? ??????????????????', max_length=100)),
                ('items', models.ManyToManyField(to='ecomapp.Cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, unique=True)),
                ('slug', models.SlugField(blank=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=ecomapp.models.image_folder)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('brand', models.ForeignKey(default='????????????', on_delete=django.db.models.deletion.SET_DEFAULT, to='ecomapp.Brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Category')),
            ],
        ),
        migrations.AddField(
            model_name='cartitem',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomapp.Service'),
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(blank=True, to='ecomapp.CartItem'),
        ),
    ]
