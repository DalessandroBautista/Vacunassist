from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
import random 
from django.urls import reverse
from django.views.generic import View, TemplateView, ListView
from django.contrib import messages
# Create your views here.

""" 
"""

    
def index(request):
    return render(request, "website/index.html")

def registrarse(request):
    if request.method == 'POST':
        form = FormularioUsuario(request.POST)
        
        if form.is_valid():
            
            mail=request.POST.get("email")         
            form.save()
            infoForm=form.cleaned_data
            send_mail(
                'VacunasSist',
                'Tu cuenta ha sido creada exitosamente!',
                'vacunassist2022@gmail.com',
                [mail],
                fail_silently=False
            )     
            messages.success(request, "Te has registrado exitosamente")   
            return HttpResponseRedirect(reverse('login'))
    else:
        form = FormularioUsuario()
    return render(request, 'website/registration/registro.html', {
        'form': form
        })

def login(request):
    if request.method=="POST":
        form=FormularioLogin(request.POST)
        username=request.POST.get("username")
        password=request.POST.get("password")
        try:
            user = Usuario.objects.get(username=username)
            if (user.password == password):
                auth.login(request, user)
                return render(request, "website/index.html")
            else:
                form=LoginForm()
                messages.error(request,"El usuario o la contraseña son incorrectos")
                return render(request, "website/registration/login.html",{"form": form})
        except Usuario.DoesNotExist:
            if form.is_valid():
                print('valido')

    else:
        form=LoginForm()

    return render(request, "website/registration/login.html",{
        "form": form,
    })


@login_required
def logout(request):
    return render(request, "website/registration/logged_out.html",{
    })
def password_reset(request):
    if request.method == 'POST':
        form = FormularioEmail(request.POST)
        mail=request.POST.get("email")
        usuario= Usuario.objects.get(email=mail)
        clave_nueva=random.randint(100000,999999)
        message="Tu nueva contraseña es: " + str(clave_nueva) + ". Por favor, al ingresar, modifica tu clave desde 'Ver mi perfil/ Modificar contraseña'."
        usuario.password=clave_nueva
        usuario.save()
        send_mail(
           'VacunasSist - Recuperación de contraseña',
            message,
            'vacunassist2022@gmail.com',
            [mail],
            fail_silently=False
        )
        messages.success(request, "Te hemos enviado tu nueva clave al email ingresado.")   
        return HttpResponseRedirect(reverse('login'))
    else:
        form = FormularioEmail()
    return render(request, 'website/registration/password_reset_form.html', {
        'form': form
    })
    
def verPerfil(request):
    id_usuario=request.user.id
    usuario= Usuario.objects.get(id=id_usuario)
    if request.method=="POST":
        print('entre al post y creo form')
        usuario_form =UpdateUsuarioForm(request.POST, instance = usuario)
        if usuario_form.is_valid():
            usuario_form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('index')
    else:
        print('no entre al post y creo form')
        usuario_form=UpdateUsuarioForm(instance = usuario)
        print('form')
        usuario_form=usuario_form.deshabilitarCampos(usuario.identidad_verificada)

    return render(request, "website/verPerfil.html",{ 'usuario_form':usuario_form})

def modificar_password(request):
    id_usuario=request.user.id
    usuario= Usuario.objects.get(id=id_usuario)
    if request.method=="POST":
        print('entre al post y creo form')
        print(usuario.residencia)
        password_form =UpdatePasswordForm(request.POST)
        password_form.is_valid()
        print(password_form.errors)
        if True:
            print('post a validar')
            mail=usuario.email
            clave_nueva=request.POST.get("password")
            usuario.set_password(clave_nueva)
            usuario.save()
            print(clave_nueva)
            message="Tu nueva contraseña es: " + str(clave_nueva)
            send_mail(
                'VacunasSist - Nueva contraseña',
                message,
                'vacunassist2022@gmail.com',
                [mail],
                fail_silently=False
            )
            messages.success(request, "Hemos modificado tu clave y te la enviamos a tu email.")   
        return HttpResponseRedirect(reverse('index'))
    else:
        password_form=UpdatePasswordForm() 
    return render(request, 'website/modificar_password.html', {
        'password_form':password_form
    })
    