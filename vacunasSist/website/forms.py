from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from website.models import Usuario
from django.contrib.auth.forms import AuthenticationForm
class FormularioContacto(forms.Form):
    asunto=forms.CharField(label="Asunto",required=True)
    email=forms.EmailField(label="Emai",required=True)
    mensaje=forms.CharField(label="Contenido", widget=forms.Textarea)
    


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario', widget=forms.TextInput(attrs={'class': 'usuario'}), max_length=150, required=True, )
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput(), max_length=30, required=True, )

class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class FormularioUsuario(forms.ModelForm):
    
    password1= forms.CharField(label="Contraseña", widget= forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese su contraseña',
            'required': 'required'
        }
        ))
    password2= forms.CharField(label="Verificacion de contraseña", widget= forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Repita su contraseña',
            'required': 'required'
        }
        ))
    
    class Meta:
        model= Usuario
        fields=('username', 'email', 'nombre', 'apellido', 'dni', 'fecha_nacimiento')
        widgets= {
            'username': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su nombre de usuario'
                    }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su email'
                    }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su nombre'
                    }
            ),
            'apellido': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su apellido'
                    }
            ),
            'dni': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su DNI'
                    }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su fecha de nacimiento'
                    }
            )
        }
    def clean_password2(self):
        """ Validación de Contraseña
        Metodo que valida que ambas contraseñas ingresadas sean igual, esto antes de ser encriptadas
        y guardadas en la base dedatos, Retornar la contraseña Válida.
        Excepciones:
        - ValidationError -- cuando las contraseñas no son iguales muestra un mensaje de error
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2

    def save(self,commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
class FormularioDatosDePerfil(forms.ModelForm):
    class Meta:
        model= Usuario
        fields=('username', 'email', 'nombre', 'apellido', 'dni', 'fecha_nacimiento', 'residencia', 'vacunatorio_preferencia', 'historial_vacunacion')
        widgets= {
            'username': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su nombre de usuario'
                    }
            )}