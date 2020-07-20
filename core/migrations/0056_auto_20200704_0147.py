# Generated by Django 2.2.10 on 2020-07-04 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_auto_20200703_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myorder',
            name='refunded',
        ),
        migrations.RemoveField(
            model_name='myorder',
            name='requested',
        ),
        migrations.AddField(
            model_name='myorder',
            name='status',
            field=models.CharField(blank=True, default='404', max_length=25, null=True),
        ),
    ]
