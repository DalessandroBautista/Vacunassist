import datetime
from datetime import datetime, timedelta
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
            if(usuario.es_vacunador==True):
                usuario_form =UpdateVacunadorAdministradorForm(request.POST, instance = usuario)
            else:
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
            id_usuario=request.user.id
            mismoUsuario= (id_usuario == usuario.id)
            print("1")
            if(usuario.es_vacunador==True or usuario.es_administrador==True):
                usuario_form=UpdateVacunadorAdministradorForm(instance = usuario)
                if(usuario.es_administrador==True):
                    print("administrador")
                    usuario_form=usuario_form.deshabilitarCamposAdministrador()
                   
                else:
                    print("vacunador")
                    usuario_form=usuario_form.deshabilitarCampos()
                return render(request, "website/ver_perfil_vacunador.html",{ 'usuario_form':usuario_form, 'id_usuario':id_usuario,'mismoUsuario':mismoUsuario, 'busqueda': False})
            else:
                usuario_form=UpdateUsuarioForm(instance = usuario)
                usuario_form=usuario_form.deshabilitarCampos(usuario.identidad_verificada)

        return render(request, "website/verPerfil.html",{ 'usuario_form':usuario_form, 'id_usuario':id_usuario, 'mismoUsuario':mismoUsuario})
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
        vacuna= Vacuna.objects.get(nombre='Covid-19')
        turnos=Turno.objects.filter(user_id=user.id).filter(vacuna=vacuna.id)
        print(not turnos)
        if ((((date.today().year-user.fecha_nacimiento.year)>18) &  (not turnos)) &  (user.residencia=="La Plata") ):
            t = Turno(user=request.user, vacuna=vacuna, estado=EstadosTurno(id=1),  vacunatorio=Vacunatorio(id=request.user.vacunatorio_preferencia_id))
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
        vacuna= Vacuna.objects.get(nombre="Gripe A")
        turnos=Turno.objects.filter(user_id=user.id).filter(vacuna=vacuna.id)
        print(not turnos)
        if ((not turnos) &  (user.residencia=="La Plata") ):
            messages.success(request,"Se ha solicitado un turno la para vacuna de la Gripe A exitosamente")
            t = Turno(user=request.user, vacuna=vacuna, estado=EstadosTurno(id=1),  vacunatorio=Vacunatorio(id=request.user.vacunatorio_preferencia_id))
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
        vacuna1ra= Vacuna.objects.get(nombre="Covid-19")
        vacuna= Vacuna.objects.get(nombre="Covid-19 2da Dosis")
        turnos=Turno.objects.filter(user_id=user.id).filter(vacuna=vacuna.id)
        primera_dosis= VacunaDeUsuario.objects.filter(user_id=user.id).filter(vacuna=vacuna1ra.id)

        if ((not turnos) &  (user.residencia=="La Plata") & (not(not primera_dosis))) :
            messages.success(request,"Se ha solicitado un turno la para vacuna de Covid-19 2da Dosis exitosamente")
            t = Turno(user=request.user, vacuna=vacuna,estado=EstadosTurno(id=1),  vacunatorio=Vacunatorio(id=request.user.vacunatorio_preferencia_id))
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
        vacunatorio= usuario.vacunatorio_preferencia
        lista_turnos= Turno.objects.filter(user_id=user_id).filter(estado=2)
        print(lista_turnos)
        if (lista_turnos):
            return render(request, 'website/ver_turnos.html', {
                'lista_turnos':lista_turnos,
                'vacunatorio':vacunatorio
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
        class Auxiliar():
            def __init__(self):
                self.vacuna = None
                self.fecha= None
                self.vacunaDeUsuario= None
            
        user_id = request.user.id
        print(user_id)
        id_vacunas= VacunaDeUsuario.objects.filter(user_id=user_id)
        lista_vacunas=[]
        print(id_vacunas)
        for vacuna in id_vacunas:
            aux= Auxiliar()
            aux.vacuna=(Vacuna.objects.get(id=vacuna.vacuna_id))
            aux.fecha=vacuna.fecha
            aux.vacunaDeUsuario=vacuna.id
            lista_vacunas.append(aux)
            
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
        datos=VacunaDeUsuario.objects.get(id=vacuna_id)
        vacuna=Vacuna.objects.get(id=datos.vacuna.id)
        fecha=datos.fecha
        buffer = io.BytesIO()

        p = canvas.Canvas(buffer)

        mensaje= "Este documento certifica que usted se vacunó para: " + vacuna.nombre + " el día " + str(fecha)
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
            cargar_vacuna_form.fields['vacuna'].initial = Vacuna.objects.get(id=1)
           

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
        
def usuarioAusente(request,turno_id):
    try:
        turno= Turno.objects.get(id=turno_id)
        turno.estado_id=6
        turno.save()
        messages.success(request, 'El turno del usuario fue marcado como ausente ')
        return render(request, 'website/index.html')
    except Exception as e: 
        messages.error(request, 'El turno no pudo ser marcado como ausente')

def usuarioNoAusente(request,turno_id):
    try:
        turno= Turno.objects.get(id=turno_id)
        turno.estado_id=2
        turno.save()
        messages.success(request, 'El turno del usuario fue desmarcado como ausente ')
        return render(request, 'website/index.html')
    except Exception as e: 
        messages.error(request, 'El turno no pudo ser desmarcado como ausente')
#ver turnos del dia
def verTurnosdelDia(request):
    list_turnos = Turno.objects.filter(fecha=datetime.date.today()).filter(vacunatorio_id=request.user.vacunatorio_preferencia_id)
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
            print(turno.estado_id)
            vacuna=Vacuna.objects.get(id=turno.vacuna.id)
            aux.turnoid=turno.id
            aux.idusuario=turno.user.id
            aux.idvacuna=vacuna.id
            aux.vacuna=vacuna.nombre
            aux.nombre=user.nombre
            aux.apellido=user.apellido
            print(turno.estado)
            aux.estado=turno.estado.estado
            arrAuxiliar.append(aux)
        fechaHoy= datetime.date.today()
        fechaHoy=fechaHoy.strftime("%d/%m/%y")
        return render(request, 'website/ver_turnos_delDia.html', {
            'list_turnos':arrAuxiliar, 'fechaHoy':fechaHoy,'turnos':True
        })
    else:
        fechaHoy= datetime.date.today()
        fechaHoy=fechaHoy.strftime("%d/%m/%y")
        return render(request, 'website/ver_turnos_delDia.html', {
            'list_turnos':arrAuxiliar, 'fechaHoy':fechaHoy, 'turnos':False
        })
def buscar(request):
    if request.GET["dni"]:
        usuarioActualId=request.user.id
        try:
            dni=request.GET.get("dni")
            dni.strip()
            print (dni)
            usuario=Usuario.objects.get(dni=dni)
            mismoUsuario= (usuarioActualId==usuario.id)
            if(usuario.es_vacunador ==True):
                usuario_form=UpdateVacunadorAdministradorForm(instance = usuario)
                usuario_form=usuario_form.deshabilitarCamposAdministrador()
                id_usuario=usuario.id
                return render(request, "website/ver_perfil_vacunador.html",{"usuario_form": usuario_form, 'id_usuario':id_usuario, 'mismoUsuario':mismoUsuario, 'busqueda':True})
            else:
                
                usuario_form=UpdateUsuarioForm(instance = usuario)
                usuario_form=usuario_form.deshabilitarCamposVacunador()
                id_usuario=usuario.id
                usuario=Usuario.objects.filter(dni=dni)
                return render(request, "website/verPerfil.html",{"usuario_form": usuario_form, 'id_usuario':id_usuario })
        except Exception as e:
            print(repr(e))   
            messages.error(request, "No se encontró un usuario con ese DNI")
            return render(request, "website/index.html",)
    else:
            messages.error(request, "No se ingresó una búsqueda")
            return render(request, "website/index.html",)
        
def verPerfilUsuario(request, usuario_id):
        print("entre")
        try:
            usuario=Usuario.objects.get(id=usuario_id)
            usuario_form=UpdateUsuarioForm(instance = usuario)
            usuario_form=usuario_form.deshabilitarCamposVacunador()
            id_usuario=usuario.id
            if not usuario:
                messages.error(request, "No se encontró un usuario con ese DNI")

            return render(request, "website/verPerfil.html",{"usuario_form": usuario_form, 'id_usuario':id_usuario })
        except Exception as e:
            print(repr(e))   
            messages.error(request, "No se encontró un usuario con ese DNI")
            return render(request, "website/index.html",)
        
def marcarVacunado(request,user_id,vacuna_id, turno_id):
    try:
        vacunador_id=request.user.id
        vacunaUsuario= VacunaDeUsuario()
        vacuna=Vacuna.objects.get(id=vacuna_id)
        usuario=Usuario.objects.get(id=user_id)
        turno=Turno.objects.get(id=turno_id)
        turno.estado=EstadosTurno.objects.get(id="4")
        turno.vacunador=Usuario.objects.get(id=vacunador_id)
        vacunaUsuario.vacuna=vacuna
        vacunaUsuario.user=usuario
        vacunaUsuario.fecha=date.today()
        vacunaUsuario.save()
        turno.save()
        messages.success(request, "El usuario se ha marcado como vacunado")
        return redirect('index')
    except Exception as e:
        print(e)

def aceptarTurnos(request):
    print("Es un post")
    print(request.method=="POST")
    if(request.method=="POST"):
        print("adentro del post")
        try:
            nacimiento=request.POST.get("nacimiento")
            turno_id= request.POST.get("turno_id")
            fecha=request.POST.get("fecha_day") + "/" + request.POST.get("fecha_month") + "/" + request.POST.get("fecha_year")
            fechaturno=request.POST.get("fecha_year") + "-" + request.POST.get("fecha_month") + "-" + request.POST.get("fecha_day")
            print(fecha + nacimiento)
            nacimiento=datetime.datetime.strptime(nacimiento, '%d/%m/%Y')
            print(type(nacimiento))
            print(type(fecha))
            fecha=datetime.datetime.strptime(fecha, '%d/%m/%Y')
            fecha=fecha.date()
            
            if ((fecha>= date.today())):
                print("fecha del turno" + fechaturno)
                turno= Turno.objects.get(id=turno_id)
                turno.fecha=fechaturno
                turno.estado_id= EstadosTurno.objects.get(id="2")
                vacunatorio=request.POST.get("vacunatorio")
                turno.vacunatorio=Vacunatorio.objects.get(id=vacunatorio)
                turno.save()
                messages.success(request, 'El turno fue aceptado correctamente')
                return render(request, 'website/index.html')
            else:
                print("entre al else")
                messages.error(request, 'La fecha del turno debe ser igual o posterior a la fecha de hoy')
                return render(request, 'website/index.html')
        except Exception as e:
            print(e)
            messages.error(request, 'El turno no fue aceptado porque debe ser dentro de los 7 proximos dias')
        
    else:
        class Auxiliar():
            def __init__(self):
                self.vacuna = None
                self.idvacuna=None
                self.turnoid= None
                self.idusuario=None
                self.nombre = None
                self.apellido = None
                self.prioridad=None
                self.mensaje=None
                self.fecha_form =None
        arrAuxiliar = []
        try:
            list_turnos = Turno.objects.filter(estado_id=1)
            for turno in list_turnos:
                user= Usuario.objects.get(id=turno.user_id)
                aux = Auxiliar()
                print(turno.vacuna)
                vacuna=Vacuna.objects.get(id=turno.vacuna.id)
                
                aux.vacuna=vacuna.nombre
                aux.turnoid=turno.id
                aux.idusuario=user.id
                aux.nombre=user.nombre
                aux.apellido=user.apellido
                fecha_form=TurnoConPrioridad()
                if ((date.today().year-user.fecha_nacimiento.year)>60):
                    fecha_form.fields['fecha'].initial = date.today() + datetime.timedelta(7)
                    aux.mensaje= "Se sugiere un turno dentro de los próximos 7 días dado que esta persona es mayor de 60 años"
                    
                else:
                    fecha_form.fields['fecha'].initial = date.today() + datetime.timedelta(30)
                    aux.mensaje= "Se sugiere un turno dentro de 30 días si la persona no es paciente de riesgo, dado que esta persona no es mayor de 60 años"
                fecha_nacimiento=user.fecha_nacimiento
                fecha_actual = date.today()
                print("1")
                resultado = fecha_actual.year - fecha_nacimiento.year
                print("2")
                resultado -= ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month,fecha_nacimiento.day))
                print("3")
                fecha_form.fields['turno_id'].initial = aux.turnoid
                print("4")
                fecha_form.fields['edad'].initial = resultado
                print("5")
                fecha_form.fields['nacimiento'].initial = user.fecha_nacimiento
                print("6")
                fecha_form.fields['vacunatorio'].initial = user.vacunatorio_preferencia
                print("7")
                fecha_form=fecha_form.deshabilitarCampos()

                print("8")
                aux.fecha_form=fecha_form
                print(user.fecha_nacimiento)
                arrAuxiliar.append(aux)
            mensaje="Aceptar Turno"
            return render(request, "website/ver_turnos_aceptables.html",{"list_turnos":arrAuxiliar, "mensaje": mensaje, "modificacion": False })

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
    
    #Toda esta parte es para las estadisticas
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
            turno = Turno.objects.filter(vacuna_id=vacuna.id).filter(vacunatorio_id=vacunatorio.id).filter(estado_id=4)
            if (turno):
                valor = len(turno)
            datosVacuna.append(vacuna.nombre)
            datosVacuna.append(valor)
            datosVacunatorio.append(datosVacuna)
        datosLocales.append(datosVacunatorio)
        datosGenerales.append(datosLocales)
        
    #Toda esta parte es para listar vacunadores
    datosVacunadores = []
    for vacunatorio in vacunatorios: 
        vacunadores = Usuario.objects.filter(vacunatorio_preferencia_id=vacunatorio.id).filter(es_vacunador=True)
        datosLocales = []
        datosLocales.append(vacunatorio.nombre+" en "+vacunatorio.ubicacion)
        if (vacunadores):
            datosLocales.append(vacunadores)
        else:
            datosLocales.append(['Sin vacunadores en este vacunatorio'])
        datosVacunadores.append(datosLocales)
        
    return render(request,"website/ver_estadisticas.html",{"datosGenerales":datosGenerales, "datosVacunadores":datosVacunadores})
