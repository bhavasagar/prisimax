# Generated by Django 2.2.10 on 2020-06-19 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200619_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='pincode',
            field=models.IntegerField(default=123456),
        ),
    ]
