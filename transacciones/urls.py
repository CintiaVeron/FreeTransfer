# movimientos/urls.py
from django.urls import path
from . import views
from transacciones.views import MotivoDeleteView,MotivoCreateView,ingresar_dinero,realizar_transferencia, confirmacion_transferencia
from usuarios.views import agregar_favorito

app_name = 'transacciones'
urlpatterns = [
    #path('', views.home, name='home'),
    path('ingresar_dinero/', views.ingresar_dinero, name='ingresar_dinero'),
    path('realizar_transferencia/', views.realizar_transferencia, name='realizar_transferencia'),
    # transferencia con username como parametro
    path('realizar_transferencia/<str:destinatario_username>/', views.realizar_transferencia, name='realizar_transferencia'),
    #path('confirmacion_transferencia/<int:pk>/', views.confirmacion_transferencia, name='confirmacion_transferencia'),
    path('confirmacion/<int:movimiento_id>/', confirmacion_transferencia, name='confirmacion_transferencia'),
    path('confirmacion_ingreso_dinero/', views.confirmacion_ingreso_dinero, name='confirmacion_ingreso_dinero'),
    path('usuarionovalido/', views.realizar_transferencia, name='destinatario_novalido'),
    path('saldoinsuficiente/', views.realizar_transferencia, name='saldoinsuficiente'),
    path('listar_movimientos/', views.listar_movimientos ,name='listar_movimientos'),
    path('listar_motivos/', views.listar_motivos,name='listar_motivos'),
    path('Modificar/<str:pk>', views.ModificarMotivo.as_view(template_name= "modificar_motivo.html"), name='modificar_motivo' ),
    path('eliminar/<int:pk>/',MotivoDeleteView.as_view(), name='eliminar_motivo'),
    path('crear/', MotivoCreateView.as_view(), name='crear_motivo'),
    path('Comprobante/<int:pk>/', views.Comprobante, name='Comprobante'),
    path('Comprobante1/', views.Comprobante, name='Comprobante1'),
    path('movimientos/favorito/<int:cuenta_destino_id>/', agregar_favorito, name='agregar_favorito'),


    #path('realizar_transferencia/', views.realizar_transferencia, name='realizar_transferencia'),
]