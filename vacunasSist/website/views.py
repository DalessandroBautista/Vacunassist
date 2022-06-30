from datetime import date
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User, auth
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
import random 
from django.urls import reverse
from django.views.generic import View, TemplateView, ListView
from django.contrib import messages
from website.models import Vacuna,Turno,Usuario,VacunaDeUsuario, Historial_Vacunacion, EstadosTurno, Vacunatorio
import reportlab
import io
from django.utils.dateparse import parse_date
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib.auth.hashers import check_password
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
        try:
            form=FormularioLogin(request.POST)
            username=request.POST.get("username")
            password=request.POST.get("password")
            user = auth.authenticate(username=username, password=password)
            usuario = Usuario.objects.get(username=username)
            pass_user= usuario.password
            print('usuario')
            print(user)
            if (user is not None):
                print('user valido')
                auth_login(request, user)
                return render(request, "website/index.html")
            else:
                form=FormularioLogin()
                messages.error(request,"El usuario o la contraseña son incorrectos")
                return render(request, "website/registration/login.html",{"form": form})
        except Exception as e: 
            form=FormularioLogin()
            messages.error(request,"El usuario o la contraseña son incorrectos")
            return render(request, "website/registration/login.html",{"form": form})
            print(repr(e))  
        """
        try:
            user = Usuario.objects.get(username=username)
            print(password)
            print(user.password)
            print(username)
            print(user.username)
            try:
                auth.login(request, user)
               
            except:
                print(errors)
                form=LoginForm()
                messages.error(request,"El usuario o la contraseña son incorrectos")
                return render(request, "website/registration/login.html",{"form": form})
        except Usuario.DoesNotExist:
            if form.is_valid():
                print('valido')
     """
    
    else:
        form=LoginForm()
        print('no es un post')
   
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
        email=request.POST.get("email")
        try:
            usuario= Usuario.objects.get(email=email)
            clave_nueva=str(random.randint(100000,999999))
            usuario.set_password(clave_nueva)
            print(clave_nueva)
            message="Tu nueva contraseña es: " + str(clave_nueva) + ". Por favor, al ingresar, modifica tu clave desde 'Ver mi perfil/ Modificar contraseña'."
            usuario.save()
            send_mail(
                'VacunasSist - Recuperación de contraseña',
                message,
                'vacunassist2022@gmail.com',
                [email],
                fail_silently=False
            )
            messages.success(request, "Te hemos enviado tu nueva clave al email ingresado.")
            return HttpResponseRedirect(reverse('login'))   
        except Exception as e: 
            print(repr(e))
            messages.error(request, "El email ingresado no se encuentra registrado en nuestro sistema.")
        
    else:
        form = FormularioEmail()
    return render(request, 'website/registration/password_reset_form.html', {
        'form': form
    })
    
def verPerfil(request):
    id_usuario=request.user.id
    try:
        usuario= Usuario.objects.get(id=id_usuario)
        
        if request.method=="POST":
            print('entre al post y creo form')
            usuario_form =UpdateUsuarioForm(request.POST, instance = usuario)
            if usuario_form.is_valid():
                try:
                    print('antes de guardar datos')
                    usuario_form.save()
                    print('en guardar datos')
                    messages.success(request, 'Perfil actualizado correctamente')
                    return redirect('index')
                except Exception as e: 
                    print(repr(e))
                    messages.error(request, 'Su perfil no se ha actualizado.')
           
        else:
            print('no entre al post y creo form')
            usuario_form=UpdateUsuarioForm(instance = usuario)
            print('form')
            usuario_form=usuario_form.deshabilitarCampos(usuario.identidad_verificada)
        print(id_usuario)
        return render(request, "website/verPerfil.html",{ 'usuario_form':usuario_form, 'id_usuario':id_usuario})
    except Exception as e: 
            print(repr(e))

