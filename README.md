# 📚 API REST de Gestión de Biblioteca

¡Bienvenido! Esta es una API REST profesional desarrollada con **Django** y **Django Rest Framework (DRF)** para la gestión automatizada de una biblioteca (libros, autores, usuarios y préstamos). Cuenta con seguridad avanzada mediante Tokens JWT y documentación interactiva.

---

## 🛠️ Tecnologías Utilizadas

*   **Backend:** Python 3.x & Django 5.x / 12 (Laravel-inspired project structure)
*   **API Framework:** Django Rest Framework (DRF)
*   **Autenticación:** JWT (JSON Web Tokens) con `django-rest-framework-simplejwt`
*   **Documentación:** Swagger & Redoc mediante `drf-spectacular`
*   **Entorno Local:** SQLite (Base de datos ligera de desarrollo)

---

## 🔐 Características Principales

*   **CRUD Completo:** Gestión total de Libros, Autores y Préstamos.
*   **Seguridad JWT:** Rutas protegidas. Los usuarios deben autenticarse para obtener su token de acceso (`Access Token`) y de actualización (`Refresh Token`).
*   **Roles de Usuario:** Restricciones de acceso según permisos (ej. solo administradores pueden registrar nuevos libros).
*   **Documentación Viva:** OpenAPI 3.0 integrada para probar los endpoints directamente desde el navegador.

---

## 🚀 Instalación y Configuración Local

Si deseas clonar este repositorio y ejecutarlo en tu máquina local, sigue estos pasos:

### 1. Clonar el repositorio
```bash
git clone https://github.com/nello27/Biblioteca_REST_API.git
cd Biblioteca_REST_API

2. Configurar el Entorno Virtual

python -m venv venv
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1

3. Instalar Dependencias

pip install -r requirements.txt

4. Variables de Entorno

Crea un archivo .env en la raíz del proyecto y configura tus credenciales locales (usa el archivo .env.example como guía):

DEBUG=True
SECRET_KEY=tu_secret_key_local
ALLOWED_HOSTS=127.0.0.1,localhost

5. Migraciones y Servidor

python manage.py migrate
python manage.py runserver


📖 Documentación de la API (Endpoints)

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva en las siguientes rutas:

    Swagger UI: http://127.0.0.1:8000/api/schema/docs/ (Para interactuar y probar los endpoints).

    Redoc: http://127.0.0.1:8000/api/schema/redoc/ (Documentación limpia y organizada para lectura).

Endpoints Principales:

    POST /api/token/ - Obtener Token JWT (Login).

    POST /api/token/refresh/ - Refrescar Token expirado.

    GET/POST /api/libros/ - Listar y crear libros (Protegido).

