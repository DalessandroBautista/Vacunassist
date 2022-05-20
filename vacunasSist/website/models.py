from django.db import models

from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager


class Vacuna(models.Model):
    nombre=models.CharField(max_length=40)
    informacion= models.TextField(max_length=700)
    class Meta:
        verbose_name='vacuna'
        verbose_name_plural='vacunas'
    
    def __str__(self):
        return self.nombre




class Vacunatorio(models.Model):
    nombre=models.CharField(max_length=40)
    ubicacion=models.CharField(max_length=40)
    
""" acá podemos hacer modelo de persona y que usuario admin y vacunador hereden lo básico"""

class UsuarioManager(BaseUserManager):
    def create_user(self, email, username, nombre, apellido, password =None):
        if not email: 
            raise ValidationError("EL usuario debne tener un email asociado")  
        user= self.model(
            username = username,
            email= self.normalize_email(email),
            nombre =nombre,
            apellido=apellido,
            )
        user.set_pasosword(password)
        user.save()
        return user
    def create_superuser(self, email, username, nombre, apellido, password = None):
        user = self.create_user(
            email,
            username=username,
            nombre=nombre,
            apellido=apellido,
            password=password
            )
        user.usuario_administrador = True
        user.save()
        return user
    
class Usuario(AbstractBaseUser):
    username =models.CharField('Nombre de usuario', unique=True, max_length=100)
    email = models.EmailField('Correo electrónico', max_length=254, unique=True)
    nombre = models.CharField('Nombre', max_length=254)
    apellido = models.CharField('apellido', max_length=254)
    dni=models.IntegerField(help_text="DNI de la persona", unique=True)
    fecha_nacimiento= models.DateField(help_text="Fecha de nacimiento de la persona")
    residencia = models.TextField(help_text="Descripción de la tarea", null=True)
    id_vacunas_aplicadas = models.ForeignKey(Vacuna, on_delete=models.CASCADE, null=True)
    vacunatorio_preferencia =models.ForeignKey(Vacunatorio, on_delete=models.CASCADE,null=True)
    historial_vacunacion=models.CharField('Historial de vacunación', max_length=1000, null= True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_activo= models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects= UsuarioManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','nombre', 'apellido','dni', 'fecha_nacimiento']