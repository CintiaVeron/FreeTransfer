from django.shortcuts import render, redirect
from django.contrib import messages

from usuarios.models import Usuario


# views.py



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth import logout
from .forms import FormUser
from django.contrib.auth import get_user_model
from transacciones.models import Cuenta, MotivoTransferencia, Movimiento
User = get_user_model()


# Vista para el home del usuario registrado
@login_required
def home(request):
    # Obtener el importe de la sesión, si está disponible
    context={}
    importe = request.session.get('importe', 0)
    cuenta = Cuenta.objects.get(usuario=request.user)
    context['monto']=cuenta.saldo

    return render(request, 'usuarios/home.html', context)

#def exit(request):
 #	loguot(request)
 #	return redirect('usuarios/registration.login.html')


def registro(request):
    if request.method == 'POST':
        form = FormUser(request.POST, request.FILES)
        if form.is_valid():
            # Obtén los datos del formulario
            password = form.cleaned_data['password1']
            user = form.save(commit=False)  # No guarda el usuario todavía

            # Encripta la contraseña y activa el usuario
            user.set_password(password)
            user.is_active = True  
            user.save()  # Guarda el usuario en la base de datos

            # Ahora que el usuario tiene un ID, crea la cuenta asociada
            Cuenta.objects.create(usuario=user, saldo=0)  # Puedes establecer un saldo inicial si lo deseas

            return redirect('login')  # Redirige a la página de login
    else:
        form = FormUser()

    return render(request, 'usuarios/registro.html', {'form': form})


from django.http import HttpResponseRedirect

def go_back(request):
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return HttpResponseRedirect(referer)
    return HttpResponseRedirect('/')  # Redirige al inicio si no hay referer