def verVacunadores(request):
    vacunatorios=Vacunatorio.objects.all()
    datosVacunadores = []
    for vacunatorio in vacunatorios: 
        vacunadores = Usuario.objects.filter(vacunatorio_preferencia_id=vacunatorio.id).filter(es_vacunador=True)
        datosLocales = []
        datosLocales.append(vacunatorio.nombre+" en "+vacunatorio.ubicacion)
        if (vacunadores):
            for vacunador in vacunadores:
                datosLocales.append(vacunador)
        else:
            datosLocales.append('Sin vacunadores en este vacunatorio')
        datosVacunadores.append(datosLocales)
        
    return render(request,'website/ver_vacunadores.html',{'datosVacunadores':datosVacunadores})
    
    
def verPerfilVacunador(request, usuario_id):
    usuario=Usuario.objects.get(id=usuario_id)
    if request.method=="POST":
            
            usuario_form =UpdateVacunadorAdministradorForm(request.POST, instance = usuario)

            if usuario_form.is_valid():
                try:
                    print('antes de guardar datos')
                    usuario_form.save()
                    print('en guardar datos')
                    messages.success(request, 'Perfil actualizado correctamente')
                    return redirect('index')
                except Exception as e: 
                    print(repr(e))
                    messages.error(request, 'El perfil no se ha actualizado.')
    else:
        id_usuario=usuario.id
        mismoUsuario=False
        usuario_form=UpdateVacunadorAdministradorForm(instance = usuario)
                
        usuario_form=usuario_form.deshabilitarCampos()
        
    return render(request, "website/ver_perfil_vacunador.html",{ 'usuario_form':usuario_form, 'id_usuario':id_usuario,'mismoUsuario':mismoUsuario, 'busqueda': False})

