# Generated by Django 2.2 on 2020-11-11 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0012_auto_20201111_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
        migrations.AlterField(
            model_name='discountgames',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
        migrations.AlterField(
            model_name='gamecategories',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
        migrations.AlterField(
            model_name='games',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
    ]
