# Generated by Django 4.1.5 on 2023-09-04 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_add_is_api_user_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile', to='customers.profile'),
        ),
    ]