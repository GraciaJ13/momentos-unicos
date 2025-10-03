
from django.shortcuts import redirect, render
from Personas.models import Persona
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import RegistroNoviosForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User


# Función auxiliar para redirección por grupo
def redireccion_por_grupo(user):
    if user.groups.filter(name='novios').exists():
        return redirect('pagina_novios')
    elif user.groups.filter(name='invitados').exists():
        return redirect('pagina_invitados')
    else:
        return redirect('home')

# Vista de login refactorizada
def login_view(request):
    print("Entró a login_view")
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            print("Usuario autenticado:", user.username)
            return redireccion_por_grupo(user)
        else:
            print("Error de autenticación")
            return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas'})

    return render(request, 'login.html', {'form': form})

# Vista principal
def paginaprincipal(request):
    return render(request, 'paginaprincipal.html')

# Vista para listar personas
def listarpersonas(request):
    personas = Persona.objects.all()
    return render(request, 'listapersonas.html', {'personas': personas})

# Vista protegida para novios
@login_required
def pagina_novios(request):
    return render(request, 'paginanovios.html')

# Vista protegida para invitados
@login_required
def pagina_invitados(request):
    return render(request, 'paginainvitados.html')

# Vista para redireccionar según grupo
@login_required
def redirect_dashboard(request):
    return redireccion_por_grupo(request.user)

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