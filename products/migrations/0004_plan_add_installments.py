# Generated by Django 3.2 on 2023-01-02 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_name_category_plan_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='installments',
            field=models.SmallIntegerField(default=1),
        ),
    ]
