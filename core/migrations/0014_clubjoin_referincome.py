# Generated by Django 2.2.10 on 2020-06-16 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20200616_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubjoin',
            name='referincome',
            field=models.FloatField(default=0.0),
        ),
    ]
