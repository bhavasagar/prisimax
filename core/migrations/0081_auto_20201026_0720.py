# Generated by Django 2.2.10 on 2020-10-26 07:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0080_auto_20201026_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='extra_images',
            field=models.ManyToManyField(blank=True, related_name='multiple_images', to='core.Multipleimage'),
        ),
    ]