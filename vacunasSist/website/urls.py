from django.urls import path, re_path
from . import views


from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import include, re_path



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
    path('ver_historial_vacunacion/<int:historial_vacuna_id2>/eliminar_vacuna_usuario/<int:historial_vacuna_id>/',views.EliminarVacunaUsuario, name="eliminar_vacuna_usuario"),
    path('cancelar_turno_usuario/<int:turno_id>/',views.CancelarTurnoUsuario, name="cancelar_turno_usuario"),
    path('ver_turnos_delDia',views.verTurnosdelDia, name="ver_turnos_delDia"),
    path('busqueda/', views.buscar, name="buscar"),
    path('marcar_vacunado/<int:user_id>/<int:vacuna_id>/<int:turno_id>/',views.marcarVacunado, name="marcar_vacunado"),
    path('aceptar_turnos',views.aceptarTurnos, name="aceptar_turnos"),
    path('rechazar_turno_usuario/<int:turno_id>/',views.RechazarTurnoUsuario, name="rechazar_turno_usuario"),
    path('ver_perfil_usuario/<int:usuario_id>/',views.verPerfilUsuario, name="ver_perfil_usuario"),
    path('ver_estadisticas',views.verEstadisticas, name="ver_estadisticas"),
    path('ver_turnos_aceptados', views.verTurnosAcepados, name="ver_turnos_aceptados"),
    path('modificar_turno/<int:turno_id>/', views.modificarTurno, name="modificar_turno"),
    path('añadir_persona', views.añadirPersona, name="añadir_persona"),
    path('registrar_desde_vacunador', views.registrarDesdeVacunador, name="registrar_desde_vacunador"),
    path('usuario_ausente/<int:turno_id>',views.usuarioAusente, name="usuario_ausente"),
    path('usuario_no_ausente/<int:turno_id>',views.usuarioNoAusente, name="usuario_no_ausente"),
    path('ver_perfil_vacunador/<int:usuario_id>/',views.verPerfilVacunador, name="ver_perfil_vacunador"),
    path('ver_vacunadores',views.verVacunadores, name="ver_vacunadores"),
    path('ver_vacunadosXvacunador/<int:usuario_id>', views.verVacunadosXvacunador, name="ver_vacunadosXvacunador"),
    path('ver_historico',views.verHistorico, name="ver_historico"),
    path('ver_cancelados',views.verTurnosCancelados, name="ver_cancelados"),
    path('registrar_vacunador',views.registrarVacunador, name="registrar_vacunador"),
    path('ver_perfil_vacunador/<int:id_usuarios>/eliminar_vacunador/<int:id_usuario>/',views.eliminarVacunador, name="eliminar_vacunador"),

]
