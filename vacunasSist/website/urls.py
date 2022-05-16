from django.urls import path, re_path
from . import views


from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('',views.index, name="index"),
    path('register', views.registrarse, name="register"),
    path('login', LoginView.as_view(template_name="website/registration/login.html"), name="login"),
    path('logout', LogoutView.as_view(template_name="website/registration/logged_out.html"), name="logout"),
    path('password_reset', views.password_reset, name="password_reset"),

]
