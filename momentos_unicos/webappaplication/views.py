from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroNoviosForm, RegaloForm
from Personas.models import Persona, Boda, Regalo, Invitado, Proveedor, Cancion
from django.contrib.auth.models import Group
from django.urls import connection

# Importa o crea forms para las nuevas funcionalidades (asume que tienes forms.py)
from .forms import BodaForm, InvitadoForm, RegaloForm, CancionForm  # Añade estos forms en forms.py

# Vista de login
def login_view(request):
    print(f"Accediendo a login_view, URL solicitada: {request.get_full_path()}")  # Depuración
    print(f"CSRF Cookie: {request.COOKIES.get('csrftoken')}")  # Depuración
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(f"Formulario recibido: {form.data}")  # Depuración
        print(f"CSRF Token en POST: {request.POST.get('csrfmiddlewaretoken')}")  # Depuración
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(f"Usuario autenticado: {user}, Es staff: {user.is_staff if user else 'Ninguno'}")  # Depuración
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next')
                print(f"Next URL: {next_url}")  # Depuración
                if next_url and next_url != '/admin/':  # Evita redirigir exactamente a /admin/
                    print(f"Redirigiendo a next_url: {next_url}")  # Depuración
                    return redirect(next_url)
                # Prioridad: Admin (is_staff) primero
                if user.is_staff:
                    print("Redirigiendo a admin")  # Depuración
                    return redirect('admin:index')
                # Luego verifica los grupos
                elif user.groups.filter(name='novios').exists():
                    print("Redirigiendo a paginanovios (grupo novios)")  # Depuración
                    return redirect('paginanovios')
                elif user.groups.filter(name='Invitados').exists():
                    print("Redirigiendo a paginavisitante (grupo Invitados)")  # Depuración
                    return redirect('paginavisitante')
                else:
                    print("Usuario sin grupo definido, redirigiendo a home")  # Depuración
                    return redirect('home')
            else:
                print("Autenticación fallida")  # Depuración
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            print(f"Errores del formulario: {form.errors}")  # Depuración
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
        print("Método no POST, renderizando login.html con formulario vacío")  # Depuración
    return render(request, 'login.html', {'form': form})

# Vista de logout personalizada
def logout_view(request):
    logout(request)
    messages.success(request, 'Cerraste la sesión.')
    return render(request, 'logout.html')

# Vista principal (página de inicio)
def paginaprincipal(request):
    return render(request, 'paginaprincipal.html')

# Vista para listar personas
def listarpersonas(request):
    personas = Persona.objects.all()
    return render(request, 'listapersonas.html', {'personas': personas})

# Vista protegida para novios (solo requiere login, sin grupos)
@login_required
def pagina_novios(request):
    return render(request, 'paginanovios.html')

# Vista protegida para invitados (solo requiere login, sin grupos)
@login_required
def pagina_invitados(request):
    return render(request, 'paginavisitante.html')

# Vista de registro para novios (sin grupos)
def registro_novios(request):
    if request.method == "POST":
        form = RegistroNoviosForm(request.POST)
        if form.is_valid():
            persona = form.save()
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.save()
            # Asigna al grupo "novios" al registrarse
            group_novios, created = Group.objects.get_or_create(name='novios')
            user.groups.add(group_novios)
            login(request, user)
            return redirect("paginanovios")
    else:
        form = RegistroNoviosForm()

    return render(request, "registro.html", {"form": form})

# Nuevas vistas para opciones en paginanovios
@login_required
def crear_boda(request):
    if request.method == 'POST':
        form = BodaForm(request.POST)
        if form.is_valid():
            boda = form.save(commit=False)
            boda.save()
            messages.success(request, 'Boda creada exitosamente.')
            return redirect('paginanovios')
        pass
        return render(request, 'crear_boda.html')
    else:
        form = BodaForm()
    return render(request, 'crear_boda.html', {'form': form})

proveedores = Proveedor.objects.all()

@login_required
def ver_proveedores(request):
    personas = Persona.objects.all()
    return render(request, 'listapersonas.html', {'personas': personas})

@login_required
def eliminar_proveedor(request, proveedor_id):
    proveedor = Proveedor.objects.filter(id=proveedor_id).first()
    if proveedor:
        proveedor.delete()  # Simplificado para permitir eliminación sin restricciones por ahora
        messages.success(request, 'Proveedor eliminado exitosamente.')
    else:
        messages.error(request, 'Proveedor no encontrado.')
    return redirect('ver_proveedores')

@login_required
def crear_invitados(request):
    if request.method == 'POST':
        form = InvitadoForm(request.POST)
        if form.is_valid():
            invitado = form.save(commit=False)
            invitado.save()
            messages.success(request, 'Lista de invitados actualizada.')
            return redirect('paginanovios')
    else:
        form = InvitadoForm()
    return render(request, 'crear_invitados.html', {'form': form})

@login_required
def gestion_regalos(request):
    regalos = Regalo.objects.all()
    if not Boda.objects.exists():  # Ajuste temporal
        messages.error(request, "Primero crea tu boda para poder avanzar.")
        return redirect('paginanovios')
    if request.method == 'POST':
        form = RegaloForm(request.POST)
        if form.is_valid():
            regalo = form.save(commit=False)
            regalo.save()
            messages.success(request, 'Regalo agregado.')
            return redirect('gestion_regalos')
    else:
        form = RegaloForm()
    return render(request, 'gestion_regalos.html', {'form': form, 'regalos': regalos})

@login_required
def agregar_cancion(request):
    if request.method == 'POST':
        form = CancionForm(request.POST)
        if form.is_valid():
            cancion = form.save(commit=False)
            cancion.save()
            messages.success(request, 'Canción agregada.')
            return redirect('paginavisitante')
    else:
        form = CancionForm()
    return render(request, 'agregar_cancion.html', {'form': form})

@login_required
def novios(request):
    has_boda = Boda.objects.exists()  # Ajuste temporal
    if not has_boda:
        messages.error(request, "Primero crea tu boda para poder avanzar.")
    return render(request, 'paginanovios.html', {'has_boda': has_boda})