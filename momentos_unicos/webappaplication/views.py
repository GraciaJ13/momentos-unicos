from django.shortcuts import redirect, render
from Personas.models import Persona
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import RegistroNoviosForm
from django.contrib.auth import authenticate, login as auth_login

# from .forms import PersonaForm
from django.contrib.auth.models import User
# Create your views here.
def paginaprincipal (request):
    return render(request, 'paginaprincipal.html')

def login_page (request):
    return render(request, 'login.html')

def listarpersonas (request):
    personas = Persona.objects.all()
    return render(request, 'listapersonas.html', {'personas': personas})

def paginanovios (request):
    return render(request, 'paginanovios.html')


@login_required
def redirect_dashboard(request):
    user = request.user  

    if user.groups.filter(name="novios").exists():
        return redirect("pagina_novios")
    elif user.groups.filter(name="invitados").exists():
        return redirect("pagina_invitados")
    else:
        return redirect("home")  # en caso de no estar en un grupo

@login_required
def pagina_novios(request):
    return render(request, "paginanovios.html")

@login_required
def pagina_invitados(request):
    return render(request, "paginainvitados.html")

def registro_novios(request):
    if request.method == "POST":
        form = RegistroNoviosForm(request.POST)
        if form.is_valid():
            # Guardamos el usuario
            persona = form.save()  # esto devuelve una Persona con su User
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # Hashea la contraseña
            user.save()

            # Agregar al grupo "novios"
            grupo_novios, created = Group.objects.get_or_create(name="novios")
            user.groups.add(grupo_novios)

            # Iniciar sesión automáticamente
            login(request, user)

            return redirect("pagina_novios") 
    else:
        form = RegistroNoviosForm()

    return render(request, "registro.html", {"form": form})


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Evita conflicto con el nombre de la función

            if user.groups.filter(name="novios").exists():
                return redirect("paginanovios")  # Asegúrate que esta URL esté registrada
            elif user.groups.filter(name="invitados").exists():
                return redirect("pagina_invitados")
            else:
                return redirect("home")  # Ruta por defecto si no pertenece a ningún grupo

        else:
            return render(request, "login.html", {"error": "Usuario o contraseña incorrectos"})
    return render(request, "login.html")