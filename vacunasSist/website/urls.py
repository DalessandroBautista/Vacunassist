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
    path('solicitar_turno_covid2',views.solicitarTurnoCovid2, name="solicitar_turno_covid2"),
    path('solicitar_turno_gripe',views.solicitarTurnoGripe, name="solicitar_turno_gripe"),
    path('ver_turnos_pendientes',views.verTurnosPendientes, name="ver_turnos_pendientes"),
    path('ver_turnos',views.verTurnos, name="ver_turnos"),
    path('ver_vacunas_aplicadas',views.verVacunasAplicadas, name="ver_vacunas_aplicadas"),
    path('certificado/<int:vacuna_id>/',views.obtenerCertificado, name="certificado"),
    path('informacion_vacuna', views.verInformacion, name="informacion_vacuna"),
    path('requisitos_vacunas', views.verRequisitos, name="requisitos_vacunas"),
    path('cargar_vacuna', views.cargarVacuna, name="cargar_vacuna"),
    path('ver_historial_vacunacion/<int:usuario_id>/',views.verHistorialVacunacion, name="ver_historial_vacunacion"),
    path('eliminar_vacuna_usuario/<int:historial_vacuna_id>/',views.EliminarVacunaUsuario, name="eliminar_vacuna_usuario"),
    path('cancelar_turno_usuario/<int:turno_id>/',views.CancelarTurnoUsuario, name="cancelar_turno_usuario"),
    path('ver_turnos_delDia',views.verTurnosdelDia, name="ver_turnos_delDia"),
    path('busqueda/', views.buscar, name="buscar"),
    path('marcar_vacunado/<int:user_id>/<int:vacuna_id>/<int:turno_id>/',views.marcarVacunado, name="marcar_vacunado"),
    path('aceptar_turnos',views.aceptarTurnos, name="aceptar_turnos"),
    path('rechazar_turno_usuario/<int:turno_id>/',views.RechazarTurnoUsuario, name="rechazar_turno_usuario"),
    path('ver_estadisticas',views.verEstadisticas, name="ver_estadisticas"),
]
