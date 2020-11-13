# Generated by Django 2.2.10 on 2020-11-05 16:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0104_auto_20201105_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='clubjoin',
            name='referer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referer', to='core.UserProfile'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='referer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='referer', to=settings.AUTH_USER_MODEL),
        ),
    ]