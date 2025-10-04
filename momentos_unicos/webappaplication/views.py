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
def login_view(request):
    # Verificamos si es una solicitud POST (formulario de inicio de sesión)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Intentamos autenticar al usuario
        user = authenticate(request, username=username, password=password)

        # Verificamos si la autenticación es exitosa
        if user is not None:
            auth_login(request, user)  # Iniciamos sesión con el usuario autenticado

            # Redirigimos según el grupo al que pertenece el usuario
            if user.groups.filter(name='admin_group').exists():
                return redirect('admin_page')  # Redirigir a la página del administrador
            elif user.groups.filter(name='novios').exists():
                return redirect('paginanovios')  # Redirigir a la página de los novios
            elif user.groups.filter(name='invitados').exists():
                return redirect('paginavisitante')  # Redirigir a la página de invitados
            else:
                return redirect('paginaprincipal')  # Página predeterminada si no pertenece a ningún grupo

        else:
            # Si las credenciales son incorrectas, renderizamos el formulario de login con el error
            messages.error(request, "Credenciales incorrectas")
            return render(request, 'login.html')

    # Si es una solicitud GET (solo mostrar el formulario de login)
    return render(request, 'login.html')


# Vista principal (página de inicio)
def paginaprincipal(request):
    return render(request, 'paginaprincipal.html')


# Vista para listar personas
def listarpersonas(request):
    personas = Persona.objects.all()
    return render(request, 'listapersonas.html', {'personas': personas})


# Vista protegida para novios
@login_required
@user_passes_test(is_novios)
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
