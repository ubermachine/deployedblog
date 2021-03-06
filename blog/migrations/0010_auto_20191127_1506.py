# Generated by Django 2.2.7 on 2019-11-27 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20191127_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL, verbose_name='Post  metaAuthor'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='publish_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Post meta Date  Published'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='title',
            field=models.CharField(max_length=120, verbose_name='Post meta Title'),
        ),
    ]
