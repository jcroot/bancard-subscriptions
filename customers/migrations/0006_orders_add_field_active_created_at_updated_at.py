# Generated by Django 4.1.5 on 2023-09-13 13:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_alter_orders_with_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='orders',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