def verTurnosAcepados(request):
    class Auxiliar():
            def __init__(self):
                self.vacuna = None
                self.idturno= None
                self.nombre = None
                self.fecha =None
                self.vacunatorio=None
                self.idusuario = None
    arrAuxiliar = []
    list_turnos= Turno.objects.filter(estado_id=2)
    for turno in list_turnos:
                user= Usuario.objects.get(id=turno.user_id)
                aux = Auxiliar()
                vacuna=Vacuna.objects.get(id=turno.vacuna.id)
                aux.vacuna=vacuna.nombre
                aux.idturno=turno.id
                print(turno.id)
                aux.idusuario=user.id
                aux.nombre=user.nombre + " " + user.apellido
                aux.fecha=turno.fecha
                vacunatorio=Vacunatorio.objects.get(id=turno.vacunatorio_id)
                aux.vacunatorio=vacunatorio.ubicacion

                arrAuxiliar.append(aux)
    return render(request,"website/ver_turnos_aceptados.html",{"list_turnos":arrAuxiliar})

def modificarTurno(request,turno_id):
        if(request.method=="POST"):
            print("adentro del post")
            try:
                nacimiento=request.POST.get("nacimiento")
                turno_id= request.POST.get("turno_id")
                fecha=request.POST.get("fecha_day") + "/" + request.POST.get("fecha_month") + "/" + request.POST.get("fecha_year")
                fechaturno=request.POST.get("fecha_year") + "-" + request.POST.get("fecha_month") + "-" + request.POST.get("fecha_day")
                print(nacimiento)
                print(turno_id)
                print(fecha)
                print(fechaturno)
                
                
                print(fecha + nacimiento)
                nacimiento=datetime.datetime.strptime(nacimiento, '%d/%m/%Y')
                print(type(nacimiento))
                print(type(fecha))
                fecha=datetime.datetime.strptime(fecha, '%d/%m/%Y')
                fecha=fecha.date()
                
                if ((fecha>= date.today())):
                    print("fecha del turno" + fechaturno)
                    turno= Turno.objects.get(id=turno_id)
                    turno.fecha=fechaturno
                    turno.estado_id= EstadosTurno.objects.get(id="2")
                    vacunatorio=request.POST.get("vacunatorio")
                    turno.vacunatorio=Vacunatorio.objects.get(id=vacunatorio)
                    turno.save()
                    messages.success(request, 'El turno fue modificado correctamente')
                    return render(request, 'website/index.html')
                else:
                    print("entre al else")
                    messages.error(request, 'La fecha del turno debe ser igual o posterior a la fecha de hoy')
                    return render(request, 'website/index.html')
            except Exception as e:
                print(e)
                messages.error(request, 'El turno no fue modificado porque debe ser dentro de los 7 proximos dias')
        
        else:
            print("else")
            class Auxiliar():
                    def __init__(self):
                        self.vacuna = None
                        self.idvacuna=None
                        self.turnoid= None
                        self.idusuario=None
                        self.nombre = None
                        self.apellido = None
                        self.prioridad=None
                        self.mensaje=None
                        self.fecha_form =None
            
            
            try:
                    turno= Turno.objects.get(id=turno_id)
                    arrAuxiliar = []
                    user= Usuario.objects.get(id=turno.user_id)
                    vacunatorio=Vacunatorio.objects.get(id=turno.vacunatorio_id)
                    aux = Auxiliar()
                    vacuna=Vacuna.objects.get(id=turno.vacuna.id)
                    aux.vacuna=vacuna.nombre
                    aux.turnoid=turno.id
                    aux.idusuario=user.id
                    aux.nombre=user.nombre
                    aux.apellido=user.apellido
                    fecha_form=TurnoConPrioridad()
                    if ((date.today().year-user.fecha_nacimiento.year)>60):
                        aux.mensaje= "Se sugiere un turno dentro de los próximos 7 días dado que esta persona es mayor de 60 años"
                        
                    else:
                        aux.mensaje= "Se sugiere un turno dentro de 30 días si la persona no es paciente de riersgo, dado que esta persona no es mayor de 60 años"
                    fecha_nacimiento=user.fecha_nacimiento
                    fecha_form.fields['fecha'].initial = turno.fecha
                    fecha_actual = date.today()
                    resultado = fecha_actual.year - fecha_nacimiento.year
                    resultado -= ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month,fecha_nacimiento.day))
                    fecha_form.fields['turno_id'].initial = aux.turnoid
                    fecha_form.fields['edad'].initial = resultado
                    fecha_form.fields['nacimiento'].initial = user.fecha_nacimiento
                    fecha_form.fields['vacunatorio'].initial = vacunatorio
                    fecha_form=fecha_form.deshabilitarCampos()
                    aux.fecha_form=fecha_form
                    arrAuxiliar.append(aux)
                    mensaje="Modificar Turno"
                    return render(request, "website/ver_turnos_aceptables.html",{"list_turnos":arrAuxiliar, "modificacion": True, "mensaje":mensaje })
            except Exception as e:
                print(e)

