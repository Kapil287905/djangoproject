# Generated by Django 5.2 on 2025-04-11 03:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('orderid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('orderdate', models.DateField()),
                ('userid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('Mobile', 'Mobile'), ('Cloths', 'Cloths'), ('Shoses', 'Shoses'), ('Electronics', 'Electronics')], max_length=30)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('image', models.ImageField(upload_to='images')),
                ('userid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('receiptid', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('paymenttype', models.CharField(choices=[('Online', 'Online'), ('Cash on delivery', 'Cash on delivery')], max_length=30)),
                ('paymentstatus', models.CharField(choices=[('Done', 'Done'), ('Failed', 'Failed')], max_length=30)),
                ('orderid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.orders')),
                ('userid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('productid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.products')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='productid',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.products'),
        ),
        migrations.CreateModel(
            name='Carts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('userid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('productid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.products')),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Fmeale')], max_length=30)),
                ('dob', models.DateField(default=None, null=True)),
                ('mobile', models.PositiveIntegerField()),
                ('address', models.TextField()),
                ('photo', models.ImageField(upload_to='images')),
                ('userid', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
