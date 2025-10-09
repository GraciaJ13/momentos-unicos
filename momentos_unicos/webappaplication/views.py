from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroNoviosForm
from Personas.models import Persona

# Vista de login
def login_view(request):
    print(f"Accediendo a login_view, URL solicitada: {request.get_full_path()}")  # Depuración
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(f"Formulario recibido: {form.data}")  # Depuración
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
                if user.is_staff:
                    print("Redirigiendo a admin")  # Depuración
                    return redirect('admin:index')
                else:
                    print("Redirigiendo a paginanovios")  # Depuración
                    return redirect('paginanovios')
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

# Vista protegida para invitados (solo requiere login, sin grupos; puedes eliminarla si no la necesitas)
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
            login(request, user)
            return redirect("paginanovios")
    else:
        form = RegistroNoviosForm()

    return render(request, "registro.html", {"form": form})