def añadirPersona(request):
    if(request.method=="POST"):
        try:
            dni=request.POST.get("user")
            user= Usuario.objects.get(dni=dni)
            vacuna=request.POST.get("vacuna")
            vacunatorio=request.POST.get("vacunatorio")
            turno= Turno()
            vacuna=Vacuna.objects.get(id=vacuna)
            turno.vacuna=vacuna
            vacunatorio=Vacunatorio.objects.get(id=vacunatorio)
            turno.vacunatorio_id=vacunatorio.id
            turno.estado_id=4
            turno.user_id=user.id
            turno.fecha=date.today()
            vacunaUsuario= VacunaDeUsuario()
            vacunaUsuario.vacuna=vacuna
            vacunaUsuario.user=user
            vacunaUsuario.fecha=date.today()
            existe=Turno.objects.filter(user_id=user.id).filter(vacuna_id=vacuna.id).filter(fecha=date.today())
            if(not existe):
                turno.save()
                vacunaUsuario.save()
                messages.success(request,"El turno fue cargado con exito")
                return render(request,"website/index.html")
            else:
                messages.errir(request,"Ya existe un turno de este usuario para esta vacuna para el día de hoy")
                return render(request,"website/index.html")
        except Exception as e:
            print(e)
            form=AñadirTurnoUsuario()
            messages.error(request, "El usuario con DNI: " + dni + " no se encuentra registrado en el sistema. Por favor registrelo y luego añadalo como vacunado.")
            return render(request,"website/añadir_turno_persona.html",{"form":form})
    else:
        form=AñadirTurnoUsuario()
        return render(request,"website/añadir_turno_persona.html",{"form":form})
