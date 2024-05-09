"""
WSGI config for MTY_SANAMENTE_BACKEND project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

run_environment_type = os.getenv("RUN_ENVIRONMENT", "dev")
settings_module = f"MTY_SANAMENTE_BACKEND.settings.{run_environment_type}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

from django.conf import settings

if settings.RUN is not False:
    application = get_wsgi_application()
else:
    settings.logger.error("El servicio no se puede ejecutar en modo producción por errores en la configuración de las variables de entorno")
