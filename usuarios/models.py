from django.db import models

# Create your models here.


from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  # Asegúrate de importar BaseUserManager
from django.db import models

class Solicitud(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.titulo




class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class Usuario(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Definir el manager
    objects = UsuarioManager()

    # Campos requeridos para la creación de un usuario
    REQUIRED_FIELDS = ['email', 'saldo', 'foto_perfil']
    
    USERNAME_FIELD = 'username'  # Especifica qué campo es el principal para el login

    def __str__(self):
        return self.username



class Transferencia(models.Model):
    usuario_origen = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transferencias_realizadas')
    usuario_destino = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='transferencias_recibidas')
    motivo = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)



class MotivoTransferencia(models.Model):
    nombre = models.CharField(max_length=100)
    