def registrarDesdeVacunador(request):
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
            messages.success(request, "Se has registrado al usuario exitosamente")  
            form=AñadirTurnoUsuario()
            return render(request,"website/añadir_turno_persona.html",{"form":form}) 
    else:
        form = FormularioUsuario()
    return render(request, 'website/registrar_desde_vacunador.html', {
        'form': form
        })

def eliminarVacunador(request, id_usuario):
    user= Usuario.objects.get(id=id_usuario)
    user.delete()
    messages.success(request, "El vacunador fue eliminado con exito")
    return render(request,"website/index.html")
    
def verVacunadosXvacunador(request,usuario_id):
    turnos = Turno.objects.filter(estado_id=4).filter(vacunador_id=usuario_id)
    return render (request, 'website/ver_vacunadosXvacunador.html',{'turnos':turnos})

def verHistorico(request):
    turnos = Turno.objects.filter(estado_id=4).order_by('user_id')
    if (turnos):
        return render (request, 'website/ver_historico.html',{'turnos':turnos})
    else:
        messages.error(request, 'Aun no hay vacunados')

def verTurnosCancelados (request):
    turnos = Turno.objects.filter(estado_id=5)
    if (turnos):
        return render(request, 'website/verTurnosCancelados.html', {'turnos':turnos})
    else:
        messages.error(request, 'No hay turnos cancelados el dia de hoy')