from .base import *
import os
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RUN = True

INSTALLED_APPS += [
    'auditlog',
]

# SECURITY WARNING: ¡No usar modo DEBUG en producción!
DEBUG = ast.literal_eval(os.getenv("DEBUG", "False"))
print("DEBUG", DEBUG)

# SECURITY WARNING: ¡Mantener la secret key secreta en producción!
SECRET_KEY = os.getenv("SECRET_KEY", "")

# SECURITY WARNING: ¡Establecer correctamente los hosts permitidos en producción!
ALLOWED_HOSTS = ast.literal_eval(os.getenv("ALLOWED_HOSTS", "[]"))

# El servicio de correo electrónico se debe configurar correctamente en producción con un servicio SMTP válido
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "localhost")
EMAIL_PORT = os.getenv("EMAIL_PORT", 25)
EMAIL_USE_TLS = ast.literal_eval(os.getenv("EMAIL_USE_TLS", "False"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

MIDDLEWARE += [
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

AUDITLOG_INCLUDE_ALL_MODELS = True

# if SECRET_KEY == "" or len(ALLOWED_HOSTS) == 0:
if DEBUG is True or SECRET_KEY == "" or len(ALLOWED_HOSTS) == 0:
    RUN = False
    logger.error(
        "DEBUG is True or SECRET_KEY is empty or ALLOWED_HOSTS is empty, el servicio no se puede ejecutar en modo producción en estas condiciones")
    raise AssertionError("El servicio no se puede ejecutar por errores en la configuración de las variables de entorno")

# DEBUG_PROPAGATE_EXCEPTIONS = True

try:
    from .auth import *
except ImportError:
    logger.error("No se encontró el archivo de autenticación en las variables de entorno")
    raise ImportError("No se encontró el archivo de autenticación en las variables de entorno")

try:
    from .recaptcha import *
except ImportError:
    logger.error("No se encontró el archivo de recaptcha en las variables de entorno")
    raise ImportError("No se encontró el archivo de recaptcha en las variables de entorno")

DJANGO_STORAGE_BACKEND = os.getenv("DJANGO_STORAGE_BACKEND", "local")

if DJANGO_STORAGE_BACKEND == "local":
    logger.info("Using local storage")
else:
    logger.info("Using Django Storages")
    try:
        from .storages import *
        STORAGES['default']['BACKEND'] = STORAGES_DEFAULT_BACKEND
        STORAGES['default']['OPTIONS'] = STORAGES_DEFAULT_OPTIONS
    except ImportError:
        logger.error("No storages settings file found")
        RUN = False
        raise ImportError("No storages configuration file found")

TEMPLATES[0]['DIRS'].append(os.path.join(PROJECT_DIR, 'templates_production'))

try:
    from .local import *
except ImportError:
    pass