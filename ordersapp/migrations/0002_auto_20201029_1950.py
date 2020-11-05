# Generated by Django 2.2 on 2020-10-29 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('FM', 'формируется'), ('STP', 'обрабатывается'), ('PRD', 'обработан'), ('PD', 'оплачен'), ('RDY', 'готов к выдаче'), ('DN', 'выдан'), ('CNC', 'отменен')], default='FM', max_length=3, verbose_name='Статус заказа'),
        ),
    ]
