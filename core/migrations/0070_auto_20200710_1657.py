# Generated by Django 2.2.10 on 2020-07-10 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0069_item_club_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='club_discount_price',
            field=models.FloatField(blank=True, default=100000, null=True),
        ),
    ]
