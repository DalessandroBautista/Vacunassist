# Generated by Django 4.0.4 on 2022-05-23 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_usuario_historial_vacunacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='identidad_verificada',
            field=models.BooleanField(default=False),
        ),
    ]