from .base import *
import os
import ast

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-key"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

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