from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='paginaprincipal.html'), name='home'),
    path('login/', views.login_view, name='custom_login'),
    path('logout/', views.logout_view, name='custom_logout'),
    path('paginaprincipal/', views.paginaprincipal, name='paginaprincipal'),
    path('listapersonas/', views.listarpersonas, name='listarpersonas'),
    path('novios/', views.pagina_novios, name='paginanovios'),
    path('pagina-invitados/', TemplateView.as_view(template_name='paginavisitante.html'), name='paginavisitante'),
    path('registro/', views.registro_novios, name='registro_novios'),
    path('crear-boda/', views.crear_boda, name='crear_boda'),
    path('ver-proveedores/', views.ver_proveedores, name='ver-proveedores'),
    path('eliminar-proveedor/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    path('crear-invitados/', views.crear_invitados, name='crear_invitados'),
    path('gestion-regalos/', views.gestion_regalos, name='gestion_regalos'),
    path('agregar-cancion/', views.agregar_cancion, name='agregar_cancion'),
]