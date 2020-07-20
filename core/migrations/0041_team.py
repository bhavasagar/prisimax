# Generated by Django 2.2.10 on 2020-06-24 18:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0040_auto_20200624_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='')),
                ('desig', models.CharField(default='CEO', max_length=20)),
                ('opinion', models.TextField()),
                ('facebook', models.URLField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_team', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
