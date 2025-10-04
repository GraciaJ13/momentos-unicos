from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from webappaplication import views
from webappaplication.views import paginaprincipal, login_view, listarpersonas, pagina_novios
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='paginaprincipal.html'), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('paginaprincipal/', paginaprincipal),
    path('listapersonas/', listarpersonas),
    path('novios/', pagina_novios, name='paginanovios'),
    path('pagina_invitados/', TemplateView.as_view(template_name='paginavisitante.html'), name='paginavisitante'),
    path("registro/", views.registro_novios, name="registro_novios"),
]
