# Generated by Django 2.2 on 2020-11-11 14:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0016_auto_20201111_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 13, 14, 30, 43, 818486, tzinfo=utc)),
        ),
    ]
