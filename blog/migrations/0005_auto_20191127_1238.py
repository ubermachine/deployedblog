# Generated by Django 2.2.7 on 2019-11-27 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20191127_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='meta_keywords',
        ),
    ]
