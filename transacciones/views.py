from django.shortcuts import render

# Create your views here.
# movimientos/views.py
from django.shortcuts import render, redirect
from .models import Cuenta, MotivoTransferencia, Movimiento
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TransferenciaForm
from .models import Cuenta
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cuenta
# transacciones/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IngresoDineroForm
from .models import Cuenta
from django.contrib.auth import get_user_model
from .forms import ModificacionMotivo
from django.views.generic.edit import DeleteView 
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

User = get_user_model()






#def home(request):
 #   context={}
  #  if request.user.is_authenticated:
        # Intentamos obtener la cuenta asociada al usuario logueado
    #    try:
     #       cuenta = Cuenta.objects.get(usuario=request.user)
      #      context['monto']=cuenta.saldo
       #     saldo=cuenta.saldo
        #except Cuenta.DoesNotExist:
         #   saldo = 0  # Si no existe la cuenta, el saldo será 0
    

    #return render(request, 'home.html', {'saldo': saldo})





def listar_cuentas(request):
    cuentas = Cuenta.objects.all()
    return render(request, 'movimientos/listar_cuentas.html', {'cuentas': cuentas})



@login_required
def ingresar_dinero(request):
    if request.method == 'POST':
        form = IngresoDineroForm(request.POST)
        if form.is_valid():
            monto = form.cleaned_data['monto']
            # Obtener la cuenta del usuario autenticado
            cuenta = Cuenta.objects.get(usuario=request.user)
            cuenta.saldo += monto
            cuenta.save()
            Movimiento.objects.create(cuenta_origen=cuenta, cuenta_movimiento=cuenta, tipo="ingreso", monto=monto)
            return redirect('transacciones:confirmacion_ingreso_dinero')  # Redirigir a la página principal o una página de confirmación
    else:
        form = IngresoDineroForm()

        # Guardar el movimiento para historial
    
            

    return render(request, 'ingresar_dinero.html', {'form': form})


@login_required
def realizar_transferencia(request):
    context={}
    if request.method == 'POST':
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            destinatario_username = form.cleaned_data['destinatario']
            monto = form.cleaned_data['monto']
            motivo = form.cleaned_data['motivo']
            
            # Verificar que el destinatario existe
            try:
                destinatario = User.objects.get(username=destinatario_username)
            except User.DoesNotExist:
                return render(request, 'destinatario_novalido.html', {'form': form})
            if destinatario.is_active == False:
                return render(request, 'destinatario_novalido.html', {'form': form})
            


            # Verificar que el remitente tiene saldo suficiente
            remitente_cuenta, _ = Cuenta.objects.get_or_create(usuario=request.user)
            if remitente_cuenta.saldo < monto:
                return render(request, 'saldoinsuficiente.html', {'form': form})

                # Obtener o crear la cuenta del destinatario
            destinatario_cuenta, _ = Cuenta.objects.get_or_create(usuario=destinatario)

                # Realizar la transferencia
            remitente_cuenta.saldo -= monto
            remitente_cuenta.save()
            
            destinatario_cuenta.saldo += monto
            destinatario_cuenta.save()

                # Guardar el movimiento para historial
            movimiento_origen = Movimiento.objects.create(cuenta_origen=remitente_cuenta, cuenta_movimiento=remitente_cuenta,cuenta_destino=destinatario_cuenta, tipo="transferencia", monto=monto, motivo=motivo)
            Movimiento.objects.create(cuenta_origen=remitente_cuenta, cuenta_movimiento=destinatario_cuenta,cuenta_destino=destinatario_cuenta, tipo="ingreso transferencia", monto=monto, motivo=motivo)

                # Redirigir a una página de confirmación
            return redirect('transacciones:confirmacion_transferencia',movimiento_origen.id)  # Redirigir a una página de confirmación
            
                
                
                
    else:
        form = TransferenciaForm()

    return render(request, 'Transferencia.html', {'form': form})



#def confirmacion_transferencia(request,movimiento_id):
 #   context={}
  #  movimiento= movimiento.objects.get(id=movimiento_id)
   # context['movimiento']= movimiento
    #return render(request, 'confirmacion_transferencia.html',context)
def confirmacion_transferencia(request, movimiento_id):
    # Obtener el objeto Movimiento basado en el movimiento_id
    movimiento = get_object_or_404(Movimiento, id=movimiento_id)

    # Pasar el objeto 'movimiento' al contexto para renderizarlo en la plantilla
    return render(request, 'confirmacion_transferencia.html', {'movimiento': movimiento})

def confirmacion_ingreso_dinero(request):
    return render(request, 'confirmacion_ingreso_dinero.html')


def listar_movimientos(request):

    context={}

    cuent= Cuenta.objects.get(usuario=request.user)#busca el objeto cuenta del usuario que esta logueado
    todos= Movimiento.objects.filter(cuenta_movimiento=cuent) # busca todos los movimientos de la cuenta del usuario logueado que buscamos anteriormente
    context['movimientos']=todos #paso todos los movimientos a context para enviar al html
    return render(request,'listado.html', context)

def listar_motivos(request):
    if not request.user.is_staff:
        messages.error(request, "No tienes permisos para acceder a esta página.")
        return render(request, 'usuarios/denegado.html')
    context={}
    todos=MotivoTransferencia.objects.all() #MotivoTransferencia.objects.all()
    context['motivos']=todos
    return render(request,'listado_motivos.html', context)


class ModificarMotivo(UpdateView):
    model = MotivoTransferencia
    form_class = ModificacionMotivo
    template_name = 'transacciones/modificar_motivo.html'
    success_url = reverse_lazy('transacciones:listar_motivos')

    def form_valid(self, form):
        
        motivo = form.save(commit = False)
        motivo.save()

        return redirect(self.success_url)


class MotivoDeleteView(DeleteView):
    model = MotivoTransferencia
    template_name = 'Confirmacion.html'
    success_url = reverse_lazy('transacciones:listar_motivos')  # Redirige tras eliminar


class MotivoCreateView(CreateView):
    model = MotivoTransferencia
    template_name = 'motivo_nuevo.html'  # La plantilla que se usará para el formulario
    fields = ['nombre']  # Campos que estarán disponibles en el formulario
    success_url = reverse_lazy('transacciones:listar_motivos')  # URL a la que se redirige después de la creación

def Comprobante(request, pk):
    movimiento = get_object_or_404(Movimiento, id=pk)
    return render(request, 'Comprobante.html',{'movimiento': movimiento})
