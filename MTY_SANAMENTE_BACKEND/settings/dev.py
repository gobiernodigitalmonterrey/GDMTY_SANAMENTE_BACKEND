from .base import *
import os
import ast
from pathlib import Path
from dotenv import load_dotenv
import logging
load_dotenv()

logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RUN = True

# SECURITY WARNING: ¡No usar modo DEBUG en producción!
DEBUG = ast.literal_eval(os.getenv("DEBUG", "True"))

# SECURITY WARNING: ¡Mantener la secret key secreta en producción!
SECRET_KEY = os.getenv("SECRET_KEY", "SECRET_KEY")

# SECURITY WARNING: ¡Establecer correctamente los hosts permitidos en producción!
ALLOWED_HOSTS = ast.literal_eval(os.getenv("ALLOWED_HOSTS", "['*']"))

# El servicio de correo electrónico se puede usar en modo consola en entornos de desarrollo
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")


# Installed apps needed for development environment
INSTALLED_APPS += [
    'drf_spectacular',
    'whitenoise.runserver_nostatic',
]

if ast.literal_eval(os.getenv("DEV_USE_AUDITLOG", "False")):
    INSTALLED_APPS += ['auditlog']
    MIDDLEWARE += ['auditlog.middleware.AuditlogMiddleware']
    logger.info("Se encontró DEV_USE_AUDITLOG en True en las variables de entorno")
else:
    logger.info("No se encontró DEV_USE_AUDITLOG en las variables de entorno")


# Default authentication classes for DRF, these are no recommended for production for security concerns
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]

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
        print("STORAGES", STORAGES)
    except ImportError:
        logger.error("No storages settings file found")
        RUN = False
        raise ImportError("No storages configuration file found")

try:
    from .local import *
except ImportError:
    pass