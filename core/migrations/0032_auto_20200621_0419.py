# Generated by Django 2.2.10 on 2020-06-21 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20200621_0258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='selcsize',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='selcsize',
            field=models.CharField(blank=True, default=False, max_length=30, null=True),
        ),
    ]
