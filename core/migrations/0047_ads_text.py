# Generated by Django 2.2.10 on 2020-06-27 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_auto_20200627_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='ads',
            name='text',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]