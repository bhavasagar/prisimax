# Generated by Django 2.2.10 on 2020-07-16 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0076_reviewsimage_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