def modificar_password(request):
    try:
        id_usuario=request.user.id
        usuario= Usuario.objects.get(id=id_usuario)
        if request.method=="POST":
            print('entre al post y creo form')
            print(usuario.residencia)
            password_form =UpdatePasswordForm(request.POST)
            password_form.is_valid()
            print(password_form.errors)
            oldpassword=request.POST.get("oldpassword")
            clave_usuario=usuario.password
            clave_nueva=request.POST.get("password")
            segunda_clave=request.POST.get("password2")
            if clave_nueva == segunda_clave:
                print(clave_usuario)
                print(oldpassword)
                if check_password(oldpassword, clave_usuario):
                    print('post a validar')
                    mail=usuario.email
                    
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
                    messages.error(request, "La contraseña ingresada no coincide con tu contraseña actual")   
                    return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, "La contraseñas ingresadas no coinciden")   
                return HttpResponseRedirect(reverse('index'))
        else:
            password_form=UpdatePasswordForm() 
        return render(request, 'website/modificar_password.html', {
            'password_form':password_form
        })
    except Exception as e: 
        print(repr(e))
    
def solicitarTurno(request):
    # Aca debe ir un "if !validoIdentidad & residencia=LP render lo de abajo"
    # turno = Turno.objects.filter(vacuna="Covid-19").filter(username="Pappo")
        user = request.user
        info = ""
        
        if (((date.today().year-user.fecha_nacimiento.year)>18) & (user.residencia=="La Plata")):
            print('estoy en solicitar turno')
            info = "Selecciona el turno a solicitar"
            return render(request,"website/solicitar_turno.html",{
           "prueba": info,}) 
        else:
            info="No puede solicitar turnos por no tener validada la identidad o no ser residente de La Plata"
            messages.error(request,"No puede solicitar turnos por no tener validada la identidad o no ser residente de La Plata")
            return render(request, "website/index.html", {
            "prueba": info,})
        #  "test": Vacuna.objects.all().first()
    # Sino mostrar alerta de  no validado o no tener residencia en LP

def solicitarTurnoCovid(request):
    try:
        user = request.user
        turnos=Turno.objects.filter(user_id=user.id).filter(vacuna='Covid-19')
        print(not turnos)
        if ((((date.today().year-user.fecha_nacimiento.year)>18) &  (not turnos)) &  (user.residencia=="La Plata") ):
            t = Turno(user=request.user, vacuna="Covid-19", estado=EstadosTurno(id=1),  vacunatorio=Vacunatorio(id=request.user.vacunatorio_preferencia_id))
            t.save()
            messages.success(request,"Se ha solicitado un turno la para vacuna de Covid-19 exitosamente")
            info = "Se ha solicitado un turno la para vacuna de Covid-19 exitosamente"
        elif (turnos):    
            if (turnos[0].estado==EstadosTurno.objects.get(id="4")):
                 messages.error(request,"No puede solicitar un turno para esta vacuna por ya habersela aplicado")
            
            else:
                messages.error(request,"No puede solicitar un turno para esta vacuna por ya tener un turno asignado para la misma")
                print("No puede solicitar turnos por ya tener un turno asignado para esta vacuna")
        elif(not ((date.today().year-user.fecha_nacimiento.year)>18)):
            messages.error(request,"No puede solicitar un turno para esta vacuna por no ser mayor de edad")
            print("No puede solicitar turnos por ya tener un turno asignado para esta vacuna")
        else:
            messages.error(request,"No puede solicitar turnos por no ser residente de La Plata")
            print("No puede solicitar turnos por no ser residente de La Plata")
        return render(request,"website/solicitar_turno.html",{})
    # Sino mostrar alerta de  no validado o no tener residencia en LP
    except Exception as e: 
        print(repr(e))

def solicitarTurnoGripe(request):
    # Aca debe ir un "if !validoIdentidad & residencia=LP render lo de abajo"
    # turno = Turno.objects.filter(vacuna="Covid-19").filter(username="Pappo")dc  
    try:
        user = request.user
        turnos=Turno.objects.filter(user_id=user.id).filter(vacuna="Gripe A") 
        print(not turnos)
        if ((not turnos) &  (user.residencia=="La Plata") ):
            messages.success(request,"Se ha solicitado un turno la para vacuna de la Gripe A exitosamente")
            t = Turno(user=request.user, vacuna="Gripe A", estado=EstadosTurno(id=1),  vacunatorio=Vacunatorio(id=request.user.vacunatorio_preferencia_id))
            t.save()
        elif (turnos):
            if (turnos[0].estado==EstadosTurno.objects.get(id="4")):
                 messages.error(request,"No puede solicitar un turno para esta vacuna por ya habersela aplicado")
            
            else:
                messages.error(request,"No puede solicitar un turno para esta vacuna por ya tener un turno asignado para la misma")
                print("No puede solicitar turnos por ya tener un turno asignado para esta vacuna")
        else:
            messages.error(request,"No puede solicitar turnos por no ser residente de La Plata")
            print("No puede solicitar turnos por no ser residente de La Plata")
        return render(request,"website/solicitar_turno.html",{})
    # Sino mostrar alerta de  no validado o no tener residencia en LP
    except Exception as e: 
        print(repr(e))

