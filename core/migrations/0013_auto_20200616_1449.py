# Generated by Django 2.2.10 on 2020-06-16 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_item_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='schargeinc',
            field=models.FloatField(blank=True, default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='dis_per',
            field=models.FloatField(blank=True, default=-1, null=True),
        ),
    ]
