from .base import *
import os
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RUN = True

INSTALLED_APPS += [
    'defender',
    'auditlog',
]

# SECURITY WARNING: ¡No usar modo DEBUG en producción!
DEBUG = ast.literal_eval(os.getenv("DEBUG", "False"))

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

# Hardening Security settings - django-session-timeout
SESSION_EXPIRE_SECONDS = 600
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT = '/wadmin/'

MIDDLEWARE += [
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
]

if DEBUG is True or SECRET_KEY == "" or len(ALLOWED_HOSTS) == 0:
    RUN = False
    logger.error("DEBUG is True or SECRET_KEY is empty or ALLOWED_HOSTS is empty, el servicio no se puede ejecutar en modo producción en estas condiciones")


try:
    from .local import *
except ImportError:
    logger.info("No local settings file found")
    pass
