# Generated by Django 2.2.10 on 2020-06-21 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20200621_0419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='size',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Sizes_class'),
        ),
    ]
