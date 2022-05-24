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
        fields=('username', 'email', 'nombre', 'apellido', 'dni', 'fecha_nacimiento', 'identidad_verificada')
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
            ),
            'identidad_verificada': forms.CheckboxInput(   
                attrs={
                    'placeholder':'Cliquee el botón si desea verificar su identidad'
                    }
            ),
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
    
class UpdateUsuarioForm(forms.ModelForm):
    class Meta:
        model= Usuario
        fields=('username', 'email', 'nombre', 'apellido', 'dni', 'identidad_verificada', 'fecha_nacimiento', 'residencia', 'vacunatorio_preferencia',)
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
             'identidad_verificada': forms.CheckboxInput(   
                attrs={
                    'placeholder':'Cliquee el botón si desea verificar su identidad'
                    }
            ),
            'fecha_nacimiento': forms.DateInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su fecha de nacimiento'
                    }
            ),
            'residencia': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su ciudad de residencia'
                    }
            ),
            'vacunatorio': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su nuevo nombre de usuario'
                    }
            ),         
            }
    def deshabilitarCampos(self, identidad):
        if identidad:
            print(' if verificado')
            #self.fields['identidad_verificada','dni','email','fecha_nacimiento','nombre','apellido'].widget.attrs.update({'disabled': True})
            self.fields['identidad_verificada'].widget.attrs.update({'disabled': True})
            self.fields['dni'].widget.attrs.update({'readonly': True})
            self.fields['email'].widget.attrs.update({'readonly': True})
            self.fields['fecha_nacimiento'].widget.attrs.update({'readonly': True})
            self.fields['nombre'].widget.attrs.update({'readonly': True})
            self.fields['apellido'].widget.attrs.update({'readonly': True})
            #self.fields['nombre'].disabled = True
        return self
    def save(self):
        user = self.instance
        user.username= self.cleaned_data['username']
        user.email= self.cleaned_data['email']
        user.nombre= self.cleaned_data['nombre']
        user.apellido = self.cleaned_data['apellido']
        user.dni= self.cleaned_data['dni']
        user.identidad_verificada= self.cleaned_data['identidad_verificada']
        user.fecha_nacimiento= self.cleaned_data['fecha_nacimiento']
        user.residencia= self.cleaned_data['residencia']
        user.vacunatorio_preferencia= self.cleaned_data['vacunatorio_preferencia']
        user.save()
        return user


class UpdatePasswordForm(forms.ModelForm):
    password2= forms.CharField(label="Verificacion de contraseña", widget= forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Repita su contraseña',
            'required': 'required'
        }
        ))
                                   
    class Meta:
        model= Usuario
        fields=('password',)
        widgets= {
            'password': forms.PasswordInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su nueva contraseña'
                    }
            ),
            'password2': forms.PasswordInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Repita su nueva contraseña'
                    }
            )       
        }
        
        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 != password2:
                raise forms.ValidationError('Contraseñas no coinciden!')
            return password2
        
        
                
class FormularioEmail(forms.ModelForm):
    password1= forms.CharField(label="Contraseña")
    class Meta:
        model= Usuario
        fields=('email',)
        widgets= {
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese su email'
                    }
            )
        }
    def save(self,commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    def save(self):
        user= self.instance
        user.set_password(self.cleaned_data['password1'])
        user.save()
        return user

