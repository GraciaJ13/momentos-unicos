from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegistroNoviosForm
from Personas.models import Persona
# Helper function to check if user is in the 'novios' group
def is_novios(user):
    return user.groups.filter(name='novios').exists()

# Helper function to check if user is in the 'invitados' group
def is_invitados(user):
    return user.groups.filter(name='invitados').exists()

# Vista de login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login_view(request, user)
            # Redirección según grupo
            if user.groups.filter(name='novios').exists():
                return redirect('paginanovios')
            else:
                return redirect('paginaprincipal')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')


def grupo_novios_requerido(view_func):
    decorated_view_func = login_required(
        user_passes_test(lambda u: u.groups.filter(name='novios').exists())(view_func)
    )
    return decorated_view_func

def grupo_novios_requerido(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.groups.filter(name='novios').exists():
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect('paginaprincipal')
        return view_func(request, *args, **kwargs)
    return wrapper

# Vista principal (página de inicio)
def paginaprincipal(request):
    return render(request, 'paginaprincipal.html')


# Vista para listar personas
def listarpersonas(request):
    personas = Persona.objects.all()
    return render(request, 'listapersonas.html', {'personas': personas})


# Vista protegida para novios
@grupo_novios_requerido
def pagina_novios(request):
    return render(request, 'paginanovios.html')


# Vista protegida para invitados
@login_required
@user_passes_test(is_invitados)
def pagina_invitados(request):
    return render(request, 'paginavisitante.html')


# Vista de registro para novios
def registro_novios(request):
    if request.method == "POST":
        form = RegistroNoviosForm(request.POST)
        if form.is_valid():
            persona = form.save()
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            # Asignamos al usuario al grupo 'novios'
            grupo_novios, created = Group.objects.get_or_create(name="novios")
            user.groups.add(grupo_novios)

            # Iniciamos sesión y redirigimos a la página de novios
            auth_login(request, user)
            return redirect("paginanovios")
    else:
        form = RegistroNoviosForm()

    return render(request, "registro.html", {"form": form})
