# Generated by Django 2.2.10 on 2020-06-15 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200615_0512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('H', 'Handicrafts'), ('SS', 'Sarees'), ('G', 'Grossery'), ('P', 'Daily Needs'), ('FW', 'FashionWear'), ('F', 'FootWear'), ('FU', 'Furniture'), ('MW', 'MensWear'), ('BC', 'BeautyCare'), ('E', 'Electronics')], max_length=2),
        ),
    ]