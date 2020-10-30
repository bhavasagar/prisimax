# Generated by Django 2.2.10 on 2020-10-28 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0092_myorder_orderitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(default='5', max_length=3)),
                ('review', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('images', models.ManyToManyField(related_name='review_images', to='core.Multiple_Pics')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.RemoveField(
            model_name='reviewsimage',
            name='item',
        ),
        migrations.RemoveField(
            model_name='reviewsimage',
            name='post',
        ),
        migrations.DeleteModel(
            name='Reviews',
        ),
        migrations.DeleteModel(
            name='ReviewsImage',
        ),
    ]
