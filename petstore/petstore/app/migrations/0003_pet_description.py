# Generated by Django 5.1.7 on 2025-04-01 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_pet_petname'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='description',
            field=models.TextField(default=None, null=True),
        ),
    ]
