# Generated by Django 2.2.10 on 2020-07-03 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_auto_20200630_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(default=False, max_length=15),
        ),
    ]
