"""
URL configuration for momentos_unicos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from webappaplication import views
from webappaplication.views import paginaprincipal
from webappaplication.views import login_view
from webappaplication.views import listarpersonas
from django.views.generic import TemplateView
from webappaplication.views import pagina_novios


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='paginaprincipal.html'), name='home'),
    path('login/', views.login_view, name='login'),
    path('paginaprincipal/', paginaprincipal),
    path('listapersonas/',listarpersonas),
    path('novios/', pagina_novios, name='paginanovios'),
    path('pagina_invitados/', TemplateView.as_view(template_name='pagina_invitados.html'), name='pagina_invitados'),
    path("registro/", views.registro_novios, name="registro_novios"),
]   