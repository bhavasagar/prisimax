# Generated by Django 2.2.10 on 2020-06-20 02:09

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_orderitem_quantit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sizes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXl', 'XXL')], max_length=100, null=True), blank=True, default=list, size=None)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='sizes',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='size', to='core.Sizes'),
        ),
    ]