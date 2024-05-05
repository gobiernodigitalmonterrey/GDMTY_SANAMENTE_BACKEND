from .base import *
import os
import ast

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(os.getenv("DEBUG", "True"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "SECRET_KEY")

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ast.literal_eval(os.getenv("ALLOWED_HOSTS", "['*']"))

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

try:
    INSTALLED_APPS += ['auditlog'] if ast.literal_eval(os.getenv("DEV_USE_AUDITLOG")) is True else []
except Exception as e:
    print("No se encontró DEV_USE_AUDITLOG en las variables de entorno o no tiene un valor Booleano")
    pass

WAGTAIL_USER_EDIT_FORM = 'users.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'users.forms.CustomUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['username']

try:
    from .local import *
except ImportError:
    pass

if DEBUG is False:
    TEMPLATES[0]['DIRS'].append(os.path.join(PROJECT_DIR, 'templates_dev'))
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
    STORAGES['staticfiles']['BACKEND'] = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    INSTALLED_APPS += ['whitenoise.runserver_nostatic']
else:
    STORAGES['staticfiles']['BACKEND'] = "django.contrib.staticfiles.storage.StaticFilesStorage"
    INSTALLED_APPS += ['drf_spectacular']
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'mty_firebase_auth.authentication.FirebaseAuthentication',
    ]
