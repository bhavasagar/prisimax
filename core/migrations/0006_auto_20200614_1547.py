# Generated by Django 2.2.10 on 2020-06-14 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200614_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubjoin',
            name='Ifsc',
            field=models.CharField(blank=True, default=False, max_length=20, null=True),
        ),
    ]