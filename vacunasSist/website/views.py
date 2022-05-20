from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .forms import *
from django.core.mail import send_mail
from django.conf import settings

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
            print("request email")
            print(request.POST.get("email"))
            print("request post")
            print(request.POST)
            print(" email")
            print(mail)          
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
    print("estoy en login")
    if request.method=="POST":
       form=FormularioLogin(request.POST)
       print(form)
       if form.is_valid():
           return render(request, "website/index.html")
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
    return render(request, "website/registration/password_reset_confirm.html",{
    })
