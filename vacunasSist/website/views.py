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
    print("nice register")
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()          
            return HttpResponseRedirect(reverse('login'))
    else:
        form = RegistroForm()
    return render(request, 'website/registration/registro.html', {
        'form': form
        })

def login(request):
    print("el formulario es algo")
    if request.method=="POST":
       form=LoginForm(request.POST)
       
       if form.is_valid():
           print("el formulario es valido")
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
