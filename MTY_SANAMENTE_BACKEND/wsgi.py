"""
WSGI config for MTY_SANAMENTE_BACKEND project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import ast
from django.core.wsgi import get_wsgi_application

RUN_TYPE = os.getenv("RUN_ENVIRONMENT", "dev")
SETTINGS_MODULE = f"MTY_SANAMENTE_BACKEND.settings.{RUN_TYPE}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)

settings = ast.literal_eval(SETTINGS_MODULE)

if SETTINGS_MODULE.RUN is not False:
    application = get_wsgi_application()
else:
    settings.logger.error("El servicio no se puede ejecutar en modo producción por errores en la configuración de las variables de entorno")