def solicitarTurnoCovid2(request):

    try:
        user = request.user
        turnos=Turno.objects.filter(user_id=user.id).filter(vacuna="Covid-19 2da Dosis")
        primera_dosis= VacunaDeUsuario.objects.filter(user_id=user.id).filter(vacuna="3")
        print(not turnos)
        print(not primera_dosis)
        if ((not turnos) &  (user.residencia=="La Plata") & (not(not primera_dosis))) :
            messages.success(request,"Se ha solicitado un turno la para vacuna de Covid-19 2da Dosis exitosamente")
            t = Turno(user=request.user, vacuna="Covid-19 2da Dosis",estado=EstadosTurno(id=1),  vacunatorio=Vacunatorio(id=request.user.vacunatorio_preferencia_id))
            t.save()
        elif (turnos):
            if (turnos[0].estado==EstadosTurno.objects.get(id="4")):
                messages.error(request,"No puede solicitar un turno para esta vacuna por ya habersela aplicado")
            else:
                messages.error(request,"No puede solicitar un turno para esta vacuna por ya tener un turno asignado para la misma")
            print("No puede solicitar turnos por ya tener un turno asignado para esta vacuna o aún no tiene la primer dosis de la vacuna de Covid-19")
        else:
            messages.error(request,"No puede solicitar turnos por no ser residente de La Plata o aún no tiene la primer dosis de la vacuna de Covid-19")
            print("No puede solicitar turnos por no ser residente de La Plata")
        return render(request,"website/solicitar_turno.html",{})
    # Sino mostrar alerta de  no validado o no tener residencia en LP
    except Exception as e: 
        print(repr(e))
    
     
 
def verTurnos(request):
    try:
        user_id = request.user.id
        usuario= Usuario.objects.get(id=user_id)
        vacunatorio_preferencia= usuario.vacunatorio_preferencia
        lista_turnos= Turno.objects.filter(user_id=user_id).filter(estado=2)
        print(lista_turnos)
        if (lista_turnos):
            return render(request, 'website/ver_turnos.html', {
                'lista_turnos':lista_turnos,
                'vacunatorio_preferencia':vacunatorio_preferencia
            })
        else:
            messages.error(request, 'Usted no tiene turnos aceptados ')
            return render(request, 'website/index.html',{})
    except Exception as e: 
        print(repr(e))


def verTurnosPendientes(request):
    try:
        user_id = request.user.id
        lista_turnos= Turno.objects.filter(user_id=user_id).filter(estado=1)
        print(lista_turnos)
        if (lista_turnos):
            return render(request, 'website/ver_turnos_pendientes.html', {
                'lista_turnos':lista_turnos
            })
        else:
            messages.error(request, 'Usted no tiene turnos pendientes')
            return render(request, 'website/index.html',{})
    except Exception as e: 
        print(repr(e))

def verVacunasAplicadas(request):
    try:
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
        if (len(lista_vacunas)>0):
            return render(request, 'website/ver_vacunas_aplicadas.html', {
                'lista_vacunas':lista_vacunas
            })
        else:
            messages.error(request, 'Usted no tiene vacunas aplicadas')
            return render(request, 'website/index.html',{})
    except Exception as e: 
        print(repr(e))
    
def obtenerCertificado(request, vacuna_id):
    try:
        vacuna=Vacuna.objects.get(id=vacuna_id)
        buffer = io.BytesIO()

        p = canvas.Canvas(buffer)

        mensaje= "Este documento certifica que usted se vacunó para: " + vacuna.nombre
        p.drawString(20, 20, mensaje)

        p.showPage()
        p.save()


        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='certificado.pdf')
    except Exception as e: 
        print(repr(e))

def verInformacion(request):
    try:
        list_vacunas= Vacuna.objects.all()
        return render(request, 'website/informacion_vacuna.html', {'list_vacunas': list_vacunas })
    except Exception as e: 
        print(repr(e))
        
