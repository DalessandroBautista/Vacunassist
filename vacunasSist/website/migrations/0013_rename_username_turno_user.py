# Generated by Django 4.0.4 on 2022-05-24 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_rename_user_turno_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turno',
            old_name='username',
            new_name='user',
        ),
    ]