from django.urls import path
from webappaplication import views
from webappaplication.views import paginaprincipal, listarpersonas, pagina_novios
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='paginaprincipal.html'), name='home'),
    path('login/', views.login_view, name='custom_login'),
    path('logout/', views.logout_view, name='custom_logout'),
    path('paginaprincipal/', paginaprincipal),
    path('listapersonas/', listarpersonas),
    path('novios/', pagina_novios, name='paginanovios'),
    path('pagina_invitados/', TemplateView.as_view(template_name='paginavisitante.html'), name='paginavisitante'),
    path("registro/", views.registro_novios, name="registro_novios"),
    # Nuevas URLs para opciones en paginanovios
    path('crear-boda/', views.crear_boda, name='crear_boda'),
    path('ver-proveedores/', views.ver_proveedores, name='ver_proveedores'),
    path('crear-invitados/', views.crear_invitados, name='crear_invitados'),
    path('gestion-regalos/', views.gestion_regalos, name='gestion_regalos'),
    path('agregar-cancion/', views.agregar_cancion, name='agregar_cancion'),
]