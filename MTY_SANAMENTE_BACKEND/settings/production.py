from .base import *
import os
import ast

DEBUG = False

INSTALLED_APPS += [
    'defender',
    'auditlog',
]

try:
    from .local import *
except ImportError:
    pass
