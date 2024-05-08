from .base import *
import os
import ast
from pathlib import Path
import logging

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


# Use of whitenoise backend without cache for static files
STORAGES['staticfiles']['BACKEND'] = "whitenoise.storage.CompressedStaticFilesStorage"

# Default authentication classes for DRF, these are no recommended for production for security concerns
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += [
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
]

try:
    from .local import *
except ImportError:
    pass

if DEBUG is False:
    # para producción
    TEMPLATES[0]['DIRS'].append(os.path.join(PROJECT_DIR, 'templates_dev'))
    MIDDLEWARE.append()
    STORAGES['staticfiles']['BACKEND'] = "whitenoise.storage.CompressedManifestStaticFilesStorage"

