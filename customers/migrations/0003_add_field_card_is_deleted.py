# Generated by Django 4.1.5 on 2023-02-20 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_rename_user_id_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercards',
            name='card_is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
