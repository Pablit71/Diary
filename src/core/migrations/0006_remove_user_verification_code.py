# Generated by Django 4.1.3 on 2022-11-18 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_id_tg_user_verification_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='verification_code',
        ),
    ]