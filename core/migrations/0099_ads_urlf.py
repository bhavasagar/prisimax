# Generated by Django 2.2.10 on 2020-11-02 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0098_auto_20201102_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='urlf',
            field=models.URLField(default='https://www.presimax.online/'),
        ),
    ]