def verRequisitos(request):
    try:
        return render(request, 'website/requisitos_vacunas.html', {})
    except Exception as e:
        print(repr(e))

def cargarVacuna(request):
    id_usuario=request.user.id
    try:
        usuario= Usuario.objects.get(id=id_usuario)
        if request.method=="POST":
            print('entre al post y creo form')
            cargar_vacuna_form =CargarVacunaUsuario(request.POST)
            nombre_vacuna= request.POST.get("vacuna")
            fecha=request.POST.get("fecha")
            date = parse_date(fecha)
            print("imprimo fecha")
            print(date)
            print("imprimo fecha 2")
            existe= Historial_Vacunacion.objects.filter(user_id=id_usuario).filter(vacuna=nombre_vacuna).filter(fecha=date)
            print(existe)
            if cargar_vacuna_form.is_valid() and not existe:
                try:
                    print('antes de guardar datos')
                    vacuna=Historial_Vacunacion()
                    cargar_vacuna_form.save(usuario, vacuna)
                    print('en guardar datos')
                    messages.success(request, 'Vacuna cargada correctamente')
                    return redirect('index')
                except Exception as e: 
                    print(repr(e))
                    messages.error(request, 'Su vacuna no ha sido cargada correctamente.')
            else:
                messages.error(request, 'Usted ya cargó esta vacuna anteriormente.')
        else:
            print('no entre al post y creo form')
            cargar_vacuna_form=CargarVacunaUsuario()
            print('form')
           

        return render(request, "website/cargar_vacuna.html",{ 'cargar_vacuna_form':cargar_vacuna_form})
    except Exception as e: 
            print(repr(e))
            

def verHistorialVacunacion(request, usuario_id):
    try:
        user_id = usuario_id
        lista_vacunas= Historial_Vacunacion.objects.filter(user_id=user_id)

        print(type(lista_vacunas))
        if (lista_vacunas):
            print("if historiaL")
            return render(request, 'website/ver_historial_vacunacion.html', {
                'lista_vacunas':lista_vacunas
            })
        else:
            messages.error(request, 'No tiene vacunas cargadas')
            return render(request, 'website/index.html',{})
    except Exception as e: 
        print(repr(e))

def EliminarVacunaUsuario(request,historial_vacuna_id):
    try:
        vacuna= Historial_Vacunacion.objects.get(id=historial_vacuna_id)
        vacuna.delete()
        messages.success(request, 'Vacuna eliminada correctamente')
        return render(request, 'website/index.html')
    except Exception as e: 
        messages.error(request, 'La vacuna no pudo ser eliminada')
        
def CancelarTurnoUsuario(request,turno_id):
    try:
        turno= Turno.objects.get(id=turno_id)
        turno.delete()
        messages.success(request, 'Su turno fue cancelado correctamente')
        return render(request, 'website/index.html')
    except Exception as e: 
        messages.error(request, 'El turno no pudo ser cancelado')

#ver turnos del dia
def verTurnosdelDia(request):
    # try:
    #     #list_turnos = Turno.objects.filter(fecha=datetime.date.today())
    #     list_turnos = Turno.objects.all()

    #     #return render(request, 'website/ver_turnos_delDia.html', {'list_turnos':list_turnos, 'fechaHoy':datetime.date.today()})
    #     #return render(request, 'website/ver_turnos_delDia.html', {})
    #     if (list_turnos):
    #         return render(request, 'website/ver_turnos_delDia.html', {
    #             'list_turnos':list_turnos
    #         })
    #     else:
    #         messages.error(request, 'No hay turnos del dia de hoy')
    #         return render(request, 'website/index.html',{})
    # except Exception as e:
    #     print(repr(e))
    list_turnos = Turno.objects.filter(fecha=datetime.date.today())
    class Auxiliar():
        def __init__(self):
            self.vacuna = None
            self.turnoid= None
            self.idvacuna=None
            self.idusuario=None
            self.nombre = None
            self.apellido = None
            self.estado = None
    arrAuxiliar = []
    if (list_turnos):
        for turno in list_turnos:
            user = Usuario.objects.get(id=turno.user.id)
            aux = Auxiliar()
            print(turno)
            print(turno.user.id)
            vacuna=Vacuna.objects.get(nombre=turno.vacuna)
            print(vacuna)
            print(vacuna.id)
            aux.turnoid=turno.id
            aux.idusuario=turno.user.id
            aux.idvacuna=vacuna.id
            aux.vacuna=turno.vacuna
            aux.nombre=user.nombre
            aux.apellido=user.apellido
            print(turno.estado)
            aux.estado=turno.estado.estado
            arrAuxiliar.append(aux)
        fechaHoy= datetime.date.today()
        fechaHoy=fechaHoy.strftime("%d/%m/%y")
        return render(request, 'website/ver_turnos_delDia.html', {
            'list_turnos':arrAuxiliar, 'fechaHoy':fechaHoy
        })
    else:
        messages.error(request, 'No hay turnos del dia de hoy')
        return render(request, 'website/index.html',{})

