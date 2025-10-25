# forms.py
from django import forms
from Personas.models import Persona
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from Personas.models import Boda, Proveedor, Invitado, Regalo, Cancion
class PersonaForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Persona
        fields = ["nombre", "apellido", "email", "cedula", "username", "password"]

    def save(self, commit=True):
        persona = super().save(commit=False)
        # Guardar la contraseña como hash
        persona.password_hash = make_password(self.cleaned_data["password"])
        if commit:
            persona.save()
        return persona
class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    
class RegistroNoviosForm(forms.ModelForm):
    username = forms.CharField(max_length=50, label="Usuario")
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar contraseña"
    )

    class Meta:
        model = Persona
        fields = ["nombre", "apellido", "cedula", "email"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Crear primero el User
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password1"],  # 👈 usamos password1
            email=self.cleaned_data["email"]
        )

        # Guardar Persona enlazada a User
        persona = super().save(commit=False)
        persona.user = user
        if commit:
            persona.save()
        return user

class BodaForm(forms.ModelForm):
    class Meta:
        model = Boda
        fields = ['nombre_boda', 'fecha_boda', 'lugar', 'codigo_boda']

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'servicio', 'contacto', 'telefono', 'email', 'url']

class InvitadoForm(forms.ModelForm):
    class Meta:
        model = Invitado
        fields = ['nombre', 'email', 'telefono', 'boda', 'invitado_registrado_por', 'regalo']

class RegaloForm(forms.ModelForm):
    class Meta:
        model = Regalo
        fields = ['nombre', 'descripcion', 'precio', 'url', 'estado', 'boda_id']

class CancionForm(forms.ModelForm):
    class Meta:
        model = Cancion
        fields = ['nombre', 'artista', 'invitado', 'boda']