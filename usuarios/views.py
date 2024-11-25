from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Usuario, Transferencia, MotivoTransferencia
from transacciones.models import Cuenta, Movimiento
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, MotivoTransferencia
from transacciones.models import Cuenta
from django.views.generic import TemplateView, UpdateView, DetailView

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import FormUser, EditarPerfil, ActivarUsuario
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView 
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import UsuarioFavorito
from django.shortcuts import render, redirect, get_object_or_404





from django.contrib.auth import authenticate, login as login_django
from django.shortcuts import render, redirect

def iniciar_sesion(request):
    se_autentico = False
    salio_mal = False
    mensaje_error = ""
    username = ""

    if request.method == "POST":
        username = request.POST.get("username", default=None)
        password = request.POST.get("password", default=None)
        usuario = authenticate(request, username=username, password=password)

        se_autentico = True

        if usuario:
            salio_mal = False
            login_django(request, usuario)
            return redirect("home")
        else:
            salio_mal = True
            mensaje_error = "Credenciales incorrectas. Por favor, verifica tus datos."

    ctx = {
        "se_autentico": se_autentico,
        "salio_mal": salio_mal,
        "mensaje_error": mensaje_error,
        "username": username,
    }

    return render(request, 'login.html', ctx)



# views.py
from django.shortcuts import render, redirect
from .forms import TransferenciaForm
from .models import Transferencia, Usuario
from django import forms


def tudinero(request):
    # Obtener el importe de la sesión, si está disponible
    importe = request.session.get('importe', 0)
    return render(request, 'tu_dinero.html', {'importe': importe})

def tuactividad(request):
    
    return render(request, 'tu_actividad.html')


def ingresar_dinero(request):
        
    return render(request, 'ingresar_dinero.html')


def realizar_transferencia(request):
    
    return render(request, 'transferencia.html')

def ingresar_monto_transferencia(request):
        
    return render(request, 'monto_tranferencia.html')


def confirmacion(request):
    # Tu lógica para manejar la transferencia
    return render(request, 'confirmacion.html')

#class EditarPerfil_clase(UpdateView):
#    model = Usuario
#    form_class = EditarPerfil
#    template_name = 'usuarios/editarperfil.html'
#    success_url = reverse_lazy('home')

#    def form_valid(self, form):
        
#        perfil = form.save(commit = False)
        
#        perfil.save()

 #       return redirect(self.success_url)
def is_staff(user):
    return user.is_staff

class EditarPerfil_clase(UpdateView):
    model = Usuario
    form_class = EditarPerfil
    template_name = 'usuarios/editarperfil.html'

    def get_success_url(self):
        # Verificar si el usuario es parte del personal (is_staff)
        if self.request.user.is_staff:
            return reverse_lazy('usuarios:listado_usuarios')  # Redirigir a listado de usuarios si es staff
        else:
            return reverse_lazy('home')  # Redirigir al home si no es staff

    def form_valid(self, form):
        perfil = form.save(commit=False)
        
        perfil.save()
        return redirect(self.get_success_url())  # Usar el método get_success_url para redirigir

class activar_usuario(UpdateView):
    model = Usuario
    form_class = ActivarUsuario
    template_name = 'usuarios/activar_usuario.html'
    success_url = reverse_lazy('usuarios:listado_usuarios')

    # Redirigir al home si no es staff

    def form_valid(self, form):
        perfil = form.save(commit=False)
        perfil.save()
        return redirect(self.get_success_url())  # Usar el método get_success_url para redirigir

class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuarios/confirmacion_eliminar_usuario.html'
    success_url = reverse_lazy('usuarios:listado_usuarios')  # Redirige tras eliminar

def listar_usuarios(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return render(request, 'usuarios/denegado.html')
    context={}
    todos=Usuario.objects.all() #MotivoTransferencia.objects.all()
    context['usuarios']=todos
    return render(request,'usuarios/listado_usuarios.html', context)
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return render(request, 'usuarios/denegado.html')



#@user_passes_test(is_staff)
def Listar_MovimientosPorUsuario(request, pk):
    # Verificar si el usuario no es staff
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return render(request, 'usuarios/denegado.html')
    # Obtener el usuario directamente por el pk (ID del usuario)
    usuario = Usuario.objects.get(pk=pk)
    
    # Obtener la cuenta del usuario
    cuenta = Cuenta.objects.get(usuario=usuario)
    
    # Obtener los movimientos de la cuenta
    movimientos = Movimiento.objects.filter(cuenta_origen=cuenta) | Movimiento.objects.filter(cuenta_destino=cuenta)
    
    # Pasar los movimientos a la plantilla
    context = {
        'usuario': usuario,
        'movimientos': movimientos
    }
    
    return render(request, 'usuarios/movimientos_por_usuario.html', context)




from transacciones.models import Cuenta  # Modelo donde resides las cuentas

@login_required
def agregar_favorito(request, cuenta_destino_id):
    # Obtener la cuenta destino
    cuenta_destino = get_object_or_404(Cuenta, id=cuenta_destino_id)

    # Obtener el usuario asociado a la cuenta destino
    usuario_destino = cuenta_destino.usuario

    # Validar que el usuario destino no sea el usuario logueado
    if usuario_destino == request.user:
        messages.error(request, "No puedes agregarte a ti mismo como favorito.")
        return redirect(request.META.get('HTTP_REFERER', '/'))  # Cambia esta URL según tu ruta de movimientos

    # Validar que no se haya agregado previamente como favorito
    favorito_existente = UsuarioFavorito.objects.filter(
        usuario_origen=request.user,
        usuario_favorito=usuario_destino
    ).exists()

    if favorito_existente:
        messages.info(request, "El usuario ya está en tu lista de favoritos.")
    else:
        # Crear el nuevo favorito
        UsuarioFavorito.objects.create(
            usuario_origen=request.user,
            usuario_favorito=usuario_destino
        )
        messages.success(request, "Usuario agregado a tus favoritos con éxito.")

    return redirect(request.META.get('HTTP_REFERER', '/'))  # Cambia esta URL según la lista de movimientos



@login_required
def eliminar_favorito(request, usuario_favorito_id):
    # Obtener el favorito a eliminar
    favorito = get_object_or_404(UsuarioFavorito, usuario_favorito_id=usuario_favorito_id, usuario_origen=request.user)

    # Eliminar el usuario favorito
    favorito.delete()

    messages.success(request, "El usuario ha sido eliminado de tu lista de favoritos.")
    
    # Redirigir de vuelta a la lista de favoritos
    return redirect('usuarios:favoritos')  # Asegúrate de que esta URL sea correcta
# @login_required
class Listar(TemplateView):
    template_name = 'usuarios/favoritos.html'
    # model = UsuarioFavorito
    context_object_name = "usuario"
    # paginate_by = 5
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Obtener el usuario actual basado en el pk de la URL
        # usuario_origen_id = self.kwargs.get('pk')
        # usuario = get_object_or_404(Usuario, id=usuario_origen_id)
        usuario = self.request.user
        # Filtrar favoritos para este usuario
        ctx['favoritos'] = UsuarioFavorito.objects.filter(usuario_origen=usuario)
        ctx["titulo"] = "LISTA DE FAVORITOS"
        return ctx