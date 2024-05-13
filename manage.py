#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        settings_module = os.environ['DJANGO_SETTINGS_MODULE']
    else:
        RUN_TYPE = os.getenv("RUN_ENVIRONMENT", "dev")
        SETTINGS_MODULE = f"MTY_SANAMENTE_BACKEND.settings.{RUN_TYPE}"
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MTY_SANAMENTE_BACKEND.settings.dev")

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)
