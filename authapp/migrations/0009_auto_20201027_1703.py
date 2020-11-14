# Generated by Django 2.2 on 2020-10-27 13:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_auto_20201027_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopuserprofile',
            name='birthday_date',
        ),
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 29, 13, 3, 36, 405642, tzinfo=utc)),
        ),
    ]
