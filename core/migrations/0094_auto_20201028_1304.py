# Generated by Django 2.2.10 on 2020-10-28 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0093_auto_20201028_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='selcsize',
        ),
        migrations.AddField(
            model_name='item',
            name='rating',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]