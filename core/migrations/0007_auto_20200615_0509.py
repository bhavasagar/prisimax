# Generated by Django 2.2.10 on 2020-06-15 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200614_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubjoin',
            name='Acno',
            field=models.CharField(blank=True, default=False, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='clubjoin',
            name='Ifsc',
            field=models.CharField(blank=True, default=False, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='clubjoin',
            name='paytm',
            field=models.CharField(blank=True, default=False, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='clubjoin',
            name='refer',
            field=models.CharField(default=False, max_length=20),
        ),
        migrations.AlterField(
            model_name='clubjoin',
            name='refered_person',
            field=models.CharField(blank=True, default=False, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='clubjoin',
            name='team',
            field=models.CharField(blank=True, default=False, max_length=30, null=True),
        ),
    ]