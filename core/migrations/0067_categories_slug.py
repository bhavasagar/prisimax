# Generated by Django 2.2.10 on 2020-07-09 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_auto_20200709_0347'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
    ]
