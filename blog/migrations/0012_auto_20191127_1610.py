# Generated by Django 2.2.7 on 2019-11-27 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20191127_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='meta_description',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='meta description'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='meta_keywords',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='meta keywords'),
        ),
    ]