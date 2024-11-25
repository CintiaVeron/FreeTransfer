# Proyecto Django: Gestión de Movimientos de Usuarios

## 📋 Descripción del Proyecto

Este proyecto es una aplicación web desarrollada con **Django** y **Python**, que permite a los usuarios registrados gestionar y visualizar sus movimientos, así como agregar ciertos destinatarios a su lista de favoritos.

- Los usuarios con rol de **administrador** tienen permisos para gestionar cuentas de usuarios registrados y supervisar su historial de transacciones.
- La aplicación utiliza **Bootstrap** para una interfaz de usuario responsiva y amigable, facilitando la interacción con las operaciones del sistema.
- La **gestión de datos de usuarios** y la **integración con la base de datos** están implementadas para garantizar una experiencia fluida y eficiente.


---

## 👥 Integrantes del Equipo

- **Cintia Verón** (Full Stack Developer)
 GitHub: [CintiaVeron](https://github.com/CintiaVeron)
- **Claudio Castillo** (Full Stack Developer)

---

## 🛠️ Instrucciones para Ejecutar el Proyecto

### 1. Clonar el repositorio

Primero, clona el repositorio desde GitHub:
```bash
git clone https://github.com/ClaudioMFCDev/app-free-transfer.git
cd FreeTransfer
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate    # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar el archivo .env
Crea un archivo .env en la raíz del proyecto y define las siguientes variables de entorno:

```bash
DEBUG=True
SECRET_KEY=tu_clave_secreta
DB_NAME=nombre_base_datos
DB_USER=usuario_base_datos
DB_PASSWORD=contraseña_base_datos
DB_HOST=localhost
DB_PORT=5432

```

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate

```

### 6. Ejecutar el servidor local

```bash
python manage.py runserver
```
Accede a la aplicación en http://127.0.0.1:8000.

### 📂 Estructura del Proyecto

```bash
proyecto-django/
│
├── FreeTransfer/           # Aplicación principal
├── usuarios/               # Módulo de autenticación, templates y gestión de usuarios
├── transacciones/          # Módulo de transacciones y templates de las cuentas de usuarios
├── static/                 # Archivos estáticos (CSS, JS, imágenes)
├── medio/avatar            # Archivo de imágenes de los usuarios
├── requirements.txt        # Dependencias del proyecto
└── manage.py               # Script principal de Django
```

### 🧩 Funcionalidades Desarrolladas

#### 1. Gestión de Movimientos
Listar movimientos de un usuario autenticado.
Filtrar movimientos por fecha o tipo.
#### 2. Favoritos
Agregar una cuenta destino como favorita usando el cuenta_destino_id.
Visualizar una lista de favoritos para acceso rápido.
#### 3. Seguridad y Autenticación
Inicio de sesión y registro de usuarios.
Roles de usuario con permisos diferenciados.
#### 4. Panel de Administración
Configuración y personalización del panel de administración de Django.
#### 5. Interfaz de Usuario
Diseño responsivo utilizando Bootstrap.
Paginación para listas de movimientos.

### 🧑‍💻 Roles y Funcionalidades
En la aplicación se distinguen tres tipos de usuarios, cada uno con permisos y funcionalidades específicas:

#### 1. Administrador
Acceso completo al panel de administración.
Gestión de usuarios (crear, editar, eliminar).
Visualización y administración de todos los movimientos de los usuarios.
#### 2. Usuario Registrado
Visualización de sus propios movimientos.
Agregar y eliminar destinatarios de su lista de favoritos.
Detalle completos de movimientos de cuentas.
Actualización de datos personales y avatar.
#### 3. Usuario Visitante
Navegación limitada (sin necesidad de registrarse).
Visualización de la página de inicio.
Acceso a formularios de registro e inicio de sesión.

### 📝 Notas Adicionales
El proyecto usa PostgreSQL como base de datos. Si deseas cambiar a SQLite para desarrollo local, edita la configuración en settings.py.
Se recomienda ejecutar las pruebas antes de implementar cambios:
```bash
python manage.py test
```

¡Gracias por utilizar este proyecto! Si tienes dudas o sugerencias, no dudes en contactarnos. 🚀



