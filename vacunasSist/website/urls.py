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



]
