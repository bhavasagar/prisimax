# Generated by Django 2.2.10 on 2020-10-26 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_auto_20201026_0728'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='extra_images',
        ),
        migrations.RemoveField(
            model_name='item',
            name='keywords',
        ),
        migrations.AddField(
            model_name='item',
            name='extra_pics',
            field=models.ManyToManyField(related_name='more_images', to='core.Multipleimage'),
        ),
        migrations.AddField(
            model_name='item',
            name='keyword',
            field=models.ManyToManyField(related_name='search_tags', to='core.Itemsearch'),
        ),
    ]