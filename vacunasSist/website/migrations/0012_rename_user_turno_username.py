# Generated by Django 4.0.4 on 2022-05-24 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_merge_20220524_0311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turno',
            old_name='user',
            new_name='username',
        ),
    ]