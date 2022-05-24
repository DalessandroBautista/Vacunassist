from datetime import date, timedelta
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
from website.models import Vacuna,Turno,Usuario,VacunaDeUsuario
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
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
            print(password)
            print(user.password)
            print(username)
            print(user.username)
            try:
                auth.login(request, user)
                return render(request, "website/index.html")
            except:
                print(errors)
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
    
def solicitarTurno(request):
    # Aca debe ir un "if !validoIdentidad & residencia=LP render lo de abajo"
    # turno = Turno.objects.filter(vacuna="Covid-19").filter(username="Pappo")
        user = request.user
        info = ""
        if ((user.residencia=="La Plata")):
           info = "Selecciona el turno a solicitar"
           return render(request,"website/solicitar_turno.html",{
           "prueba": info,}) 
        else:
            info = "No se puede solicitar turnos por no ser residente de La Plata"
            return render(request, "website/index.html", {
            "prueba": info,})
        #  "test": Vacuna.objects.all().first()
    # Sino mostrar alerta de  no validado o no tener residencia en LP

def solicitarTurnoCovid(request):
    # Aca debe ir un "if !validoIdentidad & residencia=LP render lo de abajo"
        user = request.user
        turno = Turno.objects.filter(vacuna="Covid-19").filter(user=user).filter(asignado=False).exists()
        info = ""
        if (turno):
            info = "No se puede solicitar un turno de vacuna Covid-19 por ya tener uno solicitado"
        elif (((date.today().year-user.fecha_nacimiento.year)>18)):
            t = Turno(user=request.user, vacuna="Covid-19")
            t.save()
            info = "Se ha solicitado un turno la para vacuna de Covid-19 exitosamente"
        else:
            info = "No se ha podido solicitar un turno para la vacuna de Covid-19 por ser menor de 18 años"
        return render(request,"website/solicitar_turno.html",{"prueba": info}) 
    # Sino mostrar alerta de  no validado o no tener residencia en LP

def solicitarTurnoGripe(request):
    # Aca debe ir un "if !validoIdentidad & residencia=LP render lo de abajo"
    # turno = Turno.objects.filter(vacuna="Covid-19").filter(username="Pappo")dc  
        user = request.user
        toYearAgo = date.today()-timedelta(365)
        seVacuno = Historial_Vacunacion.objects.filter(vacuna="Gripe A").filter(user=user).filter(fecha__gte=toYearAgo, fecha__lte=date.today()).exists()
        turno = Turno.objects.filter(vacuna="Gripe A").filter(user=user).filter(asignado=False).exists()
        info = ""
        if (turno):
            info = "No se puede solicitar un turno de vacuna Gripe A por ya tener uno solicitado"
        elif not (seVacuno):
            t = Turno(user=request.user, vacuna="Gripe A")
            t.save()
            info = "Se ha solicitado un turno la para vacuna de Gripe A exitosamente"
        else:
            info = "No se ha podido solicitar un turno para la vacuna de Gripe A por haberse vacunado hace menos de un año"
        return render(request,"website/solicitar_turno.html",{"prueba": info})
    # Sino mostrar alerta de  no validado o no tener residencia en LP
    
 
def verTurnos(request):
    user_id = request.user.id
    lista_turnos= Turno.objects.filter(user_id=user_id).filter(asignado=True)
    print(lista_turnos)
    if (lista_turnos):
        return render(request, 'website/ver_turnos.html', {
            'lista_turnos':lista_turnos
        })
    else:
        messages.error(request, 'Usted no tiene turnos aceptados ')
        return render(request, 'website/index.html',{})


def verTurnosPendientes(request):
    user_id = request.user.id
    lista_turnos= Turno.objects.filter(user_id=user_id).filter(asignado=False)
    print(lista_turnos)
    if (lista_turnos):
        return render(request, 'website/ver_turnos_pendientes.html', {
            'lista_turnos':lista_turnos
        })
    else:
        messages.error(request, 'Usted no tiene turnos pendientes')
        return render(request, 'website/index.html',{})
    

def verVacunasAplicadas(request):
    user_id = request.user.id
    print(user_id)
    id_vacunas= VacunaDeUsuario.objects.filter(user_id=user_id)
    lista_vacunas=[]
    print(id_vacunas)
    for vacuna in id_vacunas:
    
        print(vacuna)
        lista_vacunas.append(Vacuna.objects.get(id=vacuna.vacuna_id))
        
    print(lista_vacunas)
    print(len(lista_vacunas))
    if (len(lista_vacunas)>1):
        return render(request, 'website/ver_vacunas_aplicadas.html', {
            'lista_vacunas':lista_vacunas
        })
    else:
        messages.error(request, 'Usted no tiene vacunas aplicadas')
        return render(request, 'website/index.html',{})
    
def obtenerCertificado(request, vacuna_id):
    vacuna=Vacuna.objects.get(id=vacuna_id)
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)

    mensaje= "Este documento certifica que usted se vacunó para: " + vacuna.nombre
    p.drawString(20, 20, mensaje)

    p.showPage()
    p.save()


    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='certificado.pdf')
    
def verInformacion(request):
    list_vacunas= Vacuna.objects.all()
    return render(request, 'website/informacion_vacuna.html', {'list_vacunas': list_vacunas })
