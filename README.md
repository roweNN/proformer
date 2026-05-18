# Proformer

Proyecto base en Django para autenticacion y panel administrativo simple. Incluye login, registro, recuperacion de cuenta por correo y configuracion por entorno para desarrollo con SQLite y produccion con PostgreSQL.

## Tecnologias

- Python 3.11
- Django 5.2
- SQLite para desarrollo local
- PostgreSQL para produccion
- Mailgun API para envio de correos
- Gunicorn para despliegue WSGI
- `python-dotenv` para carga de variables de entorno
- `requests` para integracion HTTP con Mailgun
- `psycopg` para conexion PostgreSQL

## Caracteristicas

- Estructura de settings separada en `config/settings/`
- Entorno local con SQLite
- Entorno de produccion con PostgreSQL
- Login, logout y registro de usuarios
- Recuperacion de contrasena por correo
- Plantillas HTML base para auth y home
- Admin de Django habilitado
- Variables sensibles fuera de git mediante `.env`

## Estructura

```text
accounts/              # Auth, formularios, vistas, urls, servicio Mailgun
config/                # Proyecto Django y settings por entorno
config/settings/       # base.py, local.py, production.py
core/                  # Home protegida
templates/             # Templates HTML y correos
static/                # Archivos estaticos fuente
requirements.txt       # Dependencias Python
.env.example           # Variables de entorno de ejemplo
```

## Instalacion local

### 1. Crear entorno virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Crear archivo de entorno

```bash
cp .env.example .env
```

Valores minimos para entorno local:

```env
DJANGO_ENV=local
DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=127.0.0.1,localhost
SQLITE_NAME=db.sqlite3
MAILGUN_API_KEY=key-your-mailgun-key
MAILGUN_DOMAIN=mg.example.com
```

### 4. Aplicar migraciones

```bash
python3.11 manage.py migrate
```

### 5. Crear superusuario

```bash
python3.11 manage.py createsuperuser
```

### 6. Ejecutar servidor local

```bash
python3.11 manage.py runserver
```

Accesos:

- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Login: `http://127.0.0.1:8000/accounts/login/`

## Configuracion de produccion

En produccion el proyecto debe usar PostgreSQL. Ajusta `.env`:

```env
DJANGO_ENV=production
DEBUG=False
SECRET_KEY=tu-clave-segura
ALLOWED_HOSTS=proformer.cl,www.proformer.cl

POSTGRES_DB=proformer_db
POSTGRES_USER=proformer_user
POSTGRES_PASSWORD=tu-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

MAILGUN_API_KEY=key-xxxxx
MAILGUN_DOMAIN=mg.tudominio.com
MAILGUN_BASE_URL=https://api.mailgun.net/v3
DEFAULT_FROM_EMAIL=Proformer <noreply@tudominio.com>
```

### Crear usuario y base en PostgreSQL

```sql
CREATE USER proformer_user WITH ENCRYPTED PASSWORD 'tu-password';
CREATE DATABASE proformer_db OWNER proformer_user;
GRANT ALL PRIVILEGES ON DATABASE proformer_db TO proformer_user;
```

### Ejecutar migraciones en produccion

```bash
python3.11 manage.py migrate
```

### Iniciar con Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Correos con Mailgun

El proyecto envia correos en estos casos:

- Registro exitoso
- Recuperacion de cuenta

Variables requeridas:

```env
MAILGUN_API_KEY=key-xxxxx
MAILGUN_DOMAIN=mg.tudominio.com
MAILGUN_BASE_URL=https://api.mailgun.net/v3
DEFAULT_FROM_EMAIL=Proformer <noreply@tudominio.com>
EMAIL_TIMEOUT=10
```

Si faltan credenciales Mailgun, el proyecto omite envio y registra advertencia en logs.

## Comandos utiles

```bash
python3.11 manage.py check
python3.11 manage.py migrate
python3.11 manage.py createsuperuser
python3.11 manage.py collectstatic --noinput
python3.11 manage.py shell
```

## Notas

- `.env` no debe subirse a git.
- `venv/` esta excluido por `.gitignore`.
- `db.sqlite3` solo debe usarse en local o pruebas.
- Para produccion, verifica que el servidor sirva archivos estaticos desde `staticfiles/` tras `collectstatic`.
