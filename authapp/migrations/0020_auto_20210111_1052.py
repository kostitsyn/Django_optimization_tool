# Generated by Django 2.2 on 2021-01-11 06:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0019_auto_20210111_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 13, 6, 52, 27, 649682, tzinfo=utc)),
        ),
    ]