def buscar(request):
    if request.GET["dni"]:
        try:
            dni=request.GET.get("dni")
            dni.strip()
            print (dni)
            usuario=Usuario.objects.get(dni=dni)
            usuario_form=UpdateUsuarioForm(instance = usuario)
            usuario_form=usuario_form.deshabilitarCamposVacunador()
            id_usuario=usuario.id
            if not usuario:
                messages.error(request, "No se encontró un usuario con ese DNI")

            usuario=Usuario.objects.filter(dni=dni)
            return render(request, "website/verPerfil.html",{"usuario_form": usuario_form, 'id_usuario':id_usuario })
        except Exception as e:
            print(repr(e))   
            messages.error(request, "No se encontró un usuario con ese DNI")
            return render(request, "website/index.html",)
    else:
            messages.error(request, "No se ingresó una búsqueda")
            return render(request, "website/index.html",)
        
def marcarVacunado(request,user_id,vacuna_id, turno_id):
    try:
        vacunaUsuario= VacunaDeUsuario()
        vacuna=Vacuna.objects.get(id=vacuna_id)
        usuario=Usuario.objects.get(id=user_id)
        turno=Turno.objects.get(id=turno_id)
        turno.estado=EstadosTurno.objects.get(id="4")
        vacunaUsuario.vacuna=vacuna
        vacunaUsuario.user=usuario
        vacunaUsuario.save()
        turno.save()
        messages.success(request, "El usuario se ha marcado como vacunado")
        return redirect('index')
    except Exception as e:
        print(e)

def aceptarTurnos(request):
    try:
        print("estoy")
        list_turnos = Turno.objects.filter(estado_id=1)
        print("turnos")
        dic={}
        for turno in list_turnos:
            user= Usuario.objects.get(id=turno.user_id)
            print("user")
            print(user.id)
            print(turno.user_id)
            print(turno.id)
            dic[turno.id]=user
            print(dic[turno.id].nombre)
        print("for")
        fecha_form=CreateForm()
        return render(request, "website/ver_turnos_aceptables.html",{"list_turnos":list_turnos, 'dic':dic, fecha_form:fecha_form })

    except Exception as e:
        print(e)
        
def RechazarTurnoUsuario(request,turno_id):
    try:
        turno= Turno.objects.get(id=turno_id)
        turno.estado_id= EstadosTurno.objects.get(id="3")
        turno.save()
        messages.success(request, 'El turno fue rechazado correctamente')
        return render(request, 'website/index.html')
    except Exception as e: 
        messages.error(request, 'El turno no pudo ser rechazado')

def verEstadisticas (request):
    vacunas = Vacuna.objects.all()
    vacunatorios = Vacunatorio.objects.all()
    datosGenerales = []
    for vacunatorio in vacunatorios:
        datosLocales = []
        datosLocales.append(vacunatorio.nombre+" en "+vacunatorio.ubicacion)
        datosVacunatorio = []
        for vacuna in vacunas:
            datosVacuna = []
            valor=0
            turno = Turno.objects.filter(vacuna=vacuna.nombre).filter(vacunatorio_id=vacunatorio.id)
            if (turno is not None):
                valor = len(turno)
            datosVacuna.append(vacuna.nombre)
            datosVacuna.append(valor)
            datosVacunatorio.append(datosVacuna)
        datosLocales.append(datosVacunatorio)
        datosGenerales.append(datosLocales)
    return render(request,"website/ver_estadisticas.html",{"datosGenerales":datosGenerales})
