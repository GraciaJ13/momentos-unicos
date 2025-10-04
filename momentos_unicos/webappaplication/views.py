
from django.shortcuts import redirect, render
from Personas.models import Persona
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import RegistroNoviosForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Intentamos autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Inicia la sesión

            # Comprobamos a qué grupo pertenece el usuario y redirigimos a una página específica
            if user.groups.filter(name='admin_group').exists():
                # Redirigir a una página específica para administradores (cambia esta URL a la que quieras)
                return redirect('admin_page')  # Redirigir a la página del administrador
            elif user.groups.filter(name='novios').exists():
                # Redirigir a una página específica para usuarios (cambia esta URL a la que quieras)
                return redirect('paginanovios')  # Redirigir a la página del usuario
            elif user.groups.filter(name='moderator_group').exists():
                # Redirigir a una página específica para moderadores (cambia esta URL a la que quieras)
                return redirect('moderator_page')  # Redirigir a la página del moderador
            else:
                # Redirigir a la página principal o cualquier otra página predeterminada si no está en un grupo
                return redirect('home')  # Página de inicio

        else:
            # Si las credenciales no son correctas
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'login.html')

# Vista principal
def paginaprincipal(request):
    return render(request, 'paginaprincipal.html')

# Vista para listar personas
def listarpersonas(request):
    personas = Persona.objects.all()
    return render(request, 'listapersonas.html', {'personas': personas})

# Vista protegida para novios
#@login_required
def pagina_novios(request):
    return render(request, 'paginanovios.html')

# Vista protegida para invitados
@login_required
def pagina_invitados(request):
    return render(request, 'paginainvitados.html')

# Vista para redireccionar según grupo
#@login_required
#def redirect_dashboard(request):
#    return redireccion_por_grupo(request.user)


# Vista de registro para novios
def registro_novios(request):
    if request.method == "POST":
        form = RegistroNoviosForm(request.POST)
        if form.is_valid():
            persona = form.save()
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()

            grupo_novios, created = Group.objects.get_or_create(name="novios")
            user.groups.add(grupo_novios)

            auth_login(request, user)
            return redirect("pagina_novios")
    else:
        form = RegistroNoviosForm()

    return render(request, "registro.html", {"form": form})