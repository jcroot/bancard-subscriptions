# Generated by Django 4.1.5 on 2023-02-06 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='fee_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
