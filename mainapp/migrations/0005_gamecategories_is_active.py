# Generated by Django 2.2 on 2020-10-12 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_gamecategories_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamecategories',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='активна'),
        ),
    ]
