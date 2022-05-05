from django.db import models

from django.contrib.auth.models import User


class Vacuna(models.Model):
    nombre= models.CharField(max_length=100)
    informacion= models.CharField(max_length=700)

class Vacunatorio(models.Model):
    nombre=models.CharField()
    ubicacion=models.CharField()
    
""" acá podemos hacer modelo de persona y que usuario admin y vacunador hereden lo básico"""


class Usuario(models.Model):
    nombre = models.CharField(max_length=100, help_text="Nombre de la persona")
    apellido = models.CharField(max_length=100, help_text="Apellido de la persona")
    fecha_nacimiento= models.DateField(help_text="Fecha de nacimiento de la persona")
    dni=models.IntegerField(max_length=8, help_text="DNI de la persona")
    residencia = models.TextField(help_text="Descripción de la tarea")
    historial_vacunas = models.ForeignKey(User, on_delete=models.CASCADE)
    id_vacunas_aplicadas = models.ForeignKey(Vacuna)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

