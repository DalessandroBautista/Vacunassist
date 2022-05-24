from django.urls import path, re_path
from . import views


from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('',views.index, name="index"),
    path('register', views.registrarse, name="register"),
    path('login', views.login, name="login"),
    path('verPerfil', views.verPerfil, name="verPerfil"),
    path('logout', LogoutView.as_view(template_name="website/registration/logged_out.html"), name="logout"),
    path('password_reset', views.password_reset, name="password_reset"),
    path('modificar_password', views.modificar_password, name="modificar_password"),
    path('solicitar_turno',views.solicitarTurno, name="solicitar_turno"),
    path('solicitar_turno_covid',views.solicitarTurnoCovid, name="solicitar_turno_covid"),
    path('solicitar_turno_gripe',views.solicitarTurnoGripe, name="solicitar_turno_gripe"),
    path('ver_turnos_pendientes',views.verTurnosPendientes, name="ver_turnos_pendientes"),
    path('ver_turnos',views.verTurnos, name="ver_turnos"),
    path('ver_vacunas_aplicadas',views.verVacunasAplicadas, name="ver_vacunas_aplicadas"),
    path('certificado/<int:vacuna_id>/',views.obtenerCertificado, name="certificado"),
    path('informacion_vacuna', views.verInformacion, name="informacion_vacuna"),

]
