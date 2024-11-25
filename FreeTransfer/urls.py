"""
URL configuration for FreeTransfer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

# FreeTransfer/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as views_django
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth.views import LoginView
from transacciones.views import MotivoDeleteView,MotivoCreateView,ingresar_dinero,realizar_transferencia

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views_django.LoginView.as_view(template_name="login.html"), name='login'),
    path('accounts/login/registro/', views.registro, name='registro'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('go_back/', views.go_back, name='go_back'),



    # Incluir las rutas de la app transacciones
    path('transacciones/', include('transacciones.urls')),
    path('usuarios/', include('usuarios.urls')),

]


